#include "kinetic_monte_carlo.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <windows.h>

#define n 624
#define m 397
#define w 32
#define r 31
#define UMASK (0xffffffffUL << r)
#define LMASK (0xffffffffUL >> (w-r))
#define a 0x9908b0dfUL
#define u 11
#define s 7
#define t 15
#define l 18
#define b 0x9d2c5680UL
#define c 0xefc60000UL
#define f 1812433253UL

typedef struct
{
    uint32_t state_array[n];         // the array for the state vector 
    int state_index;                 // index into state vector array, 0 <= state_index <= n-1   always
} mt_state;

double random_uniform(mt_state *state, char rand_type);
int poisson_variable(mt_state *state, double lam, char rand_type);
int int_rand(int range, mt_state *state, char rand_type);
void remove_value_from_arr(int** arr, int idx_to_remove, int new_value, size_t arr_size);
void add_value_to_arr(int** arr, int value, int arr_size);
void print_arrays(int** arr1, int** arr2, int arr_size);
void print_array(int** arr, int arr_size);
void print_double_array(double** arr, int arr_size);
void print_bool_array(bool** arr, int s1);
int find_mode_count(int* arr, int max_num, int arr_size);
void initialize_state(mt_state* state, uint32_t seed);
char* generate_filename(int N, double kon, double koff, double time, bool start_bound);

void get_working_directory(char *buffer, size_t size) {
#ifdef _WIN32
    GetCurrentDirectory(size, buffer);
#else
    getcwd(buffer, size);
#endif
}

int get_particle_idx(
    int **xlink_config,
    int xlink_idx
) {
    int particle_idx = 0;
    int xlink_count = 0;
    while (xlink_count <= xlink_idx) {
        xlink_count = xlink_count + (*xlink_config)[particle_idx];
        particle_idx++;
    }
    return --particle_idx;
}

bool is_particle_bound(
    int **xlink_config,
    bool* xlink_states,
    int xlink_idx
) {
    int particle_idx = get_particle_idx(xlink_config, xlink_idx);

    int num_xlinks = (*xlink_config)[particle_idx];

    // Find correct starting position
    int xlink_idx_start = 0;
    for (int i=0; i<particle_idx; i++) {
        xlink_idx_start = xlink_idx_start + (*xlink_config)[i];
    }
    bool is_bound = false;

    for (int i=xlink_idx_start; i<xlink_idx_start+num_xlinks; i++){
        if (xlink_states[i]){
            is_bound = true;
        }
    }
    return is_bound;
}

void process_simulation(
    int *num_xlinks_on_init,
    int *num_xlinks_off_init,
    int **states,
    double **times,
    int *num_times,
    int N_xlinks,
    int N_particles,
    int *num_frames,
    double *seconds_per_frame,
    int **xlink_config,

    double **output_frames,
    bool write_raw_data
) {
    (*output_frames) = (double *)malloc(N_particles * (*num_frames) * sizeof(double));
    bool* xlink_states = (bool *)malloc(N_xlinks * sizeof(bool));
    // bool* particle_states = (bool *)malloc(N_particles * sizeof(bool));

    double* last_particle_time = (double *)malloc(N_particles * sizeof(double));
    double* accrued_unbound_times = (double *)malloc(N_particles * sizeof(double));

    for(int i=0; i<N_xlinks; i++){
        // Initial state, in run_KMC the offs get populated first so this comparison will work.
        if (i < *num_xlinks_off_init)
            xlink_states[i] = false;
        else
            xlink_states[i] = true;
    }

    int this_xlink = 0;
    for(int i=0; i<N_particles; i++) {
        // if(is_particle_bound(xlink_config, xlink_states, this_xlink)) 
        //     particle_states[i] = true;
        // else
        //     particle_states[i] = false;
        // this_xlink = this_xlink + (*xlink_config)[i];

        last_particle_time[i] = 0.0;
        accrued_unbound_times[i] = 0.0;
    }
    
    int frame_idx = 0;
    int this_frame_idx;
    double this_unbound_time;
    double to_add;

    for(int time_idx=0; time_idx<(*num_times); time_idx++) {
        double this_time = (*times)[time_idx];
        int this_xlink = (*states)[time_idx];
        int this_particle = get_particle_idx(xlink_config, this_xlink);
        // printf("\n");
        // printf("Time:%f Particle:%i\n", this_time, this_particle);
        // print_bool_array(&xlink_states,N_xlinks);
        // print_double_array(&accrued_unbound_times, N_particles);
        // print_double_array(&last_particle_time, N_particles);
        
        if ((int)(this_time/(*seconds_per_frame)) - last_particle_time[this_particle]) {
            // frame(s) have passed since this particle was last updated
            // need to bring particle information back up to speed
            // iterate through all frame(s), stored by this_frame_idx needed to catch up

            this_frame_idx = (int)(last_particle_time[this_particle]/(*seconds_per_frame));
            while (this_frame_idx < (int)(this_time/(*seconds_per_frame))) {
                // first iteration, make sure that accrued_unbound_time gets added properly
                if (this_frame_idx == (int)(last_particle_time[this_particle]/(*seconds_per_frame))) {
                    this_unbound_time = accrued_unbound_times[this_particle];
                    // if (!xlink_states[this_xlink]) {
                    if (!is_particle_bound(xlink_config, xlink_states, this_xlink)) {
                        to_add = (this_frame_idx + 1)*(*seconds_per_frame) - last_particle_time[this_particle];
                        this_unbound_time = this_unbound_time + to_add;
                        // printf("(case 1) Adding %f to unbound time (tot %f)\n", to_add, this_unbound_time);
                    }
                    (*output_frames)[this_particle*(*num_frames) + this_frame_idx] = this_unbound_time/(*seconds_per_frame);
                    accrued_unbound_times[this_particle] = 0.0;
                }

                // fill in other times, based on whether particle was bound or unbound
                else {
                    if (is_particle_bound(xlink_config, xlink_states, this_xlink))
                        (*output_frames)[this_particle*(*num_frames) + this_frame_idx] = 0;
                    else
                        (*output_frames)[this_particle*(*num_frames) + this_frame_idx] = 1;
                }
                this_frame_idx++;
            }
        }

        // printf("Frame before:%i\n", frame_idx);
        if (frame_idx*(*seconds_per_frame) <= this_time) {
            // printf("Calculation: %f, %f",this_time, (*seconds_per_frame));
            frame_idx = (int) (this_time/(*seconds_per_frame));
            // printf("Frame after:%i\n", frame_idx);
        }

        // xlink was bound
        if (xlink_states[this_xlink]) {
            xlink_states[this_xlink] = false;
        }
        // xlink was unbound
        else {
            if (!is_particle_bound(xlink_config, xlink_states, this_xlink)) {
                if (last_particle_time[this_particle] < frame_idx*(*seconds_per_frame)) {
                    to_add = this_time - frame_idx*(*seconds_per_frame);
                    // printf("to_add:%f, this_time:%f,frame_idx*(*seconds_per_frame):%f\n",to_add, this_time, frame_idx*(*seconds_per_frame));
                }
                else {
                    to_add = this_time - last_particle_time[this_particle];
                    // printf("to_add:%f, this_time:%f,last_particle_time[this_particle]:%f\n, frame_idx:%i, sec_per_frame:%f",to_add, this_time, last_particle_time[this_particle], frame_idx, (*seconds_per_frame));
                }
                accrued_unbound_times[this_particle] = accrued_unbound_times[this_particle] + to_add;
                // printf("(case 2) Adding %f to unbound time (tot %f)\n", to_add, accrued_unbound_times[this_particle]);
            }

            xlink_states[this_xlink] = true;
        }
        last_particle_time[this_particle] = this_time;

    }

    for(int this_xlink = 0; this_xlink < N_xlinks; this_xlink++) {
        // bring particle information back up to speed
        int this_particle = get_particle_idx(xlink_config, this_xlink);
        this_frame_idx = (int)(last_particle_time[this_particle]/(*seconds_per_frame));
        while (this_frame_idx < (*num_frames)) {
            // first iteration
            if (this_frame_idx == (int)(last_particle_time[this_particle]/(*seconds_per_frame))) {
                this_unbound_time = accrued_unbound_times[this_particle];
                if (!is_particle_bound(xlink_config, xlink_states, this_xlink)) {
                    to_add = (this_frame_idx + 1)*(*seconds_per_frame) - last_particle_time[this_particle];
                    this_unbound_time = this_unbound_time + to_add;
                }

                (*output_frames)[this_particle*(*num_frames) + this_frame_idx] = this_unbound_time/(*seconds_per_frame);
                accrued_unbound_times[this_particle] = 0.0;
            }
            // fill in other times
            else {
                if (is_particle_bound(xlink_config, xlink_states, this_xlink))
                    (*output_frames)[this_particle*(*num_frames) + this_frame_idx] = 0;
                else
                    (*output_frames)[this_particle*(*num_frames) + this_frame_idx] = 1;
            }
            this_frame_idx++;
        }
    }

    // particles with zero crosslinks are always unbound
    for(int particle=0;particle<N_particles;particle++){
        if ((*xlink_config)[particle]==0) {
            for (int frame_idx=0; frame_idx<(*num_frames);frame_idx++){
                (*output_frames)[particle*(*num_frames) + frame_idx]=1;
            }
        }
    }

    for(int particle=0;particle<N_particles;particle++) {
            // printf("Particle %d: [", particle);
            for(int frame=0; frame < (*num_frames); frame++) {
                // printf("%f,", (*output_frames)[particle*(*num_frames)+frame]);
            }
            // printf("]\n");
    }

    free(xlink_states);
    free(last_particle_time);
    free(accrued_unbound_times);
}

void generate_chains(
    int N_chains,
    int dp,
    double frac_groups,
    int **out_chains,
    char rand_type,
    int n_xlink_cap
) {
    // Initialize RNG
    mt_state rng_state;
    uint32_t seed;
    // set seed
    if (rand_type == 's')
        seed = 19650218UL;
    else
        seed = time(NULL);
    initialize_state(&rng_state, seed);

    (*out_chains) = (int *)malloc(N_chains * sizeof(int));

    double test_num;
    int this_idx;
    int xlink_count;
    // int this_dp;
    int this_xlink_count;
    bool override = false;
    if (frac_groups == 1){
        override = true;
    }
    for (int chain_idx=0; chain_idx < N_chains; chain_idx++) {
        // xlink_count = 0;
        if(override) {
            xlink_count = dp;
        }
        else {
            if (n_xlink_cap != -1) {
                this_xlink_count = poisson_variable(&rng_state, frac_groups*((double)dp),rand_type);
                while (this_xlink_count > n_xlink_cap) {
                    this_xlink_count = poisson_variable(&rng_state, frac_groups*((double)dp),rand_type);
                }
                xlink_count = this_xlink_count;
            }
            else {
                xlink_count = poisson_variable(&rng_state, frac_groups*((double)dp),rand_type);
            }
        }
        // this_dp = poisson_variable(&rng_state, dp, rand_type);
        // for (int chain_pos=0; chain_pos < this_dp; chain_pos++) {
        //     test_num = random_uniform(&rng_state, rand_type);
        //     this_idx = chain_idx*dp+chain_pos;
        //     if (test_num < frac_groups) {
        //         xlink_count++;
        //     }
        //     else {
        //     }
        // }
        (*out_chains)[chain_idx] = xlink_count;
    }
}

void run_KMC(
    int N_xlinks, 
    double exp_time_tot, 
    double k_on, 
    double k_off, 
    int *num_xlinks_on_init,
    int *num_xlinks_off_init,
    int **out_states,
    double **out_times,
    int *num_times,
    bool write_raw_data,
    char rand_type,
    bool test_kinetics,
    bool start_bound
) {
    // Initialize RNG
    mt_state rng_state;
    uint32_t seed;
    // set seed
    if (rand_type == 's')
        seed = 19650218UL;
    else
        seed = time(NULL);
    initialize_state(&rng_state, seed);

    int idx_to_flip;
    double eq_K = k_on / k_off;
    int N_on;
    int N_off;
    if (test_kinetics && start_bound) {
        N_on = N_xlinks;
        N_off = 0;
    }
    else if (test_kinetics && !start_bound) {
        N_on = 0;
        N_off = N_xlinks;
    }
    else {
        N_on = (int)((eq_K / (eq_K + 1)) * N_xlinks);
        N_off = N_xlinks - N_on;
    }

    // Allocate memory for the particle arrays
    int *xlinks_on = (int *)malloc(N_xlinks * sizeof(int));
    int *xlinks_off = (int *)malloc(N_xlinks * sizeof(int));
    if (!xlinks_on || !xlinks_off) {
        fprintf(stderr, "Memory allocation 1 failed.\n");
        return;
    }

    // Initialize particle arrays
    for (int i = 0; i < N_xlinks; i++) {
        if (i < N_off)
            xlinks_off[i] = i; // Unbound
        else
            xlinks_off[i] = -1;
    }

    for (int i = 0; i < N_xlinks; i++) {
        if (i < N_on)
            xlinks_on[i] = i + N_off; // Bound
        else
            xlinks_on[i] = -1;
    }

    // Arrays to store states and times
    int len_times = 4; // initial allocation length
    int len_states = N_xlinks;
    double *times = (double *)malloc(len_times*sizeof(double));
    int *states = (int *)malloc(len_times*sizeof(int));

    if (!times || !states) {
        fprintf(stderr, "Memory allocation 2 failed.\n");
        free(xlinks_on);
        free(xlinks_off);
        return;
    }

    *num_xlinks_off_init = N_off;
    *num_xlinks_on_init = N_on;

    double exp_time = 0.0;
    int timestep_index = 0;

    int case1_count = 0;
    int case2_count = 0;
    int fail_count = 0;
    // printf("N_on: %d, N_off: %d\n", N_on, N_off);

    FILE *fp;
    char* filename = generate_filename(N_xlinks, k_on, k_off, exp_time_tot, start_bound);
    
    // Check if the file already exists
    fp = fopen(filename, "r");
    if (fp != NULL) {
        // File exists, read the previous output
        printf("File %s already exists. Reading previous output.\n", filename);
        int timestep_index = 0;
        
        // Skip the header row
        char buffer[256];
        fgets(buffer, sizeof(buffer), fp);
        printf("Buffer: %s\n", buffer);

        while (fgets(buffer, sizeof(buffer), fp) != NULL) {
            // ...existing code...
            if (timestep_index >= len_times) {
                len_times *= 2;
                // Reallocate memory
                times = (double *)realloc(times, len_times * sizeof(double));
                states = (int *)realloc(states, len_times * sizeof(int));
                if (!times || !states) {
                    fprintf(stderr, "Memory allocation 3 failed.\n");
                    break;
                }
            }
            char bit_rep[65];
            int particle, switch_val;
            sscanf(buffer, "0b%64[^,],%d,%d", bit_rep, &particle, &switch_val);
            uint64_t exp_time_bits = strtoull(bit_rep, NULL, 2);
            double exp_time;
            memcpy(&exp_time, &exp_time_bits, sizeof(exp_time));
            times[timestep_index] = exp_time;
            states[timestep_index] = particle;
            timestep_index++;
        }

        fclose(fp);

        *out_states = (int *)malloc(timestep_index * sizeof(int));
        *out_times = (double *)malloc(timestep_index * sizeof(double));
        memcpy(*out_states, states, timestep_index * sizeof(int));
        memcpy(*out_times, times, timestep_index * sizeof(double));
        *num_times = timestep_index;

        free(states);
        free(times);
        return;
    }

    if (write_raw_data) {
        errno_t err = fopen_s(&fp, filename, "w");
        if (err != 0) {
            printf("Error opening file.\n");
        }
        else {
            fprintf(fp,"Time,Particle,State\n");
        }
    }

    clock_t start = clock();
    clock_t elapsed = clock();

    while (exp_time < exp_time_tot) {
        clock_t elapsed_check = clock();
        // printf("%f", (((double) (elapsed_check-elapsed)) / CLOCKS_PER_SEC));
        if ((((double) (elapsed_check-elapsed)) / CLOCKS_PER_SEC) > 1) {
            double sim_time = ((double) (elapsed_check-start)) / CLOCKS_PER_SEC;
            double percentage = (exp_time / exp_time_tot)*100;
            printf("Simulation time: %.1f s (at %.1f / %.1f s (%.1f%%))\n", sim_time, exp_time,exp_time_tot, percentage);
            elapsed = elapsed_check;
        }

        double a_KMC = k_on * N_off + k_off * N_on;
        double timestep = (1/a_KMC) * log(1/random_uniform(&rng_state, rand_type));
        // printf("Timestep: %f\n", timestep);
        // printf("Tot: %f\n", exp_time);
        exp_time += timestep;

        if (exp_time > exp_time_tot)
            break;

        if (len_times <= timestep_index+1){
            len_times = len_times * 2;
            // Reallocate memory
            times = (double *)realloc(times, len_times * sizeof(double));
            states = (int *)realloc(states, len_times * sizeof(int));
            if (!times || !states) {
                fprintf(stderr, "Memory allocation 4 failed.\n");
                break;
            }
        }

        int particle_to_move;
        bool success = false;

        // printf("N_on: %d, N_off: %d\n", N_on, N_off);
        double rand_num = random_uniform(&rng_state, rand_type)*a_KMC;
        double compare_num = ((double) N_on)*k_off;
        // printf("Testing %.4f < %.4f\n", rand_num, compare_num);
        if (rand_num < compare_num) {
            // printf("Case 1\n");
            case1_count++;
            if (N_on > 0) {
                // Flip from on to off
                idx_to_flip = int_rand(N_on, &rng_state, rand_type);
                particle_to_move = xlinks_on[idx_to_flip];
                remove_value_from_arr(&xlinks_on, idx_to_flip, -1, N_on);
                add_value_to_arr(&xlinks_off, particle_to_move, N_off);
                N_off++;
                N_on--;
                success = true;
            }
        } 
        else {
            if (N_off > 0) {
                case2_count++;
                // printf("Case 2\n");
                // Flip from off to on
                idx_to_flip = int_rand(N_off, &rng_state, rand_type);
                particle_to_move = xlinks_off[idx_to_flip];
                remove_value_from_arr(&xlinks_off, idx_to_flip, -1, N_off);
                add_value_to_arr(&xlinks_on, particle_to_move, N_on);
                N_on++;
                N_off--;
                success = true;
            }
        }

        // if (test) {
        //     int N_on_eq = (int)((eq_K / (eq_K + 1)) * N_xlinks);
        //     int N_off_eq = N_xlinks - N_on_eq;
        //     if ((timestep_index%20) == 0)
        //         printf("On index: %d, N_on: %d (?=%d), N_off: %d (?=%d)\n", timestep_index, N_on, N_on_eq, N_off, N_off_eq);
        // }

        if (success) {
            states[timestep_index] = particle_to_move;
            times[timestep_index] = exp_time;

            if (write_raw_data) {
                int switch_val = 1;
                if (rand_num < compare_num) {
                    switch_val = 0;
                }
                uint64_t exp_time_bits;
                memcpy(&exp_time_bits, &exp_time, sizeof(exp_time));
                fprintf(fp, "0b");
                for (int i = 63; i >= 0; i--) {
                    fprintf(fp, "%d", (exp_time_bits >> i) & 1);
                }
                fprintf(fp, ",%d,%d\n", particle_to_move, switch_val);
            }

            timestep_index++;
        }
        else{
            fail_count++;
        }
    }

    (*out_states) = (int *)malloc(timestep_index * sizeof(int));
    (*out_times) = (double *)malloc(timestep_index * sizeof(double));
    memcpy(*out_states,states, timestep_index * sizeof(int));
    memcpy(*out_times,times, timestep_index * sizeof(double));
    *num_times = timestep_index;
    // printf("Case1: %d, Case2: %d, fails: %d\n",case1_count, case2_count, fail_count);

    if (write_raw_data) {
        fclose(fp);
    }

    free(xlinks_on);
    free(xlinks_off);
    free(states);
    free(times);
}

void print_array(int** arr, int arr_size) {
    for(int i=0;i<arr_size;i++) {
        printf("%d ", (*arr)[i]);  
    }
    printf("\n"); 
}

void print_double_array(double** arr, int arr_size) {
    for(int i=0;i<arr_size;i++) {
        printf("%f ", (*arr)[i]);  
    }
    printf("\n"); 
}

void print_bool_array(bool** arr, int s1) {
    for(int i=0;i<s1;i++) {
        printf("%i ", (*arr)[i]);  
    }
    printf("\n"); 
}

void print_arrays(int** arr1, int** arr2, int arr_size){
    for(int i=0;i<arr_size;i++) {
        printf("%d ", (*arr1)[i]);  
    }
    printf("\n");  
    for(int i=0;i<arr_size;i++) {
        printf("%d ", (*arr2)[i]);  
    }
    printf("\n");  
}

void remove_value_from_arr(int** arr, int idx_to_remove, int new_value, size_t arr_size) {
    for(int i=idx_to_remove; i < arr_size-1; i++) {
        (*arr)[i] = (*arr)[i+1];
    }
    (*arr)[arr_size-1] = new_value;
}

void add_value_to_arr(int** arr, int value, int arr_size) {
    (*arr)[arr_size] = value;
}

int find_mode_count(int* arr, int max_num, int arr_size) {
    int max_count = 0;
    int mode = arr[0];
    int *freq = (int *)calloc(max_num, sizeof(int));

    for (int i = 0; i < arr_size; i++) {
        freq[arr[i]]++;
        if (freq[arr[i]] > max_count) {
            max_count = freq[arr[i]];
            mode = arr[i];
        }
    }
    free(freq);
    return max_count;
}

void initialize_state(mt_state* state, uint32_t seed) 
{
    uint32_t* state_array = &(state->state_array[0]);
    
    state_array[0] = seed;                          // suggested initial seed = 19650218UL
    
    for (int i=1; i<n; i++)
    {
        seed = f * (seed ^ (seed >> (w-2))) + i;    // Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier.
        state_array[i] = seed; 
    }
    
    state->state_index = 0;
}


uint32_t random_uint32(mt_state* state)
{
    uint32_t* state_array = &(state->state_array[0]);
    
    int k = state->state_index;      // point to current state location
                                     // 0 <= state_index <= n-1   always
    
//  int k = k - n;                   // point to state n iterations before
//  if (k < 0) k += n;               // modulo n circular indexing
                                     // the previous 2 lines actually do nothing
                                     //  for illustration only
    
    int j = k - (n-1);               // point to state n-1 iterations before
    if (j < 0) j += n;               // modulo n circular indexing

    uint32_t x = (state_array[k] & UMASK) | (state_array[j] & LMASK);
    
    uint32_t xA = x >> 1;
    if (x & 0x00000001UL) xA ^= a;
    
    j = k - (n-m);                   // point to state n-m iterations before
    if (j < 0) j += n;               // modulo n circular indexing
    
    x = state_array[j] ^ xA;         // compute next value in the state
    state_array[k++] = x;            // update new state value
    
    if (k >= n) k = 0;               // modulo n circular indexing
    state->state_index = k;
    
    uint32_t y = x ^ (x >> u);       // tempering 
             y = y ^ ((y << s) & b);
             y = y ^ ((y << t) & c);
    uint32_t z = y ^ (y >> l);
    
    return z; 
}

// Generate a random uniform number between 0 and 1
int int_rand(int range, mt_state *state, char rand_type) {
    // srand(time(NULL));
    int output;
    if (rand_type == 'o')
        output = 1;
    else
        output = random_uint32(state) % range;
    // printf("int: %d (%d)\n",output,range);
    return output;
}

double random_uniform(mt_state *state, char rand_type) {
    // srand(time(NULL));
    double output;
    if (rand_type == 'o') {
        output = 0.5;
    }
    else{
        output = (double)random_uint32(state) / (double)(UINT32_MAX);
        while (output==0) {
            output = (double)random_uint32(state) / (double)(UINT32_MAX);
        }
    }
    return output;
}


int poisson_variable(mt_state *state, double lam, char rand_type) {
    if (lam <= 0) {
        return -1; // Return an error code for invalid lambda
    }

    int k = 0;
    double L = exp(-lam);
    double p = 1.0;

    do {
        k++;
        double var = random_uniform(state, rand_type); // Generate a random uniform number
        p *= var;
    } while (p > L);

    return k - 1;
}

int sum_c(int **arr, int size){
    int count = 0;
    for (int i=0; i<size; i++){
        count = count + (*arr)[i];
    }
    return count;
}

void verify_simulation() {
    char rand_type = 's';
    
    // generate chains
    int N_particles=1000;
    int dp=1;
    double frac_groups = 1;
    int *xlink_config;
    int n_xlink_cap = -1;
    generate_chains(N_particles, dp, frac_groups, &xlink_config, rand_type, n_xlink_cap);

    print_array(&xlink_config, N_particles);
    int N_xlinks = sum_c(&xlink_config, N_particles);
    printf("# xlink:%i\n", N_xlinks);


    double seconds_per_frame = 5;
    int num_frames = 5;
    // int N_xlinks=200000;
    double k_on=1;
    double K =0.1;
    double k_off=k_on/K;
    double exp_time_tot= num_frames*seconds_per_frame;
    int xlinks_on_init;
    int xlinks_off_init;
    int *out_states;
    double *out_times;
    int num_times;
    bool write_raw_data = true;
    bool test = false;
    bool start_bound = true;

    clock_t start = clock();
    run_KMC(
        N_xlinks, 
        exp_time_tot, 
        k_on, 
        k_off, 
        &xlinks_on_init,
        &xlinks_off_init,
        &out_states,
        &out_times,
        &num_times,
        write_raw_data,
        rand_type,
        true,
        start_bound
    );
}

void test_simulation() {
    char rand_type = 's';
    
    // generate chains
    int N_particles=100;
    int dp=65;
    double frac_groups = 0.0308;
    int *xlink_config;
    int n_xlink_cap = -1;
    generate_chains(N_particles, dp, frac_groups, &xlink_config, rand_type, n_xlink_cap);

    print_array(&xlink_config, N_particles);
    int N_xlinks = sum_c(&xlink_config, N_particles);
    printf("# xlink:%i\n", N_xlinks);


    double seconds_per_frame = 400;
    int num_frames = 5;
    // int N_xlinks=200000;
    double k_on=1;
    double K = 0.001;
    double k_off=k_on/K;
    double exp_time_tot= num_frames*seconds_per_frame;
    int xlinks_on_init;
    int xlinks_off_init;
    int *out_states;
    double *out_times;
    int num_times;
    bool write_raw_data = true;
    bool test = false;
    bool start_bound = true;

    clock_t start = clock();
    run_KMC(
        N_xlinks, 
        exp_time_tot, 
        k_on, 
        k_off, 
        &xlinks_on_init,
        &xlinks_off_init,
        &out_states,
        &out_times,
        &num_times,
        write_raw_data,
        rand_type,
        false,
        start_bound
    );
    clock_t end = clock();
    double cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
    printf("Time simulate: %f\n", cpu_time_used);
    start = clock();

    double *output_frames;
    int mode_count;
    process_simulation(
        &xlinks_on_init,
        &xlinks_off_init,
        &out_states,
        &out_times,
        &num_times,
        N_xlinks,
        N_particles,
        &num_frames,
        &seconds_per_frame,
        &xlink_config,

        &output_frames,
        write_raw_data
    );

    end = clock();
    cpu_time_used = ((double) (end-start)) / CLOCKS_PER_SEC;
    printf("Time postprocess: %f\n", cpu_time_used);


    // FILE *fp;
    // errno_t err = fopen_s(&fp, "output_frames_data.csv", "w");
    // if (err != 0) {
        // printf("Error opening file.\n");
    // }
    // fprintf(fp,"Here");
    for(int particle=0;particle<N_particles;particle++) {
        printf("Particle %d: [", particle);
        for(int frame=0; frame < num_frames; frame++) {
            printf("%f,", output_frames[particle*num_frames+frame]);
        }
        printf("]\n");
    }
    // fclose(fp);

    free(output_frames);
    free(out_states);
    free(out_times);
}

void test_kinetics() {
    char rand_type = 's';
    
    // generate chains
    int N_particles=5;
    int dp=2;
    double frac_groups = 1;
    int *xlink_config;
    int n_xlink_cap = -1;
    generate_chains(N_particles, dp, frac_groups, &xlink_config, rand_type, n_xlink_cap);

    print_array(&xlink_config, N_particles);
    int N_xlinks = sum_c(&xlink_config, N_particles);
    printf("# xlink:%i\n", N_xlinks);

    // double seconds_per_frame = 4;
    // int num_frames = 5;
    // int N_xlinks=200000;
    double k_on=1;
    double k_off = 1;
    double exp_time_tot= 10;
    int xlinks_on_init;
    int xlinks_off_init;
    int *out_states;
    double *out_times;
    int num_times;
    bool write_raw_data = true;
    bool test = false;
    bool start_bound = true;

    clock_t start = clock();
    run_KMC(
        N_xlinks, 
        exp_time_tot, 
        k_on, 
        k_off, 
        &xlinks_on_init,
        &xlinks_off_init,
        &out_states,
        &out_times,
        &num_times,
        write_raw_data,
        rand_type,
        true,
        start_bound
    );
    print_double_array(&out_times, num_times);
    print_array(&out_states, num_times);
}

void test_uniform(){
    mt_state rng_state;
    uint32_t seed;
    seed = time(NULL);
    initialize_state(&rng_state, seed);
    char rand_type = 'r';

    // Choose size: 100, 10000, or 1000000
    const int sizes[] = {100, 10000, 1000000};
    int size = sizes[2]; // Example: choosing 10000
    double *values = (double *) malloc(size * sizeof(double));
    if (values == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return;
    }

    // Generate random uniforms
    for (int i = 0; i < size; i++) {
        values[i] = random_uniform(&rng_state, rand_type);
    }

    // Calculate the mean
    double sum = 0.0;
    for (int i = 0; i < size; i++) {
        sum += values[i];
    }
    double mean = sum / size;

    // Calculate the standard deviation
    double sum_squared_diff = 0.0;
    for (int i = 0; i < size; i++) {
        sum_squared_diff += (values[i] - mean) * (values[i] - mean);
    }
    double std_dev = sum_squared_diff / size;

    // Print the results
    printf("Sample size: %d\n", size);
    printf("Mean: %.6f (?=%.1f)\n", mean, 0.5);
    printf("Standard Deviation: %.6f(?=%.5f)\n", std_dev, (double) 1/12);

    // Free allocated memory
    free(values);
}

void test_poisson(double lam) {
    mt_state rng_state;
    uint32_t seed;
    seed = time(NULL);
    initialize_state(&rng_state, seed);
    char rand_type = 'r';

    // Choose size: 100, 10000, or 1000000
    const int sizes[] = {100, 10000, 1000000};
    int size = sizes[2]; // Example: choosing 10000
    int *values = (int*) malloc(size * sizeof(int));
    if (values == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return;
    }

    // Generate random poissons
    for (int i = 0; i < size; i++) {
        values[i] = poisson_variable(&rng_state, lam, rand_type);
    }

    // Calculate the mean
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += values[i];
    }
    double mean = (double)sum / (double)size;

    // Calculate the standard deviation
    double sum_squared_diff = 0.0;
    for (int i = 0; i < size; i++) {
        sum_squared_diff += (values[i] - mean) * (values[i] - mean);
    }
    double std_dev = sum_squared_diff / size;

    // Print the results
    printf("Sample size: %d\n", size);
    printf("Mean: %.6f (?=%.1f)\n", mean, lam);
    printf("Standard Deviation: %.6f(?=%.5f)\n", std_dev, lam);

    // Free allocated memory
    free(values);
}

char* generate_filename(int N, double kon, double koff, double time, bool start_bound) {
    static char filename[120];
    char cwd[1024];
    get_working_directory(cwd, sizeof(cwd));

    int bound_flag = start_bound ? 1 : 0;

    if (strstr(cwd, "C_code") != NULL) {
        sprintf(filename, "results/sim_n%d_kon%.2f_koff%.2f_t%.1f_b%d.csv", N, kon, koff, time, bound_flag);
    } else {
        sprintf(filename, "C_code/results/sim_n%d_kon%.2f_koff%.2f_t%.1f_b%d.csv", N, kon, koff, time, bound_flag);
    }

    return filename;
}

int main() {
    // double lam=20.512;
    // test_poisson(lam);
    // test_simulation();
    test_kinetics();
    // verify_simulation();

    // mt_state state;
    // uint32_t seed = time(NULL);
    // initialize_state(&state, seed);

    // // Generate and print 10 random numbers
    // for (int i = 0; i < 10; i++) {
    //     uint32_t random_number = random_uint32(&state);
    //     printf("Random Number %d: %u\n", i + 1, random_number);
    // }

    // int nums[20] = {0, 1, 2, 2, 5, 5, 5, 8, 9, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
    // int size = 20;
    // int *test = (int *)malloc(size*sizeof(int));
    // for (int i = 0; i < size; i++) {
    //     test[i] = nums[i];
    // }

    // printf("%d",find_mode_count(&test, 16, 10));

    // for (int i = 0; i < size; i++) {
    //     printf("%d ", test[i]);  
    // }
    // printf("\n");

    // add_value_to_arr(&test, 10, 10);

    // for (int i = 0; i < size; i++) {
    //     printf("%d ", test[i]);  
    // }
    // printf("\n");

    // printf("Num times: %d\n", num_times);
    // printf("N_on_init: %d\n", xlinks_on_init);
    // printf("N_off_init: %d\n", xlinks_off_init);

    // print_array(&xlinks_on_init, N_xlinks);
    // print_array(&xlinks_off_init, N_xlinks);
    // print_array(&out_states, num_times);
    // print_double_array(&out_times, num_times);

    // for(int particle=0; particle < N_xlinks; particle++){
    //     printf("Particle: %d\n", particle);
    //     printf("States: ");
    //     for(int i=0;i<mode_count+1;i++) {
    //         printf("%d ", output_states[particle*mode_count + i]);  
    //     }
    //     printf("\n");         
    //     printf("Times: ");
    //     for(int i=0;i<mode_count;i++) {
    //         printf("%f  ", output_times[particle*mode_count + i]);  
    //     }
    //     printf("\n");  
    // }

    // printf("FINAL DATA:\n");
    // printf("Output frames--\n");
    // for(int particle=0;particle<N_xlinks;particle++) {
    //     printf("Particle %d: [", particle);
    //     for(int frame=0; frame < (num_frames); frame++) {
    //         printf("\n(%f, ", frame*(seconds_per_frame));
    //         printf("%f)", (output_frames)[particle*(num_frames)+frame]);
    //     }
    //     printf("]\n", particle);
    // }


    // free(xlinks_on_init);

    // int N = 1000;
    // double kon = 1.0;
    // double koff = 0.1;
    // double time = 10.0;
    // char* filename = generate_filename(N, kon, koff, time);
    // printf("Generated filename: %s\n", filename);

    // char cwd[1024];
    // get_working_directory(cwd, sizeof(cwd));
    // printf("Current working directory: %s\n", cwd);

    return 1;
}
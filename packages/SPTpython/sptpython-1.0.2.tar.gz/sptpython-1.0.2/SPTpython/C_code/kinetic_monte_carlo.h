#ifndef KINETIC_MONTE_CARLO_H
#define KINETIC_MONTE_CARLO_H

#include <stdbool.h>

int sum_c(int **arr, int size);

void generate_chains(
    int N_chains,
    int dp,
    double frac_groups,
    int **out_chains,
    char rand_type,
    int n_xlink_cap
);

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
);

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
);

#endif
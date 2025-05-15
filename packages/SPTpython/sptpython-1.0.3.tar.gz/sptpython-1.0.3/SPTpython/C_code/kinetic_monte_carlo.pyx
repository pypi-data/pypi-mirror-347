cimport numpy as cnp
import numpy as np
from libcpp cimport bool
import time
import pandas as pd
from libc.stdlib cimport free

cdef extern from "kinetic_monte_carlo.h":
    int sum_c(int **arr, int size)
    void generate_chains(
        int N_chains,
        int dp,
        double frac_groups,
        int **out_chains,
        char rand_type,
        int n_xlink_cap
    )
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
    )
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
    )

def run_kinetics_test(
    int N_particles, 
    int dp,

    double k_on, 
    double k_off, 
    double exp_time_tot,
    bool start_bound,
    int n_xlink_cap
    ):
    cdef int *xlink_config

    cdef int num_xlinks_on_init
    cdef int num_xlinks_off_init
    cdef int *out_states
    cdef double *out_times
    cdef double *output_frames
    cdef int num_times
    cdef char rand_type = b'r'[0]
    cdef bool test_kinetics = True
    cdef bool write_raw_data = True
    
    cdef double frac_groups = 1.0

    # Generate chains
    generate_chains(
        N_particles,
        dp,
        frac_groups,
        &xlink_config,
        rand_type,
        n_xlink_cap
    )
    cdef int N_xlinks = sum_c(&xlink_config, N_particles)

    # Run the simulation
    t0 = time.time()
    run_KMC(
        N_xlinks, 
        exp_time_tot, 
        k_on, 
        k_off,
        &num_xlinks_on_init,
        &num_xlinks_off_init,
        &out_states,
        &out_times,
        &num_times,
        write_raw_data,
        rand_type,
        test_kinetics,
        start_bound
    )



def run_kinetic_monte_carlo(
    int N_particles, 
    int dp,
    double frac_groups,

    double k_on, 
    double k_off, 
    int num_frames, 
    double seconds_per_frame, 
    bool write_raw_data, 
    str input_rand_type,
    int n_xlink_cap):

    cdef int *xlink_config

    cdef int num_xlinks_on_init
    cdef int num_xlinks_off_init
    cdef int *out_states
    cdef double *out_times
    cdef double *output_frames
    cdef int num_times
    cdef char rand_type
    cdef bool test_kinetics = False
    cdef bool start_bound = True

    cdef double exp_time_tot = num_frames*seconds_per_frame

    if input_rand_type == "off":
        rand_type = b'o'[0]
    elif input_rand_type == "random":
        rand_type = b'r'[0]
    else:
        rand_type = b's'[0]

    # Generate chains
    generate_chains(
        N_particles,
        dp,
        frac_groups,
        &xlink_config,
        rand_type,
        n_xlink_cap
    )
    cdef int N_xlinks = sum_c(&xlink_config, N_particles)

    # Run the simulation
    t0 = time.time()
    run_KMC(
        N_xlinks, 
        exp_time_tot, 
        k_on, 
        k_off,
        &num_xlinks_on_init,
        &num_xlinks_off_init,
        &out_states,
        &out_times,
        &num_times,
        write_raw_data,
        rand_type,
        test_kinetics,
        start_bound
    )
    t1 = time.time()

    # Process the simulation
    process_simulation(
        &num_xlinks_on_init,
        &num_xlinks_off_init,
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
    )
    t2 = time.time()

    cdef cnp.ndarray video = np.empty(num_frames*N_particles, dtype=np.float64)
    cdef double[:] video_view = video

    cdef cnp.ndarray out_xlink_config = np.empty(N_particles, dtype = np.int32)
    cdef int[:] xlink_view = out_xlink_config

    cdef int i
    for i in range(num_frames*N_particles):
        video_view[i] = output_frames[i]    

    t3 = time.time()

    for i in range(N_particles):
        xlink_view[i] = xlink_config[i]

    del1 = t1-t0
    del2 = t2-t1
    del3 = t3-t2
    if del1 > 0.2 or del2 > 0.2 or del3 > 0.2:
        print("C a little slow. Sim: {0:0.3f}, Process: {1:0.3f}, np cast: {2:0.3f}".format(del1,del2,del3))

    free(out_states)
    free(out_times)
    free(output_frames)
    free(xlink_config)
    return video.reshape(N_particles, num_frames), out_xlink_config

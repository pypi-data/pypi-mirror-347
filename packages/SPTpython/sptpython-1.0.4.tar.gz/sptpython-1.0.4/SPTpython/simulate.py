import numpy as np
import scipy
import matplotlib.pyplot as plt
import trackpy as tp
import pandas as pd
import copy
if __name__ != '__main__':
    from . import postprocessing 
    from . import config
    cfg = config.load_config() # script uses config parameters
    from .utils import N_gaussian
import scipy

def KMC(N_particles: int, exp_time_tot: float, k_on: float, k_off: float, write_csv):
    """
    Perform a kinetic monte-carlo simulation of a simple first-order reaction
    based on forward rate constant k_on and backward rate constant k_off

    Args:
        N_particles (int): Total number of particles to simulate
        exp_time_tot (float): Total experiment time, with same units as k_on and k_off
        k_on (float): Forward reaction rate constant
        k_off (float): Backward reaction rate constant

    Returns:
        tuple: Tuple containing two lists: (1) list of times
        at which the state of the simulation changed, (2) a
        list of each state at those given times. This state is a list of lists,
        where each element of each inner list corresponds to a given particle,
        and 0 or 1 indicates whether the particle is unbound or bound, respectively.
    """
    eq_K = k_on/k_off
    
    N_on_init = int((eq_K/(eq_K+1))*N_particles)
    N_off_init = N_particles-N_on_init
    state = np.array([0]*N_off_init + [1]*N_on_init)
    np.random.shuffle(state)
    
    particles_changed = []
    states = [copy.deepcopy(state)]
    times = [0]
    
    exp_time = 0
    while exp_time < exp_time_tot:
        N_off = np.count_nonzero(state==0)
        N_on = np.count_nonzero(state==1)
        a = k_on*N_off+k_off*N_on
        timestep = (1/a)*np.log(1/np.random.uniform())
        exp_time += timestep
        
        frac_on = N_on/(N_off+N_on)
        # flip from on to off
        if np.random.uniform() < frac_on:
            idxs_on = np.nonzero(state==1)[0]
            idx_to_flip = idxs_on[np.random.randint(0,N_on)]
            state[idx_to_flip] = 0
        # flip from off to on
        else:
            idxs_on = np.nonzero(state==0)[0]
            idx_to_flip = idxs_on[np.random.randint(0,N_off)]
            state[idx_to_flip] = 1
        particles_changed.append(idx_to_flip)
        states.append(copy.deepcopy(state))
        times.append(exp_time)
    # print(times)
    if write_csv:
        with open("time_particle_data_python.csv", 'w') as fout:
            for time, particle in zip(times[1:], particles_changed):
                fout.write(f"Time {time}, Particle {particle}\n")
    return times, np.stack(states)

def process_KMC(times, states, exp_time_tot):
    """
    Processes results from KMC() simulation call.
    For each particle in the simulation, keep track of
    the times which the particle is bound and unbound for,
    using a list of the following form:
    [[[t11, t21], s1], [t12, t22], s2, ...]
    t11 is the start of the time range
    t21 is the end of the time range
    s1 is a boolean stating whether the particle is bound or unbound:
    IMPORTANT: ZERO is bound, ONE is unbound.

    Args:
        times (list): list of times at which the state of the simulation changed
        states (list): list of simulation states (see KMC() for more complete description)
        exp_time_tot (float): total experiment time

    Returns:
        dict: Dictionary keyed by particle, containing lists of the form described above.
    """
    particle_info = {}
    
    for particle in range(states.shape[1]):
        states_processed = []
        particle_states = states[:, particle]
        
        # find idxs of particle_states where it flips states
        # idx is off by one for the new state
        idxs_state_switch = np.nonzero(np.diff(particle_states)!=0)[0]
        for iter_idx, idx_state_switch in enumerate(idxs_state_switch):
            if particle_states[idx_state_switch+1] == 0:
                # particle just was bound
                current_state = 1
            else:
                current_state = 0
            if iter_idx == 0:
                states_processed.append([[0,times[idx_state_switch+1]],current_state])
            else:
                start_time = times[idxs_state_switch[iter_idx-1]+1]
                states_processed.append([[start_time,times[idx_state_switch+1]],current_state])

        # add in state of particle at the end
        if len(states_processed) == 0:
            states_processed.append([[0,exp_time_tot],particle_states[0]])
        else:
            states_processed.append([[times[idxs_state_switch[-1]],exp_time_tot],1-states_processed[-1][1]])
        particle_info[particle] = states_processed
        
    return particle_info

def get_fraction_unbound(t_low, t_high, info):
    """
    Steps through the information of a given particle (see process_KMC()),
    and determines the fraction of time that that particle is unbound for

    Args:
        t_low (float): lower end of time range to look in
        t_high (float): upper end of time range to look in
        info (list): particle info to look through

    Returns:
        float: fraction of time the particle is bound for
    """
    unbound_time = 0
    info_iter = 0
    
    in_time_window = False
    done = False
    while not done:
        left = info[info_iter][0][0]
        right = info[info_iter][0][1]
        state = info[info_iter][1]
        
        # window encapsulates time range given, unbound
        if not in_time_window and left <= t_low and right >= t_high and state==0:
            return 1
        
        # window encapsulates time range given, bound
        elif not in_time_window and left <= t_low and right >= t_high and state==1:
            return 0
            
        # right part of window is in, unbound
        elif not in_time_window and right >= t_low and state == 0:
            in_time_window = True
            unbound_time += right - t_low
            
        # right part of window is in, bound
        elif not in_time_window and right >= t_low and state == 1:
            in_time_window = True
            
        # entire window is in
        elif state == 0 and in_time_window and left >= t_low and right <= t_high:
            unbound_time += right - left
            
        # left part of window is in, unbound
        elif state == 0 and in_time_window and right >= t_high:
            unbound_time += t_high - left
            in_time_window = False
            done = True
            
        # left part of window is in, bound
        elif state == 1 and in_time_window and right >= t_high:
            in_time_window = False
            done = True
        
        info_iter += 1
        if info_iter == len(info):
            done = True
            
    return unbound_time / (t_high - t_low)


def gamma(x,a,b):
    """
    Computes gamma distribution according to 
    https://en.wikipedia.org/wiki/Gamma_distribution
    """
    return (np.power(b,a)/scipy.special.gamma(a))*np.power(x,a-1)*np.exp(-b*x)

def brownian_jump(D, t, shape, noise_type='random'):
    """
    Generates a brownian jump with a given diffusivity over a given time.
    Brownian jumps are governed by the normal distribution.

    Args:
        D (float): Particle diffusivity
        t (float): Time of step. Units of time must match between D and t.

    Returns:
        np.array: Resturns a (2,1) array of a coordinate pair of the brownian jump.
    """
    if noise_type == "random":
        np.random.seed(None)
        rands = np.random.normal(0,(2*D*t)**0.5,shape)
    elif noise_type == "seeded":
        np.random.seed(42)
        rands = np.random.normal(0,(2*D*t)**0.5,shape)
    else:
        rands = np.ones(shape)*D*4*t
    return rands

def simulate_video_from_C(particle_info, D, delay, n_frames, box_size, noise_dict):
    shape = (n_frames-1, particle_info.shape[0], 2)
    # print(f"Shape:{shape}")

    # initial positions
    if noise_dict["r_init_pos"] == "random":
        np.random.seed(None)
        init_pos = np.random.uniform(0,box_size,(particle_info.shape[0],2))
    elif noise_dict["r_init_pos"] == "off":
        init_pos = np.full((particle_info.shape[0],2),box_size/2)
    else:
        np.random.seed(42)
        init_pos = np.random.uniform(0,box_size,(particle_info.shape[0],2))
        
    max_jumps = brownian_jump(D, delay,shape, noise_dict["r_brownian"])
    actual_jumps = max_jumps*np.sqrt(particle_info.transpose()[:,:,np.newaxis])
    
    result = np.zeros((n_frames,particle_info.shape[0],2))
    result[0] = init_pos
    result[1:] = np.cumsum(actual_jumps, axis=0) + init_pos
    
    return result

def simulate_video(particle_info, D, delay, n_frames, box_size):
    """
    Given particle info (see process_KMC()), unbound particle diffusivity, 
    delay between frames, and number of frames, generate a video.
    For each particle in each frame, determine the fraction of that frame that
    the particle is bound for. Then, the particle only takes that fraction
    of a diffusive step. 
    
    Also, give each particle an initial position within a square box of specified size.

    Args:
        particle_info (dict): Particle info (see process_KMC())
        D (float): Unbound particle diffusivity
        delay (float): Time in between each frame in the video. Time units must match with D
        n_frames (int): Number of frames to simulate
        box_size (float): Box size. Length units must match with D.

    Returns:
        list: the "video", containing particle location at each frame.
    """
    # D in microns
    # box size in microns
    video = np.zeros((n_frames, len(particle_info), 2))
    
    unbound_fraction_sample = []
    total_time = delay*n_frames
    
    for particle in range(len(particle_info)):
        info = particle_info[particle]
        
        # initial position
        pos = np.random.uniform(0,box_size,(2,))
        video[0,particle,:] = pos
        
        total_mobile_time = 0
        
        for frame in range(1,n_frames):
            time_unbound = delay*get_fraction_unbound((frame-1)*delay,frame*delay, info)
            pos = pos + brownian_jump(D, time_unbound, (2,))
            video[frame,particle,:] = pos
            
            total_mobile_time += time_unbound
            
        unbound_fraction_sample.append(total_mobile_time/total_time)

    pd.DataFrame(np.array(unbound_fraction_sample)).to_csv("unbound_fraction_sample.csv")

    return video

def simulate_noise(n_particles, n_frames, gauss_noise, positions, noise_type):
    """
    Noise observed on a camera video results in localization uncertainty,
    which should result in gamma-shaped noise (citation?)

    Args:
        n_particles (int): number of particles to add gamma noise to
        n_frames (int): number of frames to add gamma noisee to
        gauss_noise (list): gaussian distribution standard deviation
        positions (np.array, optional): Positions to add noise to. Defaults to None.

    Returns:
        np.array: data with noise added in
    """
    shape = (n_frames,n_particles,2)
    if noise_type == "random":
        np.random.seed(None)
        noise = np.random.normal(0,gauss_noise,size=shape)
    elif noise_type == "seeded":
        np.random.seed(42)
        noise = np.random.normal(0,gauss_noise,size=shape)
    else:
        noise = np.zeros(shape)

    return positions + noise

def construct_dataframe(positions,n_particles, n_frames):
    """
    Puts positional data and particle information generated from
    generate_video() into a format compatible with information
    generated by trackpy.

    Args:
        positions (list): particle position information
            shape of positions: frames, particle, xy
        n_particles (int): total number of particles
        n_frames (int): total number of frames

    Returns:
        pd.DataFrame(): trackpy-compatible particle information.
    """
    dataframes = []
    for particle in range(n_particles):
        this_df = pd.DataFrame({'x':positions[:,particle,0],'y':positions[:,particle,1], 'particle':[particle for _ in range(n_frames)], 'frame':[i for i in range(n_frames)]})
        dataframes.append(this_df)
    return pd.concat(dataframes)

def estimate_EQ_K(msds, lag_frame):
    """
    Performs the following algorithm:
    (0) Input msd information and the lag_frame K is to be calculated at
    (1) Calculate the vertical histogram at that lag frame
    (2) Fit those vertical histogram values to a bimodal gaussian. Current initial guess is hardcoded.

    Args:
        msds (pd.DataFrame): dataFrame containing msd information
        lag_frame (int): lag frame to be used in estimate

    Returns:
        float: equilibrium K value
    """
    this_data = np.log10(np.array(msds.loc[msds.index[lag_frame],]))
    
    n, bins, _ = plt.hist(this_data, bins=cfg["num_histogram_bins"], density=True)
    xs = (bins[:-1] + bins[1:])/2
    
    # A,sig,mu
    p0 = [0.5, 1, -1, 0.5, 1, -1.2]
    fitResult,_ = scipy.optimize.curve_fit(N_gaussian, xs, n, p0)
    
    # slower is first
    if fitResult[2] < fitResult[5]:
        return fitResult[0] / fitResult[3]
    else:
        return fitResult[3] / fitResult[0]
    
if __name__ == '__main__':
    N_particles=20
    k_on=1.98e-4
    k_off=2.75e-5
    exp_time_tot = 40*5
    import time
    start = time.time()
    result = KMC(N_particles,exp_time_tot,k_on,k_off)
    end = time.time()
    print(f"Len times: {len(result[0])}")
    print(f"Time taken: {end-start}")
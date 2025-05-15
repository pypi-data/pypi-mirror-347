import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np
import kinetic_monte_carlo
import os
import pyperclip
import struct

class Polymer:
    def __init__(self, dp, start_bound):
        self.dp = dp
        self.xlinks = [int(start_bound) for _ in range(dp)]
    def set_xlink(self, idx, val):
        self.xlinks[idx] = val
    def get_bound(self):
        if 1 in self.xlinks:
            return True
        return False

def f(t, k_on, k_off, start_bound):
    if start_bound:
        return (k_on + k_off*np.exp(-(k_on+k_off)*(t)))/(k_on+k_off)
    else:
        return (k_off + k_on*np.exp(-(k_on+k_off)*(t)))/(k_on+k_off)

def f_reverse(t, k_on, k_off, start_bound):
    if start_bound:
        return (k_off - k_off*np.exp(-(k_on+k_off)*(t)))/(k_on+k_off)
    else:
        return (k_on - k_on*np.exp(-(k_on+k_off)*(t)))/(k_on+k_off)
    
def d_data(xs, ys):
    # forward difference
    return np.diff(ys) / np.diff(xs)

def rolling_average(x,n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

def check_counts(times, Ns, start, end):
    mask = (times >= start) & (times <= end)
    diffs = np.diff(Ns[mask])
    unique, counts = np.unique(diffs, return_counts=True)
    return dict(zip(unique, counts))

def run_KMC_kinetics(n_particles, dp, k_on, k_off, exp_time_tot, start_bound):
    fname = 'C_code/results/sim_n{}_kon{:.2f}_koff{:.2f}_t{:.1f}_b{}.csv'.format(n_particles*dp, k_on, k_off, exp_time_tot, int(start_bound))

    if not os.path.exists(fname):
        print("Running C code...")
        kinetic_monte_carlo.run_kinetics_test(n_particles, dp, k_on, k_off, exp_time_tot, start_bound)
        print("Done.")
    else:
        print(f"File {fname} already exists. Skipping C code execution.")

    polymers = []
    for _ in range(n_particles):
        polymers.append(Polymer(dp, start_bound))

    times = []
    Ns = []
    Nreverses = []
    last_n = n_particles
    last_n_reverse = 0

    with open(fname, 'r') as fin:
        total_lines = sum(1 for _ in fin)
        print(f"Total lines in file: {total_lines}")

    with open(fname,'r') as fin:
        fin.readline()
        for line in fin:
            line = line.replace('\n','')
            these_data = line.split(',')
            tot_xlink_idx = int(these_data[1])
            polymer_idx = tot_xlink_idx//dp
            this_xlink_idx = tot_xlink_idx - polymer_idx*dp
            
            state_before = polymers[polymer_idx].get_bound()
            polymers[polymer_idx].set_xlink(this_xlink_idx, int(these_data[2]))
            
            state_after = polymers[polymer_idx].get_bound()
            
            if (state_before == True and state_after == False and start_bound):
                last_n -= 1
                last_n_reverse += 1
            elif (state_before == False and state_after == True and start_bound):
                last_n += 1
                last_n_reverse -= 1
            elif (state_before == True and state_after == False and not start_bound):
                last_n += 1
                last_n_reverse -= 1
            elif (state_before == False and state_after == True and not start_bound):
                last_n -= 1
                last_n_reverse += 1
            
            time = struct.unpack('>d',int(these_data[0][2:],2).to_bytes(8,byteorder='big'))[0]
            times.append(time)
            Ns.append(last_n)
            Nreverses.append(last_n_reverse)
    return np.array(times), np.array(Ns), np.array(Nreverses)

def main():
    n_particles = 2e4
    dp = 4
    k_on = 4
    k_off = 1
    exp_time_tot = 10
    start_bound = True
    n_particles = int(n_particles)
    
    times, Ns, Nreverses = run_KMC_kinetics(n_particles, dp, k_on, k_off, exp_time_tot, start_bound)

    lo = 4
    hi = 10
    num = 20
    forward_sample = []
    reverse_sample = []
    for t in np.linspace(lo, hi-(hi-lo)/num, num):
        val = check_counts(times, Ns, t, t+(hi-lo)/num)
        if 1 not in val.keys():
            val[1] = 0
            print("WARNING: No 1 transitions found.")
        if -1 not in val.keys():
            val[-1] = 0
            print("WARNING: No -1 transitions found.")
            
        if start_bound:
            reverse_sample.append(val[1])
            forward_sample.append(val[-1])
        else:
            reverse_sample.append(val[-1])
            forward_sample.append(val[1])
                                
    macro_K = np.power(1+k_on/k_off,dp)-1
    N_on_eq = macro_K / (1+macro_K)*n_particles
    N_off_eq = n_particles - N_on_eq
    
    k_ons = np.array(forward_sample) / (((hi-lo)/num)*N_off_eq)
    k_offs = np.array(reverse_sample) / (((hi-lo)/num)*N_on_eq)
    
    print("k_on_approx: {:.5e} +/- {:.5e}, k_off_approx: {:.5e} +/- {:.5e}".format(np.mean(k_ons), np.std(k_ons), np.mean(k_offs), np.std(k_offs)))

    plot_config = {
        True:{'c':'k','c_r':'b', 'lab':'On','lab_r':'Off','t':'Bound Init'},
        False:{'c':'b','c_r':'k', 'lab':'Off','lab_r':'On','t':'Unbound Init'}
    }

    divisor = Ns[0]
    fitResult,_ = scipy.optimize.curve_fit(lambda t, k_on, k_off: f(t, k_on, k_off, start_bound), times, Ns/divisor)
    np.set_printoptions(precision=16)
    plt.plot(times, Ns/divisor, plot_config[start_bound]['c'], label=plot_config[start_bound]['lab'])
    plt.plot(times, f(times, *fitResult, start_bound), plot_config[start_bound]['c']+ '--', label=plot_config[start_bound]['lab']+ " fit")
    # print(fitResult)

    # Nreverses = np.array(Nreverses) / divisor
    # fitResultRev,_ = scipy.optimize.curve_fit(lambda t, k_on, k_off: f_reverse(t, k_on, k_off, start_bound), times, Nreverses)
    # plt.plot(times, Nreverses, plot_config[start_bound]['c_r'], label=plot_config[start_bound]['lab_r'])
    # plt.plot(times, f_reverse(times, *fitResultRev, start_bound), plot_config[start_bound]['c_r'] + '--', label=plot_config[start_bound]['lab_r']+ " fit")

    if start_bound:
        N_on_end = np.average(Ns[-20:-1])
        N_off_end = np.average(Nreverses[-20:-1])
    else:
        N_on_end = np.average(Nreverses[-20:-1])
        N_off_end = np.average(Ns[-20:-1])
        
    p = N_on_end / (N_on_end + N_off_end)
    K_prime = np.power(1+k_on/k_off,dp)-1
    p_hypothetical = K_prime / (K_prime + 1)
    print("Test: Ns at the end: {} / ({} + {}) = {:.4f} (?= {:.4f})".format(N_on_end, N_on_end, N_off_end, p, p_hypothetical))

    # Copy k_on, k_off, and fitResult to clipboard
    result_str = '\t'.join(map(str, [k_on, k_off, np.mean(k_ons), np.std(k_ons), np.mean(k_offs), np.std(k_offs)]))
    pyperclip.copy(result_str)
    print("k_on, k_off, and calculations copied to clipboard.")

    plt.xlabel("Time (s)")
    if start_bound:
        plt.ylabel("f_on")
    else:
        plt.ylabel("f_off")

    plt.title(plot_config[start_bound]['t'])
    plt.legend()
    plt.tight_layout()
    
    
    # plt.figure()
    # plt.plot(times[6:-7], rolling_average(d_data(times[3:-3], rolling_average(Ns,7)), 7))
    plt.show()

if __name__ == '__main__':
    main()
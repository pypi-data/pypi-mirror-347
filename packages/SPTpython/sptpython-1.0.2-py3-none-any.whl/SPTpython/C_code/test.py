import kinetic_monte_carlo
import time
import numpy as np

# Run the simulation

# N_particles=20000
# exp_time_tot=200
# k_on=0.01
# k_off=0.01
# start = time.time()
# states = kinetic_monte_carlo.run_kinetic_monte_carlo(N_particles, k_on, k_off, 50, 4)
# end = time.time()
# print(f"Time taken: {end-start}")
# print(states)
# x = states.flatten()
# x = x[x!=0]
# x = x[x!=1]
# print("number of errant data points: ", len(x))

N_particles=20
k_on=1.98e-4
k_off=2.75e-5
start = time.time()
states = kinetic_monte_carlo.run_kinetic_monte_carlo(N_particles, k_on, k_off, 5, 40)
end = time.time()
print(f"Time taken: {end-start}")
print(states)

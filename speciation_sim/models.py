import numpy as np
from .simulate import simulate_generation


def _init_pop(N): # function to create empty haploid arrays for both loci 
    return np.array(["A"] * (2 * N)), np.array(["B"] * (2 * N))


def run_allopatry(N, mu, s, gen_max=10000): # allopatric speciation model
    A, B = _init_pop(N) # create parental AABB pop
    for g in range(1, gen_max + 1):  # loop over integers to maximum generation argument

        A, B = simulate_generation(A, B, mu, s) # create next gen arrays and assign to A & B

        if all(a == "a" for a in A) and all(b == "b" for b in B): # conditional to check for fixation / speciation
            return g, True  # boolean confirms speciation occured before max gen value

    return gen_max, False  # boolean indicates speciation did not occur before max gen value

def run_parapatry(N, mu, s, m, gen_max=10000):

    A, B = _init_pop(N) # create parental AABB pop
    for g in range(1, gen_max + 1): # loop over generations as above

        A, B = simulate_generation(A, B, mu, s, m=m) # create next gen

        if all(a == "a" for a in A) and all(b == "b" for b in B): # check for speciation
            return g, True

    return gen_max, False # indicate if speciation did not occur

def run_periodic(N, mu, s, m, interval, gen_max=100000):

    A, B = _init_pop(N) # begin with usual AABB array
    regime = "parapatry" # begin with gene flow
    g = 0 # begin at generation 0

    while g < gen_max: # conditional to alternate every interval generations
        for _ in range(interval):
            g += 1 

            if regime == "parapatry":
                A, B = simulate_generation(A, B, mu, s, m=m) # pass migration argument to simulation function to trigger conditional
            else:
                A, B = simulate_generation(A, B, mu, s) # alternative sticks to allopatric model 

            if all(a == "a" for a in A) and all(b == "b" for b in B):
                return g, True

        regime = "allopatry" if regime == "parapatry" else "parapatry" # switch regime once interval gens are over

    return gen_max, False

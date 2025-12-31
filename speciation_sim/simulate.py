import numpy as np

def simulate_generation(A_pop, B_pop, mu, s, m=0.0, migrant=False):

    N = len(A_pop) // 2 # diploid population size  
    next_A = np.empty(2*N, dtype="U1") # create empty haploid population size array for locus A gametes
    next_B = np.empty(2*N, dtype="U1") # create empty haploid population size array for locus B gametes

    if migrant: # conditional for parapatric / periodic speciation model
        from_migrant = np.random.rand(2*N) < m # boolean array identifying migrant allles if samples from uniform distribution are less than m
        from_parent = ~from_migrant # bitwise inversion of migrant array

        next_A[from_migrant] = "A" # assign next generation parental A alleles
        next_B[from_migrant] = "B" # assign next generation parental B alleles

        n_parent = from_parent.sum() # calculate no. of parent pop alleles in array with .sum() function 
        if n_parent > 0: 
            wA = np.where(A_pop == "a", 1 + s, 1.0) # boost relative fitness for mutant alleles
            wB = np.where(B_pop == "b", 1 + s, 1.0)
            wA /= wA.sum() # divide by sum to get probability of sampling allele at A locus on [0,1]
            wB /= wB.sum() # divide by sum to get probability of sampling allele at B locus on [0,1]

            sampled_A = np.random.choice(A_pop, n_parent, p=wA) # pass on parental A locus gametes, with fitness advantage to pre-existing mutants
            sampled_B = np.random.choice(B_pop, n_parent, p=wB) # pass on parental A locus gametes, with fitness advantage to pre-existing mutants

            sampled_A[np.random.rand(n_parent) < mu] = "a" # unidrectional mutation to a in parental gametes if samples from uniform distribution are less than mu 
            sampled_B[np.random.rand(n_parent) < mu] = "b"  # unidrectional mutation to b in parental gametes if samples from uniform distribution are less than mu 

            next_A[from_parent] = sampled_A # put parental alleles back in next gen array
            next_B[from_parent] = sampled_B

    else: # conditional for allopatric speciation model
        wA = np.where(A_pop == "a", 1 + s, 1.0) # boost relative fitness for extant mutant alleles 
        wB = np.where(B_pop == "b", 1 + s, 1.0) 
        wA /= wA.sum() # transform to probablity of sampling
        wB /= wB.sum()

        next_A = np.random.choice(A_pop, 2*N, p=wA) # create array from parental gametes in previous generation (no migration)
        next_B = np.random.choice(B_pop, 2*N, p=wB)

        next_A[np.random.rand(2*N) < mu] = "a" # mutation works as above
        next_B[np.random.rand(2*N) < mu] = "b"

    return next_A, next_B


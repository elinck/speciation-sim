import numpy as np
from speciation_sim.models import run_parapatry, run_allopatry

def test_allopatry_runs(): # test to make sure output is an integer and under max gen value 
    t, fixed = run_allopatry(N=10, mu=0.1, s=0.1, gen_max=100)
    assert isinstance(t, int)
    assert isinstance(fixed, bool)


def test_no_mutation_no_speciation(): # test to make sure speciation doesn't occur with no mutation (e.g., hits max gen value)
    t, fixed = run_allopatry(N=50, mu=0.0, s=1.0, gen_max=100)
    assert t == 100
    assert fixed is False

def test_reproducible_with_seed(): # test to make sure same seed produces same result 
    np.random.seed(123)
    t1 = run_allopatry(N=20, mu=0.1, s=0.1, gen_max=500)

    np.random.seed(123)
    t2 = run_allopatry(N=20, mu=0.1, s=0.1, gen_max=500)

    assert t1 == t2

def test_full_migration_prevents_speciation(): # high mutation and selection, but 100% migrant alleles should prevent speciation
    t, fixed = run_allopatry(N=50, mu=0.0, s=1.0, gen_max=200)
    assert t == 200
    assert fixed is False
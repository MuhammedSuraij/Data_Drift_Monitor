import numpy as np
import pandas as pd

def calculate_psi(expected,actual,buckets=10):
    expected = np.array(expected)
    actual = np.array(actual)

    breakpoints=np.linspace(0,100,buckets+1)
    breakpoints=np.percentile(expected, breakpoints)

    expected_counts=np.histogram(expected,breakpoints)[0]
    actual_counts=np.histogram(actual,breakpoints)[0]

    expected_perc = expected_counts/len(expected)
    actual_perc=actual_counts/len(actual)

    psi=0
    
    for e,a in zip(expected_perc,actual_perc):
        if e==0:
            e=0.0001
        if a==0:
            a=0.0001
        psi += (a-e)*np.log(a/e)
    
    return psi

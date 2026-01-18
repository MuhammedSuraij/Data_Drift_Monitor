from scipy.stats import ks_2samp,chi2_contingency
import pandas as pd
import numpy as np
from src.psi import calculate_psi


def is_numeric(series):
    return series.dtype in ["int64","float64"]

def ks_drift(col_train,col_new):
    stat,p=ks_2samp(col_train,col_new)
    return p<0.05,p

# def chi_square_drift(col_train,col_new):
#     train_counts=col_train.value_counts()
#     new_counts=col_new.value_counts()

#     combined=pd.concat([train_counts,new_counts],axis=1).fillna(0)
#     chi2,p,_,_=chi2_contingency(combined)

#     return p<0.05,p

def categorical_drift(col_train,col_new):
    train_dist=col_train.value_counts(normalize=True)
    new_dist=col_new.value_counts(normalize=True)

    categories = set(train_dist.index).union(set(new_dist.index))

    expected=[]
    actual=[]

    for cat in categories:
        expected.append(train_dist.get(cat,0))
        actual.append(new_dist.get(cat,0))

    psi=calculate_psi(expected,actual)


    train_counts=col_train.value_counts()
    new_counts=col_new.value_counts()

    combined=pd.concat([train_counts,new_counts],axis=1).fillna(0)
    chi2, p, _, _ =chi2_contingency(combined)

    if psi>0.25:
        drift=True
    elif p<0.05:
        drift=True
    else:
        drift=False

    return drift,psi,p

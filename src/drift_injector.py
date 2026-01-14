import pandas as pd
import numpy as np

def inject_numeric_drift( df, column, shift_percent):
    df[column]= df[column] * (1+shift_percent/100)
    return df

def inject_category_drift( df, column, new_val, percent):
    n=int(len(df) * percent/100)
    df.loc[:n, column] = new_val
    return df

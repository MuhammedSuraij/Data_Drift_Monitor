import pandas as pd
from drift_statistical import is_numeric,ks_drift,categorical_drift

def run_drift(new_df):
    train_df=pd.read_csv("data/train.csv")

    for col in train_df.columns:
        if is_numeric(train_df[col]):
            drifted, p = ks_drift(train_df[col], new_df[col])
            print(f"{col}: Numeric Drift = {drifted}")
        else:
            drifted, psi, _ = categorical_drift(train_df[col], new_df[col])
            print(f"{col}: Categorical Drift = {drifted}")
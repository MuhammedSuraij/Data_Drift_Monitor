import pandas as pd
from src.global_drift import comput_global_drift
from src.common_engine import (
    numeric_severity,
    psi_severity,
    detect_new_categories,
    system_health,
    recommended_action
)
from src.drift_statistical import is_numeric,ks_drift,categorical_drift

def run_stream_drift(train_df,new_df):

    feature_score= {}

    print("\n--- STREAM DRIFT CHECK STARTED ---")

    for col in train_df.columns:
        if is_numeric(train_df[col]):
            drifted, p = ks_drift(train_df[col], new_df[col])
            severity= numeric_severity(p)
            feature_score[col] = 1-p
            print(f"{col}| KS  | {severity}")
        else:
            drifted, psi, _ = categorical_drift(train_df[col], new_df[col])
            severity=psi_severity(psi)
            feature_score[col]=psi
            new_cats= detect_new_categories(train_df[col],new_df[col])
            print(f"{col}| Categorical Drift = {drifted} | severity | {severity} | new | {new_cats}")
        
    weights= {"amount": 3, "category": 2, "age": 1}
    global_score= comput_global_drift(feature_score,weights)
    health = system_health(global_score)
    action= recommended_action(health)

    print("\nGLOBAL DRIFT SCORE:", round(global_score, 3))
    print("SYSTEM HEALTH:", health)
    print("ACTION:", action)

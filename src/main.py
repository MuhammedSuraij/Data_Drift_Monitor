from input_loader import load_csv
from drift_statistical import is_numeric, ks_drift,categorical_drift
from baseline import compute_baseline, save_baseline

train_df = load_csv("data/train.csv")
new_df = load_csv("data/new_batch.csv")

baseline = compute_baseline(train_df)
save_baseline(baseline, "outputs/baseline.json")

for col in train_df.columns:
    if is_numeric(train_df[col]):
        drifted,p=ks_drift(train_df[col],new_df[col])
        method="KS Test"
    else:
        drifted,psi,p=categorical_drift(train_df[col],new_df[col])
        method="PSI + Chi-Square"

    print(f"{col} | {method} | Drift= {drifted} | p-value= {p:.4f}")

print("\nDRIFT SUMMARY:\nTotal features:",len(train_df.columns))

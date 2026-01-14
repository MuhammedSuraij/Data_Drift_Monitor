from input_loader import load_csv
from drift_statistical import is_numeric, ks_drift,categorical_drift
from baseline import compute_baseline, save_baseline
from global_drift import comput_global_drift
from drift_injector import inject_category_drift,inject_numeric_drift
from common_engine import (
    numeric_severity,
    psi_severity,
    numeric_drift_reason,
    detect_new_categories,
    system_health,
    recommended_action
)
from report_generator import write_report


feature_score= {}
train_df = load_csv("data/train.csv")
new_df = load_csv("data/new_batch.csv")


new_df = inject_numeric_drift(new_df, "amount", 50)
new_df = inject_category_drift(new_df, "category", "fraud", 40)
print(new_df)

baseline = compute_baseline(train_df)
save_baseline(baseline, "outputs/baseline.json")

feature_score = {}
results = []

for col in train_df.columns:
    if is_numeric(train_df[col]):
        drifted,p=ks_drift(train_df[col],new_df[col])

        severity=numeric_severity(p)
        reason=numeric_drift_reason(train_df[col],new_df[col])

        feature_score[col] = 1-p
        method="KS Test"
        results.append({
            "feature": col,
            "method": method,
            "severity": severity,
            "reason": reason
        })
    else:
        drifted,psi,p=categorical_drift(train_df[col],new_df[col])

        severity = psi_severity(psi)
        new_cats = detect_new_categories(train_df[col], new_df[col])

        feature_score[col] = psi
        method="PSI + Chi-Square"
        results.append({
            "feature": col,
            "method": method,
            "severity": severity,
            "new_categories": new_cats
        })

    print(f"{col} | {method} | Drift= {drifted} | p-value= {p:.4f}")

weights={ "amount":3,
          "category":2,
          "age":1
         }
global_drift=comput_global_drift(feature_score,weights)
health= system_health(global_drift)
action= recommended_action(health)

print("\nSYSTEM HEALTH:", health)
print("\nGLOBAL DRIFT SCORE: ",round(global_drift,3))
print("RECOMMENDED ACTION:", action)



write_report(
    results,
    global_drift,
    health,
    action,
    "outputs/drift_report.txt"
)
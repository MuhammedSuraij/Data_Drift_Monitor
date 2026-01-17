from input_loader import load_data
from drift_statistical import is_numeric, ks_drift, categorical_drift
from baseline import compute_baseline, save_baseline
from global_drift import comput_global_drift
from drift_injector import inject_category_drift, inject_numeric_drift
from common_engine import (
    numeric_severity,
    psi_severity,
    numeric_drift_reason,
    detect_new_categories,
    system_health,
    recommended_action,
    format_numeric_reason,
    format_categorical_reason
)
from report_generator import write_report


# Load data
train_df = load_data("data/train.csv")
new_df = load_data("data/new_batch.csv")

# Artificial drift injection
new_df = inject_numeric_drift(new_df, "amount", 50)
new_df = inject_category_drift(new_df, "category", "fraud", 40)

# Baseline
baseline = compute_baseline(train_df)
save_baseline(baseline, "outputs/baseline.json")

feature_score = {}
results = []

# Drift detection loop
for col in train_df.columns:
    if is_numeric(train_df[col]):
        drifted, p = ks_drift(train_df[col], new_df[col])
        severity = numeric_severity(p)

        reason = numeric_drift_reason(train_df[col], new_df[col])
        explanation = format_numeric_reason(reason) if reason else []

        feature_score[col] = 1 - p
        method = "KS Test"

        results.append({
            "feature": col,
            "method": method,
            "drift_detected": drifted,
            "severity": severity,
            "explanation": explanation
        })

    else:
        drifted, psi, p = categorical_drift(train_df[col], new_df[col])
        severity = psi_severity(psi)

        new_cats = detect_new_categories(train_df[col], new_df[col])
        explanation = format_categorical_reason(new_cats)

        feature_score[col] = psi
        method = "PSI + Chi-Square"

        results.append({
            "feature": col,
            "method": method,
            "drift_detected": drifted,
            "severity": severity,
            "explanation": explanation
        })

    print(f"{col} | {method} | Drift={drifted} | p-value={p:.4f}")

# Global drift & system decision
weights = {
    "amount": 3,
    "category": 2,
    "age": 1
}

global_drift = comput_global_drift(feature_score, weights)
health = system_health(global_drift)
action = recommended_action(health)

print("\nSYSTEM HEALTH:", health)
print("GLOBAL DRIFT SCORE:", round(global_drift, 3))
print("RECOMMENDED ACTION:", action)

# Write report
write_report(
    results,
    global_drift,
    health,
    action,
    "outputs/drift_report.txt"
)

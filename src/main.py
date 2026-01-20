from src.input_loader import load_data
from src.common_engine import analyze_feature_drift
from src.global_drift import comput_global_drift
from src.drift_visualizer import (
    plot_numeric_drift,
    plot_categorical_drift
)
from src.common_engine import system_health,recommended_action
from src.report_generator import write_report

train_df = load_data("data/train.csv")
new_df = load_data("data/new_batch.csv")

feature_score = {}
results = []

for col in train_df.columns:
    res = analyze_feature_drift(train_df, new_df, col)

    feature_score[col] = res["score"]
    results.append(res)

    print(
        f"{col} | {res['method']} | Drift={res['drift_detected']} | Severity={res['severity']}"
    )

    # WOW-factor visualization
    if res["type"] == "numeric":
        plot_numeric_drift(train_df[col], new_df[col], col)
    else:
        plot_categorical_drift(train_df[col], new_df[col], col)




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

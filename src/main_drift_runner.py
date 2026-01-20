from src.common_engine import analyze_feature_drift
from src.global_drift import comput_global_drift
from src.common_engine import system_health, recommended_action


def run_stream_drift(train_df, new_df):

    print("\n--- STREAM DRIFT CHECK STARTED ---")

    feature_score = {}

    for col in train_df.columns:
        res = analyze_feature_drift(train_df, new_df, col)

        feature_score[col] = res["score"]

        print(
            f"{col} | {res['method']} | Drift={res['drift_detected']} | Severity={res['severity']}"
        )

    weights = {"amount": 3, "category": 2, "age": 1}
    global_score = comput_global_drift(feature_score, weights)

    health = system_health(global_score)
    action = recommended_action(health)

    print("\nGLOBAL DRIFT SCORE:", round(global_score, 3))
    print("SYSTEM HEALTH:", health)
    print("ACTION:", action)

import pandas as pd


def numeric_severity(p_value):
    if p_value < 0.01:
        return "HIGH"
    elif p_value < 0.05:
        return "MEDIUM"
    else:
        return "LOW"


def psi_severity(psi):
    if psi >= 0.25:
        return "HIGH"
    elif psi >= 0.1:
        return "MEDIUM"
    else:
        return "LOW"


def numeric_drift_reason(train_col, new_col):
    # Defensive check
    if not (
        pd.api.types.is_numeric_dtype(train_col)
        and pd.api.types.is_numeric_dtype(new_col)
    ):
        return None

    mean_change = ((new_col.mean() - train_col.mean()) / train_col.mean()) * 100
    std_change = ((new_col.std() - train_col.std()) / train_col.std()) * 100

    return {
        "mean_change_%": round(float(mean_change), 2),
        "std_change_%": round(float(std_change), 2),
        "old_range": (train_col.min(), train_col.max()),
        "new_change": (new_col.min(), new_col.max())
    }


def detect_new_categories(train_col, new_col):
    train_set = set(train_col.unique())
    new_set = set(new_col.unique())
    return list(new_set - train_set)


def system_health(global_score):
    if global_score > 0.6:
        return "CRITICAL"
    elif global_score > 0.3:
        return "WARNING"
    else:
        return "HEALTHY"


def recommended_action(health):
    if health == "CRITICAL":
        return "Retrain the Model"
    elif health == "WARNING":
        return "Investigate the Data"
    else:
        return "Continue Monitoring"


def format_numeric_reason(reason):
    return [
        f"Mean changed by {reason['mean_change_%']:.2f}%",
        f"Standard deviation changed by {reason['std_change_%']:.2f}%",
        f"Value range shifted from "
        f"[{reason['old_range'][0]} - {reason['old_range'][1]}] "
        f"to [{reason['new_change'][0]} - {reason['new_change'][1]}]"
    ]


def format_categorical_reason(new_categories):
    if new_categories:
        return [f"New unseen categories detected: {', '.join(new_categories)}"]
    else:
        return ["Significant change in category distribution"]

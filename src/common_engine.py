import pandas as pd
from src.drift_statistical import is_numeric, ks_drift, categorical_drift


# ---------------- Severity ---------------- #

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


# ---------------- Drift Reason ---------------- #

def drift_pattern(mean_change, std_change):
    if abs(mean_change) > 50 and abs(std_change) < 10:
        return "DATA SHIFT"
    elif abs(std_change) > 50:
        return "VARIANCE EXPLOSION"
    elif abs(mean_change) < 10 and abs(std_change) < 10:
        return "MINOR FLUCTUATION"
    else:
        return "COMPLEX DRIFT"


def numeric_drift_reason(train_col, new_col):
    if not (
        pd.api.types.is_numeric_dtype(train_col)
        and pd.api.types.is_numeric_dtype(new_col)
    ):
        return None

    train_col = train_col.dropna()
    new_col = new_col.dropna()

    train_mean = train_col.mean()
    train_std = train_col.std()

    mean_change = (
        ((new_col.mean() - train_mean) / train_mean) * 100
        if train_mean != 0 else 0
    )

    std_change = (
        ((new_col.std() - train_std) / train_std) * 100
        if train_std != 0 else 0
    )

    return {
        "mean_change_%": round(mean_change, 2),
        "std_change_%": round(std_change, 2),
        "old_range": (float(train_col.min()), float(train_col.max())),
        "new_range": (float(new_col.min()), float(new_col.max())),
        "pattern": drift_pattern(mean_change, std_change),
    }


def detect_new_categories(train_col, new_col):
    return list(set(new_col.unique()) - set(train_col.unique()))


# ---------------- Formatting ---------------- #

def format_numeric_reason(reason):
    return [
        f"Mean changed by {reason['mean_change_%']}%",
        f"Std changed by {reason['std_change_%']}%",
        f"Range: {reason['old_range']} → {reason['new_range']}",
        f"Pattern: {reason['pattern']}",
    ]


def format_categorical_reason(new_categories):
    if new_categories:
        return [f"New unseen categories: {', '.join(new_categories)}"]
    return ["Distribution shift detected"]


# ---------------- Core Analyzer ---------------- #

def analyze_feature_drift(train_df, new_df, col):
    result = {"feature": col}

    if is_numeric(train_df[col]):
        drifted, p = ks_drift(train_df[col], new_df[col])
        severity = numeric_severity(p)

        reason = numeric_drift_reason(train_df[col], new_df[col])
        explanation = format_numeric_reason(reason) if reason else []

        result.update({
            "type": "numeric",
            "method": "KS Test",
            "drift_detected": drifted,
            "severity": severity,
            "score": 1 - p,
            "explanation": explanation
        })

    else:
        drifted, psi, _ = categorical_drift(train_df[col], new_df[col])
        severity = psi_severity(psi)

        new_cats = detect_new_categories(train_df[col], new_df[col])
        explanation = format_categorical_reason(new_cats)

        result.update({
            "type": "categorical",
            "method": "PSI + Chi-Square",
            "drift_detected": drifted,
            "severity": severity,
            "score": psi,
            "explanation": explanation
        })

    return result


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



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
    reason={}

    mean_change = ((new_col.mean()- train_col.mean())/train_col.mean())*100
    std_change = ((new_col.std() - train_col.std())/train_col.std())*100

    reason["mean_change_%"] = round(mean_change,2)
    reason["std_change_%"] = round(std_change,2)
    reason["old_range"] = (train_col.min(),train_col.max())
    reason["new_change"] = (new_col.min(), new_col.max())

    return reason

def detect_new_categories(train_col,new_col):
    train_set= set(train_col.unique())
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
    elif health == "Warning":
        return "Investigate the Data"
    else:
        return "Continue Monitoring"
    
    
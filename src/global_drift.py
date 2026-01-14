
def comput_global_drift(feature_scores, feature_weights):
    total = 0
    weight_sum = 0

    for feature in feature_scores:
        score = feature_scores[feature]
        weight = feature_weights.get(feature,1)

        total += score * weight
        weight_sum += weight

    return total/weight_sum
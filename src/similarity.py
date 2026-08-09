from math import sqrt
from typing import Dict

def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    keys = set(vec_a) & set(vec_b)
    numerator = sum(vec_a[key] * vec_b[key] for key in keys)
    sum_a = sum(value * value for value in vec_a.values())
    sum_b = sum(value * value for value in vec_b.values())
    denominator = sqrt(sum_a) * sqrt(sum_b)
    if denominator == 0:
        return 0.0
    return numerator / denominator

def jaccard_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    set_a = set(k for k, v in vec_a.items() if v > 0)
    set_b = set(k for k, v in vec_b.items() if v > 0)
    intersection = set_a & set_b
    union = set_a | set_b
    if not union:
        return 0.0
    return len(intersection) / len(union)

def euclidean_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    union_keys = set(vec_a) | set(vec_b)
    sum_sq_diff = 0.0
    for key in union_keys:
        val_a = vec_a.get(key, 0.0)
        val_b = vec_b.get(key, 0.0)
        sum_sq_diff += (val_a - val_b) ** 2
    distance = sqrt(sum_sq_diff)
    return 1.0 / (1.0 + distance)

def pearson_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    union_keys = list(set(vec_a) | set(vec_b))
    n = len(union_keys)
    if n < 2:
        return 0.0

    mean_a = sum(vec_a.get(key, 0.0) for key in union_keys) / n
    mean_b = sum(vec_b.get(key, 0.0) for key in union_keys) / n

    num = 0.0
    den_a = 0.0
    den_b = 0.0
    for key in union_keys:
        val_a = vec_a.get(key, 0.0) - mean_a
        val_b = vec_b.get(key, 0.0) - mean_b
        num += val_a * val_b
        den_a += val_a ** 2
        den_b += val_b ** 2

    denominator = sqrt(den_a) * sqrt(den_b)
    if denominator == 0.0:
        return 0.0
    return num / denominator


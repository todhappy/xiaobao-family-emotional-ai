def compute_intimacy(memory_list, interaction_count=0):
    base_score = len(memory_list) * 0.1
    interaction_score = min(interaction_count * 0.05, 0.5)
    score = min(base_score + interaction_score, 1.0)
    return round(score, 2)
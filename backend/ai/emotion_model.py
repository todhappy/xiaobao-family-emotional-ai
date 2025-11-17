def infer_emotion(memory_list):
    emotions = []
    for m in memory_list:
        text = m.get("content", "")
        if any(k in text for k in ["开心", "快乐"]):
            emotions.append("positive")
        elif any(k in text for k in ["伤心", "难过", "生气"]):
            emotions.append("negative")
        else:
            emotions.append("neutral")
    from collections import Counter
    return dict(Counter(emotions))
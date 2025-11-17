def apply_tone(text, member_role="父亲"):
    tone_map = {"父亲": "沉稳、温和", "母亲": "温柔、关怀", "孩子": "活泼、俏皮"}
    tone = tone_map.get(member_role, "自然")
    return f"[{tone}] {text}"
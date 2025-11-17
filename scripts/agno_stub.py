import os
import json
from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

QWEN_API_BASE = os.getenv("QWEN_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_EMBED_MODEL = os.getenv("QWEN_EMBED_MODEL", "text-embedding-v1")
QWEN_CHAT_MODEL = os.getenv("QWEN_CHAT_MODEL", "qwen2.5")

def call_qwen_embeddings(text):
    if not QWEN_API_KEY:
        return None
    try:
        r = requests.post(
            f"{QWEN_API_BASE}/embeddings",
            json={"input": text, "model": QWEN_EMBED_MODEL},
            headers={"Authorization": f"Bearer {QWEN_API_KEY}"},
            timeout=12,
        )
        if r.status_code == 200:
            data = r.json()
            vec = (data.get("data") or [{}])[0].get("embedding")
            return vec
    except Exception:
        return None
    return None

def call_qwen_chat(prompt, context_text):
    if not QWEN_API_KEY:
        return None
    try:
        r = requests.post(
            f"{QWEN_API_BASE}/chat/completions",
            json={
                "model": QWEN_CHAT_MODEL,
                "messages": [
                    {"role": "system", "content": "你是孝宝系统的家庭助理，结合提供的记忆回答问题。"},
                    {"role": "user", "content": f"问题：{prompt}\n上下文：{context_text}"},
                ],
                "temperature": 0.7,
            },
            headers={"Authorization": f"Bearer {QWEN_API_KEY}"},
            timeout=15,
        )
        if r.status_code == 200:
            data = r.json()
            choices = data.get("choices") or []
            msg = choices[0].get("message", {}) if choices else {}
            return msg.get("content")
    except Exception:
        return None
    return None

@app.route("/embedding", methods=["POST"])
def embedding():
    try:
        text = (request.get_json() or {}).get("text", "")
        vec = call_qwen_embeddings(text)
        if vec and len(vec) == 1536:
            return jsonify({"embedding": vec})
        # fallback: deterministic pseudo vector
        random.seed(hash(text) % (10**9))
        vec = [random.random() * 0.01 for _ in range(1536)]
        return jsonify({"embedding": vec})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate", methods=["POST"])
def generate():
    try:
        body = request.get_json() or {}
        prompt = body.get("prompt", "")
        context = body.get("context", [])
        context_text = " ".join(context) if isinstance(context, list) else str(context)
        ans = call_qwen_chat(prompt, context_text)
        if ans:
            return jsonify({"answer": ans})
        # fallback answer
        return jsonify({"answer": f"[占位回答] {prompt} | 上下文: {context_text}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/llm", methods=["POST"])
def llm():
    return generate()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
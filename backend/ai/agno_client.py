import requests

class AgnoClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base = base_url

    def generate_response(self, prompt, context=[]):
        payload = {"prompt": prompt, "context": context}
        try:
            r = requests.post(f"{self.base}/llm/generate", json=payload, timeout=5)
            if r.status_code == 200:
                return r.json().get("answer", "")
        except Exception:
            pass
        return "抱歉，无法生成回答"
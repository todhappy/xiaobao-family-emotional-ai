import requests

class Mem0Agent:
    def __init__(self, base_url='http://localhost:8889'):
        self.base = base_url

    def retrieve_context(self, family_id, query_vector):
        payload = {"family_id": family_id, "query_vector": query_vector}
        try:
            r = requests.post(f"{self.base}/memory/search", json=payload, timeout=5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    def store_memory(self, family_id, member_id, content, embedding):
        payload = {"family_id": family_id, "member_id": member_id, "content": content, "embedding": embedding}
        try:
            r = requests.post(f"{self.base}/memory/add", json=payload, timeout=5)
            return r.status_code == 200
        except Exception:
            return False
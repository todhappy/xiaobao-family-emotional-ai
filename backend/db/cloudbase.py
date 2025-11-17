import os
import json
import subprocess
from backend.config import CLOUDBASE_ENV_ID, CLOUDBASE_SECRET_ID, CLOUDBASE_SECRET_KEY

def run_node(action, payload=None):
    env = os.environ.copy()
    env["CB_ENV_ID"] = CLOUDBASE_ENV_ID
    env["CB_SECRET_ID"] = CLOUDBASE_SECRET_ID
    env["CB_SECRET_KEY"] = CLOUDBASE_SECRET_KEY
    args = ["node", "scripts/cloudbase_ops.js", action, json.dumps(payload or {})]
    p = subprocess.run(args, capture_output=True, text=True, env=env)
    if p.returncode != 0:
        return {"error": p.stderr.strip()}
    try:
        return json.loads(p.stdout.strip())
    except Exception:
        return {"raw": p.stdout.strip()}

def create_collection(name):
    return run_node("createCollection", {"name": name})

def insert_one(collection, doc):
    return run_node("insertOne", {"collection": collection, "doc": doc})

def get_one(collection):
    return run_node("getOne", {"collection": collection})
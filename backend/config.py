import os

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql+psycopg2://family_user:Family%40123@localhost:5433/family_db")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Family@123")
CLOUDBASE_ENV_ID = os.getenv("CLOUDBASE_ENV_ID", "xiaobao-8ghot9xq5d56b3cf")
CLOUDBASE_SECRET_ID = os.getenv("CLOUDBASE_SECRET_ID", "")
CLOUDBASE_SECRET_KEY = os.getenv("CLOUDBASE_SECRET_KEY", "")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5001"))
AGNO_API_BASE = os.getenv("AGNO_API_BASE", "http://localhost:5000")
AGNO_API_KEY = os.getenv("AGNO_API_KEY", "")
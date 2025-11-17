import subprocess
import sys

subprocess.run([sys.executable, "scripts/init_postgres.py"], check=True)
subprocess.run([sys.executable, "scripts/init_neo4j.py"], check=True)
subprocess.run([sys.executable, "scripts/sync_postgres_to_neo4j.py"], check=True)

print("全部初始化与同步完成。")
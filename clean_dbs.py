import os
import shutil
from arango import ArangoClient

# 1. Clean ChromaDB
chroma_path = r"E:\test\test-api\chroma_store"
if os.path.exists(chroma_path):
    try:
        shutil.rmtree(chroma_path)
        print(f"Deleted ChromaDB folder: {chroma_path}")
    except Exception as e:
        print(f"Could not delete ChromaDB: {e}")
else:
    print("ChromaDB folder not found.")

# 2. Clean ArangoDB
try:
    client = ArangoClient(hosts="http://157.173.221.226:8529")
    sys_db = client.db('_system', username="root", password="Aiinhome@2026")
    if sys_db.has_database("graph_ai2"):
        sys_db.delete_database("graph_ai2")
        print("Deleted ArangoDB database: graph_ai2")
    else:
        print("ArangoDB database graph_ai2 does not exist.")
except Exception as e:
    print("Error deleting ArangoDB:", e)

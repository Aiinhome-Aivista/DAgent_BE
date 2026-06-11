import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.db_connection import get_db_connection

def reset():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Reset new_user_db
        cursor.execute("UPDATE users SET new_user_db = NULL")
        conn.commit()
        print(f"Updated {cursor.rowcount} users.")
        
        # Truncate tables
        tables = [
            "session_chat_history", "session_analysis_cache", "conversation_history",
            "connection_history", "database_credential", "external_db_sync_log",
            "tracker", "session_tracking", "graph", "saved_web_results",
            "sheet_scans", "`analyze`", "unstructured_docs", "error_logs"
        ]
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for t in tables:
            try:
                cursor.execute(f"TRUNCATE TABLE {t}")
                print(f"Truncated {t}")
            except Exception as e:
                print(f"Failed to truncate {t}: {e}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Done resetting database!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    reset()

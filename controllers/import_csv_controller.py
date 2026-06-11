import os
import json
import pandas as pd
import pymysql
from flask import request, jsonify
from database.config import MYSQL_CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "uploads"))

def import_csv_data(get_db_connection):
    data = request.json
    user_id = data.get("user_id")
    connection_id = data.get("connection_id")
    session_id = data.get("session_id")

    if not user_id or not connection_id or not session_id:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        imported_files = []
        affected_tables_info = []
        total_rows = 0

        # fetch credential
        query = """
        SELECT dc.credential
        FROM database_credential dc
        WHERE (dc.connection_id = %s OR dc.connection_id IS NULL)
        AND dc.user_id = %s
        AND dc.session_id = %s
        ORDER BY dc.connection_id DESC
        LIMIT 1
        """
        cursor.execute(query, (connection_id, user_id, session_id))
        result = cursor.fetchone()

        if not result:
            return jsonify({"status": "error", "message": "Credential not found"}), 404

        credential = json.loads(result["credential"])
        files = credential.get("files", [])

        # fetch user db
        cursor.execute("SELECT name,new_user_db FROM users WHERE id=%s", (user_id,))
        user_data = cursor.fetchone()

        username = user_data["name"]
        user_db = user_data["new_user_db"]

        # connect user database
        user_conn = pymysql.connect(
            host=MYSQL_CONFIG["host"],
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            database=user_db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        user_cursor = user_conn.cursor()

        files_in_folder = os.listdir(UPLOAD_DIR)

        for file in files:
            if not file.lower().endswith('.csv'):
                continue

            matched_file = next((f for f in files_in_folder if f.lower() == file.lower()), None)
            if not matched_file:
                continue

            file_path = os.path.join(UPLOAD_DIR, matched_file)
            df = pd.read_csv(file_path, encoding="utf-8-sig")

            if df.empty:
                continue

            df.columns = df.columns.str.strip().str.replace(" ", "_")
            df = df.where(pd.notnull(df), None)

            table_name = file.replace(".csv", "").lower()
            num_columns = len(df.columns)

            cols = ", ".join([f"`{c}` TEXT" for c in df.columns])
            create_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({cols})"
            user_cursor.execute(create_query)

            user_cursor.execute(f"SELECT COUNT(*) as cnt FROM `{table_name}`")
            row_cnt = user_cursor.fetchone()['cnt']

            rows_inserted = 0
            if row_cnt == 0:
                columns = ", ".join([f"`{c}`" for c in df.columns])
                placeholders = ", ".join(["%s"] * len(df.columns))
                insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                
                data_values = [tuple(None if pd.isna(x) else x for x in row) for row in df.values]
                user_cursor.executemany(insert_query, data_values)
                rows_inserted = len(df)
            else:
                rows_inserted = row_cnt

            total_rows += rows_inserted
            imported_files.append(file)
            affected_tables_info.append({
                "table": table_name,
                "rows": rows_inserted,
                "columns": num_columns
            })

            log_query = """
            INSERT INTO external_db_sync_log
            (user_id,username,external_database,table_name,
            action_type,rows_affected,session_id,new_user_db)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(log_query, (
                user_id, username, file, table_name,
                "IMPORT", rows_inserted, session_id, user_db
            ))
            conn.commit()

        # Calculate approximate data size
        data_size_mb = round((total_rows * 200) / (1024 * 1024), 2)  # Rough estimate

        return jsonify({
            "message": "Data imported successfully",
            "status": "success",
            "imported_files": imported_files,
            "data": {
                "summary": {
                    "total_rows": total_rows,
                    "total_columns": sum(t["columns"] for t in affected_tables_info),
                    "data_size_mb": max(data_size_mb, 0.01),
                    "last_sync": "Just now"
                },
                "tables": affected_tables_info
            }
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

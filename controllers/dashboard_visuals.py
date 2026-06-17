# import json
# from flask import request, jsonify
# from model.llm_client import call_llm_chat

# def graph_metrics_controller():
#     """
#     Extracts the 4 dashboard metrics dynamically from the chat context.
#     Expects JSON: { "question": "...", "answer": "..." }
#     """
#     data = request.json
#     if not data:
#         return jsonify({"error": "No data provided"}), 400
        
#     question = data.get("question", "")
#     answer = data.get("answer", "")
    
#     prompt = f"""
# You are a data extraction assistant for a sales dashboard. 
# Based on the user's question and the system's answer below, extract up to 4 key numerical highlights or metrics dynamically.

# Instead of hardcoding specific metrics, find ANY 4 meaningful metrics from the text (e.g., "Average Bulk Invoice Value", "Average Retail Invoice Value", "Volume Discount", etc.).

# Question: "{question}"
# Answer: "{answer}"

# Return EXACTLY a valid JSON object in this format, using dynamic labels for whatever metrics you find:
# {{
#   "metric_1": {{"label": "Name of Metric 1", "value": "...", "subtext": "..."}},
#   "metric_2": {{"label": "Name of Metric 2", "value": "...", "subtext": "..."}},
#   "metric_3": {{"label": "Name of Metric 3", "value": "...", "subtext": "..."}},
#   "metric_4": {{"label": "Name of Metric 4", "value": "...", "subtext": "..."}}
# }}

# If you cannot find 4 metrics, return null for the remaining metric fields (e.g., "metric_3": null).
# """
#     messages = [{"role": "user", "content": prompt}]
    
#     try:
#         response = call_llm_chat(messages, temperature=0.0)
#         # Clean json if it contains markdown formatting
#         if response.startswith("```json"):
#             response = response.replace("```json", "").replace("```", "").strip()
#         elif response.startswith("```"):
#             response = response.replace("```", "").strip()
            
#         metrics = json.loads(response)
        
#         # Provide default fallback values if any metric is null or missing
#         defaults = {
#             "metric_1": {"label": "Metric 1", "value": "N/A", "subtext": "No data available"},
#             "metric_2": {"label": "Metric 2", "value": "N/A", "subtext": "No data available"},
#             "metric_3": {"label": "Metric 3", "value": "N/A", "subtext": "No data available"},
#             "metric_4": {"label": "Metric 4", "value": "N/A", "subtext": "No data available"}
#         }
        
#         for key in defaults:
#             if key not in metrics or not metrics[key] or metrics[key].get("value") is None:
#                 metrics[key] = defaults[key]
#             else:
#                 # Ensure all required fields exist
#                 if not metrics[key].get("label"): metrics[key]["label"] = defaults[key]["label"]
#                 if not metrics[key].get("subtext"): metrics[key]["subtext"] = ""
                
#         return jsonify({"status": "success", "data": metrics}), 200
#     except Exception as e:
#         print(f"[Graph] Error extracting metrics: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500


# def extract_graph_data_controller():
#     """
#     Extracts numerical data points from the chat context (question + answer)
#     and formats them as structured chart data for frontend visualization.
#     Expects JSON: { "question": "...", "answer": "..." }
#     """
#     data = request.json
#     if not data:
#         return jsonify({"error": "No data provided"}), 400
        
#     question = data.get("question", "")
#     answer = data.get("answer", "")
    
#     prompt = f"""
# You are a data visualization assistant.
# Based on the user's question and the system's answer below, extract any numerical or sales data mentioned and format it as structured JSON.
# You must categorize the extracted data into one of the following chart data formats based on what is being compared in the text:

# 1. "dummyYoYData": Use this if the data compares Year-over-Year sales (specifically 2025 vs 2026) for different regions or cities.
#    Format of each item: {{ "name": "REGION_NAME", "y2026": float, "y2025": float }}
   
# 2. "dummyYearComparisonData": Use this if the data compares monthly sales across multiple years (2022 to 2026).
#    Format of each item: {{ "month": "MONTH_NAME", "y2022": float, "y2023": float, "y2024": float, "y2025": float, "y2026": float }}
   
# 3. "dummyZoneData": Use this if the data shows sales across different geographic zones (e.g., Central, North, East, South, West).
#    Format of each item: {{ "name": "ZONE_NAME", "value": float }}
   
# 4. "dummyTyreData": Use this if the data shows sales for different tyre categories (e.g., TRUCK, CAR, LCV, SCV, etc.).
#    Format of each item: {{ "name": "TYRE_TYPE", "value": float }}

# Important Instructions:
# - Only populate the array that matches the data category discussed in the Q&A context. 
# - For any of the 4 arrays that are NOT applicable or do not have any data mentioned in the text, return them as empty lists `[]`.
# - Include the "COLORS" key exactly as shown below.
# - Parse all numeric values as clean floats/integers.

# Question: "{question}"
# Answer: "{answer}"

# Return EXACTLY a valid JSON object in this format, with no markdown formatting or extra text:
# {{
#   "dummyYoYData": [ ... ],
#   "dummyYearComparisonData": [ ... ],
#   "dummyZoneData": [ ... ],
#   "COLORS": ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8", "#E06666", "#93C47D"],
#   "dummyTyreData": [ ... ]
# }}
# """
#     messages = [{"role": "user", "content": prompt}]
    
#     try:
#         response = call_llm_chat(messages, temperature=0.0)
#         # Clean json if it contains markdown formatting
#         if response.startswith("```json"):
#             response = response.replace("```json", "").replace("```", "").strip()
#         elif response.startswith("```"):
#             response = response.replace("```", "").strip()
            
#         chart_data = json.loads(response)
#         return jsonify({"status": "success", "data": chart_data}), 200
#     except Exception as e:
#         print(f"[Graph] Error extracting chart data: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500


import json
from flask import request, jsonify
from model.llm_client import call_llm_chat

def graph_metrics_controller():
    """
    Extracts the 4 dashboard metrics dynamically from the chat context.
    Expects JSON: { "question": "...", "answer": "..." }
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    question = data.get("question", "")
    answer = data.get("answer", "")
    
    defaults = {
        "metric_1": {"label": "Metric 1", "value": "N/A", "subtext": "No data available"},
        "metric_2": {"label": "Metric 2", "value": "N/A", "subtext": "No data available"},
        "metric_3": {"label": "Metric 3", "value": "N/A", "subtext": "No data available"},
        "metric_4": {"label": "Metric 4", "value": "N/A", "subtext": "No data available"}
    }

    if not answer.strip():
        return jsonify({"status": "success", "data": defaults}), 200
    
    prompt = f"""
You are a data extraction assistant for a sales dashboard. 
Based on the user's question and the system's answer below, extract up to 4 key numerical highlights or metrics dynamically.

Instead of hardcoding specific metrics, find ANY 4 meaningful metrics from the text (e.g., "Average Bulk Invoice Value", "Average Retail Invoice Value", "Volume Discount", etc.).

Question: "{question}"
Answer: "{answer}"

Return EXACTLY a valid JSON object in this format, using dynamic labels for whatever metrics you find:
{{
  "metric_1": {{"label": "Name of Metric 1", "value": "...", "subtext": "..."}},
  "metric_2": {{"label": "Name of Metric 2", "value": "...", "subtext": "..."}},
  "metric_3": {{"label": "Name of Metric 3", "value": "...", "subtext": "..."}},
  "metric_4": {{"label": "Name of Metric 4", "value": "...", "subtext": "..."}}
}}

If you cannot find 4 metrics, return null for the remaining metric fields (e.g., "metric_3": null).
"""
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = call_llm_chat(messages, temperature=0.0)
        # Clean json if it contains markdown formatting
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        elif response.startswith("```"):
            response = response.replace("```", "").strip()
            
        metrics = json.loads(response)
        
        # Provide default fallback values if any metric is null or missing
        defaults = {
            "metric_1": {"label": "Metric 1", "value": "N/A", "subtext": "No data available"},
            "metric_2": {"label": "Metric 2", "value": "N/A", "subtext": "No data available"},
            "metric_3": {"label": "Metric 3", "value": "N/A", "subtext": "No data available"},
            "metric_4": {"label": "Metric 4", "value": "N/A", "subtext": "No data available"}
        }
        
        for key in defaults:
            if key not in metrics or not metrics[key] or metrics[key].get("value") is None:
                metrics[key] = defaults[key]
            else:
                # Ensure all required fields exist
                if not metrics[key].get("label"): metrics[key]["label"] = defaults[key]["label"]
                if not metrics[key].get("subtext"): metrics[key]["subtext"] = ""
                
        return jsonify({"status": "success", "data": metrics}), 200
    except Exception as e:
        print(f"[Graph] Error extracting metrics: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def extract_graph_data_controller():
    """
    Extracts numerical data points from the chat context (question + answer)
    and formats them as structured chart data for frontend visualization.
    Expects JSON: { "question": "...", "answer": "..." }
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    question = data.get("question", "")
    answer = data.get("answer", "")
    
    prompt = f"""
You are a data visualization assistant.
Based on the user's question and the system's answer below, extract any numerical or sales data mentioned and format it as structured JSON.
You must categorize the extracted data into one of the following chart data formats based on what is being compared in the text:

1. "dummyYoYData": Use this if the data compares Year-over-Year sales (specifically 2025 vs 2026) for different regions or cities.
   Format of each item: {{ "name": "REGION_NAME", "y2026": float, "y2025": float }}
   
2. "dummyYearComparisonData": Use this if the data compares monthly sales across multiple years (2022 to 2026).
   Format of each item: {{ "month": "MONTH_NAME", "y2022": float, "y2023": float, "y2024": float, "y2025": float, "y2026": float }}
   
3. "dummyZoneData": Use this if the data shows sales across different geographic zones (e.g., Central, North, East, South, West).
   Format of each item: {{ "name": "ZONE_NAME", "value": float }}
   
4. "dummyTyreData": Use this if the data shows sales for different tyre categories (e.g., TRUCK, CAR, LCV, SCV, etc.).
   Format of each item: {{ "name": "TYRE_TYPE", "value": float }}

Important Instructions:
- Only populate the array that matches the data category discussed in the Q&A context. 
- For any of the 4 arrays that are NOT applicable or do not have any data mentioned in the text, return them as empty lists `[]`.
- Include the "COLORS" key exactly as shown below.
- Parse all numeric values as clean floats/integers.

Question: "{question}"
Answer: "{answer}"

Return EXACTLY a valid JSON object in this format, with no markdown formatting or extra text:
{{
  "dummyYoYData": [ ... ],
  "dummyYearComparisonData": [ ... ],
  "dummyZoneData": [ ... ],
  "COLORS": ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8", "#E06666", "#93C47D"],
  "dummyTyreData": [ ... ]
}}
"""
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = call_llm_chat(messages, temperature=0.0)
        # Clean json if it contains markdown formatting
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        elif response.startswith("```"):
            response = response.replace("```", "").strip()
            
        chart_data = json.loads(response)
        return jsonify({"status": "success", "data": chart_data}), 200
    except Exception as e:
        print(f"[Graph] Error extracting chart data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500




# default_dashboard_metrics_controller
def default_dashboard_metrics_controller(get_db_connection):
    """
    Fetches default summary metrics (total sales, top tyre, leading region, YoY growth)
    to populate the dashboard right-side panels when the page initially loads.
    Uses dynamic table mapping based on session_id from external_db_sync_log.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    session_id = data.get("session_id", "")
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    conn = None
    cursor = None
    
    # Fallback default values
    metrics_data = {
        "metric_1": {"label": "Total Sales Revenue", "value": "N/A", "subtext": "No data available"},
        "metric_2": {"label": "Top Performing Tyre", "value": "N/A", "subtext": "No data available"},
        "metric_3": {"label": "Leading Region", "value": "N/A", "subtext": "No data available"},
        "metric_4": {"label": "Year-over-Year Growth", "value": "N/A", "subtext": "No data available"}
    }

    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Failed to connect to database."}), 500
            
        cursor = conn.cursor(dictionary=True)

        # 1. Look up the dynamic table name and database from external_db_sync_log
        cursor.execute("""
            SELECT new_user_db, table_name 
            FROM external_db_sync_log 
            WHERE session_id=%s 
              AND new_user_db IS NOT NULL 
              AND new_user_db != ''
              AND table_name IS NOT NULL
            ORDER BY id DESC LIMIT 1
        """, (session_id,))
        sync_row = cursor.fetchone()

        if not sync_row:
            print(f"[Default Metrics] No dynamic table found for session {session_id}")
            return jsonify({"status": "success", "data": metrics_data}), 200

        user_db = sync_row["new_user_db"]
        tbl_name = sync_row["table_name"]
        
        # Build the dynamic fully qualified table name `db`.`table`
        table_name = f"`{user_db}`.`{tbl_name}`"
        
        # Switch to the new database just to be safe, though fully qualified name works
        cursor.execute(f"USE `{user_db}`")
        
        # Need to parse numeric values from strings if they contain commas
        revenue_expr = """
            CAST(
                REPLACE(TRIM(invoice_value), ',', '')
                AS DECIMAL(18,2)
            )
        """

        # 1. Total Sales Revenue
        cursor.execute(f"""
            SELECT
                SUM(invoice_value) AS total_sales_revenue
            FROM {table_name}
        """)
        total_revenue = cursor.fetchone()["total_sales_revenue"] or 0

        # 2. Top Performing Tyre
        cursor.execute(f"""
            SELECT
                tyre_type,
                ROUND(SUM({revenue_expr}), 2) AS revenue
            FROM {table_name}
            WHERE tyre_type IS NOT NULL
              AND tyre_type <> ''
            GROUP BY tyre_type
            ORDER BY revenue DESC
            LIMIT 1
        """)
        top_tyre_row = cursor.fetchone()
        top_tyre = top_tyre_row["tyre_type"] if top_tyre_row else ""

        # 3. Leading Region
        cursor.execute(f"""
            SELECT
                region,
                ROUND(SUM({revenue_expr}), 2) AS revenue
            FROM {table_name}
            WHERE region IS NOT NULL
              AND region <> ''
            GROUP BY region
            ORDER BY revenue DESC
            LIMIT 1
        """)
        leading_region_row = cursor.fetchone()
        leading_region = leading_region_row["region"] if leading_region_row else ""

        # 4. Current Year Revenue (Assuming dates are 'DD-MM-YYYY')
        cursor.execute(f"""
            SELECT ROUND(
                SUM({revenue_expr}),
                2
            ) AS revenue
            FROM {table_name}
            WHERE invoice_date IS NOT NULL AND invoice_date != ''
              AND YEAR(STR_TO_DATE(invoice_date, '%d-%m-%Y')) = YEAR(CURDATE())
        """)
        curr_row = cursor.fetchone()
        current_year = float(curr_row["revenue"] or 0) if curr_row else 0.0

        # 5. Previous Year Revenue
        cursor.execute(f"""
            SELECT ROUND(
                SUM({revenue_expr}),
                2
            ) AS revenue
            FROM {table_name}
            WHERE invoice_date IS NOT NULL AND invoice_date != ''
              AND YEAR(STR_TO_DATE(invoice_date, '%d-%m-%Y')) = YEAR(CURDATE()) - 1
        """)
        prev_row = cursor.fetchone()
        previous_year = float(prev_row["revenue"] or 0) if prev_row else 0.0

        yoy = 0
        if previous_year > 0:
            yoy = round(((current_year - previous_year) / previous_year) * 100, 2)

        # Format total revenue smartly (Cr or Lacs)
        formatted_revenue = f"₹{float(total_revenue):,.2f}"
        if total_revenue >= 10000000:
            formatted_revenue = f"₹{(total_revenue / 10000000):.2f} Cr"
        elif total_revenue >= 100000:
            formatted_revenue = f"₹{(total_revenue / 100000):.2f} Lac"

        # Format output as dynamic metrics for frontend
        metrics_data = {
            "metric_1": {
                "label": "Total Sales Revenue", 
                "value": formatted_revenue, 
                "subtext": "Lifetime revenue"
            },
            "metric_2": {
                "label": "Top Performing Tyre", 
                "value": str(top_tyre), 
                "subtext": "Highest revenue generator"
            },
            "metric_3": {
                "label": "Leading Region", 
                "value": str(leading_region), 
                "subtext": "Most profitable territory"
            },
            "metric_4": {
                "label": "Year-over-Year Growth", 
                "value": f"{yoy}%", 
                "subtext": "Compared to last year"
            }
        }

        return jsonify({"status": "success", "data": metrics_data}), 200

    except Exception as exc:
        print(f"[Default Metrics] Database query failed: {exc}")
        return jsonify({
            "status": "error",
            "message": "Database query failed.",
            "details": str(exc)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
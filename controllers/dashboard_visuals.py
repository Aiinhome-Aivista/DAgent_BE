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
from model.llm_client import call_llm_chat

def classify_intent(user_query: str) -> str:
    """
    Analyzes the user's query and classifies it into one of three categories:
    1. AGGREGATION: Mathematical calculation, counting, ranking, sorting.
    2. INSIGHT: Semantic relationships, reasons, 'why' questions.
    3. HYBRID: Needs both structural filtering and semantic insight.
    """
    router_prompt = f"""
    You are an AI query router for a data system. Analyze the user's query and classify it into exactly one of three categories:
    
    1. AGGREGATION: Use this if the question can be answered entirely using database operations such as filtering, grouping, counting, ranking, joining, set operations, averages, percentages, or window functions (e.g., "Identify percentage of active customers who bought both", "top 10 customers", "total sales").
    2. INSIGHT: Use this if the query requires finding conceptual relationships, trends, contextual explanations, or reading specific notes (e.g., "Why did region X fail?", "What do customers think about product Y?").
    3. HYBRID: Use this if the query requires filtering by specific IDs or categories first, and then finding semantic context (e.g., "Summarize the complaints for our top 5 most expensive products").
    
    Respond with ONLY the category name: AGGREGATION, INSIGHT, or HYBRID.
    
    User Query: "{user_query}"
    Category:"""
    
    messages = [{"role": "user", "content": router_prompt}]
    try:
        response = call_llm_chat(messages, temperature=0.0)
        if response:
            category = response.strip().upper()
            if category in ["AGGREGATION", "INSIGHT", "HYBRID"]:
                return category
    except Exception as e:
        print(f"[Router] Error classifying intent: {e}")
    
    # Default fallback
    return "INSIGHT"

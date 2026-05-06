import json
import re
from llm import llm
from tools.search_tool import web_search

def discovery_agent(state):
    """
    Finds potential leads (companies) based on the target requirements (jd.txt).
    """
    client_requirements = state.get("client_requirements", "")
    
    # 1. Use LLM to generate a clean, short search query (avoid long URL issues)
    query_prompt = f"""
    Based on these requirements, generate a short 5-8 word search query to find companies hiring for these skills:
    {client_requirements[:1000]}
    
    Return ONLY the search query string.
    """
    query_response = llm.invoke(query_prompt)
    search_query = query_response.content.strip().strip('"')
    
    # Clean query from potential markdown or extra text
    search_query = re.sub(r'^Query:\s*', '', search_query, flags=re.IGNORECASE)
    
    print(f"[DISCOVERY AGENT] Searching for: {search_query}")
    
    # 2. Perform the search
    search_results = web_search(search_query, max_results=10)

    # 3. Analyze results to find specific leads
    response = llm.invoke(
        f"""
        You are a Lead Discovery Agent.
        
        Based on the following client requirements and search results, identify 3-5 potential target companies (leads) that Webanix Solutions could approach.
        
        Target Requirements:
        {client_requirements}
        
        Search Results:
        {json.dumps(search_results, indent=2)}
        
        For each potential lead, provide:
        - company_name
        - reason_for_targeting
        - industry
        
        Return a list of leads in structured JSON format:
        {{
            "discovered_leads": [
                {{"company_name": "Name", "reason": "...", "industry": "..."}},
                ...
            ]
        }}
        """
    )

    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        data = json.loads(content)
        discovered_leads = data.get("discovered_leads", [])
    except Exception as e:
        print(f"[DISCOVERY AGENT] Error parsing leads: {e}")
        discovered_leads = []

    return {
        "discovered_leads": discovered_leads,
        "current_lead_index": 0
    }

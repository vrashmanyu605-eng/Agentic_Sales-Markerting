import json
from llm import llm
from tools.search_tool import web_search

def competitor_analysis_agent(state):
    company_name = state["company_name"]
    competitors_data = state["competitors_data"]

    # Perform internet search for fresh competitor data
    search_query = f"competitors of {company_name} {competitors_data} IT services 2024 2025"
    search_results = web_search(search_query)

    response = llm.invoke(
        f"""
        You are a Competitor Analysis Agent.

        Analyze the competitive landscape using provided data and fresh search results.

        Company Name:
        {company_name}

        Initial Competitor Data:
        {competitors_data}

        Fresh Search Results:
        {json.dumps(search_results, indent=2)}

        Analyze:
        - competitor_strengths
        - competitor_weaknesses
        - market_position
        - pricing_comparison
        - service_gaps
        - differentiators
        - market_opportunities
        - winning_strategy

        Return structured JSON only.
        """
    )

    return {
        "competitor_analysis": response.content
    }
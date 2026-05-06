import json
from llm import llm
from tools.search_tool import web_search

def sales_strategy_agent(state):
    lead_research = state["lead_research"]
    icp_analysis = state["icp_analysis"]

    # Search for sales strategies and industry pain points
    search_query = f"sales conversion strategies for IT services in {state.get('target_industry', 'tech')} 2025"
    strategy_results = web_search(search_query)

    response = llm.invoke(
        f"""
        You are a Sales Strategy Agent.

        Create a strategic conversion and upsell plan based on lead research, ICP analysis, and current market trends.

        Lead Research:
        {lead_research}

        ICP Analysis:
        {icp_analysis}

        Market Strategy Trends:
        {json.dumps(strategy_results, indent=2)}

        Analyze:
        - sales_funnel_optimization
        - key_value_propositions
        - objection_handling
        - upsell_opportunities
        - conversion_tactics
        - engagement_roadmap

        Return structured JSON only.
        """
    )

    return {
        "sales_strategy": response.content
    }
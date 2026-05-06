import json
from llm import llm
from tools.search_tool import web_search

def icp_matching_agent(state):
    lead_research = state["lead_research"]
    ideal_customer_profile = state["ideal_customer_profile"]

    # Search for industry-specific ICP benchmarks
    search_query = f"Ideal Customer Profile benchmarks for {state.get('target_industry', 'manufacturing')} IT services"
    icp_benchmarks = web_search(search_query)

    response = llm.invoke(
        f"""
        You are an ICP Matching Agent.

        Compare the lead against the Ideal Customer Profile using provided research and industry benchmarks.

        Lead Research:
        {lead_research}

        ICP Definition:
        {ideal_customer_profile}

        Industry ICP Benchmarks:
        {json.dumps(icp_benchmarks, indent=2)}

        Analyze:
        - icp_match_score
        - matching_attributes
        - missing_attributes
        - revenue_potential
        - urgency_level
        - buying_probability
        - best_service_fit

        Return structured JSON only.
        """
    )

    return {
        "icp_analysis": response.content
    }
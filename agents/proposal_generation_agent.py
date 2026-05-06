import json
from llm import llm
from tools.search_tool import web_search

def proposal_generation_agent(state):
    client_requirements = state["client_requirements"]
    company_services = state["company_services"]
    case_studies = state["case_studies"]
    pricing_data = state["pricing_data"]

    # Search for industry proposal standards and tech stack trends
    search_query = f"proposal best practices for {state.get('target_industry', 'tech')} services 2025"
    proposal_trends = web_search(search_query)

    response = llm.invoke(
        f"""
        You are a Proposal Generation Agent.

        Generate a professional IT services proposal using provided data and current industry standards.

        Client Requirements:
        {client_requirements}

        Company Services:
        {company_services}

        Case Studies:
        {case_studies}

        Pricing Data:
        {pricing_data}

        Industry Proposal Trends:
        {json.dumps(proposal_trends, indent=2)}

        Generate:
        - executive_summary
        - project_scope
        - proposed_solution
        - technology_stack
        - implementation_plan
        - estimated_timeline
        - team_structure
        - pricing_estimate
        - milestones

        Return structured JSON only.
        """
    )

    return {
        "proposal_document": response.content
    }
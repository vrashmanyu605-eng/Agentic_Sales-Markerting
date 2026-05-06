import json
from llm import llm
from tools.search_tool import web_search

def marketing_content_agent(state):
    service_details = state["service_details"]
    target_industry = state["target_industry"]
    case_studies = state["case_studies"]

    # Search for trending topics in the target industry
    search_query = f"trending marketing topics {target_industry} IT services AI automation 2024 2025"
    trending_results = web_search(search_query)

    response = llm.invoke(
        f"""
        You are a Marketing Content Agent for an IT services company.

        Generate high-quality marketing content using service details and trending industry topics.

        Service Details:
        {service_details}

        Target Industry:
        {target_industry}

        Case Studies:
        {case_studies}

        Trending Topics from Search:
        {json.dumps(trending_results, indent=2)}

        Generate:
        - linkedin_post
        - blog_topic_ideas
        - email_campaign
        - ad_copy
        - seo_keywords
        - case_study_summary
        - call_to_action
        - marketing_headlines

        Return structured JSON only.
        """
    )

    return {
        "marketing_content": response.content
    }
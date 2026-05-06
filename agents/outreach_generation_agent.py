from llm import llm


def outreach_generation_agent(state):

    lead_research = state["lead_research"]
    icp_analysis = state["icp_analysis"]
    sender_name = state["sender_name"]
    company_services = state["company_services"]

    response = llm.invoke(
        f"""
        You are a Sales Outreach Generation Agent.

        Generate personalized outreach messages for a potential client.

        Lead Research:
        {lead_research}

        ICP Analysis:
        {icp_analysis}

        Company Services:
        {company_services}

        Sender Name:
        {sender_name}

        Generate:
        - personalized_email
        - linkedin_message
        - followup_email
        - meeting_request_message
        - call_pitch
        - pain_point_based_hook
        - subject_lines

        Keep messaging professional, personalized, and sales-oriented.

        Return structured JSON only.
        """
    )

    return {
        "outreach_content": response.content
    }
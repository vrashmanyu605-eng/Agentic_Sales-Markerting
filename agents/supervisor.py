from llm import llm
import json


def supervisor_agent(state):
    """
    AI Sales & Marketing Workflow Supervisor Agent

    Responsibilities:
    - Orchestrates all marketing and sales agents
    - Prevents workflow loops
    - Validates dependencies
    - Tracks workflow progress
    - Ensures smooth multi-agent execution
    - Determines next best action dynamically
    """

    print("\n[SUPERVISOR] Evaluating Sales & Marketing Workflow...\n")

    history = state.get("workflow_history", [])

    agents_info = {

        "discovery_agent": {
            "purpose": "Finds potential companies (leads) based on JD/requirements.",
            "requires": ["client_requirements"],
            "provides": ["discovered_leads"],
            "priority": 0
        },

        "lead_research_agent": {
            "purpose": "Researches the target company and extracts business intelligence.",
            "requires": [
                "company_name"
            ],
            "provides": [
                "lead_research",
                "enriched_leads"
            ],
            "priority": 1
        },

        "icp_matching_agent": {
            "purpose": "Matches lead against Ideal Customer Profile.",
            "requires": [
                "lead_research",
                "ideal_customer_profile"
            ],
            "provides": [
                "icp_analysis"
            ],
            "priority": 2
        },

        "competitor_analysis_agent": {
            "purpose": "Analyzes competitors and identifies positioning opportunities.",
            "requires": [
                "company_name",
                "competitors_data"
            ],
            "provides": [
                "competitor_analysis"
            ],
            "priority": 3
        },

        "outreach_generation_agent": {
            "purpose": "Generates personalized outreach content and email strategy.",
            "requires": [
                "lead_research",
                "icp_analysis",
                "company_services",
                "sender_name"
            ],
            "provides": [
                "outreach_content"
            ],
            "priority": 4
        },

        "proposal_generation_agent": {
            "purpose": "Creates detailed sales proposals tailored to the lead.",
            "requires": [
                "client_requirements",
                "company_services",
                "sales_deck_text"
            ],
            "provides": [
                "proposal_document"
            ],
            "priority": 5
        },

        "crm_update_agent": {
            "purpose": "Saves all lead info, emails, and proposals into Google Sheets.",
            "requires": [
                "company_name",
                "outreach_content",
                "proposal_document"
            ],
            "provides": [
                "crm_update"
            ],
            "priority": 6
        }
    }

    discovered_leads = state.get("discovered_leads", [])
    current_index = state.get("current_lead_index", 0)
    company_name = state.get("company_name")

    # Auto-assign next lead if current one is done or not set
    updated_state = {}
    if discovered_leads and not company_name:
        lead = discovered_leads[current_index]
        company_name = lead["company_name"]
        updated_state["company_name"] = company_name
        updated_state["active_lead"] = lead
        print(f"[SUPERVISOR] Starting work on new lead: {company_name}")

    available_data = [
        key for key, value in state.items()
        if value and key not in [
            "task",
            "next_agent",
            "workflow_stage",
            "workflow_history",
            "completed",
            "error",
            "supervisor_reasoning",
            "workflow_status",
            "risk_analysis",
            "discovered_leads"
        ]
    ]

    call_counts = {}

    for agent in history:
        call_counts[agent] = call_counts.get(agent, 0) + 1

    flagged_agents = [
        agent for agent, count in call_counts.items()
        if count >= 3
    ]

    workflow_goal = state.get(
        "task",
        "Find leads and generate strategy/proposal/emails, then save to Google Sheets."
    )

    prompt = f"""
    You are an AI Sales & Marketing Workflow Supervisor.

    Your goal: {workflow_goal}

    =====================================================
    CURRENT STATE
    =====================================================

    Active Lead: {company_name}
    Available Data Fields: {json.dumps(available_data, indent=2)}
    Workflow History: {json.dumps(history[-10:], indent=2)}
    Agent Call Counts: {json.dumps(call_counts, indent=2)}

    =====================================================
    AGENT REGISTRY
    =====================================================

    {json.dumps(agents_info, indent=2)}

    =====================================================
    DECISION RULES
    =====================================================

    1. If discovered_leads is empty, call discovery_agent.
    2. Once a lead is active ({company_name}), follow this sequence:
       - lead_research_agent (must be first for a new lead)
       - icp_matching_agent
       - competitor_analysis_agent
       - outreach_generation_agent (generates emails/strategy)
       - proposal_generation_agent
       - crm_update_agent (saves everything to sheets)
    3. ONLY call crm_update_agent after outreach and proposal are ready.
    4. After crm_update_agent finishes for a lead, if there are more discovered leads, you can finish this run or signal next.
    5. For now, focus on completing the full cycle for the current lead.

    =====================================================
    RESPONSE FORMAT
    =====================================================

    Return STRICT JSON ONLY:

    {{
        "reasoning": "Detailed explanation",
        "next_agent": "selected_agent_name_or_finished",
        "workflow_status": {{
            "progress_percentage": 0,
            "current_stage": "stage_name"
        }}
    }}
    """

    try:

        response = llm.invoke(prompt)

        content = response.content.strip()

        # Remove markdown formatting
        if content.startswith("```json"):
            content = content[7:-3].strip()

        elif content.startswith("```"):
            content = content[3:-3].strip()

        decision = json.loads(content)

        next_agent = decision.get("next_agent", "finished")

        reasoning = decision.get(
            "reasoning",
            "No reasoning provided."
        )

        if next_agent in flagged_agents:

            print(
                f"[SUPERVISOR GUARDRAIL] "
                f"Loop detected for {next_agent}"
            )

            next_agent = "finished"

            reasoning = (
                f"Workflow terminated because "
                f"{next_agent} exceeded retry threshold."
            )


        print(f"\n[SUPERVISOR REASONING]\n{reasoning}\n")

        print(f"[SUPERVISOR ROUTING] -> {next_agent}")


        new_history = (
            history + [next_agent]
            if next_agent != "finished"
            else history
        )

        return {
            **updated_state,

            "next_agent": next_agent,

            "workflow_stage": next_agent,

            "workflow_history": new_history,

            "supervisor_reasoning": reasoning,

            "workflow_status": decision.get(
                "workflow_status",
                {}
            ),

            "risk_analysis": decision.get(
                "risk_analysis",
                {}
            )
        }

    except Exception as e:

        print(f"\n[SUPERVISOR ERROR] {str(e)}\n")

        return {

            "next_agent": "finished",

            "workflow_stage": "error",

            "error": str(e),

            "supervisor_reasoning": f"Supervisor failed with error: {str(e)}",

            "workflow_health": "failed"
        }
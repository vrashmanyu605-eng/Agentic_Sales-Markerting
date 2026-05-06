from graph.workflow import app

from src.services.pdf_parsing import extract_pdf_text

import json


# =========================================================
# LOAD SALES DECK
# =========================================================

sales_deck_path = "Creds_Deck_Webanix_Development_Services_2026 1.pdf"

sales_deck_text = extract_pdf_text(
    sales_deck_path
)


with open("jd.txt", "r", encoding="utf-8") as file:

    client_requirements = file.read()


initial_state = {


    "task": (
        "Find potential IT services leads, research them, "
        "generate outreach strategies and proposals, "
        "and save all details to Google Sheets."
    ),


    "company_name": None,

    "target_industry": "IT Services / AI Automation",

    "sender_name": "Vrashmanyu",

    "client_name": "Webanix Prospect",

    "sales_deck_text": sales_deck_text,

    "client_requirements": client_requirements,

    "competitors_data": "Standard AI/ML Services Competitors",

    # =====================================================
    # BUSINESS DATA
    # =====================================================

    "company_services": """
    AI Automation, Agentic AI Systems, Web Development, 
    Cloud Solutions, DevOps, Data Engineering.
    """,

    "service_details": """
    We provide enterprise AI automation, custom software development, 
    workflow orchestration, and AI-powered business solutions.
    """,

    "ideal_customer_profile": """
    Mid-size and enterprise companies investing in AI, 
    digital transformation, and operational efficiency.
    """,

    "pricing_information": "Projects range $10k-$50k.",

    "pricing_data": "Custom pricing based on scope.",

    "case_studies": """
    1. Automated inventory management.
    2. Cloud migration.
    3. AI-driven customer support.
    """,

    "meeting_transcript": "Initial discovery phase - no transcript yet.",

    "meeting_transcripts": [],

    "email_threads": [],

    "spreadsheet_id": "1MsG4jkVacHwuw2cxTQ_Vt5cW5qKoBgGJH1IqfDCdRto",

    "spreadsheet_range": "Sheet1!A1",

    "discovered_leads": [],

    "current_lead_index": 0,

    "active_lead": {},

    # =====================================================
    # WORKFLOW CONTROL
    # =====================================================

    "workflow_stage": "start",

    "workflow_history": [],

    "completed_agents": [],

    "failed_agents": [],

    # =====================================================
    # EXECUTION STATUS
    # =====================================================

    "completed": False,

    "progress_percentage": 0
}

# =========================================================
# RUN GRAPH
# =========================================================

final_state = None

print("\n")
print("=" * 60)
print("STARTING SALES & MARKETING AI WORKFLOW")
print("=" * 60)

try:

    for event in app.stream(initial_state):

        for node, state in event.items():

            print("\n")
            print("=" * 60)
            print(f"NODE: {node.upper()}")
            print("=" * 60)

            # =================================================
            # SUPERVISOR
            # =================================================

            if node == "supervisor":

                print(
                    f"\nNext Agent: "
                    f"{state.get('next_agent')}"
                )

                print(
                    f"\nReasoning:\n"
                    f"{state.get('supervisor_reasoning')}"
                )

            # =================================================
            # LEAD DISCOVERY
            # =================================================

            elif node == "discovery_agent":

                print("\n[LEAD DISCOVERY]\n")

                leads = state.get("discovered_leads", [])
                for i, lead in enumerate(leads):
                    print(f"{i+1}. {lead.get('company_name')} ({lead.get('industry')})")

            # =================================================
            # LEAD RESEARCH
            # =================================================

            elif node == "lead_research_agent":

                print("\n[LEAD RESEARCH]\n")

                print(
                    state.get(
                        "lead_research"
                    )
                )

            # =================================================
            # ICP MATCHING
            # =================================================

            elif node == "icp_matching_agent":

                print("\n[ICP ANALYSIS]\n")

                print(
                    state.get(
                        "icp_analysis"
                    )
                )

            # =================================================
            # COMPETITOR ANALYSIS
            # =================================================

            elif node == "competitor_analysis_agent":

                print("\n[COMPETITOR ANALYSIS]\n")

                print(
                    state.get(
                        "competitor_analysis"
                    )
                )

            # =================================================
            # OUTREACH GENERATION
            # =================================================

            elif node == "outreach_generation_agent":

                print("\n[OUTREACH CONTENT]\n")

                print(
                    state.get(
                        "outreach_content"
                    )
                )

            # =================================================
            # PROPOSAL GENERATION
            # =================================================

            elif node == "proposal_generation_agent":

                print("\n[PROPOSAL DOCUMENT]\n")

                print(
                    state.get(
                        "proposal_document"
                    )
                )

            # =================================================
            # SALES STRATEGY
            # =================================================

            elif node == "sales_strategy_agent":

                print("\n[SALES STRATEGY]\n")

                print(
                    state.get(
                        "sales_strategy"
                    )
                )

            # =================================================
            # MARKETING CONTENT
            # =================================================

            elif node == "marketing_content_agent":

                print("\n[MARKETING CONTENT]\n")

                print(
                    state.get(
                        "marketing_content"
                    )
                )

            # =================================================
            # CLIENT SENTIMENT
            # =================================================

            elif node == "client_sentiment_agent":

                print("\n[CLIENT SENTIMENT]\n")

                print(
                    state.get(
                        "client_sentiment"
                    )
                )

            # =================================================
            # CRM UPDATE
            # =================================================

            elif node == "crm_update_agent":

                print("\n[CRM UPDATE]\n")

                print(
                    state.get(
                        "crm_update"
                    )
                )

            final_state = state

    # =====================================================
    # FINAL SUMMARY
    # =====================================================

    print("\n")
    print("=" * 60)
    print("WORKFLOW COMPLETED")
    print("=" * 60)

    print(
        f"\nWorkflow History:\n"
        f"{json.dumps(final_state.get('workflow_history', []), indent=2)}"
    )

except Exception as e:

    print("\n")
    print("=" * 60)
    print("WORKFLOW FAILED")
    print("=" * 60)

    print(f"\nERROR:\n{str(e)}")
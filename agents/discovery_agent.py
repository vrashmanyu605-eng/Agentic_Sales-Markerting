import json
import re
from llm import llm
from tools.search_tool import web_search


def discovery_agent(state: dict) -> dict:
    """
    Finds potential leads and stores them as pending_leads.
    The supervisor will pop from this list one at a time.
    """
    client_requirements = state.get("client_requirements", "")

    # ── Step 1: Generate a clean search query ─────────────────────────────────
    query_response = llm.invoke(
        f"""Based on these requirements, generate a short 5-8 word search query
        to find companies that need these services:
        {client_requirements[:1000]}

        Return ONLY the search query string, no quotes, no preamble."""
    )
    search_query = query_response.content.strip().strip('"')
    search_query = re.sub(r'^Query:\s*', '', search_query, flags=re.IGNORECASE)

    print(f"[DISCOVERY AGENT] Searching for: {search_query}")

    # ── Step 2: Search ─────────────────────────────────────────────────────────
    search_results = web_search(search_query, max_results=10)

    # ── Step 3: Extract structured leads ──────────────────────────────────────
    response = llm.invoke(
        f"""You are a Lead Discovery Agent.

        Identify 3-5 companies from the search results that Webanix Solutions
        could approach based on the requirements below.

        Requirements:
        {client_requirements}

        Search Results:
        {json.dumps(search_results, indent=2)}

        Return STRICT JSON only — no markdown, no preamble:
        {{
            "leads": [
                {{
                    "company_name": "...",
                    "industry":     "...",
                    "reason":       "one sentence why they are a good fit"
                }}
            ]
        }}"""
    )

    try:
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()

        data          = json.loads(content)
        pending_leads = data.get("leads", [])

    except Exception as e:
        print(f"[DISCOVERY AGENT] Parse error: {e}")
        pending_leads = []

    print(f"[DISCOVERY AGENT] Found {len(pending_leads)} leads: "
          f"{[l.get('company_name') for l in pending_leads]}")

    return {
        # ── Feed the supervisor's queue ────────────────────────────────────────
        "pending_leads":       pending_leads,

        # ── Initialise tracking fields ─────────────────────────────────────────
        "current_lead":        None,
        "company_name":        None,
        "completed_leads":     [],

        # ── Clear any stale pipeline outputs ──────────────────────────────────
        "lead_research":       None,
        "icp_analysis":        None,
        "competitor_analysis": None,
        "outreach_content":    None,
        "proposal_document":   None,
        "crm_update":          None,
    }
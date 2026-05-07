def supervisor_agent(state: dict) -> dict:
    """
    Deterministic supervisor — no LLM involved.

    Single responsibility: pop the next lead from pending_leads
    and signal the pipeline to start, or signal END if none remain.

    Never routes to mid-pipeline agents. Never re-calls itself.
    """
    print("\n[SUPERVISOR] Evaluating next lead...")

    pending_leads = state.get("pending_leads", [])
    print(f"[SUPERVISOR] pending_leads received: {pending_leads}")

    # ── No leads left → end the workflow ──────────────────────────────────────
    if not pending_leads:
        print("[SUPERVISOR] No leads remaining. Workflow complete.")
        return {
            **state,
            "next_agent":      "finished",
            "current_lead":    None,
            "company_name":    None,
        }

    # ── Pop the next lead and start its pipeline ───────────────────────────────
    current_lead = pending_leads[0]
    remaining    = pending_leads[1:]

    company_name = current_lead.get("company_name", "Unknown")
    print(f"[SUPERVISOR] Starting pipeline for: {company_name}")
    print(f"[SUPERVISOR] Leads remaining after this: {len(remaining)}")

    return {
        **state,

        # Lead queue management
        "current_lead":   current_lead,
        "company_name":   company_name,
        "pending_leads":  remaining,

        # Signal the router → always starts at lead_research_agent
        "next_agent":     "lead_research_agent",

        # ── Clear previous lead's outputs so agents never see stale data ──────
        "lead_research":          None,
        "icp_analysis":           None,
        "competitor_analysis":    None,
        "outreach_content":       None,
        "proposal_document":      None,
        "crm_update":             None,
    }
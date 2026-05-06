from typing_extensions import TypedDict
from typing import Optional, List


class SalesMarketingState(TypedDict, total=False):

    # =====================================================
    # TASK INPUT
    # =====================================================

    task: str

    company_name: str

    target_industry: str

    sender_name: str

    # =====================================================
    # RAW INPUTS
    # =====================================================

    sales_deck_text: str

    client_requirements: str

    competitors_data: str

    # =====================================================
    # BUSINESS DATA
    # =====================================================

    company_services: str

    service_details: str

    ideal_customer_profile: str

    pricing_information: str

    # =====================================================
    # AGENT OUTPUTS
    # =====================================================

    lead_research: str

    icp_analysis: str

    competitor_analysis: str

    outreach_content: str

    proposal_document: str

    sales_strategy: str

    marketing_content: str

    client_sentiment: str

    crm_update: str

    enriched_leads: list

    # =====================================================
    # INPUT DATA FOR SPECIFIC AGENTS
    # =====================================================

    meeting_transcript: str

    meeting_transcripts: List[str]

    client_name: str

    email_threads: List[str]

    case_studies: str

    pricing_data: str

    spreadsheet_id: str

    spreadsheet_range: str

    discovered_leads: List[dict]

    current_lead_index: int

    active_lead: dict

    # =====================================================
    # WORKFLOW CONTROL
    # =====================================================

    workflow_stage: str

    next_agent: str

    workflow_history: List[str]

    completed_agents: List[str]

    failed_agents: List[str]

    # =====================================================
    # EXECUTION STATUS
    # =====================================================

    completed: bool

    progress_percentage: int

    supervisor_reasoning: str

    error: Optional[str]
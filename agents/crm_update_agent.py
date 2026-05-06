import json
from llm import llm
from tools.google_sheets_tool import update_google_sheet
from tools.search_tool import web_search

def crm_update_agent(state):
    meeting_transcript = state["meeting_transcript"]
    client_name = state["client_name"]
    spreadsheet_id = state.get("spreadsheet_id")
    spreadsheet_range = state.get("spreadsheet_range", "Sheet1!A1")

    # Search for any recent news about the client company
    search_query = f"recent news {client_name} company"
    client_news = web_search(search_query)

    response = llm.invoke(
        f"""
        You are a CRM Update Agent.

        Analyze the meeting transcript and fresh client news to generate CRM-ready updates.

        Client Name:
        {client_name}

        Meeting Transcript:
        {meeting_transcript}

        Fresh Client News:
        {json.dumps(client_news, indent=2)}

        Extract:
        - meeting_summary
        - client_requirements
        - objections
        - budget_signals
        - urgency_level
        - next_steps
        - opportunity_value

        Return structured JSON only.
        """
    )

    try:
        crm_data = json.loads(response.content)
        # Prepare values for Google Sheet: [Name, Summary, Requirements, Value, Next Steps]
        sheet_values = [[
            client_name,
            crm_data.get("meeting_summary", ""),
            crm_data.get("client_requirements", ""),
            crm_data.get("opportunity_value", ""),
            crm_data.get("next_steps", "")
        ]]
        
        if spreadsheet_id:
            sheet_status = update_google_sheet(spreadsheet_id, spreadsheet_range, sheet_values)
            print(f"[CRM AGENT] Google Sheet Status: {sheet_status}")
        else:
            print("[CRM AGENT] Spreadsheet ID missing, skipping Google Sheet update.")
            
    except Exception as e:
        print(f"[CRM AGENT] Error parsing CRM data or updating sheet: {e}")

    return {
        "crm_update": response.content
    }
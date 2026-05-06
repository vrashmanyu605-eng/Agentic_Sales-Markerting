from langgraph.graph import StateGraph, END
from graph.state import SalesMarketingState
from agents.supervisor import supervisor_agent
from agents.client_sentiment_agent import (client_sentiment_agent)
from agents.competitor_analysis_agent import (competitor_analysis_agent)
from agents.icp_matching_agent import (icp_matching_agent)
from agents.lead_research_agent import (lead_research_agent)
from agents.marketing_content_agent import (marketing_content_agent)
from agents.outreach_generation_agent import (outreach_generation_agent)
from agents.proposal_generation_agent import (proposal_generation_agent)
from agents.sales_strategy_agent import (sales_strategy_agent)
from agents.crm_update_agent import (crm_update_agent)
from agents.discovery_agent import (discovery_agent)


graph = StateGraph(SalesMarketingState)


graph.add_node(
    "supervisor",
    supervisor_agent
)

graph.add_node(
    "lead_research_agent",
    lead_research_agent
)

graph.add_node(
    "icp_matching_agent",
    icp_matching_agent
)

graph.add_node(
    "competitor_analysis_agent",
    competitor_analysis_agent
)

graph.add_node(
    "outreach_generation_agent",
    outreach_generation_agent
)

graph.add_node(
    "proposal_generation_agent",
    proposal_generation_agent
)

graph.add_node(
    "sales_strategy_agent",
    sales_strategy_agent
)

graph.add_node(
    "marketing_content_agent",
    marketing_content_agent
)

graph.add_node(
    "client_sentiment_agent",
    client_sentiment_agent
)

graph.add_node(
    "crm_update_agent",
    crm_update_agent
)

graph.add_node(
    "discovery_agent",
    discovery_agent
)


graph.set_entry_point("discovery_agent")

def router(state):

    next_agent = state.get(
        "next_agent",
        "finished"
    )

    print(f"\n[ROUTER] -> {next_agent}")

    return next_agent


graph.add_conditional_edges(

    "supervisor",

    router,

    {

        "lead_research_agent":
            "lead_research_agent",

        "icp_matching_agent":
            "icp_matching_agent",

        "competitor_analysis_agent":
            "competitor_analysis_agent",

        "outreach_generation_agent":
            "outreach_generation_agent",

        "proposal_generation_agent":
            "proposal_generation_agent",

        "sales_strategy_agent":
            "sales_strategy_agent",

        "marketing_content_agent":
            "marketing_content_agent",

        "client_sentiment_agent":
            "client_sentiment_agent",

        "crm_update_agent":
            "crm_update_agent",

        "discovery_agent":
            "discovery_agent",

        "finished":
            END
    }
)


graph.add_edge(
    "lead_research_agent",
    "supervisor"
)

graph.add_edge(
    "icp_matching_agent",
    "supervisor"
)

graph.add_edge(
    "competitor_analysis_agent",
    "supervisor"
)

graph.add_edge(
    "outreach_generation_agent",
    "supervisor"
)

graph.add_edge(
    "proposal_generation_agent",
    "supervisor"
)

graph.add_edge(
    "sales_strategy_agent",
    "supervisor"
)

graph.add_edge(
    "marketing_content_agent",
    "supervisor"
)

graph.add_edge(
    "client_sentiment_agent",
    "supervisor"
)

graph.add_edge(
    "crm_update_agent",
    "supervisor"
)

graph.add_edge(
    "discovery_agent",
    "supervisor"
)

app = graph.compile()
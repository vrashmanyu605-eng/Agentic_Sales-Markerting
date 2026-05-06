from llm import llm

from tools.search_tool import search_company
from tools.website_scraper import scrape_website
from tools.linkedin_finder import find_linkedin_profiles
from tools.email_generator import generate_possible_emails

import json
import re


def extract_domain(url):

    if not url:
        return None

    match = re.search(
        r"https?://(?:www\.)?([^/]+)",
        url
    )

    if match:
        return match.group(1)

    return None


def lead_research_agent(state):

    company_name = state["company_name"]


    search_data = search_company(
        company_name
    )

    company_results = search_data.get("search_results", [])

    website_url = search_data.get("website_url")

    website_content = search_data.get("website_content", "")

    linkedin_profiles = find_linkedin_profiles(
        company_name
    )

    domain = extract_domain(website_url)

    leads = []

    for profile in linkedin_profiles:

        title = profile.get("title", "")

        name_parts = title.split("-")[0].strip().split()

        if len(name_parts) >= 2:

            first_name = name_parts[0]

            last_name = name_parts[-1]

            possible_emails = []

            if domain:

                possible_emails = generate_possible_emails(
                    first_name,
                    last_name,
                    domain
                )

            leads.append({

                "name": f"{first_name} {last_name}",

                "linkedin": profile.get(
                    "linkedin_url"
                ),

                "possible_emails": possible_emails
            })

    response = llm.invoke(
        f"""
        You are a Lead Research Agent.

        Analyze the company and leads.

        Company Search Results:
        {json.dumps(company_results, indent=2)}

        Website Content:
        {website_content}

        LinkedIn Profiles:
        {json.dumps(leads, indent=2)}

        Extract:
        - company_summary
        - industry
        - likely_pain_points
        - lead_quality
        - best_decision_makers
        - outreach_strategy
        - recommended_contacts

        Return structured JSON only.
        """
    )

    return {

        "lead_research": response.content,

        "enriched_leads": leads
    }
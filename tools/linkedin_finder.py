from ddgs import DDGS

def find_linkedin_profiles(company_name):
    query = f'''
        site:linkedin.com/in/
        ("{company_name}")
        ("CTO" OR
        "CIO" OR
        "VP Engineering" OR
        "Head of Engineering" OR
        "Director Engineering" OR
        "Head of AI" OR
        "Head of Technology" OR
        "Engineering Manager")
    '''
    profiles = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                max_results=5
            ))
            for result in results:
                profiles.append({
                    "title": result.get("title"),
                    "linkedin_url": result.get("href"),
                    "snippet": result.get("body")
                })
    except Exception as e:
        print(f"LinkedIn search error: {e}")
    return profiles
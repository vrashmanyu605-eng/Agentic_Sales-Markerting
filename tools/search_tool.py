from ddgs import DDGS
from tools.website_scraper import scrape_website

def web_search(query, max_results=5):
    """
    Performs a general web search.
    """
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(
                query,
                max_results=max_results
            ))
            for result in search_results:
                results.append({
                    "title": result.get("title"),
                    "href": result.get("href"),
                    "body": result.get("body")
                })
    except Exception as e:
        print(f"Search error: {e}")
    return results

def search_company(company_name):
    """
    Specific search to find company website and scrape it.
    """
    query = f"{company_name} official company website"
    results = web_search(query, max_results=5)
    
    website_url = None
    for result in results:
        url = result.get("href", "")
        if all(x not in url for x in ["linkedin.com", "facebook.com", "twitter.com", "instagram.com"]):
            website_url = url
            break
            
    website_content = ""
    if website_url:
        print(f"\nScraping Website: {website_url}")
        website_content = scrape_website(website_url)
        
    return {
        "search_results": results,
        "website_url": website_url,
        "website_content": website_content
    }
import requests

from bs4 import BeautifulSoup


def scrape_website(url):

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        # Remove unwanted tags
        for tag in soup([
            "script",
            "style",
            "noscript"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:10000]

    except Exception as e:

        return f"Scraping Error: {str(e)}"
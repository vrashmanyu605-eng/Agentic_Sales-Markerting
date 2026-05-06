from ddgs import DDGS


def find_linkedin_profiles(company_name):

    query = (
        f"site:linkedin.com/in/ "
        f"CTO OR CEO OR Founder {company_name}"
    )

    profiles = []

    print("\n[SEARCH QUERY]")
    print(query)

    with DDGS() as ddgs:

        results = ddgs.text(
            query,
            max_results=5
        )

        print("\n[RAW RESULTS]")
        print(results)

        for result in results:

            profiles.append({

                "title": result.get("title"),

                "linkedin_url": result.get("href"),

                "snippet": result.get("body")
            })

    return profiles


profiles = find_linkedin_profiles("OpenAI")

print("\n[FINAL PROFILES]\n")

for profile in profiles:

    print(profile)
    print("\n" + "=" * 50 + "\n")
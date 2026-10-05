from ddgs import DDGS
from ddgs.exceptions import DDGSException
from urllib.parse import urlparse


DIRECTORY_DOMAINS = {
    "whatclinic.com",
    "getadoc.co.za",
    "topreviews.co.za",
    "yellosa.co.za",
    "yellowpages.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "youtube.com",
    "tiktok.com",
}


def is_directory(url):
    domain = urlparse(url).netloc.lower()
    domain = domain.removeprefix("www.")

    return any(
        domain == blocked or domain.endswith("." + blocked)
        for blocked in DIRECTORY_DOMAINS
    )


def discover_businesses(niche, location, max_results=10):

    queries = [
        f"{niche} in {location} official website",
        f"{niche} {location} contact us",
        f"independent {niche} practices in {location}",
    ]

    businesses = []
    seen_domains = set()

    try:

        with DDGS() as search:

            for query in queries:

                print(f"\nSearching: {query}")

                try:

                    results = search.text(
                        query,
                        max_results=max_results
                    )

                except DDGSException as error:

                    print(
                        f"Search failed for this query: {error}"
                    )

                    print("Trying the next search...")
                    continue

                except Exception as error:

                    print(
                        f"Unexpected search error: {error}"
                    )

                    print("Trying the next search...")
                    continue

                for result in results:

                    url = result.get("href", "").strip()
                    title = result.get("title", "").strip()
                    snippet = result.get("body", "").strip()

                    if not url.startswith(
                        ("http://", "https://")
                    ):
                        continue

                    domain = urlparse(url).netloc.lower()
                    domain = domain.removeprefix("www.")

                    if not domain:
                        continue

                    if is_directory(url):
                        continue

                    if domain in seen_domains:
                        continue

                    seen_domains.add(domain)

                    businesses.append({
                        "business_name": title,
                        "location": location,
                        "website": url,
                        "search_evidence": snippet,
                        "verified": False,
                    })

                    print(
                        f"  + Found: {title}"
                    )

                    if len(businesses) >= max_results:
                        return businesses

    except Exception as error:

        print(
            f"\nDiscovery system error: {error}"
        )

    return businesses


if __name__ == "__main__":

    leads = discover_businesses(
        niche="dentists",
        location="Johannesburg",
        max_results=10
    )

    print("\n==============================")
    print("DISCOVERY RESULTS")
    print("==============================")

    for lead in leads:

        print("\n--------------------------")
        print("Business:", lead["business_name"])
        print("Website:", lead["website"])
        print("Evidence:", lead["search_evidence"])
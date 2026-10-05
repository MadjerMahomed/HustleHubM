import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/154.0 Safari/537.36"
    )
}


BUSINESS_EMAIL_PREFIXES = {
    "info",
    "hello",
    "contact",
    "bookings",
    "booking",
    "enquiries",
    "enquiry",
    "sales",
    "office",
    "admin",
    "support",
}


def is_business_email(email):

    if not email or "@" not in email:
        return False

    local_part = email.split("@")[0].lower()

    return local_part in BUSINESS_EMAIL_PREFIXES


def extract_business_email(soup):

    # 1. Check mailto links
    for link in soup.find_all(
        "a",
        href=True
    ):

        href = link.get(
            "href",
            ""
        ).strip()

        if href.lower().startswith("mailto:"):

            email = (
                href[7:]
                .split("?")[0]
                .strip()
                .lower()
            )

            if is_business_email(email):

                return email

    # 2. Search visible page text
    page_text = soup.get_text(
        " ",
        strip=True
    )

    matches = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        page_text
    )

    for email in matches:

        email = email.lower().strip()

        if is_business_email(email):

            return email

    return ""


def find_contact_pages(base_url, soup):

    pages = []

    keywords = [
        "contact",
        "contact us",
        "get in touch",
        "about",
        "book",
        "appointment"
    ]

    base_domain = urlparse(
        base_url
    ).netloc.lower()

    for link in soup.find_all(
        "a",
        href=True
    ):

        href = link.get(
            "href",
            ""
        ).strip()

        text = link.get_text(
            " ",
            strip=True
        ).lower()

        combined = (
            f"{href} {text}"
        ).lower()

        if not any(
            keyword in combined
            for keyword in keywords
        ):
            continue

        full_url = urljoin(
            base_url,
            href
        )

        parsed = urlparse(
            full_url
        )

        # Only follow links on the same website
        if parsed.netloc.lower() != base_domain:
            continue

        if full_url not in pages:

            pages.append(full_url)

    return pages[:5]


def analyze_website(url):

    result = {
        "url": url,
        "reachable": False,
        "title": "",
        "description": "",
        "text": "",
        "has_booking": False,
        "has_contact_page": False,
        "has_email": False,
        "business_email": "",
        "has_phone": False,
        "has_whatsapp": False,
        "has_social_links": False,
        "cta_count": 0,
        "error": ""
    }

    if not url:

        result["error"] = (
            "No website provided"
        )

        return result

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True
        )

        response.raise_for_status()

        result["reachable"] = True

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Title
        if soup.title:

            result["title"] = (
                soup.title.get_text(
                    " ",
                    strip=True
                )
            )

        # Description
        description = soup.find(
            "meta",
            attrs={
                "name": "description"
            }
        )

        if description:

            result["description"] = (
                description.get(
                    "content",
                    ""
                )
            )

        # Main page text
        page_text = soup.get_text(
            " ",
            strip=True
        )

        result["text"] = (
            page_text[:8000]
        )

        # Try homepage email
        email = extract_business_email(
            soup
        )

        if email:

            result["business_email"] = email
            result["has_email"] = True

        # Find contact/about pages
        contact_pages = find_contact_pages(
            response.url,
            soup
        )

        if contact_pages:

            result["has_contact_page"] = True

        # Analyze homepage links
        for link in soup.find_all(
            "a",
            href=True
        ):

            href = link.get(
                "href",
                ""
            ).strip()

            text = link.get_text(
                " ",
                strip=True
            ).lower()

            combined = (
                f"{href} {text}"
            ).lower()

            if any(
                word in combined
                for word in [
                    "book",
                    "appointment",
                    "schedule"
                ]
            ):

                result["has_booking"] = True

            if any(
                word in combined
                for word in [
                    "contact",
                    "get in touch"
                ]
            ):

                result["has_contact_page"] = True

            if any(
                word in combined
                for word in [
                    "instagram",
                    "facebook",
                    "linkedin",
                    "tiktok"
                ]
            ):

                result["has_social_links"] = True

            if (
                "whatsapp" in combined
                or "wa.me" in combined
            ):

                result["has_whatsapp"] = True

            if href.lower().startswith(
                "tel:"
            ):

                result["has_phone"] = True

        # Search contact/about pages for email
        for page_url in contact_pages:

            if result["business_email"]:
                break

            try:

                page_response = requests.get(
                    page_url,
                    headers=HEADERS,
                    timeout=10,
                    allow_redirects=True
                )

                page_response.raise_for_status()

                page_soup = BeautifulSoup(
                    page_response.text,
                    "html.parser"
                )

                email = extract_business_email(
                    page_soup
                )

                if email:

                    result["business_email"] = (
                        email
                    )

                    result["has_email"] = True

            except requests.RequestException:

                continue

        # CTA detection
        cta_words = [
            "book now",
            "book online",
            "schedule",
            "appointment",
            "contact us",
            "get started",
            "call now",
            "request",
            "enquire",
            "enquiry"
        ]

        lower_text = page_text.lower()

        result["cta_count"] = sum(
            lower_text.count(word)
            for word in cta_words
        )

        return result

    except requests.RequestException as error:

        result["error"] = str(error)

        return result


if __name__ == "__main__":

    test_url = (
        "https://thedentistsinc.co.za/"
    )

    result = analyze_website(
        test_url
    )

    print(
        "\n=============================="
    )

    print(
        "WEBSITE ANALYSIS"
    )

    print(
        "=============================="
    )

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )
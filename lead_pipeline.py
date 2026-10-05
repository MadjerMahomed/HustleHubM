import re
from urllib.parse import urlparse

from business_discovery import discover_businesses
from lead_agent import analyze_business, generate_outreach
from database import init_db, add_lead, get_connection


def normalize_domain(url):
    if not url:
        return ""

    try:
        domain = urlparse(url).netloc.lower()
        return domain.removeprefix("www.")
    except Exception:
        return ""


def lead_already_exists(website, business_name):
    new_domain = normalize_domain(website)

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT website, business_name
        FROM leads
        """
    ).fetchall()

    conn.close()

    for row in rows:

        existing_domain = normalize_domain(
            row["website"]
        )

        existing_name = (
            row["business_name"] or ""
        ).strip().lower()

        if new_domain and existing_domain == new_domain:
            return True

        if (
            business_name
            and existing_name == business_name.strip().lower()
        ):
            return True

    return False


def parse_outreach(outreach):

    if not outreach:
        return "", ""

    outreach = outreach.strip()

    subject_match = re.search(
        r"(?im)^SUBJECT:\s*(.+)$",
        outreach
    )

    body_match = re.search(
        r"(?is)^BODY:\s*(.*)$",
        outreach
    )

    subject = ""

    if subject_match:
        subject = subject_match.group(1).strip()

    body = ""

    if body_match:
        body = body_match.group(1).strip()

    if not body:
        body = outreach

    return subject, body


def run_pipeline(
    niche,
    location,
    max_leads=5,
    minimum_score=60
):

    print("\n====================================")
    print("HUSTLEHUBM LEAD MACHINE")
    print("====================================")

    print(f"\nNiche: {niche}")
    print(f"Location: {location}")
    print(f"Target leads: {max_leads}")
    print(f"Minimum score: {minimum_score}")

    init_db()

    print("\n[1/4] Discovering businesses...")

    # Search for extra candidates because some will be rejected.
    search_limit = max(max_leads * 3, 15)

    businesses = discover_businesses(
        niche=niche,
        location=location,
        max_results=search_limit
    )

    print(
        f"\nFound {len(businesses)} candidates."
    )

    qualified_leads = []

    print(
        "\n[2/4] AI qualification and scoring..."
    )

    for index, business in enumerate(
        businesses,
        start=1
    ):

        if len(qualified_leads) >= max_leads:
            break

        business_name = business.get(
            "business_name",
            "Unknown Business"
        )

        website = business.get(
            "website",
            ""
        )

        print(
            f"\nAnalyzing {index}/{len(businesses)}: "
            f"{business_name}"
        )

        if lead_already_exists(
            website,
            business_name
        ):

            print(
                "↪ Already in database — skipping."
            )

            continue

        try:

            analysis = analyze_business(
                business
            )

            is_target = analysis.get(
                "is_target_business",
                False
            )

            score = int(
                analysis.get(
                    "lead_score",
                    0
                )
            )

            if not is_target:

                print(
                    "✗ REJECTED — Not a target business"
                )

                continue

            print(
                f"Target business: YES"
            )

            print(
                f"AI Score: {score}/100"
            )

            if score < minimum_score:

                print(
                    "✗ Below threshold — skipping."
                )

                continue

            business["analysis"] = analysis
            business["lead_score"] = score

            qualified_leads.append(
                business
            )

            print(
                f"✓ QUALIFIED — Score: {score}/100"
            )

        except Exception as error:

            print(
                f"⚠ Analysis failed: {error}"
            )

    print(
        "\n[3/4] Generating personalized outreach..."
    )

    for lead in qualified_leads:

        try:

            outreach = generate_outreach(
                lead,
                lead["analysis"]
            )

            subject, body = parse_outreach(
                outreach
            )

            lead["email_subject"] = subject
            lead["email_body"] = body

            print(
                f"✓ Outreach created for "
                f"{lead['business_name']}"
            )

        except Exception as error:

            print(
                f"⚠ Outreach generation failed "
                f"for {lead['business_name']}: {error}"
            )

            lead["email_subject"] = ""
            lead["email_body"] = ""

    print(
        "\n[4/4] Saving qualified leads..."
    )

    saved_count = 0

    for lead in qualified_leads:

        analysis = lead["analysis"]

        try:

            add_lead(
                business_name=lead.get(
                    "business_name",
                    ""
                ),
                website=lead.get(
                    "website",
                    ""
                ),
                email="",
                industry=niche,
                location=location,
                lead_score=lead.get(
                    "lead_score",
                    0
                ),
                opportunity=analysis.get(
                    "opportunity",
                    ""
                )
            )

            saved_count += 1

            print(
                f"✓ Saved: "
                f"{lead['business_name']}"
            )

        except Exception as error:

            print(
                f"⚠ Could not save "
                f"{lead['business_name']}: {error}"
            )

    print("\n====================================")
    print("PIPELINE COMPLETE")
    print("====================================")

    print(
        f"\nQualified leads: "
        f"{len(qualified_leads)}"
    )

    print(
        f"Saved to database: "
        f"{saved_count}"
    )

    return qualified_leads


if __name__ == "__main__":

    run_pipeline(
        niche="dentists",
        location="Johannesburg",
        max_leads=5,
        minimum_score=60
    )
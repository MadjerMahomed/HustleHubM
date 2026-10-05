import json

from local_ai import ask_ai
from website_analyzer import analyze_website


def analyze_business(business):

    website = business.get("website", "")

    website_data = analyze_website(website)

    prompt = f"""
You are the lead qualification AI for HustleHubM.

Your job is to determine whether a search result is a REAL
potential business client for online presence, marketing,
lead-generation, or website services.

Use ONLY the evidence provided.

BUSINESS
Name: {business.get("business_name", "")}

Location:
{business.get("location", "")}

Website:
{website}

SEARCH EVIDENCE:
{business.get("search_evidence", "")}

WEBSITE EVIDENCE:
{json.dumps(website_data, indent=2)}

IMPORTANT:

First determine whether this is an actual target business.

A TARGET BUSINESS can include:
- Dentist or dental practice
- Restaurant
- Salon
- Barber
- Gym
- Clinic
- Real estate agency
- Lawyer
- Accountant
- Professional service business
- Local service business
- Other legitimate commercial business

DO NOT qualify these as target businesses:
- Business directories
- Search directories
- Listing websites
- Universities
- Government organizations
- Government departments
- News websites
- General information websites
- Review websites
- Marketplaces
- Social media profiles
- Hospitals or organizations that are not suitable commercial prospects
- Pages that simply list other businesses

If the result is NOT a target business:

Return:

{{
    "is_target_business": false,
    "lead_score": 0,
    "qualification": "REJECT",
    "opportunity": "Not a suitable target business.",
    "evidence": "",
    "recommended_service": "",
    "outreach_angle": ""
}}

If it IS a target business:

Evaluate only observable digital/marketing opportunities.

Possible opportunities include:
- Missing website features
- Weak or unclear calls-to-action
- Poor conversion flow
- Missing booking functionality
- Missing contact options
- Weak local SEO signals
- Weak website structure
- Missing lead capture
- Weak social integration
- Poor mobile conversion signals
- Other clearly observable digital opportunities

Do NOT judge:
- Quality of medical treatment
- Quality of products or services
- Customer satisfaction unless explicitly supported by evidence
- Revenue
- Number of customers
- Search rankings unless provided by evidence
- Competitor performance
- Whether demand is "untapped"
- Whether the business is losing customers
- Anything that cannot be verified

Never invent facts.

Never assume that a feature is missing simply because it was not
detected. Say "not detected in the available evidence" when appropriate.

Lead scoring:

90-100 = Very strong, clearly supported opportunity
75-89  = Strong opportunity
60-74  = Moderate opportunity
40-59  = Weak opportunity
0-39   = Poor opportunity

HIGH = 75-100
MEDIUM = 50-74
LOW = 0-49

Return ONLY valid JSON.

Use exactly this structure:

{{
    "is_target_business": true,
    "lead_score": 0,
    "qualification": "HIGH",
    "opportunity": "",
    "evidence": "",
    "recommended_service": "",
    "outreach_angle": ""
}}
"""

    response = ask_ai(prompt)

    try:

        result = json.loads(response)

        # Safety validation
        result["lead_score"] = max(
            0,
            min(
                100,
                int(result.get("lead_score", 0))
            )
        )

        if not result.get("is_target_business", True):

            result["lead_score"] = 0
            result["qualification"] = "REJECT"

        return result

    except (json.JSONDecodeError, ValueError, TypeError):

        return {
            "is_target_business": False,
            "lead_score": 0,
            "qualification": "REVIEW",
            "opportunity": "AI returned invalid analysis.",
            "evidence": response,
            "recommended_service": "",
            "outreach_angle": ""
        }


def generate_outreach(business, analysis):

    prompt = f"""
You are writing professional B2B outreach for HustleHubM.

BUSINESS
Name: {business.get("business_name", "")}

Location:
{business.get("location", "")}

Website:
{business.get("website", "")}

VERIFIED AI ANALYSIS:
{json.dumps(analysis, indent=2)}

Write a concise personalized business email.

Rules:

- 70-100 words.
- Mention ONE specific opportunity supported by the evidence.
- Do not invent information.
- Do not claim the business is losing customers.
- Do not claim the opportunity is "untapped".
- Do not guarantee results.
- Do not pretend to be a customer.
- Do not criticize their products, services, or healthcare.
- Do not mention private information.
- Keep the tone professional and human.
- Use a low-pressure call to action.
- Do not include fake unsubscribe links.
- Do not include URLs unless one was provided in the evidence.
- Do not use exaggerated marketing language.

If the evidence says a feature was "not detected",
phrase it carefully, for example:
"I noticed that I couldn't identify..."

Return exactly:

SUBJECT: <subject>

BODY:
<body>
"""

    return ask_ai(prompt)
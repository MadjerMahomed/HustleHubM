from lead_agent import analyze_business, generate_outreach


business = {
    "business_name": "The Dentists Inc.",
    "location": "Johannesburg South",
    "website": "https://thedentistsinc.co.za/",
    "search_evidence": (
        "Two-branch dental practice in Johannesburg South — "
        "Ridgeway & Glenanda. Cosmetic, orthodontic, Invisalign "
        "and family dentistry with a genuine, personal touch."
    )
}


print("\n==============================")
print("ANALYZING REAL BUSINESS")
print("==============================")

analysis = analyze_business(business)

print("\nLEAD ANALYSIS:")
print(analysis)


print("\n==============================")
print("GENERATING OUTREACH")
print("==============================")

outreach = generate_outreach(
    business,
    analysis
)

print("\nOUTREACH:")
print(outreach)
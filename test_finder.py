from lead_finder import find_leads

leads = find_leads(
    niche="dentists",
    location="Johannesburg",
    max_results=5
)

for lead in leads:
    print("\n--------------------")
    print("Business:", lead["business_name"])
    print("Location:", lead["location"])
    print("Website:", lead["website"])
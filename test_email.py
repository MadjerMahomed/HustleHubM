from website_analyzer import analyze_website


website = "https://thedentistsinc.co.za/"


result = analyze_website(
    website
)


print("\n==============================")
print("PUBLIC BUSINESS EMAIL TEST")
print("==============================")


print(
    "Website:",
    result["url"]
)

print(
    "Reachable:",
    result["reachable"]
)

print(
    "Business email:",
    result["business_email"]
)

print(
    "Has email:",
    result["has_email"]
)
def generate_email(lead):
    business = lead["business_name"]
    opportunity = lead["opportunity"]

    subject = f"Quick idea for {business}"

    body = f"""Hi,

I came across {business} and noticed something that may be worth looking at.

I noticed: {opportunity}.

I work with businesses to improve their online presence and generate more potential customers.

I had a couple of ideas that could potentially help {business}.

Would you be open to a quick chat?

Regards,
HustleHubM
"""

    return subject, body
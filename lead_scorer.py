def score_lead(
    has_website=True,
    website_outdated=False,
    has_booking=False,
    weak_call_to_action=False,
    weak_social_presence=False,
    public_email=False
):
    score = 0
    opportunities = []

    if not has_website:
        score += 30
        opportunities.append("No website")

    if website_outdated:
        score += 20
        opportunities.append("Website may need improvement")

    if not has_booking:
        score += 15
        opportunities.append("No obvious online booking")

    if weak_call_to_action:
        score += 15
        opportunities.append("Weak call-to-action")

    if weak_social_presence:
        score += 10
        opportunities.append("Weak social presence")

    if public_email:
        score += 10

    return min(score, 100), ", ".join(opportunities)
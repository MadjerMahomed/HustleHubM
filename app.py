from flask import Flask, render_template, request, redirect

from database import init_db, add_lead, get_leads
from lead_scorer import score_lead
from email_generator import generate_email


app = Flask(__name__)

init_db()


@app.route("/")
def index():
    leads = get_leads()

    return render_template(
        "index.html",
        leads=leads
    )


@app.route("/add-lead", methods=["POST"])
def create_lead():

    business_name = request.form.get("business_name")
    website = request.form.get("website")
    email = request.form.get("email")
    industry = request.form.get("industry")
    location = request.form.get("location")

    website_outdated = request.form.get("website_outdated") == "on"
    has_booking = request.form.get("has_booking") == "on"
    weak_cta = request.form.get("weak_cta") == "on"
    weak_social = request.form.get("weak_social") == "on"

    score, opportunity = score_lead(
        has_website=bool(website),
        website_outdated=website_outdated,
        has_booking=has_booking,
        weak_call_to_action=weak_cta,
        weak_social_presence=weak_social,
        public_email=bool(email)
    )

    add_lead(
        business_name=business_name,
        website=website,
        email=email,
        industry=industry,
        location=location,
        lead_score=score,
        opportunity=opportunity
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
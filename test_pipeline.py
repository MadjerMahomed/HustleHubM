from lead_pipeline import run_pipeline


leads = run_pipeline(
    niche="dentists",
    location="Johannesburg",
    max_leads=5,
    minimum_score=60
)
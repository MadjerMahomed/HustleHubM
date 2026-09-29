import sqlite3

DATABASE = "leads.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            website TEXT,
            email TEXT,
            industry TEXT,
            location TEXT,
            lead_score INTEGER DEFAULT 0,
            opportunity TEXT,
            status TEXT DEFAULT 'New',
            email_subject TEXT,
            email_body TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_lead(
    business_name,
    website="",
    email="",
    industry="",
    location="",
    lead_score=0,
    opportunity=""
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO leads
        (
            business_name,
            website,
            email,
            industry,
            location,
            lead_score,
            opportunity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        business_name,
        website,
        email,
        industry,
        location,
        lead_score,
        opportunity
    ))

    conn.commit()
    conn.close()


def get_leads():
    conn = get_connection()

    leads = conn.execute("""
        SELECT *
        FROM leads
        ORDER BY lead_score DESC
    """).fetchall()

    conn.close()

    return leads
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "heard.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audience TEXT,
            policy_type TEXT,
            policy_text TEXT,
            summary TEXT,
            affected TEXT,
            both_sides TEXT,
            questions TEXT,
            script TEXT,
            email TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def generate_analysis(policy_text, audience, policy_type):
    text_lower = policy_text.lower()

    impact = "medium"
    if any(word in text_lower for word in ["deny", "required", "appeal", "deadline", "priority", "must"]):
        impact = "high"

    summary = f"""
This {policy_type.lower()} may affect {audience.lower()} by changing how they access services, spaces, resources, or decision-making.

In plain English, the key issue is not just the rule itself. The issue is whether people can understand it, respond to it, and participate before decisions are made.

Estimated impact level: {impact.upper()}.
"""

    affected = f"""
• {audience}
• People who may not understand formal policy language
• People who miss deadlines or do not know the process
• Smaller groups with less administrative experience
• Community members who need clearer communication or accessibility support
"""

    both_sides = f"""
Supporters may argue:
• This creates a clearer process
• It helps administrators make consistent decisions
• It reduces confusion by setting rules in advance

Critics may argue:
• The language may still be difficult to understand
• People with less time or experience may be left out
• It may favor groups that already know how the system works
• It needs a clearer feedback or appeal process
"""

    questions = """
1. Who is most affected by this rule?
2. Who was consulted before this decision?
3. What happens if someone misses the deadline or does not understand the process?
4. Is there an appeal process?
5. Will there be a plain-language version?
6. How will affected people give feedback?
7. How will success or harm be measured?
"""

    script = f"""
Hello, my name is [Name]. I am speaking as someone concerned about how this {policy_type.lower()} affects {audience.lower()}.

I understand that rules can help create structure, but people cannot participate fairly if the language is confusing or if the impact is not explained clearly.

Before this moves forward, I would like to ask for a plain-language summary, a clear explanation of who is affected, and a simple way for people to give feedback or appeal decisions.

Good policy should not only exist. It should be understandable.
"""

    email = f"""
Subject: Request for clearer explanation and public feedback

Hello,

I am writing about the recent {policy_type.lower()}.

Before this moves forward, I would like to request a plain-language explanation of what is changing, who will be affected, and how people can share feedback or ask questions.

Many people may care about this issue but may not have the time or background to understand formal policy language. A short public summary, impact explanation, and feedback process would make this decision more accessible and fair.

Thank you,
[Your Name]
"""

    return summary, affected, both_sides, questions, script, email


@app.route("/", methods=["GET", "POST"])
def index():
    init_db()

    if request.method == "POST":
        audience = request.form["audience"]
        policy_type = request.form["policy_type"]
        policy_text = request.form["policy_text"]

        summary, affected, both_sides, questions, script, email = generate_analysis(
            policy_text, audience, policy_type
        )

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO analyses (
                audience, policy_type, policy_text, summary, affected,
                both_sides, questions, script, email, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            audience, policy_type, policy_text, summary, affected,
            both_sides, questions, script, email,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        analysis_id = cur.lastrowid
        conn.close()

        return redirect(f"/result/{analysis_id}")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT 5")
    saved = cur.fetchall()
    conn.close()

    return render_template("index.html", saved=saved)


@app.route("/result/<int:analysis_id>")
def result(analysis_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,))
    analysis = cur.fetchone()
    conn.close()

    if analysis is None:
        return "Analysis not found", 404

    return render_template("result.html", analysis=analysis)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
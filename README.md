# Heard
### Turn confusing policy into public participation.

**Anthropic × Maryland Hackathon 2026 — Track 3: Governance & Accessibility**

---

## The problem

Most people don't avoid civic participation because they don't care.
They avoid it because policy language is confusing, the process feels closed off, and they don't know what to say.

Heard fixes that.

---

## What it does

Paste any policy, university rule, lease clause, or city proposal.
Heard gives you:

- **Plain English summary** — what it actually means
- **Who is affected** — which groups and why
- **Both sides** — what supporters and critics argue
- **Questions to ask** — before accepting the policy
- **Public comment script** — ready to read at a meeting
- **Email draft** — ready to send to a decision-maker
- **Saved history** — every analysis stored in a database so groups can track policies over time

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Jinja2 templates |
| Backend | Python, Flask |
| Database | SQLite |

---

## How to run locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
# http://127.0.0.1:5000
```

---

## How we used AI

The analysis engine is built on a structured rule-based system that detects policy keywords and generates civic participation outputs. The architecture is designed to plug directly into an LLM (Claude API) as the next step — the prompt structure, output format, and database schema are all ready for it. We built the full-stack workflow first to prove the concept works end to end.

---

## What could go wrong

- Template outputs are general by nature — the LLM layer makes them specific
- No user authentication — in production, analyses would be tied to accounts
- SQLite is single-file — would move to PostgreSQL at scale

---

## What we'd build next

- Connect Claude API for real, policy-specific AI analysis
- Add shareable links so communities can share analyses
- Multilingual support for non-English speakers
- Integration with local government meeting calendars

---

## Built by

University of Maryland — Anthropic × Maryland Hackathon 2026

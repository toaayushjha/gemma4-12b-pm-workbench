# Claude Opus 4.8 — baseline answers to the 7 hero prompts

**Methodology:** these are reference answers from Claude Opus 4.8 (the cloud model a
PM would normally reach for) to the *same* hero prompts run against local Gemma 4 12B.
They were produced by Claude Opus 4.8. For the audio/video prompts, Opus was given the
same instruction; in the Claude app you'd upload the clip directly. Paired side-by-side
with Gemma's outputs (and scored) in [`gemma_vs_opus.md`](gemma_vs_opus.md).

---

## dw1 — Stakeholder update email

**Subject: Weekly Product Update — activation win, incident closed, EU migration at risk**

Hi all,

A strong week with one risk to flag.

**Shipped**
- CSV export (beta) is live with 12 design partners — early feedback is positive.
- Onboarding A/B test: variant B drove **+9% activation**; rolling to 100%.

**Resolved**
- Tuesday's API rate-limit incident (40 min) is root-caused and the fix is deployed.

**Risk**
- The EU-tenant data migration is slipping **~1 week**, gated on legal's DPA sign-off
  (in review 10 days). This could affect the QBR timeline.

**Hiring:** backend role still open; two onsites this week.

**My ask:** can someone help me escalate the DPA review with legal this week? That's
the single thing standing between us and an on-time EU migration.

Thanks,
[PM]

---

## or1 — Goal → plan → JSON tasks → risks (self-serve free trial, 6 weeks)

**Phased plan**
- **Wk 1** — Lock scope; define "activation"; kick off legal review of no-card terms; design starts.
- **Wk 2–3** — Build trial state machine + auto-provisioning; finalize nudge + expiry designs.
- **Wk 3–4** — Stripe self-serve checkout; sales routing + CRM lead emit.
- **Wk 4–5** — Instrumentation; guided setup wizard; QA.
- **Wk 5–6** — Beta to ~50 prospects; fix; GA.

**Work items**
```json
[
  {"id": "T1", "title": "Define activation metric + event spec", "owner_role": "PM", "week": 1, "depends_on": []},
  {"id": "T2", "title": "Kick off legal review of no-card terms", "owner_role": "PM", "week": 1, "depends_on": []},
  {"id": "T3", "title": "Trial state machine (active→grace→soft_lock→delete)", "owner_role": "Backend", "week": 2, "depends_on": ["T1"]},
  {"id": "T4", "title": "Auto-provision trial workspace", "owner_role": "Backend", "week": 2, "depends_on": []},
  {"id": "T5", "title": "Nudge + expiry screen designs", "owner_role": "Design", "week": 3, "depends_on": []},
  {"id": "T6", "title": "Stripe self-serve checkout + webhooks", "owner_role": "Backend", "week": 4, "depends_on": ["T3"]},
  {"id": "T7", "title": "Sales routing + CRM lead emit", "owner_role": "Full-stack", "week": 4, "depends_on": ["T4"]},
  {"id": "T8", "title": "Funnel instrumentation", "owner_role": "Data", "week": 5, "depends_on": ["T1"]},
  {"id": "T9", "title": "Guided setup wizard", "owner_role": "Frontend", "week": 5, "depends_on": ["T4"]},
  {"id": "T10", "title": "Beta + GA", "owner_role": "PM", "week": 6, "depends_on": ["T6","T7","T8","T9"]}
]
```

**Risks**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Legal sign-off on no-card terms slips | Med | High | Start Wk 1; escalate early; have card-required fallback |
| Low trial activation | Med | High | Guided wizard + templates; instrument time-to-first-value |
| Cannibalizes enterprise deals | Low | Med | Route >100-seat accounts to sales; cap self-serve at Pro |
| Billing edge case (pay-at-expiry) | Med | Med | Grace state + idempotent webhooks |

---

## lc1 — Python: parse CSV + chart

```python
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Aggregate revenue (units * unit_price) per product
revenue = defaultdict(float)
with open("sample_sales.csv", newline="") as f:
    for row in csv.DictReader(f):
        revenue[row["product"]] += int(row["units"]) * float(row["unit_price"])

# Top 3 by total revenue
top3 = sorted(revenue.items(), key=lambda kv: kv[1], reverse=True)[:3]
print("Top 3 products by revenue:")
for name, total in top3:
    print(f"  {name}: ${total:,.2f}")

# Bar chart of revenue by product
products = list(revenue)
totals = [revenue[p] for p in products]
plt.figure(figsize=(8, 5))
plt.bar(products, totals)
plt.ylabel("Revenue (USD)")
plt.title("Revenue by Product")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("revenue.png", dpi=120)
print("Saved chart to revenue.png")
```

_(Expected top 3 from the sample data: Pro Plan ≈ $9,603, Enterprise ≈ $4,491,
Starter ≈ $5,742 — note Starter edges Enterprise; the script computes exact values.)_

---

## sum1 — Summarize the PRD

**TL;DR.** This PRD specifies a self-serve, no-credit-card 14-day free trial for Acme
Cloud to open a scalable, low-touch acquisition channel for small teams while
protecting the enterprise sales motion. Prospects go from website to a working
workspace in under 3 minutes, are nudged to upgrade on days 7 and 12, and convert
in-product via Stripe; at expiry the workspace soft-locks to read-only. Success is
measured by self-serve paid conversions, with an 8% trial→paid target by launch+90
days. The main open risk is legal sign-off on the no-card terms.

**Key decisions** (Appendix Decisions Log): 14-day trial, no card (D1); soft-lock to
read-only at expiry (D2); self-serve capped at Pro, Enterprise routes to sales (D3);
localization is a fast-follow (D4).

**Open risks / questions:** legal review of no-card terms is the long pole (R4);
activation definition still undefined (OQ3, blocks instrumentation); abuse/free-tier
farming (R3); pay-at-expiry billing race (R5); nudge re-show behavior (OQ2); trial
extensions undecided (OQ4).

**What's missing:** no explicit win-back/re-engagement plan for the 30-day read-only
window before deletion, and no pricing-page strategy (it's deferred but conversion
depends on it).

---

## vi1 — Read dashboard screenshot → KPIs

**KPIs (May 2026):** MRR $128.4K (+6.2%), Active Users 4,820 (+3.1%), Activation Rate
41% (**−2.0%**), Monthly Churn 3.8% (**+0.5%**), NPS 47 (+4), Trial→Paid 7.9% (+0.3%).
New signups by week: 210, 245, 198, 312.

**Most concerning:** Activation Rate at **41%, down 2.0%** — paired with churn ticking
**up** to 3.8%. Growth (MRR, signups, trial→paid) is healthy, but if a smaller share of
users activate *and* churn is rising, the top-of-funnel gains will leak out over time.

**Recommended action:** prioritize an activation deep-dive — segment the −2.0% by
cohort/source to find where new users stall in onboarding, and tie it to the rising
churn. (The Wk-3 signup dip to 198 before the Wk-4 jump to 312 is also worth a quick
check for a tracking or campaign anomaly.)

---

## au1 — Voice memo → summary + actions

**Transcript:** "Hey team, quick voice memo after the BrightWave call. They're happy
with the billing fix, but they want CSV export for invoices by the end of the month.
Priya, can you scope that this week? Also, let's add invoice-page latency to our
monitoring so we catch this earlier next time. I'll update the roadmap doc. Thanks."

**Summary.** After a positive BrightWave call, the customer has one new ask — invoice
CSV export by month-end — and the team wants better monitoring to catch billing issues
earlier.

**Action items.**
- **Priya** — scope invoice CSV export this week.
- **Eng** — add invoice-page latency to monitoring.
- **[Speaker]** — update the roadmap doc.

---

## vd1 — Summarize screen-demo video

**Step by step.** (1) Title slide — "Acme Cloud, Product Demo, May 2026." (2)
"Dashboard" — view your KPIs at a glance. (3) "Create Automation" — start from a
template. (4) "Invite Your Team" — collaborate in a shared workspace. (5) "Upgrade
In-Product" — self-serve checkout with Stripe.

**Release-notes summary.** This demo walks through Acme Cloud's core loop: see your
KPIs on the dashboard, build an automation from a template, invite your team, and
upgrade in-product when you're ready. A concise tour of dashboard, automation,
collaboration, and self-serve billing.

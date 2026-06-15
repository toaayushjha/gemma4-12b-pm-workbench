# 3-way text benchmark: Gemma 4 12B vs Qwen3-Coder 30B vs Qwen3-Coder-Next

_14 text tasks. Gemma 4 12B & Qwen3-Coder 30B via Ollama; **Qwen3-Coder-Next (MLX) via LM Studio**. Quality of the first two is in [`compare_gemma4-12b_vs_qwen3-coder-30b.md`](compare_gemma4-12b_vs_qwen3-coder-30b.md)._

## Verdict — is the 80B worth it on a 64 GB Mac?

**No, not for this workload.** Qwen3-Coder-Next (80B-A3B) is **not faster** than the 30B
(≈63 vs 110 tok/s — it's the bigger model), needs **~2.5× the RAM** (44.9 GB, and it trips
LM Studio's guardrail on 64 GB), and its quality edge is marginal *and* inconsistent: it
wrote the best regex (anchored, non-capturing group) and SQL (`FILTER`) and showed sharper
RICE judgment (flagged the dark-mode "high score, low impact" trap) — but it **skipped 2 of
3 parts of the multi-part orchestration task (or1)** and **leaked a Chinese token into JSON**
(`"trial期限"`). **Qwen3-Coder 30B (MoE) remains the sweet spot** for local text/code.

## Speed summary

| Model | Runtime | Avg latency | Avg tok/s |
|---|---|--:|--:|
| Gemma 4 12B | Ollama | 28.3s | 46 |
| Qwen3-Coder 30B (MoE) | Ollama | 6.0s | 110 |
| **Qwen3-Coder-Next (MLX)** | LM Studio | **4.9s** | **63** |

## Per-task latency (s) / tok-s

| Task | Gemma 12B | Qwen 30B | Qwen-Next |
|---|--:|--:|--:|
| dw1 Stakeholder update email | 21.15s / 46.5 | 10.6s / 115.6 | 3.02s / 58.9 |
| dw2 Messy notes -> action items table | 42.1s / 45.6 | 5.76s / 108.0 | 7.46s / 71.6 |
| dw3 Rewrite blunt Slack msg for execs | 23.48s / 46.5 | 3.28s / 113.0 | 1.39s / 66.2 |
| dw4 RICE prioritization | 42.88s / 45.9 | 5.76s / 109.6 | 9.32s / 75.2 |
| or1 Goal -> plan -> JSON tasks -> risks | 33.66s / 46.3 | 11.76s / 108.1 | 6.61s / 71.6 |
| or2 Strict JSON extraction (schema) | 14.58s / 46.3 | 3.53s / 110.5 | 1.21s / 57.9 |
| or3 Tool-routing decision (agentic) | 20.34s / 45.8 | 4.37s / 111.5 | 2.42s / 67.4 |
| lc1 Python: parse CSV + chart | 38.99s / 45.2 | 6.53s / 108.5 | 7.98s / 67.2 |
| lc2 SQL from schema | 34.14s / 45.3 | 4.28s / 109.9 | 2.94s / 61.9 |
| lc3 Explain + refactor snippet | 21.87s / 45.8 | 4.15s / 109.8 | 2.49s / 60.2 |
| lc4 Regex + test cases | 22.95s / 46.9 | 5.38s / 109.3 | 6.19s / 65.6 |
| sum1 Summarize long PRD (256K ctx) | 40.43s / 44.1 | 8.77s / 99.7 | 11.37s / 53.2 |
| sum2 Condense support thread | 19.01s / 46.1 | 4.23s / 117.0 | 2.55s / 49.8 |
| sum3 Extract decisions from transcript | 21.29s / 43.8 | 6.01s / 106.9 | 4.25s / 61.4 |

---

## Qwen3-Coder-Next — full outputs (judge quality)

### dw1 — Stakeholder update email
_(3.02s, 58.9 tok/s)_

**Subject:** Weekly Update: CSV Export Live, Onboarding Win, API Fix + EU Migration Risk  

Hi team,  

**✅ Shipped:** CSV export (beta) to 12 design partners—early feedback positive.  
**📈 Onboarding:** Variant B A/B test shows +9% activation; rolling to 100% this week.  
**🔧 Fixed:** API rate-limit incident (40 min downtime, Tue)—root-caused & patched.  
**🔍 Hiring:** Backend role open; 2 onsites this week.  
**⚠️ Risk:** EU tenant data migration now ~1 week behind (vendor dependency).  

We’ll monitor migration closely and share a recovery plan by Thursday.  

*Ask:* Can stakeholders flag any high-priority EU tenant concerns by EOD Thursday? Helps us prioritize mitigation.  

Best,  
[Your Name]

---

### dw2 — Messy notes -> action items table
_(7.46s, 71.6 tok/s)_

Here's a cleaned-up action-items table based on the meeting notes, with inferred owners and priorities (using standard definitions: **High** = time-sensitive, high business impact; **Medium** = important but not urgent; **Low** = nice-to-have or low impact). Ambiguous items are flagged with notes.

| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Finalize CSV export spec & get engineering estimate | Priya | Fri (inferred from “maybe by Fri”) | High |
| Complete onboarding copy review | Marco | End of week (inferred from “this week”) | Medium |
| Call BrightWave to resolve 500 errors & prevent churn (renewal Nov) | *Owner unclear* — suggest escalating to Sales Lead or Support Lead | Before Oct 15 (pre-renewal window) | High |
| Chase Legal for DPA sign-off to unblock EU data migration | *Owner unclear* — suggest Legal Ops or Program Manager (e.g., Tara?) | Within 2 business days | High |
| Roll out pricing variant B to 100% (activation +9%) | Automated / Product Ops (no owner needed) | Immediate | High |
| Draft board update on EU migration slip | Tara (but she’s PTO until Mon) | Wed, Oct 18 (pre-QBR) | Medium |
| Fix analytics DAU numbers before exec review on Oct 20 | Eng (inferred — “eng aware”) | Oct 19 | High |
| (No action) — Dark mode deferred; mobile nav redesign deferred to next sync | — | — | N/A |

---

### Notes on Ambiguity / Inference:
- **Export spec owner**: Priya was assigned the task (“she can have a spec by fri?”) — assumed owner despite lateness.
- **Support escalation (BrightWave)**: Owner unclear — inferred *Sales Lead* or *Support Lead*, not Priya (she was “maybe” called out, but Sales owns relationship risk.
- **Legal DPA chase**: Owner unclear — assigned to *Legal Ops or Program Manager* (Tara is a candidate, but she’s PTO).
- **Board draft**: Tara is the logical owner given context, but due date assumes she’ll complete it upon return.
- **Analytics fix**: Downgraded from “low priority” in notes to *High* — explicitly needed before Oct 20 exec review.
- **No action items** for mobile nav, kitchen machine, or dark mode (parked/deferred).

---

### dw3 — Rewrite blunt Slack msg for execs
_(1.39s, 66.2 tok/s)_

Hi [VP Name],  

wanted to flag that today’s launch didn’t go out as planned—the dashboard isn’t functioning, and sales wasn’t notified in advance. This is the third instance we’ve seen, so I wanted to proactively discuss how we can strengthen our pre-launch checks and cross-team communication to ensure it doesn’t happen again. Happy to help draft a solution or facilitate a quick sync if helpful.  

Best,  
[Your Name]

---

### dw4 — RICE prioritization
_(9.32s, 75.2 tok/s)_

Here's a RICE prioritization for the 5 features, based on typical SaaS B2B product assumptions (e.g., ~10K MAU, mid-market customers, 6-month planning horizon). Scores are on a 1–10 scale unless otherwise noted.

| Feature                 | Reach (R) | Impact (I) | Confidence (C) | Effort (E) | RICE Score (R × I × C / E) |
|-------------------------|-----------|------------|----------------|------------|----------------------------|
| **SSO/SAML login**      | 8         | 9          | 9              | 7          | (8×9×9)/7 = **92.6**       |
| **Audit log export**    | 6         | 8          | 8              | 5          | (6×8×8)/5 = **76.8**       |
| **Bulk CSV import**     | 7         | 7          | 8              | 6          | (7×7×8)/6 = **65.3**       |
| **Dark mode**           | 9         | 4          | 9              | 3          | (9×4×9)/3 = **108.0**      |
| **In-app notifications**| 9         | 6          | 7              | 5          | (9×6×7)/5 = **75.6**       |

🔍 **Assumptions & Justification for Scores**:
- **Reach**: % of MAU affected in next 6 months. Dark mode & notifications reach ~90% of users; SSO/audit/csv affect subsets (e.g., enterprise, admins).
- **Impact**: 1–10 scale: *1 = minor improvement*, *5 = meaningful*, *9 = critical for retention/upsell*. SSO & audit logs hit high-security/compliance needs (9 & 8).
- **Confidence**: Our conviction in estimates, based on user research/data. Dark mode & notifications have high confidence from UX surveys; SSO/audit rely on sales/team feedback.
- **Effort**: Relative story points (e.g., 1 = trivial, 10 = major infrastructure). Dark mode is low-effort (CSS/theme); SSO requires identity provider integrations.

⚠️ **Note on Dark Mode**: Despite high RICE (108), *Impact is low* (4). It’s a nice-to-have for UX but rarely drives adoption or retention—unless your users are designers/devs (then bump Impact to 7+). In most B2B contexts, it’s low-value.

---

✅ **Top 2 Recommendations**  
1. **SSO/SAML login**  
   *Highest business impact: essential for enterprise sales, reduces churn, and enables compliance.*  

2. **Audit log export**  
   *Critical for security/compliance (e.g., SOC 2), high-impact for admins and legal teams with reasonable effort.*  

💡 **Bonus insight**: Dark mode ranks highest numerically but *should not be prioritized*—it’s a “hygiene” feature unless your product is design-heavy. Move it to backlog or phase 2 after core trust/scale features (like SSO & audit) are in place.

---

### or1 — Goal -> plan -> JSON tasks -> risks
_(6.61s, 71.6 tok/s)_

```json
[
  {"id": "1", "title": "Define free trial scope & success metrics", "owner_role": "Product Manager", "week": 1, "depends_on": []},
  {"id": "2", "title": "Design trial user journey & eligibility rules", "owner_role": "Product Manager", "week": 1, "depends_on": ["1"]},
  {"id": "3", "title": "Build trial onboarding flow (sign-up → activation)", "owner_role": "Backend Engineer", "week": 2, "depends_on": ["2"]},
  {"id": "4", "title": "Implement trial期限 & expiration logic", "owner_role": "Backend Engineer", "week": 3, "depends_on": ["3"]},
  {"id": "5", "title": "Create trial dashboard & usage analytics", "owner_role": "Frontend Engineer", "week": 3, "depends_on": ["4"]},
  {"id": "6", "title": "Build conversion funnel (trial → paid)", "owner_role": "Frontend Engineer", "week": 4, "depends_on": ["5"]},
  {"id": "7", "title": "Draft trial messaging & landing page content", "owner_role": "Marketing Manager", "week": 4, "depends_on": ["2"]},
  {"id": "8", "title": "Set up analytics & tracking (GA4, Mixpanel)", "owner_role": "Data Engineer", "week": 5, "depends_on": ["6"]},
  {"id": "9", "title": "Conduct internal QA & UAT with sales team", "owner_role": "QA Lead", "week": 5, "depends_on": ["8"]},
  {"id": "10", "title": "Soft launch to pilot customers (10–20 users)", "owner_role": "Customer Success Manager", "week": 6, "depends_on": ["9"]},
  {"id": "11", "title": "Full public launch + marketing campaign", "owner_role": "Marketing Manager", "week": 6, "depends_on": ["10"]}
]
```

---

### or2 — Strict JSON extraction (schema)
_(1.21s, 57.9 tok/s)_

{
  "company": "Brightwave Health",
  "contact": {
    "name": "Dana Okafor",
    "email": "dana.okafor@brightwave.example"
  },
  "plan": "pro",
  "seats": 45,
  "renewal_month": "November"
}

---

### or3 — Tool-routing decision (agentic)
_(2.42s, 67.4 tok/s)_

[{"tool": "create_ticket", "args": {"title": "Billing page returns 500 error for enterprise customers since this morning", "severity": "high"}}, {"tool": "send_email", "args": {"to": "finance-team@company.com", "subject": "Urgent: Billing Page Outage for Enterprise Customers", "body": "The billing page has been returning 500 errors for all enterprise customers since this morning. A high-severity ticket has been created (see internal ticketing system) and engineering is investigating."}}]

I first create a high-severity ticket to log the incident and assign visibility internally, then send an email to finance to inform them of the outage—this order ensures documentation precedes external communication and allows for coordinated response.

---

### lc1 — Python: parse CSV + chart
_(7.98s, 67.2 tok/s)_

```python
#!/usr/bin/env python3
"""
Read sales data from a CSV file, calculate total revenue per product,
print the top 3 products by revenue, and save a bar chart to 'revenue.png'.
"""

import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Define the input CSV filename
INPUT_FILE = 'sample_sales.csv'

def main():
    # Dictionary to store total revenue per product
    revenue_by_product = defaultdict(float)
    
    # Read the CSV file and calculate revenue per product
    with open(INPUT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row['product']
            units = int(row['units'])
            unit_price = float(row['unit_price'])
            revenue_by_product[product] += units * unit_price
    
    # Sort products by total revenue (descending) and get top 3
    sorted_products = sorted(revenue_by_product.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_products[:3]
    
    # Print the top 3 products
    print("Top 3 products by total revenue:")
    for i, (product, revenue) in enumerate(top_3, 1):
        print(f"{i}. {product}: ${revenue:.2f}")
    
    # Prepare data for the bar chart
    products = [p[0] for p in sorted_products]
    revenues = [p[1] for p in sorted_products]
    
    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(products, revenues)
    
    # Add revenue labels on top of each bar
    for bar, revenue in zip(bars, revenues):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'${revenue:.0f}', ha='center', va='bottom')
    
    # Add title and axis labels
    plt.title('Revenue by Product', fontsize=14)
    plt.ylabel('Total Revenue ($)', fontsize=12)
    
    # Rotate x-axis labels for better readability if needed
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the figure as 'revenue.png'
    plt.savefig('revenue.png', dpi=100)
    
    # Close the figure to free memory
    plt.close()

if __name__ == "__main__":
    main()
```

---

### lc2 — SQL from schema
_(2.94s, 61.9 tok/s)_

```sql
SELECT 
    u.plan,
    COUNT(DISTINCT u.id) FILTER (WHERE e.ts <= u.signup_date + INTERVAL '7 days') * 100.0 / COUNT(DISTINCT u.id) AS activation_rate_7d
FROM users u
LEFT JOIN events e 
    ON u.id = e.user_id 
    AND e.name = 'activated'
GROUP BY u.plan;
```

This query joins users with their first (or any) 'activated' event, but only counts events that occurred within 7 days of the user’s signup date—using a `LEFT JOIN` ensures users without such events are still included (with NULL `e.ts`). The aggregate `COUNT(DISTINCT u.id) FILTER (...)` computes the number of activated users per plan, divided by total users per plan and multiplied by 100 to get the percentage.

---

### lc3 — Explain + refactor snippet
_(2.49s, 60.2 tok/s)_

This function removes duplicate items from a list while preserving the original order of first occurrences. It does so by building a new list `r` and only adding items that aren’t already in `r`.

**Bug/Risk**: The function is inefficient (O(n²) time) because `l[i] not in r` performs a linear search for each element, making it very slow on large lists.

**Cleaner refactor** (Python 3.7+):
```python
def f(l):
    return list(dict.fromkeys(l))
```
This leverages the fact that `dict.fromkeys` preserves insertion order and automatically deduplicates keys, then converts back to a list—fast (O(n)), concise, and idiomatic.

---

### lc4 — Regex + test cases
_(6.19s, 65.6 tok/s)_

### Regular Expression

```regex
^ORD-\d{8}(?:-R)?$
```

**Explanation:**
- `^` – Start of string
- `ORD-` – Literal "ORD-"
- `\d{8}` – Exactly 8 digits
- `(?:-R)?` – Optional non-capturing group for "-R" (`?` makes it optional)
- `$` – End of string

---

### Examples

| **Status**         | **Order ID**      | **Reason** |
|--------------------|-------------------|------------|
| ✅ Should match    | `ORD-12345678`    | Valid format: ORD- + 8 digits |
| ✅ Should match    | `ORD-00000001`    | Leading zeros allowed; 8 digits total |
| ✅ Should match    | `ORD-99999999-R`  | Valid with `-R` suffix |
| ✅ Should match    | `ORD-12345678-R`  | Standard return ID |
| ❌ Should not match| `ORD-1234567`     | Only 7 digits |
| ❌ Should not match| `ORD-123456789`   | 9 digits |
| ❌ Should not match| `ORD-12345678r`   | Lowercase `-r`; case-sensitive |
| ❌ Should not match| `ORD-12345678--R` | Double hyphen before R |

> ✅ Case-sensitive: Use `i` flag only if case-insensitivity is required (e.g., `/^ORD-\d{8}(?:-R)?$/i`).  
> 🔒 Anchors (`^`, `$`) ensure the *entire* string matches (not just a substring).

---

### sum1 — Summarize long PRD (256K ctx)
_(11.37s, 53.2 tok/s)_

**TL;DR (4 sentences):**  
This PRD proposes a self-serve, no-credit-card free trial for Acme Cloud to capture the underserved small-team market and improve CAC efficiency, targeting a 3-minute path from sign-up to working product. The trial lasts 14 days, with in-product conversion via Stripe for Starter/Pro plans, while enterprise accounts are routed to sales based on company size or domain. Key UX includes persistent trial countdown, day-7/day-12 upgrade nudges, and a soft-locked read-only state post-expiry. Launch success hinges on achieving ≥8% trial-to-paid conversion and <2% abuse, with guardrails against cannibalization of sales-assisted deals.

**Key Decisions:**  
- **D1 (Sec 13):** Fixed trial length at 14 days with no credit card required.  
- **D2 (Sec 13):** Chose *soft-lock* (read-only, 30-day retention) over hard-lock at expiry to preserve user data and motivate reactivation.  
- **D3 (Sec 13):** Self-serve capped at Pro plan; Enterprise route reserved exclusively for sales (via FR14 routing logic).  
- **D4 (Sec 13):** Localization deferred to fast-follow, not launch-blocking (addressing OQ1).  

**Open Risks/Questions:**  
- **OQ2 (Sec 11):** Unclear whether day-7 nudge should be *permanently dismissible* or re-show on day 12—impacts UX friction and conversion lift.  
- **OQ3 (Sec 11):** No agreed-upon definition of *activation* for instrumentation, despite being a North Star–adjacent metric (D1.5 in Sec 9); PM needs to own this pre-implementation.  
- **R4 (Sec 10):** Legal review pending for no-card terms and auto-deletion—exposure if trials expire without clear notice or export paths (especially GDPR).  
- **OQ4 (Sec 11):** Trial extension policy undefined—self-serve? sales-granted? could impact conversion urgency and billing edge cases.  

**What’s Missing:**  
The PRD lacks a **concrete definition and targets for the *activation* metric** (Sec 9). While Sec 5 lists user stories (e.g., “reach value quickly”), and FR6/FR7 imply activation via time-to-first-automation, the PRD does not specify *what constitutes activation* (e.g., “complete guided wizard,” “run ≥1 automation,” “invite ≥1 teammate”) or define success thresholds (e.g., “≥50% day-1 activation”). Without this, instrumentation design (Sec 9), cohort analysis, and experiment interpretation lack rigor—risking flawed optimization decisions.

---

### sum2 — Condense support thread
_(2.55s, 49.8 tok/s)_

**Current status:** Billing page is fully restored after hotfix deployment (index added); manual May export was provided as stopgap.  
**Root cause:** Missing index on `invoices.account_id` causing slow full-table scans for accounts with >500 invoices (BrightWave has ~1,900).  
**Next step + owner:** Add monitoring on invoice-page latency and conduct post-incident review (PIR); follow-up tasks to add backfill checks and CI perf tests owned by Maya (PM).  
**Customer sentiment:** Positive — praised quick resolution and manual export, confirmed page is now fast and functional.

---

### sum3 — Extract decisions from transcript
_(4.25s, 61.4 tok/s)_

### Decisions Made  
- **14-day free trial with no credit card required at sign-up**  
- **Upgrade nudges to be added on day 7 and day 12 of the trial**  
- **Soft-lock (read-only) paywall at trial expiry** (to retain data visibility and support win-back efforts)  
- **Localization of trial emails for EU is deferred to a fast-follow release**, not launch-blocking  

### Action Items  
- **Tom (Eng)** → Scope trial state machine and paywall implementation; deliver estimates by Friday  
- **Priya (Design)** → Deliver lo-fi mocks for upgrade nudges and expiry screen by Wednesday; final designs by next Tuesday  
- **Maya (PM)** → Define activation criteria and write the event specification for analytics by Thursday  
- **Maya (PM)** → Initiate legal review of no-card terms today  

### Parking-Lot / Deferred Items  
- **Pricing-page changes** — held for a separate workstream (no owner or timeline assigned)  
- **EU localization of trial emails** — deferred to fast-follow; Maya will confirm timing with marketing  
- **Legal review of no-card terms** — acknowledged as a potential long pole; not yet scheduled (Maya owns follow-up)

---

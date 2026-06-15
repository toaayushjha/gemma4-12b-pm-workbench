# Head-to-head: `gemma4:12b` vs `qwen3-coder:30b` (text tasks)

_14 text tasks · multimodal tasks skipped (coder models can't see images/audio)._

## Speed summary

| Model | Avg latency | Avg tok/s |
|---|--:|--:|
| `gemma4:12b` | 28.3s | 46 |
| `qwen3-coder:30b` | 6.0s | 110 |

## Per-task

| Task | `gemma4:12b` lat / tok-s | `qwen3-coder:30b` lat / tok-s |
|---|--:|--:|
| dw1 Stakeholder update email | 21.15s / 46.5 | 10.6s / 115.6 |
| dw2 Messy notes -> action items table | 42.1s / 45.6 | 5.76s / 108.0 |
| dw3 Rewrite blunt Slack msg for execs | 23.48s / 46.5 | 3.28s / 113.0 |
| dw4 RICE prioritization | 42.88s / 45.9 | 5.76s / 109.6 |
| or1 Goal -> plan -> JSON tasks -> risks | 33.66s / 46.3 | 11.76s / 108.1 |
| or2 Strict JSON extraction (schema) | 14.58s / 46.3 | 3.53s / 110.5 |
| or3 Tool-routing decision (agentic) | 20.34s / 45.8 | 4.37s / 111.5 |
| lc1 Python: parse CSV + chart | 38.99s / 45.2 | 6.53s / 108.5 |
| lc2 SQL from schema | 34.14s / 45.3 | 4.28s / 109.9 |
| lc3 Explain + refactor snippet | 21.87s / 45.8 | 4.15s / 109.8 |
| lc4 Regex + test cases | 22.95s / 46.9 | 5.38s / 109.3 |
| sum1 Summarize long PRD (256K ctx) | 40.43s / 44.1 | 8.77s / 99.7 |
| sum2 Condense support thread | 19.01s / 46.1 | 4.23s / 117.0 |
| sum3 Extract decisions from transcript | 21.29s / 43.8 | 6.01s / 106.9 |

---

## Full outputs (judge quality yourself)

### dw1 — Stakeholder update email

**`gemma4:12b`** _(21.15s, 46.5 tok/s)_

Subject: Product Update | [Date]

Hi Team,

Below is this week’s update on product progress, stability, and upcoming risks.

**🚀 Key Wins & Shipments**
*   **CSV Export:** Beta successfully launched to 12 design partners for initial feedback.
*   **Onboarding Optimization:** Variant B outperformed expectations with a **+9% lift in activation**. We are rolling this out to 100% of users.

**🛠️ Stability & Engineering**
*   **API Incident:** Resolved Tuesday's rate-limit issue (40-minute downtime). The root cause was identified and a permanent fix has been deployed.

**👥 Hiring & Growth**
*   **Backend Role:** Still active; we have 2 candidates moving to the onsite stage this week.

**⚠️ Risks**
*   **EU Data Migration:** We are tracking roughly **one week behind** on the migration timeline. The team is currently re-allocating resources to recover the schedule.

**Action Item:** 
Please let me know if you have any questions regarding the updated EU migration timeline by EOD Friday.

Best,

[Your Name]


**`qwen3-coder:30b`** _(10.6s, 115.6 tok/s)_

**Weekly Product Update - Week 45**

**Shipping Progress**
• CSV export (beta) successfully shipped to 12 design partners
• Onboarding flow A/B test: Variant B +9% activation rate, now rolling to 100%

**Incidents & Fixes**
• API rate-limit incident Tuesday (40 min downtime) - root-caused and fix deployed

**Team & Hiring**
• Backend role still open - 2 onsites scheduled this week
• Hiring pipeline progressing steadily

**Key Risks**
• EU tenant data migration slipping ~1 week due to complexity

**Next Steps**
We're executing well on core initiatives while managing operational risks. Need stakeholders to review the CSV export feedback from our design partners by Friday.

Questions or concerns? Let's chat.

Best,
[Your Name]

---

### dw2 — Messy notes -> action items table

**`gemma4:12b`** _(42.1s, 45.6 tok/s)_

### Q3 Planning Sync - Action Items

| Action | Owner | Due | Priority |
| :--- | :--- | :--- | :--- |
| Create technical spec for CSV export | Priya | Friday | High |
| Review copy for onboarding redesign | Marco | End of week | Medium |
| Call BrightWave regarding 500 errors (Escalation) | TBD (Priya or Sales) | ASAP | High |
| Chase Legal for DPA sign-off | TBD | ASAP | High |
| Draft board communication regarding migration slip | Tara | Next Week | Medium |
| Fix DAU numbers on analytics dashboard | Engineering | Before the 20th | Medium |
| Send agenda for next sync | Priya | Thursday | Low |
| Fix kitchen coffee machine | TBD | ASAP |

***

**Notes & Ambiguities:**
*   **Support Escalation:** Ownership is currently unassigned; it was unclear if this should be handled by Priya or the Sales team.
*   **EU Migration:** The specific person tasked with "chasing legal" was not identified in the notes (marked as TBD).
*   **Pricing Experiment:** No action item added to the table as the decision to roll to 100% is noted as automatic/no owner needed.
*   **Mobile Nav Redesign:** This was moved to the next sync due to time constraints and is not listed as a current task for this week.


**`qwen3-coder:30b`** _(5.76s, 108.0 tok/s)_

# Action Items

| Action | Owner | Due | Priority |
|--------|-------|-----|----------|
| Export to CSV spec development | Priya | Friday | High |
| Onboarding redesign copy review | Marco | This week | Medium |
| Follow up with BrightWave on 500 errors | ? (Priya or Sales) | ASAP | High |
| Chase legal for DPA sign-off | ? (Someone from the team) | Asap | High |
| Draft board update on migration slip | Tara | Before QBR | High |
| Fix analytics dashboard DAU numbers | Engineering | Before 20th | High |
| Implement pricing experiment variant B | ? (Automated) | N/A | Low |

**Notes:**
- "Follow up with BrightWave" - unclear who owns this specific task, needs clarification between Priya and Sales
- "Chase legal for DPA sign-off" - no specific owner assigned, needs team member to take ownership
- "Draft board update" - Tara is assigned but will be on PTO until Monday
- "Implement pricing experiment" - marked as automatic with no owner needed
- "Onboarding redesign copy review" - Marco has the copy but hasn't completed it despite repeated promises
- The kitchen coffee machine issue was noted but not included in action items table

**Next Sync:** Thursday (Priya to send agenda, though she won't)

---

### dw3 — Rewrite blunt Slack msg for execs

**`gemma4:12b`** _(23.48s, 46.5 tok/s)_

Depending on your relationship with the VP and how much detail you want to include, here are a few ways to rewrite this:

**Option 1: Direct & Solution-Oriented (Best for most situations)**
> "Hi [Name], we’re seeing some stability issues with the dashboard following today's launch. There was also a delay in communicating these bugs to the Sales team. I’d love to chat about how we can tighten our post-launch checklist and internal communication to ensure a smoother experience for the customers."

**Option 2: Short & Action-Oriented (Best if you just want to get it on their radar)**
> "Hi [Name], we've hit some recurring bugs with the dashboard post-launch that impacted the Sales team’s ability to support customers. Can we sync briefly on how to improve our deployment process and internal alerts for future releases?"

**Option 3: Slightly more "Soft" (If you want to emphasize the partnership)**
> "Hi [Name], I'm concerned about some recurring issues with the dashboard launch. It’s becoming difficult for Sales to manage customer expectations without earlier notice. I’d love to work together on a plan to streamline communication between Engineering and Sales during these rollouts."

### Key Changes Made:
*   **"Eng dropped the ball"** $\rightarrow$ replaced with **"stability issues"** or **"technical bugs."** (Focuses on the *problem*, not the *person*).
*   **"Broken AGAIN / Third time"** $\rightarrow$ replaced with **"recurring issues."** (Highlights the pattern without sounding like a personal attack).
*   **"Nobody told sales"** $\rightarrow$ replaced with **"communication gap"** or **"internal alert process."** (Identifies the process failure instead of blaming an individual).
*   **"We look incompetent"** $\rightarrow$ replaced with **"impacted customer experience/management."** (Focuses on the business impact rather than your internal feelings).


**`qwen3-coder:30b`** _(3.28s, 113.0 tok/s)_

"Follow-up on the recent launch issues. The dashboard malfunction has occurred three times, and sales wasn't notified of the previous two incidents. We need to improve our communication protocols and ensure all stakeholders are informed of technical issues moving forward."

---

### dw4 — RICE prioritization

**`gemma4:12b`** _(42.88s, 45.9 tok/s)_

To prioritize these features, I am assuming we are building a **B2B SaaS platform** (e.g., a CRM or Project Management tool) where enterprise adoption and user onboarding efficiency are primary goals.

### Assumptions for Scoring:
*   **Reach:** How many users will interact with this? (10 = All Users, 5 = Many, 1 = Few/Admin only).
*   **Impact:** How much does it help the core "Job to be Done"? (3 = Massive, 2 = High, 1 = Medium/Low).
*   **Confidence:** How certain are we about our estimates? (1.0 = High, 0.8 = Medium, 0.5 = Low).
*   **Effort:** Estimated person-months or complexity units (1 = Easy, 3 = Moderate, 5 = Complex/Heavy Engineering).

### RICE Prioritization Table

| Feature | Reach (1-10) | Impact (1-3) | Confidence (0.5-1) | Effort (1-5) | **RICE Score** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **SSO/SAML Login** | 9 | 3 | 1.0 | 4 | **6.75** |
| **Bulk CSV Import** | 8 | 2 | 1.0 | 3 | **5.33** |
| **In-app Notifications** | 9 | 2 | 0.8 | 3 | **4.80** |
| **Dark Mode** | 10 | 1 | 1.0 | 3 | **3.33** |
| **Audit Log Export** | 4 | 2 | 1.0 | 3 | **2.67** |

---

### Final Recommendations

**1. SSO/SAML Login**
*Rationale:* This is a non-negotiable requirement for enterprise sales and security compliance, directly enabling the acquisition of high-value corporate clients.

**2. Bulk CSV Import**
*Rationale:* This significantly reduces friction during the onboarding phase, allowing users to migrate data quickly and reach "time-to-value" faster.


**`qwen3-coder:30b`** _(5.76s, 109.6 tok/s)_

## RICE Prioritization Matrix

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| **SSO/SAML login** | 8 | 9 | 8 | 7 | **51.2** |
| **Bulk CSV import** | 7 | 8 | 7 | 6 | **39.2** |
| **Dark mode** | 9 | 3 | 9 | 4 | **24.3** |
| **In-app notifications** | 8 | 7 | 8 | 5 | **22.4** |
| **Audit log export** | 6 | 6 | 7 | 6 | **18.9** |

## Top 2 Recommendations

1. **SSO/SAML login** - High reach across all users with significant impact on security and user experience, moderate effort with high confidence in implementation success

2. **Bulk CSV import** - Strong impact for power users with good reach, relatively low effort investment, and high confidence in delivery timeline

## Assumptions
- Reach = % of users affected (1-10 scale)
- Impact = Business/user value (1-10 scale) 
- Confidence = Probability of successful delivery (1-10 scale)
- Effort = Development resources needed (1-10 scale)
- RICE = (Reach × Impact × Confidence) ÷ Effort

---

### or1 — Goal -> plan -> JSON tasks -> risks

**`gemma4:12b`** _(33.66s, 46.3 tok/s)_

### 1) Phased Launch Plan

**Phase 1: Discovery & Definition (Weeks 1-2)**
Define the "Aha! Moment" for users, determine trial duration and limitations (e.g., number of seats or data limits), map out the automated onboarding email sequence, and audit the current authentication flow to identify friction points.

**Phase 2: Development & Integration (Weeks 3-4)**
Build the automated account provisioning logic, implement "paywall" gates for premium features, integrate the payment gateway for seamless conversion, and develop in-app notifications to guide users through the setup process.

**Phase 3: Testing & Enablement (Weeks 5-6)**
Conduct rigorous QA on the self-serve flow, create internal documentation and scripts for Sales/Support teams to handle trial inquiries, prepare marketing collateral (landing pages/ads), and execute a soft launch followed by full rollout.

### 2. Work Items
```json
[
  {"id": "1", "title": "Define trial scope and 'Aha!' moment", "owner_role": "Product Manager", "week": 1, "depends_on": null},
  {"id": "2", "title": "Map automated onboarding email journey", "owner_role": "Marketing", "week": 1, "depends_on": "1"},
  {"id": "3", "title": "Audit and update Auth flow for self-serve", "owner_role": "Engineering", "week": 2, "depends_on": "1"},
  {"id": "4", "title": "Design/Build automated account provisioning", "owner_role": "Engineering", "week": 3, "depends_on": "3"},
  {"id": "5", "title": "Implement feature gating logic", "owner_role": "Engineering", "week": 3, "depends_on": "4"},
  {"id": "6", "title": "Integrate payment gateway for conversion", "owner_role": "DevOps", "week": 4, "depends_on": "5"},
  {"id": "7", "title": "Create marketing collateral and landing pages", "owner_role": "Marketing", "week": 5, "depends_on": "2"},
  {"id": "8", "title": "QA testing and bug fixing", "owner_role": "QA", "week": 6, "depends_on": "6"},
  {"id": "9", "title": "Internal team training (Sales/Support)", "owner_role": "Success", "week": 6, "depends_on": "7"},
  {"id": "10", "title": "Final Go-Live", "owner_role": "Product Manager", "week": 6, "depends_on": "8"}
]
```

### 3. Risk Table

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| **Low Conversion** | High | High | Implement a high-frequency automated email nurture sequence for trial users. |
| **Technical Provisioning Errors** | Medium | High | Conduct a 1-week "beta" period with internal staff before public launch. |
| **Scope Creep** | High | Medium | Strict adherence to MVP requirements; defer non-essential features to v2. |
| **Poor User Experience (UX)** | Medium | High | Conduct usability testing on the signup flow in Week 4 before final integration. |


**`qwen3-coder:30b`** _(11.76s, 108.1 tok/s)_

# 1) Phased Plan (Weeks 1-6)

**Week 1:** Define trial parameters, set up development environment, and establish team alignment on requirements. Create initial user flow diagrams and determine trial limits.

**Week 2:** Build core trial infrastructure including user authentication, trial creation workflow, and basic account management features. Begin integration with existing systems.

**Week 3:** Develop trial dashboard UI/UX, implement usage tracking, and create automated trial expiration processes. Start testing with internal users.

**Week 4:** Launch beta trial program with select customers. Implement monitoring tools and begin gathering feedback on user experience.

**Week 5:** Refine trial experience based on beta feedback, optimize conversion funnels, and prepare marketing materials for full launch.

**Week 6:** Full production launch of self-serve free trial with comprehensive monitoring, support processes, and performance tracking in place.

# 2) Work Items JSON Array

```json
[
  {
    "id": "1",
    "title": "Define trial parameters and limits",
    "owner_role": "Product Manager",
    "week": 1,
    "depends_on": []
  },
  {
    "id": "2",
    "title": "Set up development environment",
    "owner_role": "Engineering Lead",
    "week": 1,
    "depends_on": []
  },
  {
    "id": "3",
    "title": "Create user flow diagrams",
    "owner_role": "UX Designer",
    "week": 1,
    "depends_on": ["1"]
  },
  {
    "id": "4",
    "title": "Build trial infrastructure and authentication",
    "owner_role": "Backend Engineer",
    "week": 2,
    "depends_on": ["2"]
  },
  {
    "id": "5",
    "title": "Implement account management features",
    "owner_role": "Frontend Engineer",
    "week": 2,
    "depends_on": ["4"]
  },
  {
    "id": "6",
    "title": "Develop trial dashboard UI/UX",
    "owner_role": "UX Designer",
    "week": 3,
    "depends_on": ["3"]
  },
  {
    "id": "7",
    "title": "Implement usage tracking and expiration processes",
    "owner_role": "Backend Engineer",
    "week": 3,
    "depends_on": ["4"]
  },
  {
    "id": "8",
    "title": "Conduct internal beta testing",
    "owner_role": "QA Lead",
    "week": 4,
    "depends_on": ["6", "7"]
  },
  {
    "id": "9",
    "title": "Gather and analyze beta feedback",
    "owner_role": "Product Manager",
    "week": 5,
    "depends_on": ["8"]
  },
  {
    "id": "10",
    "title": "Optimize trial conversion funnels",
    "owner_role": "Product Manager",
    "week": 5,
    "depends_on": ["9"]
  },
  {
    "id": "11",
    "title": "Prepare marketing materials for launch",
    "owner_role": "Marketing Lead",
    "week": 5,
    "depends_on": ["10"]
  },
  {
    "id": "12",
    "title": "Launch full self-serve free trial program",
    "owner_role": "Product Manager",
    "week": 6,
    "depends_on": ["11"]
  }
]
```

# 3) Risk Table

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Technical infrastructure fails during trial launch | Medium | High | Implement comprehensive testing, load testing, and rollback procedures before launch |
| Users abuse the trial by creating multiple accounts | High | Medium | Implement account verification, IP monitoring, and automated fraud detection systems |
| Trial conversion rates lower than expected | Medium | Medium | Conduct A/B testing on different trial experiences and optimize based on early data |
| Security vulnerabilities in trial system | Low | High | Perform security audit and penetration testing before launch |
| Marketing campaign underperforms | Medium | Medium | Develop multiple marketing channels and create contingency promotional plans |
| Support team overwhelmed by trial sign-ups | Medium | Medium | Set up automated responses, expand support capacity, and create self-service resources |
| Data migration issues from old system | Low | High | Create detailed data migration plan with backup procedures and rollback capabilities |

---

### or2 — Strict JSON extraction (schema)

**`gemma4:12b`** _(14.58s, 46.3 tok/s)_

```json
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
```


**`qwen3-coder:30b`** _(3.53s, 110.5 tok/s)_

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

**`gemma4:12b`** _(20.34s, 45.8 tok/s)_

```json
[
  {"tool": "create_ticket", "args": {"title": "Billing page 500 error for enterprise customers", "severity": "high"}},
  {"tool": "send_email", "args": {"to": "finance@company.com", "subject": "Urgent: Billing Page Issue", "body": "The billing page is returning a 500 error for all enterprise customers; a high-priority ticket has been created to address this."}}
]
```
I am creating a high-severity ticket to alert the technical team and sending an email to inform the finance department about the issue.


**`qwen3-coder:30b`** _(4.37s, 111.5 tok/s)_

[
  {"tool": "create_ticket", "args": {"title": "Billing page 500 error for enterprise customers", "severity": "high"}},
  {"tool": "send_email", "args": {"to": "finance@company.com", "subject": "Billing page issue - enterprise customers affected", "body": "The billing page is returning 500 errors for all enterprise customers since this morning. A ticket has been created and the IT team is investigating."}}
]

I need to create a high-severity ticket to track the technical issue with the billing page, and then notify the finance team who would be directly impacted by this issue affecting their customers. The ticket will ensure the problem gets proper attention and tracking, while the email informs finance about the situation and that action is being taken.

---

### lc1 — Python: parse CSV + chart

**`gemma4:12b`** _(38.99s, 45.2 tok/s)_

```python
import csv
import io
import matplotlib.pyplot as plt

# The raw data provided in the prompt
csv_data = """order_date,product,units,unit_price
2026-05-01,Starter Plan,42,29.00
2026-05-02,Pro Plan,18,99.00
2026-05-03,Enterprise Plan,3,499.00
2026-05-04,Starter Plan,55,29.00
2026-05-05,Add-on: Seats,120,9.00
2026-05-06,Pro Plan,22,99.00
2026-05-07,Add-on: Storage,64,5.00
2026-05-08,Enterprise Plan,2,499.00
2026-05-09,Pro Plan,31,99.00
2026-05-10,Starter Plan,40,29.00
2026-05-11,Add-on: Seats,85,9.00
2026-05-12,Enterprise Plan,4,499.00
2026-05-13,Pro Plan,27,99.00
2026-05-14,Add-on: Storage,48,5.00
2026-05-15,Starter Plan,61,29.00"""

def main():
    # Use io.StringIO to treat the string like a file for the csv module
    f = io.StringIO(csv_data.strip())
    reader = csv.DictReader(f)
    
    # Dictionary to store total revenue per product
    revenue_map = {}

    for row in reader:
        product = row['product']
        units = int(row['units'])
        price = float(row['unit_price'])
        revenue = units * price
        
        # Accumulate totals
        revenue_map[product] = revenue_map.get(product, 0) + revenue

    # Sort products by revenue in descending order
    sorted_products = sorted(revenue_map.items(), key=lambda x: x[1], reverse=True)

    # Print the top 3 products
    print("Top 3 Products by Total Revenue:")
    for i, (name, rev) in enumerate(sorted_products[:3]):
        print(f"{i+1}. {name}: ${rev:,.2f}")

    # Create a bar chart of all products
    # We use the order from sorted_products to ensure the plot is organized
    labels = [item[0] for item in sorted_products]
    values = [item[1] for item in sorted_products]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Product')
    plt.ylabel('Total Revenue ($)')
    plt.title('Total Revenue by Product')
    # Rotate labels slightly for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig('revenue.png')
    print("\nChart saved as 'revenue.png'")

if __name__ == "__main__":
    main()
```


**`qwen3-coder:30b`** _(6.53s, 108.5 tok/s)_

```python
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Read the CSV data
products = defaultdict(float)
with open('sample_sales.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row['product']
        units = int(row['units'])
        unit_price = float(row['unit_price'])
        revenue = units * unit_price
        products[product] += revenue

# Find top 3 products by total revenue
top_products = sorted(products.items(), key=lambda x: x[1], reverse=True)[:3]

# Print top 3 products
print("Top 3 products by total revenue:")
for i, (product, revenue) in enumerate(top_products, 1):
    print(f"{i}. {product}: ${revenue:,.2f}")

# Create bar chart
plt.figure(figsize=(10, 6))
product_names = [item[0] for item in top_products]
revenues = [item[1] for item in top_products]
bars = plt.bar(product_names, revenues, color=['#4CAF50', '#2196F3', '#FF9800'])

# Add value labels on bars
for bar, revenue in zip(bars, revenues):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(revenues)*0.01,
             f'${revenue:,.0f}', ha='center', va='bottom')

plt.xlabel('Product')
plt.ylabel('Total Revenue ($)')
plt.title('Revenue by Product (Top 3)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the chart
plt.savefig('revenue.png')
```

---

### lc2 — SQL from schema

**`gemma4:12b`** _(34.14s, 45.3 tok/s)_

```sql
SELECT 
    u.plan,
    COUNT(DISTINCT CASE WHEN e.name = 'activated' AND e.ts <= u.signup_date + INTERVAL '7 days' THEN u.id END) * 100.0 / 
    NULLIF(COUNT(DISTINCT u.id), 0) AS activation_rate
FROM users u
LEFT JOIN events e ON u.id = e.user_id
GROUP BY u.plan;
```

### Explanation
The query identifies unique users who triggered an 'activated' event within a 7-day window of their signup date and joins this logic against the total user base. It then calculates the percentage by dividing those successful activations by the total number of users per plan, using `NULLIF` to prevent division by zero errors.


**`qwen3-coder:30b`** _(4.28s, 109.9 tok/s)_

```sql
SELECT 
    u.plan,
    ROUND(
        COUNT(CASE WHEN e.name = 'activated' AND e.ts <= u.signup_date + INTERVAL '7 days' THEN 1 END) * 100.0 / COUNT(u.id),
        2
    ) AS activation_rate
FROM users u
LEFT JOIN events e ON u.id = e.user_id
GROUP BY u.plan;
```

This query joins the users and events tables to calculate the percentage of users who completed the 'activated' event within 7 days of signing up, grouped by their subscription plan. It uses a LEFT JOIN to include all users even if they haven't triggered any events, and applies conditional aggregation to count only those who activated within the time window.

---

### lc3 — Explain + refactor snippet

**`gemma4:12b`** _(21.87s, 45.8 tok/s)_

**Explanation**
This function removes duplicate items from a list while preserving the original order of the elements. It does this by creating a new list and only adding an item if it hasn't been encountered yet.

**Risk/Bug**
The primary risk is **performance (Time Complexity)**: because searching a list (`if l[i] not in r`) takes longer as the list grows, this function has $O(n^2)$ complexity, making it very slow for large datasets.

**Refactor**
If you need to preserve the order of items, use `dict.fromkeys()` (which is highly optimized):

```python
def unique_elements(items):
    return list(dict.fromkeys(items))
```


**`qwen3-coder:30b`** _(4.15s, 109.8 tok/s)_

This Python function removes duplicate items from a list while preserving the order of first occurrences - it goes through each item in the input list and only adds it to the result if it hasn't been added before.

**Bug/Risk**: The function has poor performance with large lists because `l[i] not in r` checks the entire result list for each element, making it O(n²) time complexity instead of O(n).

**Cleaner refactor**:
```python
def f(l):
    seen = set()
    result = []
    for item in l:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```
This version uses a set for O(1) lookup time, making it O(n) instead of O(n²), while maintaining the same order preservation behavior.

---

### lc4 — Regex + test cases

**`gemma4:12b`** _(22.95s, 46.9 tok/s)_

Here is the regular expression to match the specified order ID format:

### The Regex
```regex
ORD-\d{8}(-R)?
```

**Explanation:**
*   `ORD-` : Matches the literal characters "ORD-" exactly.
*   `\d{8}` : Matches exactly 8 digits (0-9).
*   `(-R)?` : A non-capturing group that makes the "-R" suffix optional.

---

### Test Cases

| Input String | Match? | Reason |
| :--- | :--- | :--- |
| **ORD-12345678** | ✅ Yes | Matches "ORD-" followed by 8 digits. |
| **ORD-00009999** | ✅ Yes | Matches "ORD-" followed by 8 digits (including leading zeros). |
| **ORD-11223344-R** | ✅ Yes | Matches the standard format plus the optional "-R" suffix. |
| **ORD-88776655-R** | ✅ Yes | Matches the full format with a different digit set. |
| **ORD-1234567** | ❌ No | Only contains 7 digits instead of 8. |
| **ORD-123456789** | ❌ No | Contains 9 digits; the regex requires exactly 8. |
| **ABC-12345678** | ❌ No | Starts with "ABC-" instead of "ORD-". |
| **ORD-12345678-X** | ❌ No | Contains an invalid suffix ("-X") instead of "-R". |


**`qwen3-coder:30b`** _(5.38s, 109.3 tok/s)_

## Regular Expression

```
^ORD-\d{8}(-R)?$
```

## Examples Table

| Example | Should Match? | Explanation |
|---------|---------------|-------------|
| `ORD-12345678` | ✅ Yes | Matches exactly 8 digits after "ORD-" with no suffix |
| `ORD-98765432-R` | ✅ Yes | Matches 8 digits followed by "-R" suffix |
| `ORD-1234567` | ❌ No | Only 7 digits (missing one) |
| `ORD-123456789` | ❌ No | 9 digits (too many) |
| `ORD-12345678X` | ❌ No | Invalid suffix (X instead of -R) |
| `ORDER-12345678` | ❌ No | Wrong prefix (should be "ORD-", not "ORDER-") |

## Regex Breakdown

- `^` - Start of string
- `ORD-` - Literal text "ORD-"
- `\d{8}` - Exactly 8 digits
- `(-R)?` - Optional group containing "-R"
- `$` - End of string

---

### sum1 — Summarize long PRD (256K ctx)

**`gemma4:12b`** _(40.43s, 44.1 tok/s)_

Here is my review of the Self-Serve Free Trial PRD:

**TL;DR**
Acme Cloud is launching a self-serve, no-credit-card trial to capture "bottoms-up" growth from small teams who are currently ignored by the sales-assisted motion (Section 1 & 2). The initiative automates provisioning and provides a 14-day window for users to experience value before being prompted to convert via in-product Stripe checkout (Section 3 & 6.2). To protect existing revenue, the system will automatically route large enterprise accounts back to the sales team while providing restricted "soft-lock" access after trial expiration (Section 6.4 & 8). The primary success metric is a $\ge$8% conversion rate from trial to paid plans within 90 days of launch (Section 9).

**Key Decisions**
*   **Trial Parameters:** A 14-day duration with no credit card required at sign-up (D1, FR5).
*   **Post-Expiry State:** A "soft-lock" read-only state for 30 days following expiration, rather than immediate deletion (D2, FR8).
*   **Segmentation Logic:** Self-serve is capped at the "Pro" tier; accounts identified as large/enterprise via domain or size are routed to sales (D3, FR14).
*   **Localization Strategy:** Non-English markets are excluded from the initial launch and will be handled as a fast-follow (D4, NG2).

**Open Risks/Questions**
*   **Activation Definition:** The specific "activation" events required for instrumentation are not yet defined (OQ3).
*   **Nudge Persistence:** It is unclear if the Day 7 nudge can be dismissed or will reappear on Day 12 (OQ2).
*   **Trial Extensions:** The PRD does not yet specify if users can request or grant trial extensions (OQ4).
*   **Legal Hurdles:** Legal review of "no-credit-card" terms and automated data deletion is still pending and considered a long pole (R4).

**What's Missing**
The PRD lacks a **Support/Success Strategy for the Self-Serve Segment.** While FR7 outlines automated nudges, there is no defined workflow for how a "Solo starter" (who avoids sales calls) can get help if they hit a technical blocker during their 14-day window. We need to define if these users go to a community forum, a knowledge base, or a specific low-touch support queue to ensure they don't churn due to friction before the Day 7 nudge.


**`qwen3-coder:30b`** _(8.77s, 99.7 tok/s)_

### **TL;DR**
This PRD outlines a self-serve free trial feature for Acme Cloud to capture small-team prospects who currently go unserved by the sales-assisted model. The goal is to enable instant access, in-product conversion, and scalable growth while protecting enterprise deals through intelligent routing. The solution includes a 14-day trial with no credit card required, guided setup, and integration with Stripe for checkout.

---

### **Key Decisions**
- **Trial length:** 14 days from first sign-in (Section 6.2).
- **No credit card required** to start the trial (Section 6.1 FR3).
- **Self-serve capped at Pro plan**, Enterprise routes to sales (Section 6.3, D3).
- **Soft-lock read-only state post-expiry** for 30 days (Section 6.2 FR8).
- **Sales routing based on company size and domain** to avoid cannibalizing enterprise deals (Section 6.4).

---

### **Open Risks/Questions**
- **Legal exposure** around no-card terms and auto-deletion — pending legal review (Section 10, R4).
- Whether **day-7 nudge should be dismissible permanently or re-shown on day 12** (Section 11, OQ2).
- Definition of **"activation" for instrumentation purposes** (Section 11, OQ3).
- **Trial extension policy** — self-serve or sales-granted (Section 11, OQ4).

---

### **What's Missing**
The PRD lacks a **clear definition of how trial users will be segmented and tracked for attribution**, especially in the context of Growth experiments and funnel optimization. While Section 9 mentions instrumentation and funnel metrics, there is no specific plan or framework outlined for how user behavior will be tracked across different touchpoints to support data-driven iteration (e.g., cohort analysis, UTM tagging strategy). This is critical for optimizing activation and conversion rates post-launch.

---

### sum2 — Condense support thread

**`gemma4:12b`** _(19.01s, 46.1 tok/s)_

**Current status:** Resolved; hotfix deployed and customer received a manual invoice export.
**Root cause if known:** A missing index on `invoices.account_id` caused full table scans and 500 errors for accounts with high invoice volumes following a Friday release.
**Next step + owner:** Conduct backfill checks for other large accounts and implement performance test gates in CI (Maya).
**Customer sentiment:** Positive; the customer expressed appreciation for both the rapid technical fix and the manual workaround provided during their month-end close.


**`qwen3-coder:30b`** _(4.23s, 117.0 tok/s)_

- **Current status:** Billing page is fixed and performing normally after a hotfix deployment.  
- **Root cause:** Missing index on `invoices.account_id` caused full table scans for accounts with >500 invoices (BrightWave had ~1,900).  
- **Next step + owner:** Monitor invoice-page latency and conduct post-incident review; PM to file follow-ups including backfill check and perf test gate.  
- **Customer sentiment:** Positive. The customer appreciated the quick resolution and manual export that unblocked their month-end close.

---

### sum3 — Extract decisions from transcript

**`gemma4:12b`** _(21.29s, 43.8 tok/s)_

**Decisions Made**
* 14-day trial period with no credit card required upfront.
* Inclusion of upgrade nudges on day 7 and day 12 of the trial.
* Implementation of a "soft-lock" (read-only access) upon trial expiry.

**Action Items**
* **Tom** -> Scope the trial state machine and paywall; provide estimates by Friday.
* **Priya** -> Create lo-fi mocks for nudge designs and expiry screen by Wednesday; finalize designs by next Tuesday.
* **Maya** -> Define activation terms and event specifications by Thursday.
* **Maya** -> Contact legal today to begin review of no-card terms.

**Parking-lot/Deferred Items**
* Pricing-page changes (moved to a separate workstream).
* Localization of trial emails for the EU (marked as a "fast-follow" after launch).


**`qwen3-coder:30b`** _(6.01s, 106.9 tok/s)_

### **Decisions Made**
- **Trial Length & Card Requirement**: 14-day trial with no credit card required.
- **Upgrade Nudges**: Add in-trial upgrade nudges on day 7 and day 12.
- **Paywall Behavior**: Soft-lock (read-only) at trial expiry to retain user data and aid win-back.
- **Localization**: Postpone localization of trial emails for EU to a fast-follow, not launch-blocking.
- **Pricing Page Changes**: Deferred to a separate workstream; not part of this scope.

---

### **Action Items**
- **Tom (Eng Lead)**  
  - Own the trial state machine and paywall logic.  
  - Scope the backend work and provide estimates by Friday.

- **Priya (Design)**  
  - Own the nudge designs and expiry screen.  
  - Deliver lo-fi mocks by Wednesday; final designs by next Tuesday.

- **Maya (PM)**  
  - Define activation and event spec for analytics instrumentation by Thursday.  
  - Ping legal to initiate terms review for the no-card trial.

---

### **Parking-Lot / Deferred Items**
- **Pricing Page Changes**: Not part of current scope; to be handled in a separate workstream.
- **Localization (EU Trial Emails)**: To be addressed as a fast-follow, not required for launch.
- **Legal Terms Review**: Needs early start due to potential delays; will be managed by Maya.

---

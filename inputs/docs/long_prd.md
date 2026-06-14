# PRD: Self-Serve Free Trial for Acme Cloud (synthetic)

**Status:** Draft v0.7 · **Author:** Maya Chen (PM) · **Last updated:** 2026-06-10
**Reviewers:** Eng (T. Alvarez), Design (P. Rao), Growth (J. Kim), Legal (pending)

---

## 1. Overview

Acme Cloud is a B2B SaaS workflow-automation platform sold today almost entirely
through a sales-assisted motion: a prospect books a demo, talks to an account
executive, and is issued a manually provisioned trial. This works for large
deals but is a poor fit for the growing volume of small-team and bottoms-up
prospects who want to try the product immediately without talking to anyone.

This document specifies a **self-serve free trial**: a prospect can sign up on
the website, use a time-boxed version of the product without a credit card, and
convert to a paid plan in-product. The goal is to open a scalable, low-touch
acquisition channel while protecting the existing sales motion for enterprise.

## 2. Problem & Background

Three signals motivate this work:

1. **Demand we are turning away.** In Q1, 38% of website "Start trial" clicks
   came from companies under 25 employees. Our sales team does not prioritize
   these accounts, so most never get a trial. We estimate ~600 qualified
   small-team prospects/month go unserved.
2. **Competitive pressure.** Two direct competitors launched no-credit-card
   trials in the last year and now rank above us for "free trial" search terms.
3. **CAC efficiency.** Sales-assisted trials cost an estimated $420 in blended
   sales time to provision and nurture. A self-serve path could serve the
   long tail at near-zero marginal cost.

Prior attempt: a 2024 "request a trial" form increased lead volume but not
conversion, because the manual provisioning step (median 2.3 days) killed
momentum. The lesson: **instant access matters more than lead capture.**

## 3. Goals & Non-Goals

### Goals
- G1. Let a prospect go from website to working product in **under 3 minutes**,
  no credit card, no sales contact.
- G2. Convert trials to paid **in-product**, with no human in the loop.
- G3. Instrument the full funnel so Growth can iterate on activation.
- G4. Protect enterprise: route large/known accounts to sales, not self-serve.

### Non-Goals
- NG1. Replacing the sales-assisted motion for mid-market/enterprise.
- NG2. Localizing the trial experience for non-English markets at launch
  (fast-follow).
- NG3. Building a usage-based billing system (we remain seat-based for now).
- NG4. A mobile-app trial experience (web only at launch).

## 4. Target Users & Personas

- **"Solo starter" (primary):** an ops or eng lead at a <25-person company,
  evaluating tools on their own, allergic to sales calls. Wants to validate the
  product against a real workflow within an afternoon.
- **"Team champion" (secondary):** an early adopter who wants to invite 2–3
  colleagues during the trial to prove value before requesting budget.
- **"Enterprise scout" (route away):** someone from a large org who lands on the
  self-serve flow but should be routed to sales. Detected via work-email domain
  and self-reported company size.

## 5. User Stories

- As a solo starter, I can sign up with email + Google SSO and reach an empty
  workspace immediately, so I can start without waiting.
- As a solo starter, I can follow a short guided setup that creates my first
  automation from a template, so I reach value quickly.
- As a team champion, I can invite teammates during the trial, so we can
  evaluate together.
- As a trialing user near expiry, I can upgrade to a paid plan in a few clicks,
  so I don't lose access or my work.
- As an expired user, I can still see (read-only) what I built, so I'm motivated
  to come back and convert.

## 6. Functional Requirements

### 6.1 Sign-up & provisioning
- FR1. Support email/password and Google SSO sign-up.
- FR2. Provision an isolated trial workspace automatically on sign-up
  (target p95 < 10 seconds).
- FR3. No credit card required to start.
- FR4. Enforce one active trial per email domain for free-mail excluded
  domains; allow multiple for generic domains (gmail, etc.) with rate limits to
  deter abuse.

### 6.2 Trial lifecycle
- FR5. Trial length is **14 days** from first sign-in (configurable via flag).
- FR6. Show remaining trial days persistently in the top nav.
- FR7. Upgrade nudges at **day 7** and **day 12** (in-app modal + email).
- FR8. At expiry, transition the workspace to a **soft-locked, read-only**
  state for 30 days, then schedule for deletion with two warning emails.
- FR9. A grace state: if a user starts checkout before expiry, do not lock.

### 6.3 In-product conversion
- FR10. An always-available "Upgrade" entry point.
- FR11. Self-serve checkout for Starter and Pro plans (Stripe).
- FR12. On successful payment, immediately remove limits and convert the
  workspace in place (no data migration).
- FR13. Enterprise plan shows "Contact sales" instead of self-checkout.

### 6.4 Sales routing
- FR14. During sign-up, ask company size. If >100 employees OR the email domain
  matches a known target-account list, show a "Talk to sales" path in parallel
  with self-serve (do not block self-serve).
- FR15. Emit a lead record to the CRM for all sign-ups, tagged by routing class.

## 7. UX Flow (happy path)

1. Website "Start free trial" → sign-up screen (email/SSO).
2. One-question qualifier: company size.
3. Workspace provisioned → guided setup wizard (pick a template, connect one
   data source, run first automation).
4. "Aha" confirmation screen with next steps and an invite-teammates prompt.
5. Normal product usage with a persistent trial-days indicator.
6. Day 7 / Day 12 nudges → Upgrade modal → Stripe checkout → converted.

## 8. Technical Considerations

- **Trial state machine.** States: `active → grace → soft_locked → scheduled_deletion`.
  Must be auditable and idempotent; transitions driven by a daily scheduled job
  plus event triggers (checkout started, payment succeeded).
- **Billing integration.** Stripe Checkout + webhooks for payment events. Must
  handle the race where a user pays in the final minutes before expiry.
- **Isolation & abuse.** Per-workspace resource quotas; sign-up rate limiting;
  disposable-email detection.
- **Data retention.** Read-only retention 30 days post-expiry; deletion must be
  GDPR-compliant with export-before-delete for EU tenants.
- **Feature flags.** Trial length, nudge timing, and paywall behavior behind
  flags for experimentation.

## 9. Success Metrics

- **North star:** number of self-serve paid conversions / month.
- Funnel: trial start rate, time-to-first-automation, day-1 / day-7 activation,
  nudge CTR, trial→paid conversion rate, 60-day retention of self-serve paid.
- Guardrails: support ticket volume from trial users; fraud/abuse rate;
  cannibalization of sales-assisted deals (monitored, should be near zero for
  >100-employee accounts).
- Target at launch+90 days: ≥ 8% trial→paid conversion; < 2% abuse rate.

## 10. Risks & Mitigations

- **R1. Low activation** because users don't reach value. *Mitigation:* the
  guided setup wizard and templates; instrument time-to-first-automation.
- **R2. Cannibalization** of enterprise deals. *Mitigation:* sales routing
  (FR14) and monitoring; self-serve caps at Pro.
- **R3. Abuse / free-tier farming.** *Mitigation:* rate limits, domain rules,
  disposable-email detection.
- **R4. Legal exposure** on no-card terms and auto-deletion. *Mitigation:* legal
  review of terms (pending — long pole); clear in-product disclosures.
- **R5. Billing edge cases** (pay-at-expiry race). *Mitigation:* grace state
  (FR9) and idempotent webhook handling.

## 11. Open Questions

- OQ1. Do we localize trial emails for EU at launch or fast-follow? (Leaning
  fast-follow.)
- OQ2. Should day-7 nudge be dismissible permanently, or re-show on day 12?
- OQ3. What is the exact definition of "activation" for instrumentation? (Owner:
  PM, due before instrumentation work.)
- OQ4. Do we allow trial extension (self-serve or sales-granted)?

## 12. Timeline (proposed, 6 weeks)

- Wk 1: Spec sign-off, activation definition, legal review kickoff, designs start.
- Wk 2–3: Trial state machine + provisioning; nudge + expiry designs final.
- Wk 3–4: Stripe self-checkout; sales routing + CRM lead emit.
- Wk 4–5: Instrumentation; guided setup wizard; QA.
- Wk 5–6: Beta to 50 prospects, fix, GA.

## 13. Appendix: Decisions Log

- D1 (2026-06-03): 14-day trial, no credit card. Owner: Maya.
- D2 (2026-06-03): Soft-lock to read-only at expiry (not hard-lock). Owner: Priya.
- D3 (2026-06-05): Self-serve capped at Pro; Enterprise routes to sales. Owner: Maya.
- D4 (2026-06-10): Localization is a fast-follow, not launch-blocking. Owner: Maya.

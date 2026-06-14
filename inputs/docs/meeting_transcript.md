# Transcript — Trial Conversion Working Group (synthetic, ~20 min excerpt)

**Maya (PM):** Alright, let's start. Goal today: lock the scope for the self-serve free trial and agree owners. Quick reminder we want to ship in six weeks.

**Tom (Eng lead):** Before that — did everyone see the game last night? Wild ending.

**Maya:** Ha, parking the sports talk. Tom, can eng support a 14-day trial with no credit card up front?

**Tom:** Yes, but the gating logic touches billing. If we do no-card, we need a hard paywall when the trial ends, and a grace state. That's maybe two weeks of backend work.

**Priya (Design):** From research, no-credit-card lifts trial starts a lot but conversion quality drops. I'd recommend no card, but add an in-trial upgrade nudge on day 7 and day 12.

**Maya:** I like that. Decision: 14-day trial, no credit card required, with upgrade nudges on day 7 and 12. Everyone good? ... Okay, decided.

**Tom:** For the paywall, do we soft-lock (read-only) or hard-lock at expiry?

**Priya:** Soft-lock. Read-only keeps their data visible, which helps win-back.

**Maya:** Agreed, soft-lock to read-only at expiry. Tom, can your team own the trial state machine and the paywall?

**Tom:** Yes. I'll scope it this week and have estimates by Friday.

**Maya:** Great. Priya, can you own the nudge designs and the expiry screen?

**Priya:** Yes. I'll have lo-fi mocks by Wednesday, final by next Tuesday.

**Maya:** We also need analytics — trial start, activation, day-7 nudge CTR, conversion. Who owns instrumentation?

**Tom:** Dev can add events but we need the definitions. Maya, can you write the activation definition?

**Maya:** Yes, I'll define activation and the event spec by Thursday. Let's hold pricing-page changes for a separate workstream — parking that for now.

**Priya:** One open question: do we localize the trial emails for EU at launch, or fast-follow?

**Maya:** Good flag. Let's park localization as a fast-follow, not launch-blocking. I'll confirm with marketing.

**Tom:** Last thing — legal needs to review the no-card terms. That could be a long pole.

**Maya:** Right. Action: I'll ping legal today to start the terms review early. Okay, that's time. Thanks everyone.

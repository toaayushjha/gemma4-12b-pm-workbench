# Support ticket #48217 — "Billing page 500 error" (synthetic)

**Customer:** BrightWave Health (Enterprise, 45 seats) · **Opened:** 2026-06-09 08:14

---

**[08:14] Dana O. (customer):** Our whole finance team is getting a 500 error when they open the Billing page. Started this morning. We have month-end close today so this is urgent.

**[08:31] Sam (support):** Hi Dana, thanks for flagging and sorry for the disruption. I can reproduce on our side for enterprise accounts. Escalating to engineering now with P1.

**[08:52] Ravi (engineering):** Looking. Initial guess: the invoices service is timing out when an account has >500 historical invoices. BrightWave has ~1,900. Correlates with a query we shipped Friday.

**[09:20] Ravi (engineering):** Confirmed. A missing index on invoices.account_id is causing full table scans under load. Short-term: I can add the index in a hotfix. ETA 1–2 hours including review.

**[09:25] Dana O. (customer):** Thank you. Is there any way for us to export invoices in the meantime? We just need May.

**[09:40] Sam (support):** Yes — I can pull a May invoice export for you manually and send a CSV within the hour as a stopgap.

**[10:15] Sam (support):** CSV sent to your finance@ alias. Let me know it arrived.

**[10:18] Dana O. (customer):** Got it, that unblocks close. Appreciated. Still need the page fixed though — we use it daily.

**[11:48] Ravi (engineering):** Hotfix with the index is merged and deploying to production now. Should be live in ~15 min.

**[12:10] Ravi (engineering):** Deployed. Billing page p95 load time back to 0.4s (was timing out at 30s). Please confirm.

**[12:26] Dana O. (customer):** Confirmed, it's fast again for the whole team. Thanks for the quick turnaround — the manual export earlier really helped.

**[12:30] Sam (support):** Glad it's resolved. We'll add monitoring on invoice-page latency and do a short post-incident review. I'll keep this ticket open until the PIR is attached.

**[13:05] Maya (PM, internal note):** Root cause = un-indexed query from Friday's release. Need a backfill check for other large accounts and a perf test gate in CI. Will file follow-ups.

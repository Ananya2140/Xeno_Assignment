# Reconciliation Bridge and Walkthrough
Merchant: `501`  
Timeframe: October 2026  
Final Target Base: `22`
---

## 1. Reconciliation Bridge

| Step | Description | Result | Reason |
| :---: | :--- | :---: | :--- |
| 0 | Naive count (`01_base.sql`) | 30 | (starting point) Joined raw communication logs directly to campaign table with no filtering on failure states or approvals. |
| 1 | Deduplicate by customer (`02_distinct.sql`) | 20 | Collapsed distinct marketing campaigns sent to the same user during the month, which undercounted legitimate reaches. |
| 2 | Deduplicate per campaign (`03_per_campaign.sql`) | 29 | Deduplicated repeat dispatches within the same campaign ID, but didn't account for retries spawning under new child campaign IDs. |
| 3 | Filter on successful delivery status (`04_delivery.sql`) | 26 | Filtered out 4 delivery errors (`status = 1100`), which naturally kept only the final successful message in retry loops. |
| final | Exclude pending/unapproved campaigns (`05_reconcilation.sql`) | 22 | Filtered out 4 records fired under campaign 9004 that were still marked `approval_awaiting`. |

---

## 2. Walkthrough

* Step 0 (`01_base.sql`) - **Count: 30**
  I started by joining `communication_log` and `campaign` for merchant 501 over October. This includes all delivery drops, unapproved campaigns, and retry loops.

* Step 1 (`02_distinct.sql`) - **Count: 20**
Tested `COUNT(DISTINCT customer_id)`, but it over-deduplicated. It collapsed valid, separate campaigns sent to the same user throughout the month.

* Step 2 (`03_per_campaign.sql`) - **Count: 29**
Deduped per campaign ID, removing one redundant send in standalone campaign 9101. However, it missed retries that spawned under separate child campaign IDs.

* Step 3 (`04_delivery.sql`) - **Count: 26**  
Filtered on `delivery_status = 900`. This removed 4 soft failures (`1100`) and cleanly resolved retry chains by keeping only the delivered attempt.

* Final Step (`05_reconcilation.sql`) - **Count: 22**  
Excluded campaign 9004 because it was still flagged `approval_awaiting`. Removing these 4 unapproved dispatches yielded the verified target base of **22**
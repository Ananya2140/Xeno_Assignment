Reconciliation analysis for Merchant 501 (October 2026). Final target base count is **22**.

* **Reconciliation Bridge:** See (Reconcilation.md) for the 5-step table and discovery walkthrough.
* **SQL Queries:** Located in the `/sql` directory (`01_base.sql` to `05_reconcilation.sql`).
* **Run Final Query:**
  ```
  sqlite3 data/comm_log.db < sql/05_reconcilation.sql

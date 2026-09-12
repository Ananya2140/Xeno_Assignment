import csv
import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
MERCHANT_ID = 501

campaigns = [
    (9001, None, "Diwali Cart Recovery - Wave 1", "approved", "processed"),
    (9002, 9001, "Diwali Cart Recovery - Retry A", "approved", "processed"),
    (9003, 9002, "Diwali Cart Recovery - Retry B", "approved", "processed"),
    (9004, 9001, "Diwali Cart Recovery - Retry C (pending)", "approval_awaiting", "processed"),
    (9101, None, "Diwali Flash Sale - Standalone", "approved", "processed"),
    (9201, None, "Diwali Wave 2", "approved", "processed"),
    (9202, 9201, "Diwali Wave 2 - Retry", "approved", "processed"),
]

rows = []
_next_id = [1]

def log_row(communication_id, customer_id, delivery_status, sent_time, credit_used=1):
    cid = _next_id[0]
    _next_id[0] += 1
    rows.append((cid, MERCHANT_ID, communication_id, customer_id, "2", delivery_status, sent_time, sent_time, credit_used, "sms"))

# Family A
log_row(9001, "C1", 900, "2026-10-01 10:00:00")
log_row(9001, "C2", 1100, "2026-10-01 10:00:00")
log_row(9002, "C2", 900, "2026-10-04 10:00:00")
log_row(9001, "C3", 1100, "2026-10-01 10:00:00")
log_row(9002, "C3", 1100, "2026-10-04 10:00:00")
log_row(9003, "C3", 900, "2026-10-05 10:00:00")
for i in range(4, 11):
    log_row(9001, f"C{i}", 900, "2026-10-01 10:00:00")

# Ineligible retry branch
for i in range(11, 15):
    log_row(9004, f"C{i}", 900, "2026-10-06 10:00:00")

# Standalone leaf
log_row(9101, "C20", 900, "2026-10-10 10:00:00")
log_row(9101, "C20", 900, "2026-10-20 10:00:00")
for i in range(21, 26):
    log_row(9101, f"C{i}", 900, "2026-10-15 10:00:00")

# Family B
log_row(9201, "D1", 1100, "2026-10-07 10:00:00")
log_row(9202, "D1", 900, "2026-10-08 10:00:00")
for i in range(2, 6):
    log_row(9201, f"D{i}", 900, "2026-10-07 10:00:00")

def write_csvs():
    with open(DATA_DIR / "campaign.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "merchant_id", "parent_id", "name", "creation_status", "processing_status"])
        for cid, parent_id, name, cs, ps in campaigns:
            w.writerow([cid, MERCHANT_ID, parent_id if parent_id is not None else "", name, cs, ps])

    with open(DATA_DIR / "communication_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "merchant_id", "communication_id", "customer_id", "communication_type", "delivery_status", "sent_time", "scheduled_time", "credit_used", "channel"])
        for r in rows:
            w.writerow(r)

def write_sqlite():
    db_path = DATA_DIR / "comm_log.db"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE campaign (
        id INTEGER PRIMARY KEY,
        merchant_id INTEGER NOT NULL,
        parent_id INTEGER,
        name TEXT NOT NULL,
        creation_status TEXT NOT NULL,
        processing_status TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE communication_log (
        id INTEGER PRIMARY KEY,
        merchant_id INTEGER NOT NULL,
        communication_id INTEGER NOT NULL,
        customer_id TEXT NOT NULL,
        communication_type TEXT NOT NULL,
        delivery_status INTEGER NOT NULL,
        sent_time TEXT NOT NULL,
        scheduled_time TEXT NOT NULL,
        credit_used INTEGER NOT NULL,
        channel TEXT NOT NULL
    );
    """)
    cur.executemany("INSERT INTO campaign VALUES (?,?,?,?,?,?);", [(cid, MERCHANT_ID, parent_id, name, cs, ps) for cid, parent_id, name, cs, ps in campaigns])
    cur.executemany("INSERT INTO communication_log VALUES (?,?,?,?,?,?,?,?,?,?);", rows)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    write_csvs()
    write_sqlite()
    print("Dataset generated successfully.")
import sqlite3

def init_db(db_name="github_analytics.db"):
    """Creates the SQLite database and table if they do not exist."""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pull_requests (
        pr_id INTEGER PRIMARY KEY,
        repo_name TEXT,
        pr_number INTEGER,
        author TEXT,
        created_at TIMESTAMP,
        closed_at TIMESTAMP,
        merged_at TIMESTAMP,
        state TEXT,
        time_to_merge_hours REAL
    );
    """)
    conn.commit()
    conn.close()

def upsert_pr(db_name, pr_data):
    """Inserts a PR record or updates it if it already exists."""
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO pull_requests (
        pr_id, repo_name, pr_number, author, created_at, closed_at, merged_at, state, time_to_merge_hours
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(pr_id) DO UPDATE SET
        closed_at=excluded.closed_at,
        merged_at=excluded.merged_at,
        state=excluded.state,
        time_to_merge_hours=excluded.time_to_merge_hours;
    """, pr_data)
    conn.commit()
    conn.close()
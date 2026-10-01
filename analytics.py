import sqlite3
import pandas as pd

def run_analytics(db_name="github_analytics.db"):
    conn = sqlite3.connect(db_name)
    query = """
    SELECT 
        author,
        COUNT(pr_number) AS total_prs,
        ROUND(COALESCE(AVG(time_to_merge_hours), 0.0), 2) AS avg_merge_hours,
        SUM(CASE WHEN state = 'closed' AND merged_at IS NOT NULL THEN 1 ELSE 0 END) AS merged_count
    FROM pull_requests
    GROUP BY author
    ORDER BY merged_count DESC, total_prs DESC
    LIMIT 10;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print("\n========================================================")
    print("             DEVELOPER VELOCITY REPORT                  ")
    print("========================================================")
    print(df.to_string(index=False))

if __name__ == "__main__":
    run_analytics()
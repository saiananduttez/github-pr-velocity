import requests
from datetime import datetime
from database import init_db, upsert_pr

# Map the active contributors in this dataset to clean names
NAME_MAPPING = {
    "davidism": "David Lord (Lead Maintainer)",
    "sunis2005": "Sunil Sharma",
    "lphuc2250gma": "Phuc Le",
    "ghost": "Deleted Contributor",
    "gasalabi": "Gabriel Salabi",
    "aliunsal": "Ali Unsal",
    "Tarunjit45": "Tarunjit Singh",
    "MervanPalmer": "Mervan Palmer",
    "JosefVacha": "Josef Vacha",
    "0x-aleph-phi-phi-conjugate-null": "Alex Chen",
}

class GitHubCollector:
    def __init__(self, repo_owner, repo_name):
        self.repo = f"{repo_owner}/{repo_name}"
        self.base_url = f"https://api.github.com/repos/{self.repo}/pulls"

    def fetch_recent_prs(self, count=100):
        params = {"state": "all", "per_page": count}
        headers = {"Accept": "application/vnd.github.v3+json"}
        response = requests.get(self.base_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return []
        return response.json()

    def parse_and_load(self, pr_list, db_name="github_analytics.db"):
        for pr in pr_list:
            pr_id = pr.get("id")
            pr_num = pr.get("number")
            raw_author = pr.get("user", {}).get("login", "unknown")
            author = NAME_MAPPING.get(raw_author, raw_author.title())
            
            created_at = pr.get("created_at")
            closed_at = pr.get("closed_at")
            merged_at = pr.get("merged_at")
            state = pr.get("state")

            ttm = None
            if merged_at and created_at:
                t_create = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                t_merge = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
                ttm = round((t_merge - t_create).total_seconds() / 3600, 2)

            upsert_pr(db_name, (pr_id, self.repo, pr_num, author, created_at, closed_at, merged_at, state, ttm))
        print(f"Success: Processed {len(pr_list)} pull requests for {self.repo}.")

if __name__ == "__main__":
    init_db()
    collector = GitHubCollector("pallets", "flask")
    data = collector.fetch_recent_prs(count=100)
    collector.parse_and_load(data)
from github import Github
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github(query="security", limit=8):
    """Safe GitHub fetch with limited requests"""
    try:
        time.sleep(random.uniform(2, 3))  # Delay before request
        
        g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()
        
        repos = g.search_repositories(query=query)
        results = []
        
        for i, repo in enumerate(repos):
            if i >= min(limit, 8):
                break
                
            results.append({
                "platform": "github",
                "user": repo.owner.login,
                "timestamp": str(repo.created_at),
                "text": repo.description or f"Repository: {repo.name}",
                "url": repo.html_url
            })
        
        print(f"GitHub: Collected {len(results)} repos for '{query}'")
        return results
        
    except Exception as e:
        print(f"GitHub error: {e}")
        return []
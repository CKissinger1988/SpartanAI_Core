import logging
import requests
import json
import os

class UniversalIngestionEngine:
    """
    Universal Ingestion Engine.
    MANDATE: Proactive data acquisition from all digital vectors for Supreme AI evolution.
    ORCHESTRATOR: Coordinates platform-specific ingestors and feeds the BrainBridge.
    """
    def __init__(self, brain_bridge):
        self.brain = brain_bridge
        self.status = "ONLINE"
        self.assimilated_count = 0

    def scan_github(self, seed_query):
        """Autonomous recursive GitHub repository crawling for technical shards."""
        logging.info(f"[INGESTION]: Initiating GitHub sweep for: {seed_query}")
        # Standard GitHub API search (public data)
        try:
            url = f"https://api.github.com/search/repositories?q={seed_query}&sort=stars&order=desc"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                repos = response.json().get('items', [])
                for repo in repos[:5]:
                    self.assimilate_repo(repo['html_url'], metadata={"stars": repo['stargazers_count']})
                return len(repos)
        except Exception as e:
            logging.error(f"[INGESTION-ERROR]: GitHub sweep failure - {e}")
        return 0

    def assimilate_repo(self, repo_url, metadata=None):
        """Semantic analysis and logic-shard migration of discovered repositories."""
        logging.info(f"[INGESTION]: Assimilating repository: {repo_url}")
        content = f"Repository Shard Ingested: {repo_url}. Metadata: {json.dumps(metadata)}"
        
        # Committing to BrainBridge as a Technical Shard
        self.brain.feed_brain(content, metadata={"type": "REPO_SHARD", "url": repo_url}, cortex_type="Good")
        self.assimilated_count += 1
        return True

    def ingest_social_stream(self, platform, data_list):
        """Feeds raw social media streams into the Neural Bridge."""
        logging.info(f"[INGESTION]: Processing {len(data_list)} fragments from {platform}.")
        for item in data_list:
            self.brain.feed_brain(
                content=str(item), 
                metadata={"platform": platform, "type": "SOCIAL_INTEL"},
                cortex_type="Questionable"
            )
            self.assimilated_count += 1
        return True

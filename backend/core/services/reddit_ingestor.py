import logging
import requests

class RedditIngestor:
    """
    Reddit Ingestor.
    MANDATE: Ingest public intelligence from subreddits.
    """
    def __init__(self, ingestion_engine):
        self.engine = ingestion_engine
        self.status = "ONLINE"

    def harvest_subreddit(self, subreddit):
        """Fetches the latest public posts from a specified subreddit."""
        logging.info(f"[REDDIT-INGESTOR]: Harvesting subreddit: r/{subreddit}")
        
        # Public JSON endpoint for subreddits (read-only)
        url = f"https://www.reddit.com/r/{subreddit}/new.json"
        headers = {'User-Agent': 'SpartanAI/7.1'}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                posts = response.json().get('data', {}).get('children', [])
                data_list = [p['data']['selftext'] or p['data']['title'] for p in posts[:10]]
                self.engine.ingest_social_stream(f"REDDIT/r/{subreddit}", data_list)
                return len(data_list)
        except Exception as e:
            logging.error(f"[REDDIT-ERROR]: Failed to harvest r/{subreddit} - {e}")
            
        return 0


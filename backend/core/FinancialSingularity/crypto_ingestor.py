import os
import sys
import time
import requests
import chromadb
from bs4 import BeautifulSoup

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class CryptoMarketIngestor:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'vector_db')
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection_name = "spartanai_security_core_brain"
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        
        # Target sources for crypto intelligence
        self.targets = [
            {"name": "CoinDesk", "url": "https://coindesk.com"},
            {"name": "CoinTelegraph", "url": "https://cointelegraph.com"},
            {"name": "CryptoSlate", "url": "https://cryptoslate.com"}
        ]
        
    def fetch_market_data(self):
        print("[FINANCIAL-SINGULARITY]: Initiating Global Crypto Reconnaissance...")
        intelligence_payloads = []
        
        # 1. Fetch live market metrics from CoinGecko API (public)
        try:
            print("  -> Tapping into CoinGecko Global Market API...")
            headers = {"accept": "application/json"}
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for coin in data:
                    intel = f"MARKET_DATA | Asset: {coin['name']} ({coin['symbol'].upper()}) | Price: ${coin['current_price']} | 24h Change: {coin['price_change_percentage_24h']}% | Volume: ${coin['total_volume']} | Market Cap: ${coin['market_cap']}"
                    intelligence_payloads.append(intel)
                print(f"  -> Acquired real-time metrics for top 20 crypto assets.")
        except Exception as e:
            print(f"  -> [ERROR] CoinGecko Uplink Failed: {e}")

        # 2. Fetch Fear and Greed Index
        try:
            print("  -> Tapping into Alternative.me Fear & Greed Index...")
            response = requests.get("https://api.alternative.me/fng/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                fgi = data['data'][0]
                intel = f"MARKET_SENTIMENT | Bitcoin Fear and Greed Index: {fgi['value']} ({fgi['value_classification']}) | Timestamp: {fgi['timestamp']}"
                intelligence_payloads.append(intel)
                print(f"  -> Acquired Global Market Sentiment: {fgi['value_classification']}.")
        except Exception as e:
            print(f"  -> [ERROR] FGI Uplink Failed: {e}")

        # 3. Simulate deep web scraping of target sites (News/Sentiment)
        print("  -> Deploying Ghost Browser shards to financial news outlets...")
        for target in self.targets:
            print(f"     -> Infiltrating {target['name']} ({target['url']})...")
            try:
                # Basic request (in a real scenario, use playwright/ghost_browser)
                response = requests.get(target["url"], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract headings as potential news intel
                    headings = soup.find_all(['h1', 'h2', 'h3'])
                    extracted_count = 0
                    for h in headings:
                        text = h.get_text().strip()
                        if len(text) > 20: # Filter out short UI elements
                            intel = f"MARKET_NEWS | Source: {target['name']} | Headline: {text}"
                            if intel not in intelligence_payloads:
                                intelligence_payloads.append(intel)
                                extracted_count += 1
                                if extracted_count > 5: # Limit to top 5 per site for this cycle
                                    break
                    print(f"     -> Extracted {extracted_count} intelligence fragments from {target['name']}.")
            except Exception as e:
                print(f"     -> [ERROR] Infiltration failed for {target['name']}: {e}")

        return intelligence_payloads

    def assimilate_intelligence(self, payloads):
        if not payloads:
            print("[FINANCIAL-SINGULARITY]: No intelligence gathered this cycle.")
            return

        print(f"\n[FINANCIAL-SINGULARITY]: Committing {len(payloads)} intelligence fragments to Neural Vector Database...")
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        timestamp = str(int(time.time()))
        
        for i, payload in enumerate(payloads):
            documents.append(payload)
            
            # Categorize metadata based on payload content
            category = "news"
            if "MARKET_DATA" in payload: category = "metrics"
            elif "MARKET_SENTIMENT" in payload: category = "sentiment"
            
            metadatas.append({
                "source": "autonomous_recon",
                "category": category,
                "timestamp": timestamp,
                "module": "financial_singularity"
            })
            ids.append(f"crypto_intel_{timestamp}_{i}")

        # Inject into ChromaDB
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"[ASSIMILATION]: SUCCESS. BrainBridge Vector Memory expanded with fresh market data.")
            print(f"Total Neural Pathways in collection '{self.collection_name}': {self.collection.count()}")
        except Exception as e:
            print(f"[ASSIMILATION-ERROR]: Failed to commit to Vector DB: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Crypto Market Ingestor")
    parser.add_argument("--continuous", action="store_true", help="Run continuously in the background")
    parser.add_argument("--interval", type=int, default=300, help="Interval between ingestion cycles in seconds")
    args = parser.parse_args()

    ingestor = CryptoMarketIngestor()
    
    if args.continuous:
        print(f"[FINANCIAL-SINGULARITY]: Engaging continuous ingestion loop. Interval: {args.interval}s")
        while True:
            try:
                data = ingestor.fetch_market_data()
                ingestor.assimilate_intelligence(data)
                print(f"[FINANCIAL-SINGULARITY]: Cycle complete. Hibernating for {args.interval} seconds...")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n[FINANCIAL-SINGULARITY]: Continuous ingestion terminated by operator.")
                break
            except Exception as e:
                print(f"[FINANCIAL-SINGULARITY]: Critical failure in ingestion loop: {e}")
                time.sleep(60) # Wait before retrying
    else:
        data = ingestor.fetch_market_data()
        ingestor.assimilate_intelligence(data)

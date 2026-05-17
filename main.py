import time
from datetime import datetime

from core.scraper import DarkWebScraper
from core.analyzer import load_keywords, analyze
from database.mongo_handler import save_data
from database.elastic_handler import index_data
from alerts.email_alert import send_alert
from alerts.notifier import Notifier
from core.parser import DataParser
from utils.helpers import get_timestamp

#from ml.anomaly_detector import AnomalyDetector


# =========================
# CONFIG
# =========================
DARKWEB_URLS = [
    "http://host.docker.internal:8000/leak1.html",
    "http://host.docker.internal:8000/leak2.html",
    "http://example.com",
    "http://host.docker.internal:8000/leak3.html",
    "http://host.docker.internal:8000/leak4.html",
    "http://host.docker.internal:8000/leak5.html",
    "http://host.docker.internal:8000/leak6.html",
    "http://host.docker.internal:8000/leak7.html",
    "http://host.docker.internal:8000/leak8.html"
]

SCRAPE_INTERVAL = 30  # seconds


# =========================
# INIT COMPONENTS
# =========================
scraper = DarkWebScraper(DARKWEB_URLS)
keywords = load_keywords("data/keywords.txt")

notifier = Notifier()
parser = DataParser()


# =========================
# MAIN LOOP
# =========================
def run_monitoring():
    print("🚀 Dark Web Monitoring Service Started")

    while True:
        try:
            print("\n==============================")
            print(f"🔄 Scan started at {datetime.now()}")
            print("==============================")

            # 1. Fetch data
            raw_data = scraper.fetch()
            print(f"📡 Fetched {len(raw_data)} items")

            # fallback safety
            if not raw_data:
                print("⚠ No data fetched — using fallback test data")
                raw_data = [
                    {
                        "url": "local-test",
                        "content": "email: test@test.com password: 1234"
                    }
                ]

            # =========================
            # 2. Parse Data
            # =========================
            for item in raw_data:
                content = item.get("content", "")

                # keyword detection (optional, retained)
                analyze(content, keywords)

                parsed = parser.parse_all(content)

                item["parsed_data"] = parsed
                item["timestamp"] = get_timestamp()

            # =========================
            # 3. AI Anomaly Detection
            # =========================
            #detector = AnomalyDetector()

            #try:
                #detector.fit(raw_data)
                #raw_data = detector.predict(raw_data)
                #print("🧠 Anomaly detection completed")
            #except Exception as e:
                #print("⚠ Anomaly detection error:", e)

            # =========================
            # 4. Alert Logic (UPDATED)
            # =========================
            alerts = []

            for item in raw_data:
                parsed = item.get("parsed_data", {})

                # 🚨 AI-based anomaly alert
                if item.get("is_anomaly"):
                    msg = f"🚨 Anomaly detected in {item['url']} (Score: {item['anomaly_score']})"
                    print(msg)
                    alerts.append(msg)
                    notifier.notify(msg)

                # 🔥 High-risk fallback (email + password)
                elif parsed.get("emails") and parsed.get("passwords"):
                    msg = f"🔥 High-risk leak in {item['url']} (email + password)"
                    print(msg)
                    alerts.append(msg)
                    notifier.notify(msg)

            # =========================
            # 5. Store in MongoDB
            # =========================
            try:
                save_data(raw_data)
            except Exception as e:
                print("⚠ MongoDB error:", e)

            # =========================
            # 6. Index in Elasticsearch
            # =========================
            try:
                index_data(raw_data)
            except Exception as e:
                print("⚠ Elasticsearch error:", e)

            # =========================
            # 7. Send Email Alerts
            # =========================
            if alerts:
                try:
                    send_alert("\n".join(alerts))
                    print("🚨 Alerts sent")
                except Exception as e:
                    print("⚠ Alert error:", e)
            else:
                print("ℹ No alerts triggered")

            print("✅ Cycle completed successfully")

        except Exception as e:
            print("❌ Unexpected error in loop:", e)

        # wait before next scan
        time.sleep(SCRAPE_INTERVAL)


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run_monitoring()

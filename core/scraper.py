import requests
from bs4 import BeautifulSoup

class DarkWebScraper:
    def __init__(self, urls):
        self.urls = urls

    def fetch(self):
        data = []

        for url in self.urls:
            try:
                if ".onion" in url:
                    proxies = {
                        "http": "socks5h://tor:9050",
                        "https": "socks5h://tor:9050"
                    }
                    response = requests.get(url, proxies=proxies, timeout=30)
                else:
                    response = requests.get(url, timeout=10)

                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()

                data.append({
                    "url": url,
                    "content": text
                })

            except Exception as e:
                print(f"Error: {url} -> {e}")

        return data

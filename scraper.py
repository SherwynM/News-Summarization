import requests
from bs4 import BeautifulSoup
import time
import urllib.parse  

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def extract_full_article(article_url):
    response = requests.get(article_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='content_wrapper')
        if content_div:
            paragraphs = content_div.find_all('p')
            full_content = ' '.join(p.get_text(strip=True) for p in paragraphs)
            return full_content
        else:
            print(f"Content area not found in {article_url}")
            return None
    else:
        print(f"Failed to retrieve {article_url}")
        return None

def extract_news(tag):
    # URL-encode the tag to handle spaces and special characters.
    tag_encoded = urllib.parse.quote(tag)
    base_url = f"https://www.moneycontrol.com/news/tags/{tag_encoded}.html"
    urls = [base_url] + [f"{base_url}/page-{i}/" for i in range(2, 3)]
    news_data = []

    for url in urls:
        print(f"Scraping {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            container = soup.find('ul', id='cagetory')
            if container:
                articles = container.find_all('li', class_='clearfix')
                # Restrict to 2 articles per page (update comment if needed)
                articles = articles[:2]
                for article in articles:
                    heading_tag = article.find('h2')
                    heading = heading_tag.get_text(strip=True) if heading_tag else "No heading"
                    link_tag = article.find('a', href=True)
                    article_url = link_tag['href'] if link_tag else None
                    full_content = extract_full_article(article_url) if article_url else "No URL"

                    news_data.append({
                        "Title": heading,
                        "URL": article_url,
                        "Full Content": full_content,
                        "Summary": "",  
                        "Sentiment": "",  
                        "Topics": ""
                    })
                    time.sleep(1)  # Delay
            else:
                print("No container found on this page.")
        else:
            print(f"Failed to retrieve {url}")
    return news_data

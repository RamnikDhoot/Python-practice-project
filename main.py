from http.client import REQUEST_ENTITY_TOO_LARGE
from urllib import request
import aiohttp
import asyncio
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from dotenv import load_dotenv
import argparse
import random
import schedule
import time
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["articles"]

def save_to_db(data):
    collection.insert_one(data)

def job():
    print("Scraping...")

schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Command-line arguments
parser = argparse.ArgumentParser(description="News Web Scraper")
parser.add_argument('--category', help='Category to scrape', default='')
parser.add_argument('--pages', help='Number of pages to scrape', type=int, default=1)
parser.add_argument('--output', help='Output CSV file name', default=f"news_headlines_{datetime.now().strftime('%Y-%m-%d')}.csv")
args = parser.parse_args()

USER_AGENTS = [
    # List of user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
    # Adding more user agents later
]
def save_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'URL', 'Publication Date'])
        writer.writerows(articles)

async def fetch(session, url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        async with session.get(url, headers=headers) as response:
            return await response.text()
    except Exception as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None
def get_news_data(url, category=None):
    try:
        response = request.get(url)
        response.raise_for_status()
    except REQUEST_ENTITY_TOO_LARGE.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []

    # Define the logic to fetch articles from different categories if specified
    if category:
        category_section = soup.find('section', id=category)
        if not category_section:
            print(f"No category section found for {category}")
            return []
        headlines = category_section.find_all('h2')
    else:
        headlines = soup.find_all('h2')

    for tag in headlines:
        headline = tag.get_text().strip()
        article_url = tag.find('a')['href'] if tag.find('a') else 'No URL'
        date_tag = tag.find('span', class_='date')
        pub_date = date_tag.get_text() if date_tag else 'No Date'
        articles.append((headline, article_url, pub_date))

    return articles

def clean_data(data):
    ##################
    return cleaned_data




def main():
    url = 'https://www.bbc.co.uk/news'  
    print("Sports") #Category to scrape
    category = input().strip()
    
    print("1") #How many pages to scrape
    num_pages = int(input().strip() or 1)

    all_articles = []
    for page in range(1, num_pages + 1):
        page_url = f"{url}/page/{page}"
        if category:
            page_url += f"/{category}"
        articles = get_news_data(page_url, category)
        all_articles.extend(articles)

    if all_articles:
        print("News Headlines:")
        for i, (headline, url, date) in enumerate(all_articles, 1):
            print(f"{i}. {headline} (Date: {date}) - {url}")

        # Save to CSV
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"news_headlines_{today}.csv"
        save_to_csv(all_articles, filename)
        print(f"\nData saved to {filename}")

if __name__ == "__main__":
    main()

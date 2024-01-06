import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_news_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for tag in soup.find_all('h2'):  # Assuming headlines are in <h2> tags 
        headline = tag.get_text().strip()
        article_url = tag.find('a')['href'] if tag.find('a') else 'No URL'
        # Assuming the publication date is in a <span> with class 'date' 
        date_tag = tag.find('span', class_='date')
        pub_date = date_tag.get_text() if date_tag else 'No Date'

        articles.append((headline, article_url, pub_date))

    return articles

def save_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'URL', 'Publication Date'])
        writer.writerows(articles)

def main():
    url = 'https://www.bbc.co.uk/news'  
    articles = get_news_data(url)

    if articles:
        print("News Headlines:")
        for i, (headline, url, date) in enumerate(articles, 1):
            print(f"{i}. {headline} (Date: {date}) - {url}")

        # Save to CSV
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"news_headlines_{today}.csv"
        save_to_csv(articles, filename)
        print(f"\nData saved to {filename}")

if __name__ == "__main__":
    main()

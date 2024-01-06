import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_news_data(url, category=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
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

def save_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'URL', 'Publication Date'])
        writer.writerows(articles)

def main():
    url = 'https://www.bbc.co.uk/news'  
    print("Enter a category to scrape (e.g., sports, politics), or leave blank for general headlines:")
    category = input().strip()
    
    print("Enter the number of pages to scrape (default is 1):")
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

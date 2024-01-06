import requests
from bs4 import BeautifulSoup

def get_news_headlines(url):
    # Send a request to the website
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract headlines: Assuming headlines are in <h2> tags (change as needed)
    headlines = soup.find_all('h2')
    return [headline.get_text() for headline in headlines]

def main():
    url = 'https://example-news.com'  # Replace with the actual URL
    headlines = get_news_headlines(url)
    for i, headline in enumerate(headlines, 1):
        print(f"{i}. {headline}")

if __name__ == "__main__":
    main()

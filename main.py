import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import time
import re
import gzip
import zlib
import brotli
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

def save_text_to_file(text, filename):
    with open(f"./scraped_text/{filename}.txt", "w", encoding='utf-8') as file:
        file.write(text)


def keyword_filter(text, keywords):
    # Tokenize and lemmatize the text and keywords
    text_words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text)]
    lemmatized_keywords = [lemmatizer.lemmatize(keyword.lower()) for keyword in keywords]

    # Check if any of the specified keywords appear in the text
    for keyword in lemmatized_keywords:
        regex = r'\b' + re.escape(keyword) + r'\b'
        if any(re.search(regex, word) for word in text_words):
            return True
    return False
  
def find_news_with_matching_keywords(domain, delay, keywords):
    def extract_text_from_article(url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])
        return article_text

    def find_article_links(url):
      response = requests.get(url, headers=headers)
      soup = BeautifulSoup(response.content, "html.parser")

      # Remove unnecessary sections like navlinks and footlinks
      for nav in soup.find_all("nav"):
          nav.decompose()
      for footer in soup.find_all("footer"):
          footer.decompose()

      # Find internal article links
      article_links = []
      domain_parsed = urlparse(url)
      for link in soup.find_all("a", href=True):
          href = link["href"]
          print(f"Found link: {href}")
          href_parsed = urlparse(href)
          if (href_parsed.netloc == domain_parsed.netloc or not href_parsed.netloc) and '2023' in href:
              article_links.append(urljoin(url, urldefrag(href)[0]))
              
      print(f"Link List: {article_links}")
      return list(set(article_links))

    texts = []
    article_links = find_article_links(domain)
    print(f"Found {len(article_links)} articles")
    for link in article_links:
        time.sleep(delay)
        article_text = extract_text_from_article(link)
        print(f"Extracted text from article: {link}")
        if keyword_filter(article_text, keywords):
            save_text_to_file(article_text, urlparse(link).path.split("/")[-1])
            texts.append(article_text)
            print(f"Saved article: {link}")

    return texts


def main(): 
  newsSources = ["https://finance.yahoo.com/crypto/",
  "https://seekingalpha.com/market-news"]
  
  keywords = [
    "Digital asset custody",
    "Cryptocurrency security",
    "Institutional crypto services",
    "Crypto asset management",
    "Blockchain technology",
    "Digital asset trading",
    "Cryptocurrency lending",
    "Trust company",
    "Crypto portfolio management",
    "Crypto tax software",
    "Digital asset storage",
    "Crypto prime brokerage",
    "Crypto API and SDK",
    "Digital asset settlement",
    "Virtual currency business",
    "Crypto financial services",
  ]
  
  for newsSource in newsSources:
    find_news_with_matching_keywords(domain=newsSource, delay=2, keywords=keywords)
    
  # texts = find_news_with_matching_keywords(domain=newsSource, delay=2, keywords=keywords)
  
  print('Done.')


if __name__ == "__main__":
    main()
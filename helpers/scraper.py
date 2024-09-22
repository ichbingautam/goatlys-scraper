from bs4 import BeautifulSoup
import requests
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
import sqlite3
import requests.adapters
from requests.adapters import HTTPAdapter
from models.product import Product

class Scraper:
  def __init__(self, config):
    self.config = config
    self.session = requests.Session()
    self.adapter = HTTPAdapter(max_retries=3)  # Retry up to 3 times with backoff
    self.session.mount('http://', self.adapter)
    self.session.mount('https://', self.adapter)

  def scrape_page(self, page_num) -> List[Product]:
    url = f"{self.config.BASE_URL}?page={page_num}"
    headers = {"Authorization": f"Bearer {self.config.STATIC_TOKEN}"}
    try:
      response = self.session.get(url, headers=headers)
      response.raise_for_status()
    except requests.exceptions.RequestException as e:
      print(f"Error scraping page {page_num}: {e}")
      raise
    contents = response.content
    soup = BeautifulSoup(contents, 'html.parser')
    products = []
    for item in soup.find_all('li', class_='product'):
      name = item.find('h2', class_='woo-loop-product__title').text() if item.find('h2', class_='woo-loop-product__title') else 'N/A'
      price = item.find('span', class_='woocommerce-Price-amount.amount').text() if item.find('span', class_='woocommerce-Price-amount.amount') else 'N/A'
      image = item.find('img', class_='attachment-woocommerce_thumbnail')['src'] if item.find('img', class_='attachment-woocommerce_thumbnail') else 'N/A'
      product = Product(product_title=name, product_price=price, path_to_image=image)
      products.append(product)
    return products
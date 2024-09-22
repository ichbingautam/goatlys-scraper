from fastapi import FastAPI, Query, HTTPException, Depends
import requests
from pydantic import BaseModel, Field
import requests.adapters
import uvicorn
from typing import List, Optional, Annotated
from models.product import Product
from config.db_config import Config
from fastapi import APIRouter
from dependencies.auth_helper import get_current_user
from helpers.database import Database
from helpers.scraper import Scraper
router = APIRouter()
app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello Atlys!!!"}

@app.get("/scrape", dependencies=[Depends(get_current_user)])
async def scrape(pages: Annotated[int, Query(ge=1, le=10)] = Config.MAX_PAGES, proxy: Optional[str] = None):
  db = Database("products.db")
  scraper = Scraper(Config)
  total_scraped = 0
  total_updated = 0
  for page_num in range(1, pages + 1):
      products = scraper.scrape_page(page_num)
      for product in products:
          cached_price = db.get_cached_price(product.product_title)
          if not cached_price or cached_price != product.product_price:
              db.insert_product(product)
              db.store_cache_price(product.product_title, product.product_price)
              total_updated += 1
      total_scraped += len(products)
  db.close()
  print(f"Scraped {total_scraped} products. Updated {total_updated} products in the database.")
  return {"message": f"Scraped {total_scraped} products. Updated {total_updated} products."}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8181)
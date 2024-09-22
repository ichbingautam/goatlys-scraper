# Atlys Scraper
  1. Implemented the scrape API to scrape product data and store them in the database.
  2. Implemented the cache mechanism to retrieve data and in case of a miss, update the store
  3. Implemented the auth mechanism to authenticate the request with a `Bearer` token.
  ## Setup
    pip3 install -r requirements.txt
  ## Run Server
    uvicorn main:app --port 8181  --reload
  ## API request
    curl -X GET "http://localhost:8181/scrape" \
      -H "Authorization: Bearer 80bef3cb4339d58442fdb3959a43732e7d58680ee3b2a9bf847987886ee2cbd40a0a3ff58ffc3e16f0746b8e09c66e37a3cf0ca03ab530964e4d43e494434b8f"
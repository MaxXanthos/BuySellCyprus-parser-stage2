# BuySell Parser (Stage 2)

High-performance real estate parser from the [BuySellCyprus](https://www.buysellcyprus.com/) website.
It collects detailed information about each property and stores the results in a PostgreSQL database.
---

## Features

- Extracts:
  - Title
  - Price in EUR
  - Region and City
  - Coordinates (Latitude, Longitude)
  - Description
  - Key Features
  - Photo URLs
  - Agency Name
  - Registration & License information
- Bypass Cloudflare and other bot protections (via selenium-stealth and proxy)
- Proxy rotation support [Webshare](webshare.io)
- Uses `ThreadPoolExecutor` for concurrent processing
- Batch inserts into the database for performance and stability

---

## Installation


---

## Project structure

---

## Feedback
If you find a bug or want to suggest an improvement, open [issue](https://github.com/MaxXanthos/BuySellCyprus-parser2/issues).
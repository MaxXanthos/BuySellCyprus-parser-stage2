# BuySell Parser (Stage 2)

High-performance real estate parser from the [BuySellCyprus](https://www.buysellcyprus.com/) website.
Parses individual listing pages and stores structured property data in a PostgreSQL database.
Handles Cloudflare protection, dynamic JS content, and bot detection via Selenium and stealth techniques.
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

1. **Clone the repository**
    ```bash
   git clone https://github.com/yourusername/BuySellCyprus-parser2.git
    cd BuySellCyprus-parser2
    ```
2. **Create and activate a virtual environment**
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install dependencies**
    ```bash
   pip install -r requirements.txt
   ```
4. **Configure the project**
   - Edit the `config.py`file and set your database and parsing parameters.
   - Run the `proxy_writer.py` file to write your proxy
---
5. **Run the parser**
    ```bash
    python main.py
    ```

## Project structure

- BuySellCyprus-parser-stage2/
  - core/ — Driver logic and progress management
    - __init__.py
    - driver_manager.py
  - data/ — Data files
    - many_proxy.json
    - parser.lock
  - extensions/
    - __init__.py
    - proxy_extension.py
  - proxy_manager/ — Everything related to proxies
    - __init__.py
    - many_proxy.py
    - proxy_writer.py
  - main.py
  - parser
  - config.py
  - db_utils.py
  - lock_utils.py
  - README.md
  - requirements.txt
  - .gitignore

---

## Feedback
If you find a bug or want to suggest an improvement, open [issue](https://github.com/MaxXanthos/BuySellCyprus-parser-stage2/issues).
import json


DATABASE_URL = "postgresql+psycopg2://postgres:123123000@localhost:5432/postgres"
#   postgresql://USER_NAME:PASSWORD@EXTERNAL_HOST:PORT/DATABASE_NAME

WEBSHAREIO_PROXY_API_KEY = ""


# Параметры
MAX_RETRIES = 3
BATCH_SIZE = 10
MAX_WORKERS = 4


QUERY = """
SELECT a.id, a.link
FROM buysellcyprus1 a
LEFT JOIN buysellcyprus2 b ON a.id = b.id
WHERE b.id IS NULL
   OR b.price IS DISTINCT FROM a.price
LIMIT 30
"""


# [Files]
LOCK_FILE = "data/parser.lock"
PROXY_PATH = "data/many_proxy.json"


with open(PROXY_PATH, "r") as f:
    proxies = json.load(f)
if not proxies:
    raise ValueError("Прокси список пуст")
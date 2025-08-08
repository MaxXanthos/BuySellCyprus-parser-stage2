from proxy_manager.many_proxy import fetch_all_webshare_proxies
from config import WEBSHAREIO_PROXY_API_KEY

proxies = fetch_all_webshare_proxies(WEBSHAREIO_PROXY_API_KEY)

from urllib.parse import urlparse
from config import PROXY_PATH

def parse_proxy(proxy_str):
    # proxy_str пример: "http://username:password@104.239.88.88:5708"
    parsed = urlparse(proxy_str)
    # parsed.username, parsed.password, parsed.hostname, parsed.port

    return {
        "username": parsed.username,
        "password": parsed.password,
        "proxy_address": parsed.hostname,
        "port": parsed.port
    }

proxies_dicts = [parse_proxy(p) for p in proxies]

import json

with open(PROXY_PATH, "w", encoding="utf-8") as f:
    json.dump(proxies_dicts, f, ensure_ascii=False, indent=4)
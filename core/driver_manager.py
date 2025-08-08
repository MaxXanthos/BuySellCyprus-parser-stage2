from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from extensions.proxy_extension import create_proxy_auth_extension

import uuid
from tempfile import gettempdir

def get_driver_with_proxy(proxy_data):
    ip = proxy_data["proxy_address"]
    port = proxy_data["port"]
    username = proxy_data["username"]
    password = proxy_data["password"]

    pluginfile_path = Path(gettempdir()) / f"proxy_auth_plugin_{uuid.uuid4().hex}.zip"
    create_proxy_auth_extension(ip, port, username, password, pluginfile_path)

    chrome_options = Options()

    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Быстродействие (ускоряет запуск, может палиться, но эффективно)
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    # Маскировка
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.5845.140 Safari/537.36"
    )

    # WebRTC отключение (IP защита)
    chrome_options.add_argument("--disable-webrtc")

    # Прокси как расширение
    chrome_options.add_extension(str(pluginfile_path))

    # повышаю скорость JS загрузки на фоне
    chrome_options.add_argument("--disable-renderer-backgrounding")


    service = Service(ChromeDriverManager().install(), log_path="NUL")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    stealth(driver,
            languages = ("en-US", "en"),
            vendor = "Google Inc.",
            platform = "Win64",
            webgl_vendor = "NVIDIA Corporation",
            renderer = "NVIDIA GeForce RTX 3060/PCIe/SSE2",
            fix_hairline=True,
            )

    # Удаление navigator.webdriver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                """
        }
    )

    driver.set_page_load_timeout(15)
    #driver.implicitly_wait(0)

    if not pluginfile_path.exists():
        raise FileNotFoundError(f"[ERROR] Расширение не создано: {pluginfile_path}")

    return driver, pluginfile_path
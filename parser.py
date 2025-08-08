import time
import random
import re
import ast

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from core.driver_manager import get_driver_with_proxy
from config import MAX_RETRIES, proxies


# ========== Main part ==========  start
def parse_property_page(link):
    start_time = time.time()

    property_data = {
        "link": link,
        "title": "N/A",
        "price": None,
        "region": "N/A",
        "city": "N/A",
        "latitude": None,
        "longitude": None,
        "description": "N/A",
        "photos": [],
        "key_features": [],
        "agency": "N/A",
        "registration_and_license": "N/A"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        proxy_data = random.choice(proxies)
        driver, pluginfile_path = get_driver_with_proxy(proxy_data)

        try:
            driver.get(link)

            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']"))
            )

            if any(error in driver.page_source for error in ["Checking your browser", "Access denied", "cf-browser-verification"]) or len(driver.page_source.strip()) < 500:
                raise Exception("Страница не загрузилась или заблокирована")


            # кодовое имя объекта ищу
            try:
                property_data["title"] = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']").text.strip()
            except Exception:
                print(f"[{attempt}] Failed to extract title: {link}")

            # ищу цену объекта (в евро)
            try:
                price_text = driver.find_element(By.CSS_SELECTOR, "span.bs-listing-title-price-base").text.strip()
                digits = re.sub(r"[^\d.]", "", price_text.replace(",", ""))
                property_data["price"] = float(digits) if digits else None
            except Exception:
                print(f"[{attempt}](Very rarely, but sometimes there is no price there) Failed to extract price: {link}")

            # регион и город
            try:
                location = driver.find_element(By.CSS_SELECTOR, "meta[itemprop='streetAddress']").get_attribute("content")
                parts = location.split(",")
                property_data["city"] = parts[1].strip() if len(parts) > 1 else "N/A"
                property_data["region"] = parts[0].strip() if len(parts) > 1 else "N/A"
            except Exception:
                print(f"[{attempt}] Failed to extract region and city: {link}")

            # координаты
            try:
                html = driver.page_source
                pattern = r"showGridItemMap\((\{.*?\})\);"
                match = re.search(pattern, html)
                if match:
                    js_data_raw = match.group(1)
                    js_data_fixed = js_data_raw.replace("false", "False").replace("true", "True").replace("null", "None")

                    data = ast.literal_eval(js_data_fixed)
                    property_data["latitude"] = float(data.get("centerLat", None))
                    property_data["longitude"] = float(data.get("centerLng", None))
                else:
                    print(f"[{attempt}] showGridItemMap not found for {link}")
                    property_data["latitude"] = None
                    property_data["longitude"] = None

            except Exception as e:
                print(f"[{attempt}] Failed to extract coordinates: {e}")
                property_data["latitude"] = None
                property_data["longitude"] = None

            # описание
            try:
                property_data["description"]  = driver.find_element(By.CSS_SELECTOR,"p.description-text[itemprop='description']").text.strip()
            except Exception:
                print(f"[{attempt}] Failed to extract description: {link}")

            # Key Features
            try:
                WebDriverWait(driver, 3).until(
                    ec.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.bs-listing-info-features-list ul#multi-column li span")
                    ))
                features = driver.find_elements(By.CSS_SELECTOR,"div.bs-listing-info-features-list ul#multi-column li span")
                property_data["key_features"] = [span.text.strip() for span in features if span.text.strip()]
            except Exception:
                print(f"[{attempt}] Failed to extract Key Features: {link}")

            # Ссылки на фото
            try:
                images = driver.find_elements(By.CSS_SELECTOR, "img.js-lazy-image.swiper-slide-img")
                property_data["photos"] = [img.get_attribute("data-src") for img in images if img.get_attribute("data-src")]
            except Exception:
                print(f"[{attempt}]Failed to extract photo's URLs: {link}")

            # название агенства
            try:
                meta_desc = driver.find_element(By.CSS_SELECTOR, "meta[name = 'description']").get_attribute("content")
                if "by " in meta_desc:
                    property_data["agency"] = meta_desc.split("by ")[1].split(" on ")[0].strip()
            except Exception:
                print(f"[{attempt}] Failed to extract name of agency: {link}")

            # регистрация и лицензия
            try:
                footnote = WebDriverWait(driver, 3).until(
                    ec.presence_of_element_located((By.CLASS_NAME, "footnote"))
                )
                reg_lic_text = footnote.get_attribute("innerText").strip()
                property_data["registration_and_license"] = reg_lic_text
            except Exception:
                print(f"[{attempt}](Sometimes there is no registration or license) Failed to extract registration and license of agency: {link}")

            duration_for_one = time.time() - start_time

            print(f"Parsed {link} in {duration_for_one:.2f} seconds")
            return property_data

        except Exception as e:
            print(f"[{attempt}] Fail of parsing {link}: {e}")
            time.sleep(1)


        finally:
            try:
                driver.quit()
            except Exception as e:
                print(f"[WARNING] Ошибка при закрытии драйвера: {e}")
            try:
                if pluginfile_path and pluginfile_path.exists():
                    pluginfile_path.unlink()
            except Exception as e:
                print(f"[WARNING] Не удалось удалить расширение: {e}")

    print(f"Failed to parse {link} after {MAX_RETRIES} attempts.")

    duration_for_driver = time.time() - start_time
    print(f"Failed to parse {link} after {MAX_RETRIES} attempts. Time spent: {duration_for_driver:.2f} seconds")


    return property_data
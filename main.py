import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import BATCH_SIZE , QUERY, MAX_WORKERS
from parser import parse_property_page
from db_utils import insert_rows_to_db, engine
from lock_utils import acquire_lock, release_lock

def main():
    start_time = time.time()

    df_links = pd.read_sql(QUERY, engine)
    if df_links.empty:
        print("Нет новых или изменённых ссылок для парсинга.")
        return

    print(f"Найдено {len(df_links)} новых или изменённых объектов для парсинга.")
    results_batch = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_id = {
            executor.submit(parse_property_page, row['link']): row['id']
            for _, row in df_links.iterrows()
        }

        for future in as_completed(future_to_id):
            property_id = future_to_id[future]
            try:
                result = future.result()
                result['id'] = property_id
                results_batch.append(result)

                if len(results_batch) >= BATCH_SIZE:
                    insert_rows_to_db(results_batch)
                    results_batch = []

            except Exception as e:
                print(f"Error while processing {property_id}: {e}")

    if results_batch:
        insert_rows_to_db(results_batch)

    total_time = time.time() - start_time
    print(f"\nПарсинг завершён за {total_time:.2f} секунд для {len(df_links)} объектов.")
    print(f"Среднее время на объект: {total_time / len(df_links):.2f} секунд.")


if __name__ == "__main__":
    if not acquire_lock():
        print("Другой процесс уже выполняется. Завершение текущего запуска.")
    else:
        try:
            main()
        finally:
            release_lock()
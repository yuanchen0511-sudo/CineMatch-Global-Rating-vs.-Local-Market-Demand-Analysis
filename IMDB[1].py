import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. 設定儲存路徑
# 根據你的需求，指定到 02_ML 下的 data 資料夾
save_path = r"C:\Users\user\Desktop\2026Python\02_ML-20260306T070809Z-1-001\02_ML\data"

# 如果該資料夾不存在，自動建立它
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 2. 啟動瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    url = "https://www.imdb.com/chart/moviemeter/?ref_=sr_nv_menu"
    print(f"正在連線至：{url}")
    driver.get(url)
    time.sleep(5) # 等待頁面動態內容載入
    
    # 3. 執行抓取
    movie_items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
    scraped_data = []
    
    for item in movie_items[:50]: # 練習抓取前 50 名
        try:
            # 抓取標題
            title = item.find_element(By.CLASS_NAME, "ipc-title__text").text
            
            # 抓取年份
            metadata = item.find_elements(By.CLASS_NAME, "cli-title-metadata-item")
            year = metadata[0].text if len(metadata) > 0 else "N/A"
            
            # 抓取評分
            try:
                rating_text = item.find_element(By.CLASS_NAME, "ipc-rating-star--imdb").text
                rating = rating_text.split()[0]
            except:
                rating = "N/A"
            
            scraped_data.append({
                "Title": title,
                "Year": year,
                "Rating": rating
            })
            print(f"已讀取: {title}")
        except:
            continue

    # 4. 存檔至指定路徑
    df = pd.DataFrame(scraped_data)
    final_file_path = os.path.join(save_path, "imdb_popular_movies.csv")
    df.to_csv(final_file_path, index=False, encoding="utf-8-sig")
    
    print("\n" + "="*60)
    print(f"【存檔成功！】檔案已歸類至：\n{final_file_path}")
    print("="*60)

finally:
    driver.quit()
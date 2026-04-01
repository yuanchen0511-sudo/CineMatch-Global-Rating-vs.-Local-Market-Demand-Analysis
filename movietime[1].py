import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import pandas as pd
import re

# 1. 設定與初始化
days_to_fetch = 7
today = datetime.now()
date_list = [(today + timedelta(days=i)).strftime('%Y/%m/%d') for i in range(days_to_fetch)]

theaters = {
    "微風國賓": "84b87b82-b936-4a39-b91f-e88328d33b4e",
    "台北長春國賓": "453b2966-f7c2-44a9-b2eb-687493855d0e",
    "新莊晶冠國賓": "3301d822-b385-4aa8-a9eb-aa59d58e95c9",
    "林口昕境國賓": "9383c5fa-b4f3-4ba8-ba7a-c25c7df95fd0",
    "淡水禮萊國賓": "1e42d235-c3cf-4f75-a382-af60f67a4aad",
    "八德廣豐國賓": "8fda9934-73d4-4c14-b1c4-386c2b81045c",
    "高雄義大國賓": "ec07626b-b382-474e-be39-ad45eac5cd1c",
    "屏東環球國賓": "41aae717-4464-49f4-ac26-fec2d16acbd6",
}

all_results = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"🚀 開始抓取未來 {days_to_fetch} 天的場次資料...")

# 2. 爬蟲核心迴圈
for theater_name, theater_id in theaters.items():
    for date in date_list:
        url = f"https://www.ambassador.com.tw/home/Showtime?ID={theater_id}&DT={date}"
        print(f"正在抓取：{theater_name} | 日期：{date}...", end="\r")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 國賓網頁的場次區塊通常在 cell-showtime-theater 內
            movie_blocks = soup.select('div.showtime-item')
            
            for block in movie_blocks:
                # 取得電影名稱 (過濾空白與特殊字元)
                title_tag = block.find('h3')
                if not title_tag: continue
                title = title_tag.get_text(strip=True).split('|')[0].strip()
                
                # 取得該電影的所有時間點
                time_list = block.find_all('li')
                for t_item in time_list:
                    time_str = t_item.get_text(strip=True)
                    # 使用正則表達式只抓取 HH:MM 格式
                    clean_times = re.findall(r'\d{2}:\d{2}', time_str)
                    
                    for t in clean_times:
                        all_results.append({
                            "影城": theater_name,
                            "日期": date,
                            "電影名稱": title,
                            "場次時間": t
                        })
            
            time.sleep(1) # 縮短一點點等待時間，提高效率
            
        except Exception as e:
            print(f"\n❌ 抓取 {theater_name} ({date}) 時發生錯誤: {e}")

# 3. 資料處理與統計
if all_results:
    df = pd.DataFrame(all_results)
    
    # 存出原始明細檔
    df.to_csv("ambassador_raw_data.csv", index=False, encoding="utf-8-sig")
    
    # --- 統計功能 ---
    # 統計每部電影的總場次
    movie_stats = df.groupby('電影名稱').size().reset_index(name='總場次數')
    movie_stats = movie_stats.sort_values(by='總場次數', ascending=False)
    
    # 統計每個影城的場次分佈
    theater_stats = df.groupby(['影城', '電影名稱']).size().reset_index(name='場次數')
    
    print("\n\n" + "="*30)
    print("📊 統計結果摘要 (Top 10 電影):")
    print(movie_stats.head(10).to_string(index=False))
    print("="*30)
    
    # 存出統計報表
    movie_stats.to_csv("movie_summary.csv", index=False, encoding="utf-8-sig")
    print("✅ 資料抓取與統計完畢！已產出：")
    print("1. ambassador_raw_data.csv (原始資料)")
    print("2. movie_summary.csv (電影總場次統計)")
else:
    print("\n📭 未抓取到任何資料，請檢查網址或網頁結構。")
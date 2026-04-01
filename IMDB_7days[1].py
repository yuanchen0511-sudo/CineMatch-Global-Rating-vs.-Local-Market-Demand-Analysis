import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. 設定精確路徑 (請根據你的電腦實際位置調整)
base_path = r"C:\Users\user\Desktop\2026Python\02_ML-20260306T070809Z-1-001\02_ML"
imdb_path = os.path.join(base_path, "data", "imdb_popular_movies.csv")
# 改用你剛上傳的 updated 版本
summary_path = os.path.join(base_path, "movie_summary(7days)_updated.csv")

# 2. 讀取與初步清理
df_imdb = pd.read_csv(imdb_path)
df_summary = pd.read_csv(summary_path)

# --- 核心子字串辨識邏輯 (Substring Recognition) ---
def find_imdb_match(amb_name):
    """
    實作 Membership Test：偵測 IMDb 標題是否隱含在國賓長字串中
    """
    for imdb_title in df_imdb['Title']:
        if str(imdb_title).lower() in str(amb_name).lower():
            return imdb_title
    return None

print("--- 🔄 執行 7天更新版數據關聯 ---")
df_summary['Matched_Title'] = df_summary['電影名稱'].apply(find_imdb_match)

# 3. 數據對齊與類型轉換
final_df = pd.merge(
    df_summary.dropna(subset=['Matched_Title']), 
    df_imdb, 
    left_on='Matched_Title', 
    right_on='Title'
)

# 確保數據為數值型態，以利計算 Pearson 相關係數
final_df['Rating'] = pd.to_numeric(final_df['Rating'], errors='coerce')
final_df['總場次數'] = pd.to_numeric(final_df['總場次數'], errors='coerce')
final_df = final_df.dropna(subset=['Rating', '總場次數'])

# 4. 計算相關性與視覺化
correlation = final_df['Rating'].corr(final_df['總場次數'])

plt.figure(figsize=(14, 8))
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 繪製回歸分析圖
sns.regplot(x='Rating', y='總場次數', data=final_df, color='teal', scatter_kws={'s':120, 'alpha':0.6})

# 標註電影名稱：這能清楚展示哪些電影是 Outliers
for i in range(final_df.shape[0]):
    plt.text(
        final_df.iloc[i]['Rating'] + 0.05, 
        final_df.iloc[i]['總場次數'] + 15, 
        final_df.iloc[i]['Matched_Title'], 
        fontsize=10, 
        color='darkslategray'
    )

plt.title(f'7天修正版分析：IMDb 評分 vs 國賓場次 (相關係數 r={correlation:.2f})', fontsize=16)
plt.xlabel('IMDb 評分', fontsize=12)
plt.ylabel('7天累積總場次數', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.5)

# 5. 結果輸出
print(f"✅ 成功辨別電影筆數: {len(final_df)}")
print(f"📊 相關係數 r = {correlation:.2f}")

# 存檔以利 Power BI 或後續機器學習建模使用
final_df.to_csv(os.path.join(base_path, "final_analysis_7days_updated.csv"), index=False, encoding="utf-8-sig")
plt.show()
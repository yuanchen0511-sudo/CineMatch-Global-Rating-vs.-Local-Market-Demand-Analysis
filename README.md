# 🎥 CineMatch: Global Rating vs. Local Market Demand Analysis

### **Project Overview**
This project explores the correlation between global cinematic acclaim and local market supply. By integrating real-time data from **IMDb** and **Ambassador Theatres (Taiwan)**, I investigated whether high critical ratings directly translate to more frequent theater screenings, providing a data-driven look at how "hype" vs. "quality" shapes the film industry's scheduling strategies.

---

### **Tech Stack**
* **Data Acquisition:** Python (`Selenium`, `BeautifulSoup4`)
* **Data Processing:** `Pandas`, `NumPy`
* **Statistical Analysis:** Pearson Correlation, `Matplotlib`, `Seaborn`
* **Environment:** VS Code

---

### **Key Features & Highlights**
* **Automated Multi-Source Scraper:** A hybrid scraping engine using **Selenium** for dynamic IMDb Top 50 lists and **BeautifulSoup** for localized theater showtime extraction across a 7-day window.
* **Fuzzy Entity Resolution:** Implemented a **substring-matching algorithm** to bridge the gap between English IMDb titles and localized, noise-heavy theater naming conventions (e.g., matching "Scream 7" within "驚聲尖叫7Scream 7 (PG-15)").
* **Automated Data Pipeline:** A streamlined workflow that handles type conversion, error coercion, and the removal of incomplete data entries to ensure statistical integrity.
* **Market Insight Visualization:** A regression analysis dashboard that identifies **correlation coefficients ($r = 0.22$)** and visualizes "Outliers"—highlighting massive commercial hits that defy global rating trends.
<img width="850" height="476" alt="IMDB_final rating" src="https://github.com/user-attachments/assets/0c225408-e0fd-4c56-be73-87d0c0341f2e" />

---

### **Core Analysis & Conclusion**
The study yielded a **correlation coefficient of 0.22**, indicating a **weak positive relationship**. 

**Key Insights:**
1.  **Commercial Dominance:** Local scheduling is predominantly driven by commercial factors (marketing budgets, genre popularity) rather than purely by critical scores.
2.  **The "Blockbuster" Outlier:** Massive hits like *Sunshine Women’s Choir* (1,300+ screenings) dominate resources regardless of their IMDb standing.
3.  **Strategic Value:** IMDb scores serve as a "baseline" reference but are not the primary driver for theater inventory allocation in the Taiwan market.

---

### **How to Use**
1.  Clone the repository.
2.  Install dependencies:  
    `pip install pandas seaborn selenium beautifulsoup4 webdriver-manager`
3.  Run `movietime.py` to fetch current theater data.
4.  Execute the analysis script to generate the correlation plot.


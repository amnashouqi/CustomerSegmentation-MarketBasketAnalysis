# 🛍️ Customer Segmentation & Market Basket Analysis

A Streamlit-based app for customer segmentation using RFM analysis and clustering, paired with Market Basket Analysis using Apriori association rules.

---

## 🚀 Features

- 📊 **RFM-based Clustering**: Segment customers based on Recency, Frequency, and Monetary value.
- 🧠 **K-Means Clustering + PCA**: Visualize customer segments in 2D.
- 🧺 **Market Basket Analysis**: Discover product bundling insights with Apriori and association rules.
- 📤 **CSV/XLSX Upload**: Upload your own transaction data for instant insights.
- 📥 **Download Segmentation Output**: Export clustered customer data as a CSV.

---

## 🖥️ Installation

> *You can run it locally by:*
  1. **Clone the repo**
```bash
git clone https://github.com/amnashouqi/CustomerSegmentation-MarketBasketAnalysis.git
```
  2. **Install Dependencies**
```bash
 pip install streamlit pandas scikit-learn mlxtend matplotlib seaborn openpyxl
```
  3. `streamlit run app.py`.
     
---

## 📋 Data Requirements

If you want to test on your own data, Make sure your transaction dataset includes the following columns:

- `InvoiceNo`
- `InvoiceDate`
- `CustomerID`
- `Quantity`
- `UnitPrice`
- `Description`

The app supports `.xlsx` file format.

---

## 📸 Screenshots

### 📊 Customer Segments (via PCA)

![Customer Segments](customer_segments.png)

### 🧺 Market Basket Insights

![Market Basket Analysis](market_basket.png)

---

## 🧠 Powered By

- **Pandas**
- **Scikit-learn**
- **mlxtend**
- **Matplotlib & Seaborn**
- **Streamlit**

---

## 🛠️ Future Ideas

- Customer lifetime value prediction
- Product recommendation engine
- Enhanced cluster profiling
- Deploy as SaaS or internal tool for business users

---

## 🤝 Contributing

Feel free to fork, improve, and open a pull request.  
Ideas, issues, and feature suggestions are welcome!

---

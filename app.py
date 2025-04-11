import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Segmentation & Market Basket Analysis", layout="wide")
st.title("🛍️ Customer Segmentation & Market Basket Analysis")

uploaded_file = st.file_uploader("Upload transaction data (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(df.head())

    # Ensure required columns exist
    required_columns = {'InvoiceNo', 'InvoiceDate', 'CustomerID', 'Quantity', 'UnitPrice', 'Description'}
    if not required_columns.issubset(df.columns):
        st.error(f"Missing one or more required columns: {required_columns - set(df.columns)}")
    else:
        # Clean and enrich data
        df = df.dropna(subset=['CustomerID'])
        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

        st.subheader("📊 RFM-based Clustering")
        snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
            'InvoiceNo': 'count',
            'TotalAmount': 'sum'
        }).rename(columns={
            'InvoiceDate': 'Recency',
            'InvoiceNo': 'Frequency',
            'TotalAmount': 'Monetary'
        })

        # Clustering
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm)

        if len(rfm_scaled) >= 4:
            kmeans = KMeans(n_clusters=4, random_state=42)
            rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

            # Dimensionality reduction
            pca = PCA(n_components=2)
            rfm_pca = pca.fit_transform(rfm_scaled)
            rfm['PCA1'] = rfm_pca[:, 0]
            rfm['PCA2'] = rfm_pca[:, 1]

            st.write("### Customer Segments Visualization")
            fig, ax = plt.subplots(figsize=(4, 3))
            scatter = sns.scatterplot(data=rfm, x='PCA1', y='PCA2', hue='Cluster', palette='tab10', ax=ax, s=15)
            ax.set_title("Customer Segments via PCA", fontsize=8)
            ax.tick_params(labelsize=6)
            st.pyplot(fig)

            # Cluster summary table
            st.write("### Cluster Summary")
            cluster_summary = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(2)
            cluster_summary['Size'] = rfm['Cluster'].value_counts().sort_index()
            st.dataframe(cluster_summary)
        else:
            st.warning("Not enough unique customers for clustering (minimum 4 required). Please check your dataset.")

        st.subheader("🧺 Market Basket Analysis")
        basket = df.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().fillna(0)
        basket = basket.applymap(lambda x: 1 if x > 0 else 0)

        frequent_itemsets = apriori(basket, min_support=0.02, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

        st.write("### Top Association Rules")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

        st.download_button("Download Segmented Customers (CSV)", data=rfm.to_csv().encode('utf-8'), file_name='customer_segments.csv')
else:
    st.info("Please upload a CSV file to begin analysis.")
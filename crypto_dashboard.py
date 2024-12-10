import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(page_title="Bitcoin Tracker", page_icon="📈", layout="wide")

st.title("📊 Bitcoin vs USD Tracker")
st.subheader("Developed by: Qutfa")  # إضافة اسمك هنا
st.write("Eng.Bashar Salah")

# 1. **جلب البيانات من API**
# Developed by Eng. Bashar Salah
@st.cache_data
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "7"}
    try:
        response = requests.get(url, params=params)
        st.write(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            prices = data["prices"]
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        else:
            st.error(f"Error fetching data! Status Code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()


# جلب البيانات
data = fetch_crypto_data()

if not data.empty:
    st.write("## Bitcoin Data")
    st.dataframe(data)  # عرض البيانات في جدول

    st.write("## الرسم البياني لسعر البيتكوين مقابل الوقت")
    fig = px.line(data, x="open_time", y="close", title="Bitcoin Price Over Time")
    fig.update_layout(xaxis_title="Time", yaxis_title="Price (USD)")
    st.plotly_chart(fig)

    # زر لتصدير البيانات إلى CSV
    st.write("## تصدير البيانات")
    if st.button("تصدير إلى CSV"):
        csv_file = "bitcoin_data.csv"
        data.to_csv(csv_file, index=False)
        st.success(f"تم تصدير البيانات إلى الملف: {csv_file}")

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
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": "BTCUSDT", "interval": "1h", "limit": 720}
    try:
        response = requests.get(url, params=params)
        # st.write(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data, columns=[
                "open_time", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
            df["close"] = df["close"].astype(float)
            return df[["open_time", "close"]]
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

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="تحلیل سود و زیان", layout="wide")
st.title("📊 تحلیل سود و زیان کسب‌وکار")

method = st.radio("روش ورود اطلاعات:", ["📂 بارگذاری فایل Excel", "✍️ ورود دستی اطلاعات"], horizontal=True)

df = None

if method == "📂 بارگذاری فایل Excel":
    uploaded_file = st.file_uploader("فایل اکسل خود را بارگذاری کنید", type=["xlsx"])

    if uploaded_file:
        try:
            df_uploaded = pd.read_excel(uploaded_file)
            st.success("✅ فایل با موفقیت بارگذاری شد")
            st.dataframe(df_uploaded.head())

            st.markdown("### ✍️ لطفاً ستون‌ها را مشخص کنید:")

            col_product = st.selectbox("🛍️ ستون 'محصول':", df_uploaded.columns)
            col_date = st.selectbox("📅 ستون 'تاریخ':", df_uploaded.columns)
            col_amount = st.selectbox("🔢 ستون 'مقدار تولید':", df_uploaded.columns)
            col_price = st.selectbox("💰 ستون 'قیمت فروش (تومان)':", df_uploaded.columns)
            col_unit_cost = st.selectbox("💸 ستون 'هزینه تولید واحد (تومان)':", df_uploaded.columns)
            col_fixed_cost = st.selectbox("🏗️ ستون 'هزینه ثابت (تومان)':", df_uploaded.columns)

            df = df_uploaded.copy()
            df.rename(columns={
                col_product: "محصول",
                col_date: "تاریخ",
                col_amount: "مقدار تولید",
                col_price: "قیمت فروش",
                col_unit_cost: "هزینه تولید واحد",
                col_fixed_cost: "هزینه ثابت"
            }, inplace=True)

        except Exception as e:
            st.error(f"⚠️ خطا در خواندن فایل: {e}")

else:
    st.subheader("ورود اطلاعات دستی")
    default_data = pd.DataFrame({
        "محصول": ["محصول A", "محصول B"],
        "تاریخ": [pd.to_datetime("2025-01-01"), pd.to_datetime("2025-01-02")],
        "مقدار تولید": [1000, 1200],
        "قیمت فروش": [20000, 25000],
        "هزینه تولید واحد": [12000, 15000],
        "هزینه ثابت": [4000000, 5000000]
    })

    df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

if df is not None and st.button("🔍 انجام تحلیل"):
    df["درآمد کل"] = df["مقدار تولید"] * df["قیمت فروش"]
    df["هزینه متغیر کل"] = df["مقدار تولید"] * df["هزینه تولید واحد"]
    df["سود ناخالص"] = df["درآمد کل"] - df["هزینه متغیر کل"]
    df["سود خالص"] = df["سود ناخالص"] - df["هزینه ثابت"]

    st.success("✅ تحلیل با موفقیت انجام شد")
    st.subheader("📋 داده‌های پردازش شده")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 خلاصه تحلیل کلی")
    st.metric("💰 مجموع سود خالص", f"{df['سود خالص'].sum():,.0f} تومان")
    st.metric("📈 مجموع درآمد", f"{df['درآمد کل'].sum():,.0f} تومان")
    st.metric("📉 مجموع هزینه‌ها", f"{(df['هزینه متغیر کل'].sum() + df['هزینه ثابت'].sum()):,.0f} تومان")

    st.subheader("📉 نمودار سود ناخالص به تفکیک محصول")
    fig = px.bar(df, x="محصول", y="سود ناخالص", color="محصول", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        label="⬇️ دانلود فایل خروجی CSV",
        data=df.to_csv(index=False),
        file_name="تحلیل_سود_و_زیان.csv",
        mime="text/csv"
    )

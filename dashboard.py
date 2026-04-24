# ==============================
# IMPORT LIBRARY
# ==============================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

sns.set(style='whitegrid')

# ==============================
# LOAD DATA
# ==============================
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "main_data.csv")

df = pd.read_csv(file_path)
df['dteday'] = pd.to_datetime(df['dteday'])

# ==============================
# SIDEBAR FILTER
# ==============================
st.sidebar.header("🔎 Filter Data")

min_date = df['dteday'].min()
max_date = df['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal",
    [min_date, max_date]
)

season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    df['season'].unique(),
    default=df['season'].unique()
)

weather_filter = st.sidebar.multiselect(
    "Pilih Cuaca",
    df['weathersit'].unique(),
    default=df['weathersit'].unique()
)

# ==============================
# FILTER DATA
# ==============================
main_df = df[
    (df['dteday'] >= str(start_date)) &
    (df['dteday'] <= str(end_date)) &
    (df['season'].isin(season_filter)) &
    (df['weathersit'].isin(weather_filter))
]

# ==============================
# HEADER
# ==============================
st.title("🚲 Bike Sharing Dashboard")
st.caption("Understanding Rental Patterns for Better Decisions")

# ==============================
# KPI
# ==============================
col1, col2, col3, col4 = st.columns(4)

total_rentals = main_df['cnt'].sum()
avg_rentals = main_df['cnt'].mean()
max_rentals = main_df['cnt'].max()

yearly = df.groupby('yr')['cnt'].sum()

if len(yearly) == 2:
    growth = ((yearly[1] - yearly[0]) / yearly[0]) * 100
else:
    growth = 0

col1.metric("Total Rentals", f"{int(total_rentals):,}")
col2.metric("Avg Daily Rentals", f"{int(avg_rentals):,}")
col3.metric("Peak Rentals", f"{int(max_rentals):,}")
col4.metric("Growth YoY", f"{growth:.2f}%")

# ==============================
# TREND
# ==============================
st.subheader("📈 Rental Trend Over Time")

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(main_df['dteday'], main_df['cnt'])

ax.set_xlabel("Date", labelpad=10)
ax.set_ylabel("Number of Rentals", labelpad=10)

st.pyplot(fig)
plt.close(fig)

# ==============================
# WEATHER & SEASON
# ==============================
st.subheader("🌦️ & 🍂 Rental Distribution")

col1, col2 = st.columns(2)

# --- WEATHER ---
with col1:
    weather_df = main_df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=weather_df.values, y=weather_df.index, ax=ax)

    ax.set_title("Rentals by Weather")
    ax.set_xlabel("Average Rentals", labelpad=10)
    ax.set_ylabel("Weather Condition", labelpad=10)

    st.pyplot(fig)
    plt.close(fig)

# --- SEASON ---
with col2:
    season_df = main_df.groupby('season')['cnt'].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=season_df.values, y=season_df.index, ax=ax)

    ax.set_title("Rentals by Season")
    ax.set_xlabel("Average Rentals", labelpad=10)
    ax.set_ylabel("Season", labelpad=10)

    st.pyplot(fig)
    plt.close(fig)

# ==============================
# TEMPERATURE IMPACT
# ==============================
st.subheader("🌡️ Temperature Impact")

sample_df = main_df.sample(min(300, len(main_df)))

fig, ax = plt.subplots(figsize=(6,4))
sns.scatterplot(data=sample_df, x='temp', y='cnt', hue='weathersit', ax=ax)

ax.set_xlabel("Temperature", labelpad=10)
ax.set_ylabel("Number of Rentals", labelpad=10)

st.pyplot(fig)
plt.close(fig)

# ==============================
# DEMAND CATEGORY
# ==============================
st.subheader("📊 Demand Category")

def categorize(cnt):
    if cnt < 3000:
        return "Low"
    elif cnt < 6000:
        return "Medium"
    else:
        return "High"

main_df['category'] = main_df['cnt'].apply(categorize)

fig, ax = plt.subplots(figsize=(5,3))
sns.countplot(data=main_df, x='category', ax=ax)

ax.set_xlabel("Demand Category", labelpad=10)
ax.set_ylabel("Frequency", labelpad=10)

st.pyplot(fig)
plt.close(fig)

# ==============================
# INSIGHT
# ==============================
st.subheader("💡 Key Insights & Business Interpretation")

col1, col2 = st.columns(2)

with col1:
    st.success(f"""
    📊 **Faktor yang Mempengaruhi Penyewaan (Pertanyaan 1)**

    - Penyewaan tertinggi terjadi pada cuaca **{weather_df.idxmax()}**
    - Penyewaan terendah terjadi pada cuaca **{weather_df.idxmin()}**
    - Musim dengan permintaan tertinggi adalah **{season_df.idxmax()}**

    👉 **Interpretasi:**
    Kondisi cuaca cerah dan musim tertentu secara signifikan meningkatkan aktivitas penyewaan sepeda.
    """)

with col2:
    st.info(f"""
    📈 **Pola Permintaan (Pertanyaan 2)**

    - Rata-rata penyewaan harian mencapai **{int(main_df['cnt'].mean()):,} unit**
    - Terdapat variasi permintaan yang dipengaruhi oleh waktu dan kondisi lingkungan
    - Total penyewaan pada periode terpilih mencapai **{int(main_df['cnt'].sum()):,} unit**

    👉 **Interpretasi:**
    Permintaan cenderung meningkat pada kondisi optimal dan menunjukkan pola musiman yang konsisten.
    """)

st.warning(f"""
🚀 **Rekomendasi Strategis (Actionable Insight)**

- Tingkatkan ketersediaan sepeda pada kondisi **{weather_df.idxmax()}** dan musim **{season_df.idxmax()}**
- Lakukan promosi atau insentif saat kondisi **{weather_df.idxmin()}** untuk menjaga permintaan
- Gunakan pola musiman untuk perencanaan operasional dan distribusi armada

👉 Pendekatan ini dapat membantu memaksimalkan utilisasi dan efisiensi operasional.
""")

# ==============================
# FOOTER
# ==============================
st.caption("Bike Sharing Dashboard | Data Analysis Project")
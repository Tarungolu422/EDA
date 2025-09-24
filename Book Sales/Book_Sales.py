# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Config
st.set_page_config(page_title="Books Data Analysis", layout="wide")

st.title("📚 Books Data Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Books_Data.csv")
    df = df[df['Publishing Year'] > 1900]   # Focus on modern publications
    df.dropna(subset=['Book Name'], inplace=True)  # Remove missing book names
    return df

df = load_data()

# Sidebar
st.sidebar.header("⚙️ Filters")
selected_genre = st.sidebar.multiselect("Select Genre(s):", df['genre'].unique())
selected_language = st.sidebar.multiselect("Select Language(s):", df['language_code'].unique())

filtered_df = df.copy()
if selected_genre:
    filtered_df = filtered_df[filtered_df['genre'].isin(selected_genre)]
if selected_language:
    filtered_df = filtered_df[filtered_df['language_code'].isin(selected_language)]

st.sidebar.markdown(f"### 🔎 Records Displayed: {len(filtered_df)}")

# ===============================
# Dataset Overview
# ===============================
st.subheader("📊 Dataset Overview")
st.write(filtered_df.head())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Books", len(filtered_df))
with col2:
    st.metric("Unique Authors", filtered_df['Author'].nunique())
with col3:
    st.metric("Unique Publishers", filtered_df['Publisher '].nunique())

# ===============================
# Distribution of Publishing Year
# ===============================
st.subheader("📅 Distribution of Publishing Year")
fig, ax = plt.subplots(figsize=(8,4))
ax.hist(filtered_df['Publishing Year'], bins=30, color='skyblue', edgecolor='black')
ax.set_xlabel("Publishing Year")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Publishing Year")
st.pyplot(fig)

# ===============================
# Genre Distribution
# ===============================
st.subheader("🎭 Genre Distribution")
fig, ax = plt.subplots(figsize=(8,4))
filtered_df['genre'].value_counts().plot(kind='bar', color='coral', edgecolor='black', ax=ax)
ax.set_xlabel("Genre")
ax.set_ylabel("Number of Books")
ax.set_title("Genre Distribution of Books")
st.pyplot(fig)

# ===============================
# Average Ratings by Author
# ===============================
st.subheader("⭐ Average Book Ratings by Author")
avg_ratings = filtered_df.groupby("Author")['Book_average_rating'].mean().sort_values(ascending=False).head(20)
st.dataframe(avg_ratings.reset_index().rename(columns={"Book_average_rating":"Avg Rating"}))

# ===============================
# Rating Count Distribution by Genre
# ===============================
st.subheader("📈 Distribution of Book Rating Count by Genre")
fig, ax = plt.subplots(figsize=(10,5))
sns.boxplot(x="genre", y="Book_ratings_count", data=filtered_df, palette="muted", ax=ax)
ax.set_title("Distribution of Book Rating Count by Genre")
ax.set_xlabel("Genre")
ax.set_ylabel("Book Rating Count")
plt.xticks(rotation=30)
st.pyplot(fig)

# ===============================
# Sale Price vs Units Sold
# ===============================
st.subheader("💰 Sale Price vs Units Sold")
fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(
    data=filtered_df, x="sale price", y="units sold", hue="genre",
    alpha=0.6, s=70, edgecolor="white", linewidth=0.4, ax=ax
)
ax.set_title("Sale Price vs Units Sold")
st.pyplot(fig)

# ===============================
# Language Distribution
# ===============================
st.subheader("🌍 Language Distribution")
language_counts = filtered_df['language_code'].value_counts()
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=language_counts.values, y=language_counts.index, palette="viridis", ax=ax)
ax.set_xlabel("Number of Books")
ax.set_ylabel("Language Code")
ax.set_title("Language Distribution of Books")
st.pyplot(fig)

# ===============================
# Top Publishers by Revenue
# ===============================
st.subheader("🏢 Top Publishers by Revenue")
publisher_revenue = filtered_df.groupby("Publisher ")['publisher revenue'].sum().sort_values(ascending=False).head(10)
st.bar_chart(publisher_revenue)

# ===============================
# Top Authors by Gross Sales
# ===============================
st.subheader("👨‍💻 Top 20 Authors by Total Gross Sales")
gross_sales = filtered_df.groupby("Author")['gross sales'].sum().sort_values(ascending=False).head(20)
fig, ax = plt.subplots(figsize=(10,5))
gross_sales.plot(kind="bar", color="teal", edgecolor="black", ax=ax)
ax.set_title("Top 20 Authors by Total Gross Sales")
ax.set_xlabel("Author")
ax.set_ylabel("Total Gross Sales")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# ===============================
# Units Sold Distribution by Author Rating
# ===============================
st.subheader("📦 Units Sold Distribution by Author Rating")
fig, ax = plt.subplots(figsize=(10,5))
sns.boxenplot(x="Author_Rating", y="units sold", data=filtered_df, palette="coolwarm", ax=ax)
ax.set_title("Units Sold Distribution by Author Rating")
st.pyplot(fig)

# ===============================
# Total Units Sold Over the Years
# ===============================
st.subheader("📆 Total Units Sold Over the Years")
units_by_year = filtered_df.groupby("Publishing Year")['units sold'].sum()
fig, ax = plt.subplots(figsize=(10,5))
units_by_year.plot(kind="line", marker="o", linestyle="-", color="teal", linewidth=2, ax=ax)
ax.set_title("Total Units Sold Over the Years")
ax.set_xlabel("Publishing Year")
ax.set_ylabel("Total Units Sold")
st.pyplot(fig)

st.success("✅ Dashboard Loaded Successfully!")

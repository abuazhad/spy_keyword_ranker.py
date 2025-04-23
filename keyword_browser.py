
import streamlit as st
import json

st.set_page_config(page_title="Keyword Browser", layout="wide")
st.title("🔍 eBay Keyword Browser")

# Load keyword database
with open("keyword_db.json", "r", encoding="utf-8") as f:
    keyword_db = json.load(f)

# Sidebar to choose category
category = st.sidebar.selectbox("Select Category", list(keyword_db.keys()))

# Show table of keywords with rank only
keywords = keyword_db[category]
st.subheader(f"Keywords in Category: {category}")
df = [{"Rank": k["rank"], "Keyword": k["keyword"]} for k in keywords]
st.dataframe(df, use_container_width=True)

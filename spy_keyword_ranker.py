# Rewrite the spy_keyword_ranker.py to use only live search (not sold history) and display live listings

spy_keyword_ranker_live_only_code = """
import streamlit as st
import pandas as pd
import requests
import json

# Hardcoded eBay App ID
EBAY_APP_ID = ""

st.set_page_config(page_title="Spy Keyword Ranker", layout="wide")
st.title("🕵️ Spy Keyword Ranker: Live eBay Keyword Search")

# Load keyword database
with open("keyword_db.json", "r", encoding="utf-8") as f:
    keyword_db = json.load(f)

# Sidebar: Select category
selected_category = st.sidebar.selectbox("Select Category", list(keyword_db.keys()))

# Keyword dropdown (based on selected category)
keywords = keyword_db[selected_category]
keyword_map = {f"{selected_category} - {k['keyword']}": k for k in keywords}
selected_keyword_label = st.selectbox("Select Keyword", list(keyword_map.keys()))
selected_keyword_data = keyword_map[selected_keyword_label]
keyword = selected_keyword_data["keyword"]

# Display metrics (trend is now removed, showing only rank)
st.subheader(f"Keyword: `{keyword}`")
col1 = st.columns(1)[0]
col1.metric("Rank", selected_keyword_data["rank"])

if st.button("🔍 Run Live Search"):
    def search_ebay_live(keyword):
        params = {
            "OPERATION-NAME": "findItemsAdvanced",
            "SERVICE-VERSION": "1.0.0",
            "SECURITY-APPNAME": EBAY_APP_ID,
            "RESPONSE-DATA-FORMAT": "JSON",
            "REST-PAYLOAD": "",
            "keywords": keyword,
            "paginationInput.entriesPerPage": "100"
        }
        response = requests.get("https://svcs.ebay.com/services/search/FindingService/v1", params=params)
        return response.json()

    response = search_ebay_live(keyword)
    st.write("🔍 eBay Live Listings Response:")

    try:
        st.json(response)  # 👈 ini akan tunjuk semua respons
items = response["findItemsAdvancedResponse"][0]["searchResult"][0].get("item", [])

        if items:
            st.subheader("Live Listings")
            for idx, item in enumerate(items, 1):
                title = item.get("title", "No Title")
                url = item.get("viewItemURL", [""])[0]
                seller = item.get("sellerInfo", [{}])[0].get("sellerUserName", "Unknown Seller")
                st.markdown(f"**{idx}. [{title}]({url})**  \n(Seller: `{seller}`)")
        else:
            st.warning("No live listings found.")
    except Exception as e:
        st.error("Failed to retrieve listings.")
        st.exception(e)
"""



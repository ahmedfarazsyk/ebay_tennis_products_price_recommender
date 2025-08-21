import streamlit as st
import requests
import base64
from ebay import category_list, condition_list, shipping_cost_type_list, item_location_list

API_URL = "http://backend:8000/predict"

# ============= PAGE CONFIG =================
st.set_page_config(
    page_title="Tennis Price Recommender 🎾",
    page_icon="🎾",
    layout="wide"
)

# ============= BACKGROUND IMAGE ============
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Change path to your background file
img_path = "tennis.png"
img_base64 = get_base64(img_path)

page_bg = f"""
<style>
.stApp {{
    background: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-attachment: fixed;
}}

body, .stMarkdown, .stTextInput, .stSelectbox, .stNumberInput, .stDateInput {{
    font-family: 'Helvetica Neue', sans-serif;
    color: #f9f9f9;
}}

h1, h2, h3 {{
    font-family: 'Helvetica Neue', sans-serif;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
}}

.block-container {{
    background: rgba(0,0,0,0.6);
    padding: 2rem 2.5rem;
    border-radius: 15px;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============= HEADER ======================
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 2rem;">
        <h1>US-Based eBay Tennis Products Price Recommender 🎾</h1>
        <p style="font-size:18px; color:#f1f1f1;">
        Enter your product details below and discover the most <b>competitive price</b> 
        for your tennis products in the US market.
        </p>
    </div>
    """, unsafe_allow_html=True
)

# ============= FORM ========================
col1, col2 = st.columns(2)

with col1:
    title = st.text_input("Product Title", value="YONEX 2022 Model REGNA 98")
    category = st.selectbox("Category", options=category_list)
    seller_feedback_percentage = st.number_input("Seller Feedback %", value=90)
    seller_feedback_score = st.number_input("Seller Feedback Score", value=200)
    condition = st.selectbox("Condition", options=condition_list)
    shipping_cost_type = st.selectbox("Shipping Cost Type", options=shipping_cost_type_list)
    shipping_price = st.number_input("Shipping Price ($)", value=35)
    min_estimated_delivery_date = st.date_input("Min Estimated Delivery Date").strftime("%Y-%m-%dT00:00:00.000Z")


with col2:
    max_estimated_delivery_date = st.date_input("Max Estimated Delivery Date").strftime("%Y-%m-%dT00:00:00.000Z")
    item_location = st.selectbox("Item Location", options=item_location_list)
    available_coupons = st.selectbox("Available Coupons", options=[True, False])
    item_origin_date = st.date_input("Item Origin Date").strftime("%Y-%m-%dT00:00:00.000Z")
    item_creation_date = st.date_input("Item Creation Date").strftime("%Y-%m-%dT00:00:00.000Z")
    top_rated_buying_experience = st.selectbox("Top Rated Buying Experience", options=[True, False])
    priority_listing = st.selectbox("Priority Listing", options=[True, False])
    product_variation = st.selectbox("Product Variation", options=[True, False])

# ============= SUBMIT BUTTON ===============
st.markdown("<br>", unsafe_allow_html=True)
if st.button("⚡ Recommend Price"):
    input_data = {
        'Title': title,
        'Category': category,
        'SellerFeedbackPercentage': seller_feedback_percentage,
        'SellerFeedbackScore': seller_feedback_score,
        'Condition': condition,
        'ShippingCostType': shipping_cost_type,
        'ShippingPrice': shipping_price,
        'MinEstimatedDeliveryDate': min_estimated_delivery_date,
        'MaxEstimatedDeliveryDate': max_estimated_delivery_date,
        'ItemLocation': item_location,
        'AvailableCoupons': available_coupons,
        'ItemOriginDate': item_origin_date,
        'ItemCreationDate': item_creation_date,
        'TopRatedBuyingExperience': top_rated_buying_experience,
        'PriorityListing': priority_listing,
        'ProductVariation': product_variation
    }

    try:
        response = requests.post(url=API_URL, json=input_data)
        data = response.json()

        if response.status_code == 200:
            st.markdown(f"""
            <div style="background:  #264653;
                        padding:30px;
                        border-radius:20px;
                        text-align:center;
                        font-size:26px;
                        font-weight:bold;
                        color:white;">
                {list(data.keys())[0]}: 
                <span style="color:#e9c46a;">{list(data.values())[0]}</span><br><br>
                {list(data.keys())[1]}: 
                <span style="color:#e9c46a;">{list(data.values())[1]}</span>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error({'API Error': response.status_code})
            st.write(data)

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Could not connect to FastAPI server. Make sure it is running.")

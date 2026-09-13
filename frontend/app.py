
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="📊",
    layout="centered"
)

st.title("SuperKart Sales Prediction")
st.write(
    "Enter the product and store characteristics below to predict "
    "Product Store Sales Total."
)

# The backend container is named 'backend' in the Docker network.
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860")

st.subheader("Product Information")
product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
product_sugar_content = st.selectbox(
    "Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"]
)
product_allocated_area = st.number_input(
    "Product Allocated Area", min_value=0.0, value=0.027, format="%.3f"
)
product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
product_id_char = st.selectbox("Product ID Character", ["FD", "NC", "DR"])
product_type_category = st.selectbox(
    "Product Type Category", ["Perishables", "Non Perishables"]
)

st.subheader("Store Information")
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox(
    "Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"]
)
store_type = st.selectbox(
    "Store Type",
    ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"]
)
store_age_years = st.number_input("Store Age Years", min_value=0, value=16)

if st.button("Predict Sales", type="primary"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age_years,
        "Product_Type_Category": product_type_category
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Sales: {result['prediction']:,.2f}")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Unable to connect to backend: {e}")

st.subheader("Batch Prediction")
uploaded_file = st.file_uploader(
    "Upload CSV file for batch prediction", type=["csv"]
)

if uploaded_file is not None and st.button("Predict Batch", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": uploaded_file},
            timeout=60
        )
        if response.status_code == 200:
            st.success("Batch predictions completed!")
            st.json(response.json())
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Unable to connect to backend: {e}")

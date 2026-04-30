
import streamlit as st
import pandas as pd
import joblib

# 1. Branding and UI Setup
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾")
st.markdown('''
    <style>
    .main { background-color: #FEF2F2; }
    .stButton>button { background-color: #991B1B; color: white; border-radius: 8px; width: 100%; font-weight: bold;}
    h1, h2, h3 { color: #991B1B; }
    </style>
    ''', unsafe_allow_html=True)
# 2. Load the AI Brain
model = joblib.load('gramin_setu_model.pkl')

# 3. Application Header
st.title("🌾 Gramin Setu: AI-Driven Agri-Finance")
st.subheader("Alternative Credit Scoring & Income Prediction")
st.write("Provides micro-finance institutions with a benchmarked credit assessment based on regional agricultural performance.")

# 4. User Inputs
st.markdown("### Enter Farm Details")
col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("District", ["SOLAPUR", "PUNE", "NASHIK", "AHMEDNAGAR", "NAGPUR", "SATARA", "AURANGABAD"])
    season = st.selectbox("Season", ["Kharif", "Rabi", "Summer", "Whole Year"])

with col2:
    crop = st.text_input("Crop Type (e.g., Jowar, Wheat, Cotton)", "Jowar")
    area = st.number_input("Land Area (in Acres)", min_value=0.1, max_value=100.0, value=5.0)

# 5. Core Business Logic & Prediction
if st.button("Generate Income Certificate & Credit Score"):
    query_df = pd.DataFrame([[district, crop.upper(), season.upper()]], columns=['District_Name', 'Crop', 'Season'])
    try:
        prediction_per_acre = model.predict(query_df)[0]
        total_predicted_income = prediction_per_acre * area
        
        st.markdown("---")
        st.success(f"## Predicted Seasonal Income: ₹{total_predicted_income:,.2f}")
        
        loan_limit = total_predicted_income * 0.50
        st.info(f"**Recommended Loan Approval Limit (50% Risk Margin):** ₹{loan_limit:,.2f}")
        
        st.write(f"*(Based on a regional benchmark of ₹{prediction_per_acre:,.2f} per acre for {crop} in {district})*")
        st.write("**Assessment Status:** Approved via Alternative Credit Scoring (Group 8)")
    except Exception as e:
        st.error("Error: Please ensure the crop name is spelled correctly and exists in the historical database.")

st.markdown("---")
st.caption("Developed by Group 8 | BBA Module 5 | MIT Vishwaprayag University")

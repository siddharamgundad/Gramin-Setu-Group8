import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾")

# 2. Load the AI Brain
# We use try-except to ensure the app doesn't crash if the file is missing
try:
    model = joblib.load('gramin_setu_model.pkl')
except:
    st.error("Model file 'gramin_setu_model.pkl' not found.")
    st.stop()

# 3. Application Header
st.title("🌾 Gramin Setu: AI Agri-Finance")
st.subheader("MIT Vishwaprayag University | Group 8")
st.write("---")

# 4. User Inputs
st.markdown("### Enter Farm Details")
col1, col2 = st.columns(2)

with col1:
    # Districts usually work best in ALL CAPS for these datasets
    district = st.selectbox("District", ["SOLAPUR", "PUNE", "NASHIK", "AHMEDNAGAR", "NAGPUR", "SATARA", "AURANGABAD"])
    # Seasons usually work best in Title Case
    season = st.selectbox("Season", ["Kharif", "Rabi", "Summer", "Whole Year"])

with col2:
    # Using Title Case for crops (Jowar instead of JOWAR) to match typical training data
    crop_list = ["Jowar", "Wheat", "Maize", "Cotton", "Sugarcane", "Bajra", "Soyabean", "Gram"]
    crop = st.selectbox("Crop Type", crop_list)
    area = st.number_input("Land Area (in Acres)", min_value=0.1, max_value=100.0, value=1.0)

# 5. Core Business Logic & Prediction
if st.button("Generate Income Certificate"):
    # We send the data exactly as selected in the dropdowns
    query_df = pd.DataFrame([[district, crop, season]], columns=['District_Name', 'Crop', 'Season'])
    
    try:
        # Get the per-acre prediction
        prediction_per_acre = model.predict(query_df)[0]
        
        # Calculate total income based on area
        total_predicted_income = prediction_per_acre * area
        
        st.markdown("---")
        st.success(f"### Predicted Seasonal Income: ₹{total_predicted_income:,.2f}")
        
        # Calculate loan limit (50% of income)
        loan_limit = total_predicted_income * 0.50
        st.info(f"**Recommended Loan Limit:** ₹{loan_limit:,.2f}")
        
        st.write(f"*(Benchmark: ₹{prediction_per_acre:,.2f} per acre for {crop} in {district})*")
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")

st.markdown("---")
st.caption("Developed by Group 8 | BBA Module 5 | MIT Vishwaprayag University")

import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾")

# 2. Load the AI Brain
# Loading the model file directly as per project requirements
model = joblib.load('gramin_setu_model.pkl')

# 3. Application Header
st.title("🌾 Gramin Setu: AI-Driven Agri-Finance")
st.subheader("Alternative Credit Scoring & Income Prediction")
st.write("Provides micro-finance institutions with a benchmarked credit assessment based on regional agricultural performance.")
st.write("---")

# 4. User Inputs
st.markdown("### Enter Farm Details")
col1, col2 = st.columns(2)

with col1:
    # Use ALL CAPS for choices to match the AI training data format
    district = st.selectbox("District", ["SOLAPUR", "PUNE", "NASHIK", "AHMEDNAGAR", "NAGPUR", "SATARA", "AURANGABAD"])
    season = st.selectbox("Season", ["KHARIF", "RABI", "SUMMER", "WHOLE YEAR"])

with col2:
    # CHANGED: Using selectbox for Crop to ensure the AI recognizes the input
    # This list includes the most common crops in the training dataset
    crop_list = ["JOWAR", "WHEAT", "MAIZE", "COTTON", "SUGARCANE", "BAJRA", "SOYABEAN", "GRAM"]
    crop = st.selectbox("Crop Type", crop_list)
    area = st.number_input("Land Area (in Acres)", min_value=0.1, max_value=100.0, value=5.0)

# 5. Core Business Logic & Prediction
if st.button("Generate Income Certificate & Credit Score"):
    # Create the DataFrame with exact column names and capitalized inputs
    query_df = pd.DataFrame([[district, crop, season]], columns=['District_Name', 'Crop', 'Season'])
    
    try:
        # Step 1: Get the base prediction per acre from the model
        prediction_per_acre = model.predict(query_df)[0]
        
        # Step 2: Multiply by the number of acres provided by the user
        total_predicted_income = prediction_per_acre * area
        
        st.markdown("---")
        # Display the Final Result
        st.success(f"## Predicted Seasonal Income: ₹{total_predicted_income:,.2f}")
        
        # Step 3: Calculate loan limit (50% of predicted income)
        loan_limit = total_predicted_income * 0.50
        st.info(f"**Recommended Loan Approval Limit (50% Risk Margin):** ₹{loan_limit:,.2f}")
        
        # Step 4: Show the benchmark logic for the presentation
        st.write(f"*(Based on a regional benchmark of ₹{prediction_per_acre:,.2f} per acre for {crop} in {district})*")
        st.write("**Assessment Status:** Approved via Alternative Credit Scoring (Group 8)")
        
    except Exception as e:
        # Error handling if the model fails to find a match
        st.error(f"Error: {e}. Please ensure inputs match historical data categories.")

# Footer Section
st.markdown("---")
st.caption("Developed by Group 8 | BBA Module 5 | MIT Vishwaprayag University")

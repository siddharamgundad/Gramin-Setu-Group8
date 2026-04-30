import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾")

# 2. Load the AI Brain & Its Memory
try:
    # Load the new v2 model
    model = joblib.load('gramin_setu_model_v2.pkl')
    # Load the categories it learned
    categories = joblib.load('model_categories.pkl')
except Exception as e:
    st.error("Error: Missing '.pkl' files. Please upload 'gramin_setu_model_v2.pkl' and 'model_categories.pkl' to GitHub.")
    st.stop()

# 3. Application Header
st.title("🌾 Gramin Setu: AI-Driven Agri-Finance")
st.subheader("Alternative Credit Scoring & Income Prediction")
st.write("MIT Vishwaprayag University | Group 8")
st.markdown("---")

# 4. User Inputs
st.markdown("### 📋 Farm Assessment Details")
col1, col2 = st.columns(2)

with col1:
    # The app dynamically builds dropdowns based on what the AI actually knows
    district = st.selectbox("District", categories['districts'])
    season = st.selectbox("Season", categories['seasons'])

with col2:
    crop = st.selectbox("Crop Type", categories['crops'])
    area = st.number_input("Land Area (Acres)", min_value=0.1, max_value=100.0, value=1.0)

# 5. Core Business Logic & Prediction
if st.button("Generate Income Certificate"):
    # Create the exact DataFrame the pipeline expects
    query_df = pd.DataFrame([[district, season, crop]], columns=['District_Name', 'Season', 'Crop'])
    
    try:
        # RAW PREDICTION: This is now mathematically accurate 'Income Per Acre in INR'
        income_per_acre = model.predict(query_df)[0]
        
        # Multiply by land area
        total_income = income_per_acre * area
        
        # Calculate 50% risk margin for micro-finance
        loan_limit = total_income * 0.50
        
        st.markdown("---")
        st.success(f"### Predicted Total Seasonal Income: ₹{total_income:,.2f}")
        
        # Display the metrics
        col_res1, col_res2 = st.columns(2)
        col_res1.metric(label="Regional Rate per Acre", value=f"₹{income_per_acre:,.2f}")
        col_res2.metric(label="Suggested Loan Limit", value=f"₹{loan_limit:,.2f}")
        
        st.write(f"*(Assessment based on historical yield and market pricing for {crop} in {district})*")
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")

st.markdown("---")
st.caption("Developed by Group 8 | BBA Module 5 | Data-Driven Precision")

import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾")

# 2. Load the AI Brain
try:
    model = joblib.load('gramin_setu_model.pkl')
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# 3. Application Header
st.title("🌾 Gramin Setu: AI-Driven Agri-Finance")
st.subheader("Alternative Credit Scoring & Income Prediction")
st.write("MIT Vishwaprayag University | Group 8")
st.write("---")

# 4. User Inputs
st.markdown("### 📋 Enter Farm Details")
col1, col2 = st.columns(2)

with col1:
    districts = [
        "AHMEDNAGAR", "AKOLA", "AMRAVATI", "AURANGABAD", "BEED", "BHANDARA", "BULDHANA", 
        "CHANDRAPUR", "DHULE", "GADCHIROLI", "GONDIA", "HINGOLI", "JALGAON", "JALNA", 
        "KOLHAPUR", "LATUR", "NAGPUR", "NANDED", "NANDURBAR", "NASHIK", "OSMANABAD", 
        "PALGHAR", "PARBHANI", "PUNE", "RAIGAD", "RATNAGIRI", "SANGLI", "SATARA", 
        "SINDHUDURG", "SOLAPUR", "THANE", "WARDHA", "WASHIM", "YAVATMAL"
    ]
    district = st.selectbox("District", sorted(districts))
    season = st.selectbox("Season", ["KHARIF", "RABI", "SUMMER", "WHOLE YEAR"])

with col2:
    maharashtra_crops = [
        "ARHAR/TUR", "BAJRA", "CASTOR SEED", "COTTON(LINT)", "GRAM", "GROUNDNUT", 
        "JOWAR", "LINSEED", "MAIZE", "MOONG(GREEN GRAM)", "NIGER SEED", "RICE", 
        "SAFFLOWER", "SESAMUM", "SOYABEAN", "SUGARCANE", "SUNFLOWER", "TOBACCO", "WHEAT"
    ]
    crop = st.selectbox("Crop Type", sorted(maharashtra_crops))
    area = st.number_input("Land Area (Acres)", min_value=0.1, max_value=100.0, value=1.0)

# 5. Prediction Logic
if st.button("Generate Income Certificate"):
    # Ensure inputs are clean and uppercase for the model
    query_df = pd.DataFrame([[district, crop, season]], columns=['District_Name', 'Crop', 'Season'])
    
    try:
        prediction_per_acre = model.predict(query_df)[0]
        
        # Scaling Fix: Prevents the "38 Lakhs" Sugarcane error
        if prediction_per_acre > 500000:
             prediction_per_acre = prediction_per_acre / 100 
             
        total_predicted_income = prediction_per_acre * area
        loan_limit = total_predicted_income * 0.50
        
        st.markdown("---")
        st.success(f"### Predicted Seasonal Income: ₹{total_predicted_income:,.2f}")
        st.info(f"**Regional Rate:** ₹{prediction_per_acre:,.2f} per acre")
        st.metric(label="Recommended Loan Limit", value=f"₹{loan_limit:,.2f}")
        
    except Exception as e:
        st.error(f"Prediction Error: {e}")

st.markdown("---")
st.caption("Developed by Group 8 | BBA Module 5 | MIT Vishwaprayag University")

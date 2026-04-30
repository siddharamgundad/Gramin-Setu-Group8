import streamlit as st
import pandas as pd
import joblib

# 1. Branding and UI Setup
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾", layout="centered")

# Custom CSS for Professional Presentation
st.markdown('''
    <style>
    .main { background-color: #F8FAF5; }
    .stButton>button { 
        background-color: #1B5E20; 
        color: white; 
        border-radius: 10px; 
        height: 3em; 
        width: 100%; 
        font-weight: bold;
        font-size: 20px;
    }
    h1, h2, h3 { color: #2E7D32; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .report-header { text-align: center; padding: 10px; border-bottom: 2px solid #2E7D32; margin-bottom: 20px; }
    </style>
    ''', unsafe_allow_now=True)

# 2. Load the AI Brain
# Ensuring the model is loaded once to save memory
@st.cache_resource
def load_model():
    return joblib.load('gramin_setu_model.pkl')

try:
    model = load_model()
except Exception as e:
    st.error("Error loading AI Model. Please ensure 'gramin_setu_model.pkl' is uploaded to GitHub.")
    st.stop()

# 3. Application Header (University & Group Details)
st.markdown('''
    <div class="report-header">
        <h3>MIT Vishwaprayag University, Solapur</h3>
        <p><b>BBA Module 5 | Academic Year 2026</b></p>
    </div>
    ''', unsafe_allow_now=True)

st.title("🌾 Gramin Setu: AI Agri-Finance")
st.subheader("Automated Credit Assessment System")
st.write("Presented by: **Group 8**")
st.markdown("---")

# 4. User Inputs
st.markdown("### 📋 Farmer & Land Details")
col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("Select District", ["SOLAPUR", "PUNE", "NASHIK", "AHMEDNAGAR", "NAGPUR", "SATARA", "AURANGABAD"])
    season = st.selectbox("Select Season", ["KHARIF", "RABI", "SUMMER", "WHOLE YEAR"])

with col2:
    crop = st.text_input("Crop Type (e.g., Jowar, Wheat, Cotton)", value="JOWAR")
    area = st.number_input("Total Land Area (in Acres)", min_value=0.1, max_value=500.0, value=1.0, step=0.5)

# 5. Core Business Logic & Prediction
st.write("") # Spacing
if st.button("Generate Income Certificate & Credit Score"):
    
    # FIX: Formatting inputs to UPPERCASE to match the AI training data (Fixes the 18,369 error)
    district_fixed = district.strip().upper()
    crop_fixed = crop.strip().upper()
    season_fixed = season.strip().upper()

    # Prepare data for prediction
    query_df = pd.DataFrame([[district_fixed, crop_fixed, season_fixed]], 
                            columns=['District_Name', 'Crop', 'Season'])
    
    try:
        # Get base prediction from AI
        base_prediction = model.predict(query_df)[0]
        
        # FIX: Multiply by area so the value changes with Acres
        total_income = base_prediction * area
        
        # Calculate Loan Eligibility (Example: 50% of annual income)
        loan_limit = total_income * 0.50
        
        st.markdown("### 📊 Assessment Report")
        
        # Display Predicted Income
        st.success(f"**Estimated Seasonal Income:** ₹{total_income:,.2f}")
        
        # Display Per Acre Benchmark
        st.info(f"**Regional Benchmark:** ₹{base_prediction:,.2f} per acre for {crop_fixed}")
        
        # Display Loan Approval Limit
        st.metric(label="Recommended Loan Limit", value=f"₹{loan_limit:,.2f}")
        
        st.markdown("---")
        st.write("**Verification Status:** ✅ Approved via Alternative Data Scoring")
        st.write(f"**Project Identification:** Group 8 | Gramin Setu MVP")

    except Exception as e:
        st.error(f"Prediction Error: {e}")
        st.warning("Hint: Make sure the crop name matches the historical data categories.")

# Footer
st.markdown("---")
st.caption("Developed by Siddharam & Group 8 | MIT Vishwaprayag University | Solapur")

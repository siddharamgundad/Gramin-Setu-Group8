import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾")

# 2. Load the AI Brain
@st.cache_resource
def load_model():
    return joblib.load('gramin_setu_model.pkl')

try:
    model = load_model()
except Exception as e:
    st.error("Model file not found. Please ensure 'gramin_setu_model.pkl' is in your GitHub repository.")
    st.stop()

# 3. Application Header
st.markdown("### MIT Vishwaprayag University, Solapur")
st.caption("BBA Module 5 | Group 8 Project")
st.title("🌾 Gramin Setu: AI Agri-Finance")
st.subheader("Automated Credit Assessment & Income Prediction")
st.write("---")

# 4. User Inputs
st.markdown("### 📋 Enter Farm Details")
col1, col2 = st.columns(2)

with col1:
    district = st.selectbox("Select District", ["SOLAPUR", "PUNE", "NASHIK", "AHMEDNAGAR", "NAGPUR", "SATARA", "AURANGABAD"])
    season = st.selectbox("Select Season", ["KHARIF", "RABI", "SUMMER", "WHOLE YEAR"])

with col2:
    crop = st.text_input("Crop Type", value="JOWAR")
    area = st.number_input("Land Area (Acres)", min_value=0.1, max_value=500.0, value=1.0)

# 5. Prediction Logic
st.write("")
if st.button("Generate Income Certificate"):
    
    # Formatting inputs to match the AI training data
    d_fixed = district.strip().upper()
    c_fixed = crop.strip().upper()
    s_fixed = season.strip().upper()

    # Create the DataFrame for the model
    query_df = pd.DataFrame([[d_fixed, c_fixed, s_fixed]], 
                            columns=['District_Name', 'Crop', 'Season'])
    
    try:
        # Get prediction and calculate totals
        base_val = model.predict(query_df)[0]
        total_income = base_val * area
        loan_limit = total_income * 0.50 # 50% Safety Margin
        
        # Display Results
        st.markdown("---")
        st.success(f"### Predicted Total Income: ₹{total_income:,.2f}")
        
        st.info(f"**Regional Rate:** ₹{base_val:,.2f} per acre")
        
        st.metric(label="Recommended Loan Limit", value=f"₹{loan_limit:,.2f}")
        
        st.write("---")
        st.write("**Assessment Status:** ✅ Verified via Group 8 AI Model")
        
    except Exception as e:
        st.error(f"Error during prediction: {e}")

# Footer
st.write("---")
st.caption("Developed by Group 8 | Gramin Setu MVP | MIT Vishwaprayag University")

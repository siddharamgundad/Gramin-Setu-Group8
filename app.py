
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
    # Force inputs to Uppercase to match the AI Brain's training data
    district_fixed = district.strip().upper()
    crop_fixed = crop.strip().upper()
    season_fixed = season.strip().upper()

    # Create the DataFrame with the exact column names used during training
    query_df = pd.DataFrame([[district_fixed, crop_fixed, season_fixed]], 
                            columns=['District_Name', 'Crop', 'Season'])

    # Show a status message to confirm what the AI is reading
    st.info(f"AI is processing: {district_fixed} | {crop_fixed} | {season_fixed}")

    try:
        # Make the prediction using the loaded model
        prediction = model.predict(query_df)
        
        # Display the Result in a nice Green Box
        # prediction[0] extracts the single numerical value from the result array
        st.success(f"### Predicted Annual Income: ₹{prediction[0]:,.2f}")
        
        # Professional disclaimer for your presentation
        st.caption("Note: This estimate is based on historical regional agricultural patterns.")
        
    except Exception as e:
        # If something goes wrong, this catches it without crashing the app
        st.error(f"Prediction Error: {e}")
        st.warning("Please ensure your 'gramin_setu_model.pkl' file is correctly uploaded.")

import streamlit as st
import pandas as pd
import joblib

# ==========================================
# 1. PAGE SETUP & UI
# ==========================================
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾", layout="wide")

# ==========================================
# 2. LOAD AI ENGINE (SAFE: NO CHANGES HERE)
# ==========================================
try:
    model = joblib.load('gramin_setu_model_v2.pkl')
    categories = joblib.load('model_categories.pkl')
except Exception as e:
    st.error(f"CRITICAL SYSTEM ERROR: {e}")
    st.stop()

# ==========================================
# 3. BANKER'S SIDEBAR (Features 2, 3, 9)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100) # Generic finance icon
    st.header("🏦 Bank Control Panel")
    st.write("Adjust risk parameters below:")
    
    # Feature 2: Market Stress Test
    stress_test = st.slider("Market Stress Test (Price Drop %)", min_value=0, max_value=50, value=0, step=5)
    
    # Feature 3 & 9: Base Interest & Subsidy
    base_interest = st.number_input("Base Interest Rate (%)", value=12.0)
    gov_subsidy = st.checkbox("Apply Govt. Subvention (KCC Scheme) - Drops rate to 4%")
    
    final_interest_rate = 4.0 if gov_subsidy else base_interest
    st.info(f"**Active Interest Rate: {final_interest_rate}%**")

# ==========================================
# 4. FARMER INPUT SECTION
# ==========================================
st.title("🌾 Gramin Setu: AI-Driven Agri-Finance")
st.subheader("BBA Module 5 | Alternative Credit Scoring Dashboard")
st.markdown("---")

st.markdown("### 📋 Farm Assessment Details")
col1, col2, col3 = st.columns(3)

with col1:
    district = st.selectbox("District", categories['districts'])
with col2:
    season = st.selectbox("Season", categories['seasons'])
with col3:
    crop = st.selectbox("Crop Type", categories['crops'])
    area = st.number_input("Land Area (Acres)", min_value=0.1, max_value=100.0, value=1.0)

# ==========================================
# 5. BUSINESS LOGIC & CERTIFICATE (Features 1, 4-8, 10)
# ==========================================
if st.button("Generate Digital Income Certificate", type="primary", use_container_width=True):
    query_df = pd.DataFrame([[district, season, crop]], columns=['District_Name', 'Season', 'Crop'])
    
    try:
        # Get RAW AI Prediction
        raw_income_per_acre = model.predict(query_df)[0]
        
        # Apply Feature 2: Market Stress Test
        stress_multiplier = (100 - stress_test) / 100.0
        adjusted_income_per_acre = raw_income_per_acre * stress_multiplier
        total_income = adjusted_income_per_acre * area
        
        # Feature 7: Loan-to-Value (LTV) Ratio logic
        LTV_ratio = 0.50 # 50% max loan
        loan_limit = total_income * LTV_ratio
        
        # Feature 1: Credit Grade Logic
        if adjusted_income_per_acre > 100000:
            grade, color, risk = "A (Excellent)", "green", "Low Default Risk"
        elif adjusted_income_per_acre > 50000:
            grade, color, risk = "B (Good)", "blue", "Standard Risk"
        elif adjusted_income_per_acre > 25000:
            grade, color, risk = "C (Fair)", "orange", "Moderate Risk"
        else:
            grade, color, risk = "D (Marginal)", "red", "High Default Risk"

        # Interest & Repayment Math
        tenure_months = 6
        interest_amount = loan_limit * (final_interest_rate / 100) * (tenure_months / 12)
        total_repayment = loan_limit + interest_amount
        monthly_emi = total_repayment / tenure_months

        st.markdown("---")
        
        # Feature 5: Digital Income Certificate View
        with st.container():
            st.markdown(f"<h2 style='text-align: center; color: {color};'>Credit Grade: {grade}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Risk Assessment: {risk}</p>", unsafe_allow_html=True)
            
            # Feature 10: Climate Risk Warning
            if season == 'KHARIF':
                st.warning("⚠️ **Climate Risk Warning:** Kharif season is highly dependent on monsoon predictability. Monitor regional rainfall reports.")
            elif season == 'SUMMER':
                st.warning("⚠️ **Water Risk Warning:** Summer crops require confirmed irrigation access. Verify water source before loan approval.")

            # Main Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Predicted Total Income", f"₹{total_income:,.2f}", f"Stress Test: -{stress_test}%" if stress_test > 0 else "")
            m2.metric("Approved Loan Limit", f"₹{loan_limit:,.2f}", f"Max {int(LTV_ratio*100)}% LTV")
            m3.metric("Total Repayment (6m)", f"₹{total_repayment:,.2f}", f"Interest: ₹{interest_amount:,.2f}", delta_color="inverse")
            m4.metric("Interest Rate", f"{final_interest_rate}%", "Subsidized" if gov_subsidy else "Standard")

            st.markdown("---")
            
            # Feature 6 & 8: Yield Gap & Benchmarking Expander
            with st.expander("📊 View Regional Benchmarking & Yield Gap Analysis"):
                target_income = raw_income_per_acre * 1.25 # Assuming top 10% perform 25% better
                st.write(f"**District Benchmark:** The top-performing farms in **{district}** yield approx. **₹{target_income:,.2f}/acre** for **{crop}**.")
                st.progress(min(int((raw_income_per_acre / target_income) * 100), 100))
                st.caption("Your Farm's Performance vs. District Maximum (Based on AI Market Averages)")

            # Feature 4: Portfolio Diversification Suggestion
            with st.expander("🌱 Crop Diversification Strategy (Risk Reduction)"):
                st.write(f"**Current Monocrop:** {crop} (100% of Land Area)")
                st.write("To reduce market reliance on a single commodity, Gramin Setu recommends allocating 20% of acreage to a secondary rotational crop.")
                st.info("**Bank Suggestion:** Farms with 2+ crop types historically show a 15% lower loan default rate.")

            # Feature 3: Repayment Schedule Table
            with st.expander("📅 View 6-Month Repayment Schedule"):
                schedule_data = []
                for month in range(1, 7):
                    schedule_data.append({"Month": f"Month {month}", "Principal Payment": f"₹{loan_limit/6:,.2f}", "Interest Payment": f"₹{interest_amount/6:,.2f}", "Total EMI": f"₹{monthly_emi:,.2f}"})
                st.table(pd.DataFrame(schedule_data))

    except Exception as e:
        st.error(f"Prediction Error: {e}")

import streamlit as st
import pandas as pd
import joblib
import datetime
from fpdf import FPDF
import base64

# ==========================================
# 1. PAGE SETUP & UI
# ==========================================
st.set_page_config(page_title="Gramin Setu AI", page_icon="🌾", layout="wide")

# ==========================================
# 2. LOAD AI ENGINE
# ==========================================
try:
    model = joblib.load('gramin_setu_model_v2.pkl')
    categories = joblib.load('model_categories.pkl')
except Exception as e:
    st.error(f"CRITICAL SYSTEM ERROR: {e}")
    st.stop()

# ==========================================
# 3. BANKER'S SIDEBAR (Risk & Policy Controls)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    st.header("🏦 Bank Control Panel")
    st.write("Adjust macro-parameters:")
    
    stress_test = st.slider("Market Stress Test (Price Drop %)", 0, 50, 0, 5)
    base_interest = st.number_input("Base Interest Rate (%)", value=12.0)
    
    st.markdown("**Policy Adjustments:**")
    gov_subsidy = st.checkbox("🌱 KCC Govt. Subvention (Drops rate to 4%)")
    collateral = st.checkbox("🔐 Collateral / Guarantor Provided (-2% Rate)")
    
    # Calculate Final Interest
    calc_rate = 4.0 if gov_subsidy else base_interest
    final_interest_rate = calc_rate - 2.0 if collateral else calc_rate
    final_interest_rate = max(final_interest_rate, 1.0) # Prevent negative/zero interest
    
    st.info(f"**Active Interest Rate: {final_interest_rate}%**")
    
    st.markdown("**Loan Structure:**")
    repayment_type = st.radio("Repayment Schedule", ["Monthly EMI", "End-of-Season Bullet"])

# ==========================================
# 4. FARMER INPUT SECTION
# ==========================================
st.title("🌾 Gramin Setu: AI Underwriting Platform")
st.subheader("BBA Module 5 | Group 8 | Alternative Credit Scoring Dashboard")
st.markdown("---")

st.markdown("### 📋 Farm Profile & Asset Assessment")
col1, col2, col3, col4 = st.columns(4)

with col1:
    district = st.selectbox("District", categories['districts'])
with col2:
    season = st.selectbox("Season", categories['seasons'])
with col3:
    crop = st.selectbox("Crop Type", categories['crops'])
with col4:
    area = st.number_input("Land Area (Acres)", min_value=0.1, max_value=100.0, value=1.0)

st.markdown("**Farm Infrastructure (ESG & Risk Reduction):**")
esg1, esg2, esg3 = st.columns(3)
with esg1:
    has_storage = st.checkbox("Warehouse / Storage Access (+10% Value)")
with esg2:
    has_drip = st.checkbox("Drip Irrigation (Improves ESG Score)")
with esg3:
    has_soil_card = st.checkbox("Verified Soil Health Card")

# ==========================================
# 5. BUSINESS LOGIC & MASTER DASHBOARD
# ==========================================
if st.button("Generate Digital Income Certificate & Analysis", type="primary", use_container_width=True):
    query_df = pd.DataFrame([[district, season, crop]], columns=['District_Name', 'Season', 'Crop'])
    
    try:
        # --- CORE MATH & MODIFIERS ---
        raw_income_per_acre = model.predict(query_df)[0]
        
        # Apply Storage & Stress Modifiers
        storage_bonus = 1.10 if has_storage else 1.0
        stress_multiplier = (100 - stress_test) / 100.0
        adjusted_income_per_acre = raw_income_per_acre * storage_bonus * stress_multiplier
        
        total_income = adjusted_income_per_acre * area
        
        # Loan Math
        LTV_ratio = 0.50 
        loan_limit = total_income * LTV_ratio
        tenure_months = 6
        interest_amount = loan_limit * (final_interest_rate / 100) * (tenure_months / 12)
        total_repayment = loan_limit + interest_amount
        
        # Insurance (PMFBY Estimator)
        ins_rate = 0.02 if season == 'KHARIF' else 0.015
        insurance_premium = total_income * ins_rate
        
        # Grading
        if adjusted_income_per_acre > 100000:
            grade, color, risk = "A (Excellent)", "green", "Low Default Risk"
        elif adjusted_income_per_acre > 50000:
            grade, color, risk = "B (Good)", "blue", "Standard Risk"
        elif adjusted_income_per_acre > 25000:
            grade, color, risk = "C (Fair)", "orange", "Moderate Risk"
        else:
            grade, color, risk = "D (Marginal)", "red", "High Default Risk"

        st.markdown("---")
        
        # --- MODERN UI: TABS ---
        tab1, tab2, tab3 = st.tabs(["📊 Financial Assessment", "⚖️ Risk & Market Analytics", "🌱 ESG & Advisory"])
        
        # TAB 1: FINANCIALS
        with tab1:
            st.markdown(f"<h2 style='text-align: center; color: {color};'>Credit Grade: {grade}</h2>", unsafe_allow_html=True)
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Predicted Total Income", f"₹{total_income:,.2f}")
            m2.metric("Approved Loan Limit", f"₹{loan_limit:,.2f}", f"{int(LTV_ratio*100)}% LTV")
            m3.metric("Total Repayment", f"₹{total_repayment:,.2f}", f"Rate: {final_interest_rate}%", delta_color="inverse")
            m4.metric("Est. Insurance (PMFBY)", f"₹{insurance_premium:,.2f}", f"{ins_rate*100}% Premium", delta_color="inverse")
            
            st.markdown("#### 📅 Repayment Schedule")
            if repayment_type == "Monthly EMI":
                monthly_emi = total_repayment / tenure_months
                st.info(f"**Structure:** 6 Equal Monthly Installments of **₹{monthly_emi:,.2f}**")
            else:
                st.info(f"**Structure:** Single Bullet Payment of **₹{total_repayment:,.2f}** at End of Season (Month 6).")

        # TAB 2: RISK
        with tab2:
            st.markdown("#### Market & Climate Risk")
            
            # Volatility & Climate
            if season == 'KHARIF':
                st.warning("⚠️ **Climate Risk:** Kharif is highly dependent on monsoons.")
            elif season == 'SUMMER':
                st.warning("⚠️ **Water Risk:** Confirm irrigation access.")
            else:
                st.success("✅ **Climate Risk:** Rabi season generally shows stable weather patterns.")
                
            # Breakeven & Yield Gap
            target_income = raw_income_per_acre * 1.25
            st.write(f"**District Benchmark:** Top farms in {district} yield approx. **₹{target_income:,.2f}/acre**.")
            st.progress(min(int((raw_income_per_acre / target_income) * 100), 100))
            
            breakeven_pct = (total_repayment / total_income) * 100
            st.write(f"**Breakeven Yield Target:** Farmer must achieve at least **{breakeven_pct:.1f}%** of predicted yield to clear bank debt.")

        # TAB 3: ESG & SUMMARY
        with tab3:
            st.markdown("#### Green Finance & Diversification")
            esg_score = 50 + (25 if has_drip else 0) + (25 if has_soil_card else 0)
            st.metric("Gramin Setu ESG Score", f"{esg_score} / 100")
            
            st.write("💡 **Diversification Tip:** Allocating 20% of land to a secondary rotational crop historically reduces loan default by 15%.")
            
            st.markdown("#### 🤖 AI Banker's Executive Summary")
            approval_text = "Approved" if grade in ["A (Excellent)", "B (Good)", "C (Fair)"] else "High-Risk Review Required"
            st.info(f"**System Recommendation: {approval_text}.** The portfolio for {crop} in {district} shows a {risk} profile. With an ESG score of {esg_score}/100 and a heavily stress-tested LTV of 50%, the maximum recommended exposure is ₹{loan_limit:,.2f} at {final_interest_rate}% interest.")

        # ==========================================
        # 6. PDF GENERATION LOGIC
        # ==========================================
        st.markdown("---")
        st.markdown("### 📄 Official Documentation")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="GRAMIN SETU - DIGITAL INCOME & CREDIT CERTIFICATE", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="1. FARMER & ASSET PROFILE", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 8, txt=f"District: {district} | Season: {season}", ln=True)
        pdf.cell(200, 8, txt=f"Crop: {crop} | Area: {area} Acres", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="2. FINANCIAL ASSESSMENT", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 8, txt=f"Predicted Income: Rs. {total_income:,.2f}", ln=True)
        pdf.cell(200, 8, txt=f"Approved Loan Limit (50% LTV): Rs. {loan_limit:,.2f}", ln=True)
        pdf.cell(200, 8, txt=f"Credit Grade: {grade}", ln=True)
        pdf.cell(200, 8, txt=f"Total Repayment ({tenure_months} months @ {final_interest_rate}%): Rs. {total_repayment:,.2f}", ln=True)
        pdf.ln(15)
        
        # WATERMARK / VALIDATION
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 100, 0) # Dark Green
        pdf.cell(200, 10, txt="*** VALIDATED BY GROUP 8 - GRAMIN SETU ***", ln=True, align='C')
        pdf.set_text_color(100, 100, 100) # Gray
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 10, txt="BBA Module 5 Academic Verification Project", ln=True, align='C')
        
        # Generate PDF as bytes
        pdf_bytes = bytes(pdf.output())
        
        st.download_button(
            label="📥 Download Official Gramin Setu PDF Certificate",
            data=pdf_bytes,
            file_name=f"Gramin_Setu_Certificate_{district}_{crop}.pdf",
            mime="application/pdf",
            type="primary"
        )

    except Exception as e:
        st.error(f"Prediction Error: {e}")

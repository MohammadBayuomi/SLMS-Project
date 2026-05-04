import streamlit as st
import joblib
import pandas as pd
import numpy as np
from datetime import datetime



st.set_page_config(page_title="SLMS Predictor", page_icon="📦")
# 1. Load your model and encoders
model = joblib.load('SLMS.joblib')
le_category = joblib.load('le_category.joblib')
le_state = joblib.load('le_state.joblib')

# 2. Optimized Data Loading
@st.cache_data
def get_data():
    data = pd.read_excel('historical_data.xlsx')
    data['Date'] = pd.to_datetime(data['Date'])
    return data

df = get_data()

st.title("📦 SLMS: Predictive Analytics")

# --- UI INPUTS ---
col1, col2 = st.columns(2)
with col1:
    selected_cat_name = st.selectbox("Product Category", le_category.classes_)
with col2:
    selected_state_name = st.selectbox("Target State/Region", le_state.classes_)

selected_date = st.date_input("Prediction Date", datetime.now())

if st.button("Run Forecast"):
    # Fix: Using 'df' consistently
    cat_data = df[df['Category'] == selected_cat_name].sort_values('Date')
    
    if cat_data.empty:
        st.error("Historical data for this category not found.")
    else:
        cat_encoded = le_category.transform([selected_cat_name])[0]
        state_encoded = le_state.transform([selected_state_name])[0]
        
        # Calculation logic
        latest_record = cat_data.iloc[-1]
        lag_1 = latest_record['Sales_Volume']
        roll_7 = cat_data['Sales_Volume'].tail(7).mean()
        
        # Xmas Logic
        xmas_date = datetime(selected_date.year, 12, 25)
        if selected_date > xmas_date.date(): # Handle dates after Xmas in current year
            xmas_date = datetime(selected_date.year + 1, 12, 25)
        days_to_xmas = (xmas_date - datetime.combine(selected_date, datetime.min.time())).days

        X_input = pd.DataFrame({
            'Category_Encoded': [cat_encoded],
            'State_Encoded': [state_encoded],
            'Lag_1': [lag_1],
            'Rolling_Mean_7': [roll_7],
            'Days_To_Xmas': [days_to_xmas]
        })

        pred_log = model.predict(X_input)
        pred_real = np.expm1(pred_log)
        final_sales = int(np.maximum(pred_real[0], 0))

        st.divider()
        st.subheader("Forecast Results")
        st.metric(label=f"Predicted Sales for {selected_cat_name}", value=f"{final_sales} Units")
        st.write(f"Region: {selected_state_name} | Days to Christmas: {days_to_xmas}")


# Add this at the very end of app.py
st.sidebar.divider()
st.sidebar.write("💡 **Want to learn more?**")
if st.sidebar.button("Meet the SLMS Team"):
    st.switch_page("pages/1_Know_more.py")
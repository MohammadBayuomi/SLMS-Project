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
    # 1. Load the original file
    data = pd.read_excel('historical_data.xlsx')
    
    # 2. THE FIX: Strip hidden spaces from the column headers
    data.columns = data.columns.str.strip()
    
    # 3. Strip hidden spaces from the Category values if they were strings
    # (Though in your image they are already numbers)
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
    # 1. Translate the user's selected word into the ID (e.g., "Bed" -> 23)
    cat_id = le_category.transform([selected_cat_name])[0]
    
    # 2. FIX: Look for 'Category_Encoded' instead of 'Category'
    cat_data = df[df['Category_Encoded'] == cat_id].sort_values('Date')

    if cat_data.empty:
        st.error(f"Historical data for category ID {cat_id} ({selected_cat_name}) not found in the file.")
    else:
        latest = cat_data.iloc[-1]
        
        # 3. Calculate Days_To_Xmas (needed for the variable in your metric)
        xmas_date = datetime(selected_date.year, 12, 25)
        days_to_xmas = (xmas_date - datetime.combine(selected_date, datetime.min.time())).days

        # 4. Create X_input matching your original data's column names
        X_input = pd.DataFrame({
            'Category_Encoded': [cat_id],
            'State_Encoded': [le_state.transform([selected_state_name])[0]],
            'Month': [selected_date.month],
            'DayOfWeek': [selected_date.weekday()],
            'Lag_1': [latest['Lag_1']], 
            'Rolling_Mean_7': [latest['Rolling_Mean_7']],
            'Is_Magic_Date': [latest['Is_Magic_Date']],
            'Pre_Magic_Date': [latest['Pre_Magic_Date']],
            'Is_Holiday': [latest['Is_Holiday']],
            'Days_To_Xmas': [days_to_xmas],
            'Is_Holiday_Season': [latest['Is_Holiday_Season']],
            'Day': [selected_date.day],
            'Is_Weekend': [1 if selected_date.weekday() >= 5 else 0],
            'Lag_7': [latest['Lag_7']],
            'Rolling_Max_7': [latest['Rolling_Max_7']],
            'Rolling_Mean_30': [latest['Rolling_Mean_30']],
            'Lag_364': [latest['Lag_364']],
            'Rolling_Mean_3': [latest['Rolling_Mean_3']]
        })

        # 5. Predict
        pred_log = model.predict(X_input)
        final_sales = int(np.expm1(pred_log)[0])

        st.divider()
        st.subheader("Forecast Results:")
        st.metric(label=f"Predicted Sales for {selected_cat_name}", value=f"{final_sales} Units")
        st.write(f"Region: {selected_state_name} | Days to Christmas: {days_to_xmas}")
        
        # st.success(f"Predicted Sales Volume: {final_sales}")




## The Team page
st.sidebar.divider()
st.sidebar.write("💡 **Want to learn more?**")
if st.sidebar.button("Meet the SLMS Team"):
    st.switch_page("pages/1_Know_more.py")

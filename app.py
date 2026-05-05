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
    # Use read_excel for .xlsx files
    data = pd.read_excel('historical_data.xlsx')
    data['Date'] = pd.to_datetime(data['Date'])
    # Clean whitespace just in case
    data['Category'] = data['Category'].str.strip() 
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
    # 1. Translate user's string selection to the number in your table
    cat_id = le_category.transform([selected_cat_name])[0]
    
    # 2. Find the latest record in your original data for that Category_Encoded
    cat_data = df[df['Category_Encoded'] == cat_id].sort_values('Date')
    
    if cat_data.empty:
        st.error(f"No data found for category ID {cat_id}")
    else:
        latest = cat_data.iloc[-1]
        
        # 3. Create the input for the model using your exact column names
        X_input = pd.DataFrame({
            'Category_Encoded': [cat_id],
            'State_Encoded': [le_state.transform([selected_state_name])[0]],
            'Month': [selected_date.month],
            'DayOfWeek': [selected_date.weekday()],
            'Lag_1': [latest['Lag_1']], # Taking the lag directly from your table
            'Rolling_Mean_7': [latest['Rolling_Mean_7']],
            'Days_To_Xmas': [days_to_xmas],
            # Add the other columns from your image that the model needs:
            'Is_Magic_Date': [latest['Is_Magic_Date']],
            'Pre_Magic_Date': [latest['Pre_Magic_Date']],
            'Is_Holiday': [0], # You can calculate this based on the date
            'Is_Weekend': [1 if selected_date.weekday() >= 5 else 0]
        })

        # 4. Predict
        pred_log = model.predict(X_input)
        final_sales = int(np.expm1(pred_log)[0])
        
        # st.success(f"Predicted Sales Volume: {final_sales}")

        st.divider()
        st.subheader("Forecast Results:")
        st.metric(label=f"Predicted Sales for {selected_cat_name}", value=f"{final_sales} Units")
        st.write(f"Region: {selected_state_name} | Days to Christmas: {days_to_xmas}")


## The Team page
st.sidebar.divider()
st.sidebar.write("💡 **Want to learn more?**")
if st.sidebar.button("Meet the SLMS Team"):
    st.switch_page("pages/1_Know_more.py")
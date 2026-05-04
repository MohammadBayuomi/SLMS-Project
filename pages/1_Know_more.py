# import streamlit as st

# st.set_page_config(page_title="Team Info", layout="wide")

# st.title(" About SLMS Team")

# # Create two columns with specific widths (e.g., 2 parts text, 1 part image)
# col_text, col_img = st.columns([2, 1])

# with col_text:
#     st.subheader("Mohammad Bayuomi")
#     st.write("""
#     Bachelor in Data Science and a Full Stack Developer. 
#     My work on the **Smart Logistic Management System (SLMS)** focuses on 
#     bridging the gap between complex predictive modeling and user-friendly 
#     logistics interfaces. 
    
#     This project secured **First Place** in the Logistics path at the 
#     First Research Conference for University Students in Makkah.
#     """)
#     st.info("Specialization: Data Science ")

# with col_img:
#     # Ensure your image file is in the same folder or root directory
#     st.image("First_place.jpg", caption="Mohammad Bayuomi", use_container_width=True)

import streamlit as st

# Set this to wide to give the description more room
st.set_page_config(page_title="Team Info", layout="wide")

st.title("Meet the Team")

#[cite: 1] - Using the structure from your previous edits
col_text, col_space, col_img = st.columns([10, 1, 5]) # Added a 'space' column for padding

with col_text:
    st.markdown("### Our Mission")
    st.write("Bachelor in Data Science, Passionate Ai and predictive modeling using machine learning with python and experts in data analysis ")
    st.write("Participating with our graduation project SLMS which uses Ai and machine learning techniques " \
    "to improve logistics, We called it SLMS (Smart Logistics Management System) in the Logistics" \
    " path we Achieved the first place in the Conference.")

with col_img:
    # Use the filename of the image you uploaded to your root folder
    st.image("First_place.jpg", use_container_width=True)
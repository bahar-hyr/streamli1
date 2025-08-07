import streamlit as st
import pandas as pd
from PIL import Image
import math



menu = st.sidebar.radio("Choose an option:", ["📝 Form", "📊 csv uploader", " 🖼️ Image Gallery"])


if menu == "📝 Form":
    st.header("User Information Form")

    if "form_data" not in st.session_state:
        st.session_state.form_data = {"name": "", "age": "", "days": 0, "feedback": "", "gender": "Male", "agree": False}

    st.session_state.form_data["name"] = st.text_input("name", value=st.session_state.form_data["name"])
    st.session_state.form_data["age"] = st.text_input("age", value=st.session_state.form_data["age"])
    st.session_state.form_data["days"] = st.slider("How many days do you work per week?", 0, 7, value=st.session_state.form_data["days"])
    st.session_state.form_data["feedback"] = st.text_input("your feedback :", value=st.session_state.form_data["feedback"])
    st.session_state.form_data["gender"] = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.form_data["gender"]))
    st.session_state.form_data["agree"] = st.checkbox("I accept the terms and conditions", value=st.session_state.form_data["agree"])

    st.write("Selected gender:", st.session_state.form_data["gender"])
    st.write("Agreed to terms:", st.session_state.form_data["agree"])

    if st.button("Submit"):
        data = st.session_state.form_data
        if not data["name"]:
            st.warning("Please enter your name.")
        elif not data["agree"]:
            st.warning("You must agree to the terms.")
        else:
            st.success(f"Thank you for submitting {data['name']}")
            st.write("Age:", data["age"])
            st.write("Gender:", data["gender"])
            st.write("Days active per week:", data["days"])
            st.write("You have accepted the terms")




@st.cache_data

def load_csv(file):
    return pd.read_csv(file)

if menu == "📊 csv uploader":
    st.header("Upload SVM (CSV File)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_csv(uploaded_file)

        search_text = st.text_input("🔍 Search in data:")
        if search_text:
            df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1)]
        else:
            df_filtered = df

        rows_per_page = 10
        total_rows = len(df_filtered)
        total_pages = math.ceil(total_rows / rows_per_page)

        selected_page = st.slider("Select page", min_value=1, max_value=total_pages, step=1)
        start_index = (selected_page - 1) * rows_per_page
        end_index = start_index + rows_per_page

        st.subheader("📋 Preview of your data")
        st.markdown("### DATA TABLE")
        st.dataframe(df_filtered.iloc[start_index:end_index], use_container_width=True)




if menu == " 🖼️ Image Gallery":
    st.title("Image Gallery with Batch Upload")
    st.header("Upload an Image")

    if "image_files" not in st.session_state:
        st.session_state.image_files = []

    image_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)

    if image_files:
        st.session_state.image_files = image_files
        st.success(f"✅ {len(image_files)} image(s) uploaded successfully!")

    for image_file in st.session_state.image_files:
        st.write("**File name:**", image_file.name)
        st.image(image_file, caption=image_file.name, use_column_width=True)

    if not st.session_state.image_files:
        st.info("📷 Please upload one or more image files.")

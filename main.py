import streamlit as st
import os
import pandas as pd
from cc_bca_pdf2csv import parse  # Make sure this matches the file name

st.set_page_config(page_title="BCA PDF to CSV", layout="centered")

st.title("📄 BCA Credit Card PDF ➜ 📊 CSV Converter")
st.write("Upload your **BCA credit card PDF**, and this tool will extract transactions into a clean CSV file.")

# Debug: Confirm Streamlit is running
# st.info("✅ App loaded successfully.")

uploaded_file = st.file_uploader("📁 Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    
    if st.button("🚀 Convert to CSV"):
        temp_path = f"temp_{uploaded_file.name}"
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            df = parse(temp_path)
            st.success("✅ PDF successfully converted!")

            st.download_button(
                label="📥 Download CSV",
                data=df.to_csv(index=False),
                file_name="transaction.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error during parsing: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
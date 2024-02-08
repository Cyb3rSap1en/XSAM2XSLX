import streamlit as st
from openpyxl import Workbook
import pandas as pd
import xml.etree.ElementTree as ET
import damage_scenario as ds
import io

    

st.set_page_config(page_title="XSAM TO EXCEL CONVERTER", layout="centered")
st.title("XSAM TO EXCEL CONVERTER")
xsam_file = st.file_uploader("Upload XSAM File", type=["xsam"])


if xsam_file:
        st.success("File successfully uploaded")
        
        st.write("***File Info***")
        st.write(f"File name: {xsam_file.name}")
        st.write(f"File type: {xsam_file.type}")
        st.write(f"File size: {xsam_file.size} bytes")
    
    # if st.button("Convert XSAM to Excel"):
    #     with st.spinner("Converting..."):
        df = ds.xsam_to_excel_converter(xsam_file)
            
        excel_data = io.BytesIO()
    
        with pd.ExcelWriter(excel_data, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            
#     df.to_csv(excel_data, index=False)
        excel_data.seek(0)
    
    
            
            # excel_data.seek(0)
            # excel_content = excel_data.read()            
            
        st.download_button(label='Download Excel',data=excel_data.read(), file_name='output.xlsx')
            # if st.button(f"Conversion successful! [Download Excel file]({excel_file_path})"):
            #     st.success("Downloaded Successfully")

        excel_data.close()
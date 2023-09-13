# import streamlit as st

# from streamlit_back_camera_input import back_camera_input

# image = back_camera_input()
# if image:
#     st.image(image)

# import streamlit as st
# from streamlit_qrcode_scanner import qrcode_scanner

# qr_code = qrcode_scanner(key='qrcode_scanner')

# if qr_code:
#     st.write(qr_code)
import streamlit as st

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as bytes:
    bytes_data = img_file_buffer.getvalue()
    # Check the type of bytes_data:
    # Should output: <class 'bytes'>
    st.write(type(bytes_data))
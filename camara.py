# import streamlit as st

# from streamlit_back_camera_input import back_camera_input

# image = back_camera_input()
# if image:
#     st.image(image)

import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

qr_code = qrcode_scanner(key='qrcode_scanner')

if qr_code:
    st.write(qr_code)
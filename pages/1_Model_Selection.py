# pages/1_Model_Selection.py
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from modules.models import MODELS_DATA

st.set_page_config(page_title="Chọn Mô Hình", layout="wide")

if 'translations' not in st.session_state:
    st.error("Vui lòng bắt đầu từ trang chính (streamlit_main.py).")
    st.stop()

T = st.session_state.translations
st.title(T['screen1_title'])

# Lấy danh sách tên model đã dịch để hiển thị trong selectbox
model_display_names = [T[data['name_key']] for data in MODELS_DATA.values()]
# Tạo map để tra cứu ID của model từ tên hiển thị
name_to_id_map = {T[data['name_key']]: model_id for model_id, data in MODELS_DATA.items()}

selected_model_name = st.selectbox(
    label="Chọn một mô hình để xem thông tin:",
    options=model_display_names,
    label_visibility="collapsed"
)

if selected_model_name:
    selected_model_id = name_to_id_map[selected_model_name]
    model_data = MODELS_DATA[selected_model_id]

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader(T['screen1_model_info_group_title'])
            st.markdown(f"**{T['screen1_equation_label']}**")
            st.markdown(T[model_data['equation_key']], unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"**{T['screen1_description_label']}**")
            st.markdown(T[model_data['description_key']], unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.subheader(T['screen1_model_application_group_title'])
            model_id_str = model_data['id']
            lang_suffix = "Vie" if st.session_state.lang == 'vi' else "Eng"
            image_filename = f"model_{model_id_str[5:]}_{lang_suffix}.png"
            image_path = os.path.join("fig", image_filename)

            if os.path.exists(image_path):
                st.image(image_path)
            else:
                st.warning(f"Không tìm thấy ảnh: {image_path}")
    
    # Lưu model đã chọn vào session state
    st.session_state.selected_model_id = selected_model_id
    st.session_state.selected_model_data = model_data
    
    st.success(f"Đã chọn: **{selected_model_name}**. Chuyển đến trang 'Simulation' ở thanh bên để nhập tham số và chạy mô phỏng.")

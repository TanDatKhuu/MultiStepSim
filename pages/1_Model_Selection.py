# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from modules.models import MODELS_DATA


# Bắt buộc phải có để Streamlit biết cách cấu hình trang
st.set_page_config(page_title="Chọn Mô Hình", layout="wide")

# Kiểm tra xem session_state đã được khởi tạo từ trang chính chưa
if 'translations' not in st.session_state:
    st.error("Vui lòng bắt đầu từ trang chính (streamlit_main.py).")
    st.stop()

# Lấy dữ liệu cần thiết từ session_state
T = st.session_state.translations

# --- Giao diện ---
st.title(T['screen1_title'])

# Tạo danh sách tên model đã được dịch để hiển thị cho người dùng
model_display_names = [T[f"{data['id']}_name"] for data in MODELS_DATA.values()]
# Tạo map để tra cứu key nội bộ từ tên hiển thị
model_vi_keys = list(MODELS_DATA.keys())
name_to_key_map = dict(zip(model_display_names, model_vi_keys))

selected_model_name = st.selectbox(
    label="Chọn một mô hình để xem thông tin:",
    options=model_display_names,
    label_visibility="collapsed"
)

if selected_model_name:
    selected_model_vi_key = name_to_key_map[selected_model_name]
    model_data = MODELS_DATA[selected_model_vi_key]

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
            model_id = model_data['id']
            # Xác định tên file ảnh dựa trên ngôn ngữ đang chọn
            lang_suffix = "Vie" if st.session_state.lang == 'vi' else "Eng"
            image_filename = f"model_{model_id[5:]}_{lang_suffix}.png"
            image_path = os.path.join("fig", image_filename)

            if os.path.exists(image_path):
                st.image(image_path)
            else:
                st.warning(f"Không tìm thấy ảnh: {image_path}")
    
    # Lưu model đã chọn vào session_state để các trang khác có thể sử dụng
    st.session_state.selected_model_vi_key = selected_model_vi_key
    st.session_state.selected_model_data = model_data
    
    st.success(f"Đã chọn: **{selected_model_name}**. Chuyển đến trang 'Simulation' ở thanh bên để nhập tham số và chạy mô phỏng.")

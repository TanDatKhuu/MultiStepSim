import streamlit as st
from modules.translations import LANG_VI, LANG_EN
import os

# Cấu hình trang (phải là lệnh đầu tiên sau khi import và định nghĩa hàm)
st.set_page_config(
    page_title="MultiStepSim",
    page_icon=os.path.join("fig", "icon-app.ico"),
    layout="wide"
)

# Khởi tạo st.session_state để lưu trạng thái
if 'lang' not in st.session_state:
    st.session_state.lang = 'vi'
    st.session_state.translations = LANG_VI

def set_language(lang_code):
    st.session_state.lang = lang_code
    st.session_state.translations = LANG_EN if lang_code == 'en' else LANG_VI
    st.rerun()

# Lấy bản dịch hiện tại từ session_state
T = st.session_state.translations

# --- Giao diện ---
with st.sidebar:
    st.header("Language / Ngôn ngữ")
    if st.button(T['lang_vi'], use_container_width=True):
        set_language('vi')
    if st.button(T['lang_en'], use_container_width=True):
        set_language('en')

# --- Nội dung chính của trang Welcome ---
# (Phần này bạn có thể giữ nguyên hoặc bỏ đi nếu muốn trang chủ chỉ có ảnh nền)
# Để giống ứng dụng gốc, ta sẽ giữ lại
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image(os.path.join("fig", "logotdtu1.png"), width=150)
with col2:
    st.markdown(f"<h2 style='text-align: center; color: #000080;'>{T['welcome_uni']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #000080;'>{T['welcome_faculty']}</h2>", unsafe_allow_html=True)
with col3:
    st.image(os.path.join("fig", "logokhoa1@2.png"), width=100)

st.markdown("---")

welcome_title_html = T['welcome_project_title'].replace('\n', '<br>')
st.markdown(f"<h1 style='text-align: center; color: #990000;'>{welcome_title_html}</h1>", unsafe_allow_html=True)

st.markdown("---")

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.subheader(T['welcome_authors_title'])
    st.write(T['welcome_authors_names'])
with col_info2:
    st.subheader(T['welcome_advisors_title'])
    st.write(T['welcome_advisor1'])
    st.write(T['welcome_advisor2'])

st.info("Chào mừng bạn đến với ứng dụng mô phỏng! Vui lòng chọn một trang từ thanh công cụ bên trái để bắt đầu.")

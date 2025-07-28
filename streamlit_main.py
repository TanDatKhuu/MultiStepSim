# ==============================================
#           IMPORTS & GLOBAL VARIABLES
# ==============================================
import sys
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTextEdit, QPushButton, QStackedWidget,
    QRadioButton, QButtonGroup, QCheckBox, QFormLayout, QLineEdit,
    QGridLayout, QGroupBox, QSizePolicy, QSpacerItem, QFileDialog,
    QMessageBox, QFrame, QSlider
)
from PySide6.QtGui import QFont, Qt, QPixmap, QPainter, QPalette, QBrush, QIcon # Thêm QIcon
from PySide6.QtCore import Slot, QSize, Signal, QEvent, Qt
from matplotlib.ticker import MaxNLocator, LogLocator, NullFormatter
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from matplotlib.figure import Figure
from matplotlib.patches import Circle as MplCircle 
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from datetime import datetime

base_path = os.path.dirname(os.path.abspath(__file__))
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception as e:
        # Bạn có thể log lỗi này nếu muốn, nhưng thường thì bỏ qua cũng không sao
        # print(f"Warning: Could not reconfigure stdout: {e}")
        pass
elif sys.stdout is None:
    # print("Warning: sys.stdout is None, skipping reconfigure.") # Tùy chọn: in ra cảnh báo khi debug
    pass
                
# ==============================================
#           TRANSLATION DICTIONARIES
# ==============================================
# ==============================================
#           TRANSLATION DICTIONARIES
# ==============================================
LANG_VI = {
    "app_title": "Ứng dụng mô phỏng phương pháp đa bước - FMS TDTU", # <<< Sửa
    # Welcome Screen
    "welcome_uni": "TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG", # Giữ nguyên vì là tên riêng
    "welcome_faculty": "KHOA TOÁN - THỐNG KÊ", # Giữ nguyên vì là tên riêng
    "welcome_project_title": "Phương pháp đa bước và ứng dụng\ntrong mô phỏng một số mô hình thực tế", # <<< Sửa
    "welcome_authors_title": "Tác giả",
    "welcome_authors_names": "   Khưu Tấn Đạt – Huỳnh Nhựt Trường – Đào Nhật Gia Ân", # Giữ nguyên tên riêng
    "welcome_advisors_title": "Giảng viên hướng dẫn",
    "welcome_advisor1": "PGS. TS. Trần Minh Phương", # Giữ nguyên tên riêng
    "welcome_advisor2": "TS. Nguyễn Hữu Cần", # Giữ nguyên tên riêng
    "lang_vi": "Tiếng Việt",
    "lang_en": "English", # Sẽ sửa ở LANG_EN
    "start_button": "Bắt đầu",
    # Screen 1
    "screen1_title": "Chọn mô hình thực tế",
    "screen1_model_info_group_title": "Thông tin mô hình",
    "screen1_model_application_group_title": "Ứng dụng của mô hình",
    "screen1_equation_label": "Phương trình vi phân/Nghiệm giải tích:",
    "screen1_description_label": "Mô tả và ý nghĩa tham số:",
    "screen1_continue_button": "Tiếp tục với mô hình này",
    # ================== MODEL 1: Energy Demand ==================
    "model1_name": "Mô hình 1: Nguồn năng lượng",
    "model1_eq": "dO/dt = kO<br>O(t) = O<sub>0</sub>e<sup>kt</sup>",#-t<sub>0</sub>
    "model1_desc": ("Mô hình tăng trưởng theo hàm mũ, mô tả mức tiêu thụ năng lượng theo thời gian.<br>"
                   "O(t): Mức tiêu thụ năng lượng tại thời điểm t.<br>"
                   "dO/dt: Tốc độ tăng trưởng mức tiêu thụ năng lượng.<br>"
                   "O<sub>0</sub>: Mức tiêu thụ năng lượng ban đầu tại thời điểm t<sub>0</sub>.<br>"
                   "k: Hằng số biểu thị tốc độ tăng trưởng.<br>"),
                   #"t<sub>0</sub>: Thời điểm ban đầu."),
    "model1_param1": "Mức tiêu thụ năng lượng ban đầu (O₀)",
    "model1_param2": "Hằng số tốc độ tăng trưởng (k)",
    "model1_param3": "Thời điểm ban đầu (t₀)",
    "model1_param4": "Thời điểm kết thúc (t₁)",
    # ================== MODEl 2 ==================
    "model2_name": "Mô hình 2: Sự tăng trưởng tế bào",
    "model2_eq": "dx/dt = cx<sup>2/3</sup><br>x(t) = (x<sub>0</sub><sup>1/3</sup> + ct/3)<sup>3</sup>",
    "model2_desc": ("Mô hình mô phỏng sự tăng trưởng khối lượng của tế bào.<br>"
                   "x(t): Khối lượng của tế bào tại thời điểm t.<br>"
                   "c: Hằng số biểu thị tốc độ tăng trưởng của tế bào.<br>"
                   "dx/dt: Tốc độ thay đổi của khối lượng tế bào theo thời gian.<br>"
                   "x<sub>0</sub>: Khối lượng ban đầu của tế bào (tại t=0 nếu nghiệm là ct/3)."),
    "model2_param1": "Khối lượng ban đầu (x₀)",
    "model2_param3": "Thời điểm ban đầu (t₀)",
    "model2_param4": "Thời điểm kết thúc (t₁)",
    "model2_calculated_c_label": "Hằng số tốc độ tăng trưởng (c):",
    # ================== MODEL 3: Spread of epidemic ==================
    "model3_name": "Mô hình 3: Sự lây lan dịch bệnh",
    "model3_eq": "y'(t) = -r*y(t)*(n+1-y(t))<br>y(t)  = n(n+1)e<sup>-r(n+1)(t-t<sub>0</sub>)</sup>/(1+ne<sup>-r(n+1)(t-t<sub>0</sub>)</sup>)",
    "model3_desc": ("Mô hình mô phỏng sự thay đổi về số lượng cá thể chưa bị nhiễm bệnh trong một cộng đồng theo thời gian.<br>" # <<< SỬA: "chưa bị nhiễm" như tài liệu hình 3 >>>
                   "x(t): Số lượng cá thể chưa bị nhiễm tại thời điểm t.<br>" # <<< SỬA: theo tài liệu hình 3 >>>
                   "n: Số lượng cá thể dễ bị nhiễm ban đầu.<br>" # <<< SỬA: theo tài liệu hình 3 >>>
                   "r: Hằng số dương đo lường tốc độ lây nhiễm.<br>" # <<< SỬA: theo tài liệu hình 3 >>>
                   "dx/dt: Tốc độ giảm của số người chưa nhiễm (tốc độ lây nhiễm).<br>" # <<< SỬA: theo tài liệu hình 3 >>>
                   "t<sub>0</sub>: Thời điểm ban đầu."),
    "model3_param2": "Số lượng cá thể dễ bị nhiễm ban đầu (n)", # <<< SỬA: theo tài liệu hình 3 >>>
    "model3_param4": "Thời điểm ban đầu (t₀)",
    "model3_param5": "Thời điểm kết thúc (t₁)",
    "model3_calculated_r_label": "Hằng số tốc độ lây nhiễm (r):", # <<< SỬA: theo tài liệu hình 3 >>>
    # ================== MODEL 4: National Economy ==================
    "model4_name": "Mô hình 4: Nền kinh tế quốc gia",
    "model4_eq": "Y''(t) + αY'(t) + βY(t) = mlG", # Giữ nguyên ký hiệu
    "model4_desc": ("Mô hình mô phỏng sự thay đổi của nền kinh tế theo thời gian dựa trên các biến số của kinh tế vĩ mô.<br>"
                   "Y(t): Thu nhập quốc dân.<br>"
                   "Y'(t): Tốc độ thay đổi thu nhập.<br>"
                   "α: Hệ số liên quan đến khuynh hướng tiêu dùng/đầu tư (α = m + ls - lma).<br>" # Bỏ dấu * cho gọn
                   "β: Hệ số phản ứng đầu tư theo thay đổi thu nhập (β = lms).<br>" # Bỏ dấu *
                   "m: Số nhân chi tiêu chính phủ.<br>"
                   "l: Tham số liên quan đến cầu tiền.<br>"
                   "a: Tham số độ nhạy đầu tư theo lãi suất.<br>"
                   "s: Tham số độ nhạy cầu tiền theo lãi suất.<br>"
                   "G: Chi tiêu chính phủ (hằng số)."),
    "model4_param_alpha": "Hệ số α", # <<< Sửa >>>
    "model4_param_beta": "Hệ số β", # <<< Sửa >>>
    "model4_param_a": "Tham số a",
    "model4_param_s": "Tham số s",
    "model4_param_m": "Số nhân m",
    "model4_param_G": "Chi tiêu G",
    "model4_param_l": "Tham số l",
    "model4_param_Y0": "Y(t₀)",
    "model4_param_dY0": "Y'(t₀)",
    "model4_param_t0": "Thời gian t₀",
    "model4_param_t1": "Thời gian t₁",
    # ================== MODEL 5: Pursuit Curve ==================
    "model5_name": "Mô hình 5: Đường cong truy đuổi",
    "model5_eq": "dx/dt = -v * x / √(x<sup>2</sup>+y<sup>2</sup>)<br>dy/dt = -v * y / √(x<sup>2</sup>+y<sup>2</sup>) - u",
    "model5_desc": ("Mô hình tìm quỹ đạo của con thuyền di chuyển dưới tác động của dòng chảy.<br>"
                   "(x(t), y(t)): Tọa độ của con thuyền tại thời điểm t.<br>"
                   "v: Vận tốc của con thuyền (tương đối so với nước).<br>"
                   "u: Vận tốc của dòng chảy (theo chiều âm trục y).<br>"
                   "x<sub>0</sub>, y<sub>0</sub>: Tọa độ ban đầu của con thuyền.<br>"
                   "t<sub>0</sub>, t<sub>1</sub>: Khoảng thời gian mô phỏng."),
    "model5_param_x0": "Tọa độ x ban đầu (x₀)",
    "model5_param_y0": "Tọa độ y ban đầu (y₀)",
    "model5_param_u": "Vận tốc dòng chảy (u)",
    "model5_param_v": "Vận tốc thuyền (v)",
    "model5_param_t0": "Thời điểm bắt đầu (t₀)",
    "model5_param_t1": "Thời điểm kết thúc (t₁)",
    "model5_select_component": "Chọn thành phần để hiển thị:",
    "model5_component_x": "Thành phần X",
    "model5_component_y": "Thành phần Y",

    # Screen 2
    #"screen2_back_button": "⬅ Quay lại chọn mô hình", # <<< Sửa >>>
    #"screen2_goto_screen3_button": "Xem mô phỏng động ➡", # <<< Sửa >>>
    "screen2_back_button": "Quay lại chọn mô hình", # <<< Sửa >>>
    "screen2_goto_screen3_button": "Xem mô phỏng động", # <<< Sửa >>>
    "screen2_goto_screen3_tooltip": "Chuyển đến màn hình mô phỏng động (nếu có)",
    "screen2_method_group": "1. Chọn phương pháp chính",
    "screen2_method_ab": "Adams-Bashforth (AB)",
    "screen2_method_am": "Adams-Moulton (AM)",
    "screen2_details_group_ab": "2. Chi tiết Adams-Bashforth",
    "screen2_details_group_am": "2. Chi tiết Adams-Moulton",
    "screen2_steps_label": "Số bước:",
    "screen2_select_all_steps_cb": "Tất cả",
    "screen2_step2": "2 bước",
    "screen2_step3": "3 bước",
    "screen2_step4": "4 bước",
    "screen2_step5": "5 bước",
    "param_placeholder": "Nhập giá trị số...",
    "screen2_h_label": "Bước nhảy (h):",
    "screen2_sim_toggle": "Hiển thị cửa sổ mô phỏng động riêng",
    "screen2_params_group": "3. Tham số đầu vào của mô hình",
    "screen2_actions_group": "4. Thực thi và lưu trữ", # <<< Sửa >>>
    "screen2_init_button": "🚀 Khởi tạo và vẽ đồ thị", # <<< Sửa >>>
    "screen2_refresh_button": "🔄 Làm mới thông số",
    "screen2_show_data_button": "📊 Xem dữ liệu số",
    "screen2_save_button": "💾 Lưu hình ảnh đồ thị",
    "screen2_plot_solution_title": "Đồ thị nghiệm",
    "screen2_plot_error_title": "Đồ thị sai số L∞",
    "screen2_plot_order_title": "Đồ thị bậc hội tụ",
    "screen2_plot_t_axis": "Thời gian (t)",
    "screen2_plot_value_axis": "Giá trị nghiệm",
    "screen2_plot_n_axis": "Số khoảng con (N)",
    "screen2_plot_h_axis": "Bước nhảy (h)",
    "screen2_plot_error_axis": "Sai số L∞",
    "screen2_plot_log_h_axis": "log(h)",
    "screen2_plot_log_error_axis": "log(Sai số L∞)",
    "screen2_plot_exact_label": "Nghiệm chính xác / Tham chiếu",
    "screen2_plot_error_label_prefix": "Sai số ",
    "screen2_plot_order_data_label_suffix": " (dữ liệu)",
    "screen2_plot_order_fit_label_suffix": " Fit: O(h<sup>{:.2f}</sup>)",
    "screen2_info_area_init": "Nhấn 'Khởi tạo và vẽ đồ thị' để bắt đầu mô phỏng.", # <<< Sửa >>>
    "screen2_info_area_running": "Đang xử lý, vui lòng chờ...",
    "screen2_info_area_error": "Lỗi: ",
    "screen2_info_area_no_results": "Không có kết quả mô phỏng để hiển thị.",
    "screen2_info_area_no_show_data": "Chưa có dữ liệu. Vui lòng chạy mô phỏng trước.",
    "screen2_info_area_show_data_method": "Phương pháp:",
    "screen2_info_area_show_data_textCont1": "bước",
    "screen2_info_area_show_data_textCont2": "với",
    "screen2_info_area_show_data_order": "Bậc hội tụ ước tính:",
    "screen2_info_area_show_data_points_header": "Bảng sai số",
    "screen2_info_area_show_data_time": "t", # Rút gọn
    "screen2_info_area_show_data_approx": "Xấp xỉ", # Rút gọn
    "screen2_info_area_show_data_exact": "Chính xác", # Rút gọn
    "screen2_info_area_show_data_error": "Sai số",
    "screen2_info_area_show_data_more": "(và các điểm khác...)",
    "screen2_info_area_show_data_no_points": "(Không có dữ liệu điểm)",
    "screen2_info_area_refreshed": "Đã làm mới. Sẵn sàng cho mô phỏng mới.",
    "screen2_info_area_complete": "Hoàn thành!",
    "screen2_legend_title": "Chú thích",
    "screen2_legend_order_title": "Bậc hội tụ:",
    "screen2_plot_value_axis_base": "Giá trị",
    "screen2_plot_value_axis_x": "Giá trị (thành phần X)", # <<< Sửa >>>
    "screen2_plot_value_axis_y": "Giá trị (thành phần Y)", # <<< Sửa >>>
    "screen2_plot_error_axis_base": "Sai số L∞",
    "screen2_plot_error_axis_x": "Sai số L∞ (thành phần X)", # <<< Sửa >>>
    "screen2_plot_error_axis_y": "Sai số L∞ (thành phần Y)", # <<< Sửa >>>
    "screen2_plot_log_error_axis_base": "log(Sai số L∞)",
    "screen2_plot_log_error_axis_x": "log(Sai số L∞ X)",
    "screen2_plot_log_error_axis_y": "log(Sai số L∞ Y)",

    "screen2_info_area_show_data_approx_x": "Xấp xỉ",    # Key mới
    "screen2_info_area_show_data_approx_y": "Xấp xỉ",    # Key mới
    "screen2_info_area_show_data_exact_x": "Tham chiếu", # Key mới
    "screen2_info_area_show_data_exact_y": "Tham chiếu", # Key mới
    "screen2_info_area_show_data_error_x": "Sai số",     # Key mới
    "screen2_info_area_show_data_error_y": "Sai số",     # Key mới

    # Simulation Plot Window
    "sim_window_title": "Cửa sổ đồ thị mô phỏng động", # <<< Sửa >>>
    "sim_window_plot_title": "Mô phỏng nghiệm theo thời gian", # <<< Sửa >>>
    "sim_window_t_axis": "Thời gian (t)",
    "sim_window_value_axis": "Giá trị nghiệm", # <<< Sửa >>>
    "sim_window_no_data": "Không có dữ liệu hợp lệ để vẽ đồ thị động",

    # Messages
    "msg_error": "Lỗi",
    "msg_warning": "Cảnh báo",
    "msg_info": "Thông báo",
    "msg_select_method": "Vui lòng chọn một phương pháp.",
    "msg_select_step": "Vui lòng chọn ít nhất một số bước.",
    "msg_select_h": "Vui lòng chọn một giá trị bước nhảy (h).",
    "msg_invalid_h": "Giá trị bước nhảy h không hợp lệ: '{}'.",
    "msg_invalid_input_title": "Lỗi nhập liệu",
    "msg_invalid_input_text": "Vui lòng kiểm tra lại các tham số được tô đỏ.",
    "msg_invalid_param_value": "Tham số '{}' không phải là một số hợp lệ (giá trị nhận được: '{}').",
    "msg_missing_param_value": "Tham số '{}' không được để trống.",
    "msg_model_error_title": "Lỗi mô hình", # <<< Sửa >>>
    "msg_model_no_ode": "Mô hình '{}' chưa được định nghĩa hàm PTVP.",
    "msg_param_error_title": "Lỗi tham số", # <<< Sửa >>>
    "msg_missing_keys": "Thiếu các tham số bắt buộc: {}",
    "msg_missing_y0": "Thiếu điều kiện ban đầu (ví dụ: O₀, x₀, Y(t₀)).",
    "msg_param_value_error_title": "Lỗi giá trị tham số", # <<< Sửa >>>
    "msg_param_value_error_text": "Lỗi giá trị trong tham số: {}",
    "msg_t_end_error": "Thời điểm kết thúc t₁ phải lớn hơn thời điểm bắt đầu t₀.",
    "msg_unknown_error_title": "Lỗi không xác định",
    "msg_unknown_error_prep": "Đã xảy ra lỗi khi chuẩn bị cho mô phỏng: {}",
    "msg_internal_error_title": "Lỗi nội bộ",
    "msg_internal_error_steps": "Giá trị số bước không hợp lệ: {}",
    "msg_simulation_error_title": "Lỗi trong quá trình mô phỏng",
    "msg_simulation_error_text": "Đã xảy ra lỗi trong quá trình chạy mô phỏng: {}",
    "msg_no_results_title": "Không có kết quả",
    "msg_no_results_text": "Không tạo được kết quả mô phỏng hợp lệ.",
    "msg_sim_window_no_data": "Không có dữ liệu để hiển thị trong cửa sổ mô phỏng động.",
    "msg_show_data_no_data": "Chưa có dữ liệu mô phỏng để hiển thị.",
    "msg_save_no_plots": "Chưa có đồ thị nào được tạo để lưu.",
    "msg_save_select_dir": "Vui lòng chọn thư mục để lưu hình ảnh",
    "msg_save_cancelled": "Đã hủy thao tác chọn thư mục.",
    "msg_save_success_title": "Lưu thành công",
    "msg_save_success_text": "Đã lưu {} hình ảnh vào thư mục:\n{}",
    "msg_save_error_title": "Lỗi khi lưu",
    "msg_save_error_text": "Đã lưu {} hình ảnh nhưng gặp một số lỗi:\n{}",
    "msg_save_fail_title": "Lưu thất bại",
    "msg_save_fail_text": "Không thể lưu hình ảnh do lỗi:\n{}",
    "msg_saving_plot_error": "Lỗi khi lưu đồ thị '{}': {}",
    "msg_skipping_save": "Bỏ qua việc lưu đồ thị '{}' (không có dữ liệu).",

    #Screen 3
    "screen3_back_button": "Quay lại nhập tham số", # <<< Sửa >>>
    "screen3_double_back_button": "Quay lại chọn mô hình", # <<< Sửa >>>
    "screen3_dyn_only_title": "Mô phỏng động của mô hình",
    "screen3_dyn_back_tooltip": "Quay lại màn hình nhập liệu và các đồ thị kết quả tĩnh",
    "screen3_settings_group_title": "Cài đặt mô phỏng động", # <<< Sửa >>>
    "screen3_speed_label": "Tốc độ phát lại:",
    "screen3_results_group_title": "Thông tin mô phỏng động",
    "screen3_unified_results_title": "Thông tin mô phỏng",
    "screen3_stop_button": "⏹ Dừng/Tiếp tục mô phỏng", # <<< Sửa >>>
    "screen3_result_time": "Thời gian mô phỏng (t):",
    "screen3_result_c": "Hằng số tăng trưởng (c):",
    "screen3_result_mass": "Số lượng tế bào (hoặc khối lượng):",
    "screen3_legend_model2_cell": "Tế bào",
    "screen3_waiting_for_data": "Đang chờ dữ liệu hoặc bắt đầu mô phỏng...",
    "screen3_result_r_param": "Tham số tốc độ lây nhiễm (r):",
    "screen3_model3_simulation_time_label": "Thời gian mô phỏng ABM (bước):",
    "screen3_actual_time": "Thời gian thực tế (giây):",
    "screen3_total_pop": "Tổng số cá thể ban đầu:",
    "screen3_infected_pop": "Số lượng cá thể bị nhiễm:",
    "screen3_susceptible_pop": "Số lượng cá thể chưa nhiễm:",
    "screen3_legend_abm_susceptible": "Chưa nhiễm",
    "screen3_legend_abm_infected": "Bị nhiễm",

    "screen3_sim_list_group_title": "Danh sách mô phỏng",
    "screen3_sim1_name_m5": "Mô phỏng 1: Bài toán con thuyền sang sông nhằm đích cố định",
    "screen3_sim2_name_m5": "Mô phỏng 2: Bài toán tàu khu trục lùng bắt tàu ngầm (trong sương mù)",

    "screen3_info_m5_sim1_title": "Thông tin mô phỏng 1 (con thuyền)", # <<< Sửa >>>
    "screen3_m5_boat_speed": "Vận tốc thuyền (v):",
    "screen3_m5_water_speed": "Vận tốc dòng nước (u):",
    "screen3_m5_crossing_time": "Thời gian mô phỏng (t):",
    "screen3_m5_start_point_boat": "Điểm bắt đầu của thuyền:",
    "screen3_m5_boat_reaches_target": "Thuyền có đến được đích không?",
    "screen3_m5_boat_final_pos": "Vị trí cuối cùng của thuyền:",
    "screen3_m5_determining_status": "Đang xác định...",
    "answer_yes": "Có",
    "answer_no": "Không",

    "screen3_info_m5_sim2_title": "Thông tin mô phỏng 2 (tàu khu trục vs tàu ngầm)", # <<< Sửa >>>
    "screen3_m5_submarine_speed": "Vận tốc tàu ngầm (v<sub>target</sub>):",
    "screen3_m5_destroyer_speed": "Vận tốc tàu khu trục (v<sub>pursuer</sub>):",
    "screen3_legend_m5s2_tn_avoid_radius": "Radar của tàu ngầm",
    "screen3_legend_m5s2_kt_radar_radius": "Radar của tàu khu trục",
    "screen3_m5_submarine_trajectory": "Phương trình quỹ đạo cơ sở của tàu ngầm:",
    "screen3_m5_start_point_submarine": "Điểm bắt đầu của tàu ngầm:",
    "screen3_m5_start_point_destroyer": "Điểm bắt đầu của tàu khu trục:",
    "screen3_m5_destroyer_catches_submarine": "Tàu khu trục có bắt được tàu ngầm không?",
    "screen3_m5_catch_point": "Điểm bắt được (tọa độ):",
    "screen3_m5_catch_time": "Thời gian mô phỏng:", # <<< SỬA: Để là "Thời gian mô phỏng" ban đầu >>>
    "screen3_model5_not_implemented_msg": "Mô phỏng cho kịch bản này chưa được triển khai.",

    "screen3_model2_anim_plot_title": "Mô phỏng động: Sự tăng trưởng tế bào", # <<< Sửa >>>
    "screen3_abm_anim_plot_title": "Mô phỏng động: Sự lây lan dịch bệnh (ABM)", # <<< Sửa >>>

    "screen3_model5_plot_title_sim1": "Mô phỏng động: Con thuyền qua sông", # <<< Sửa >>>
    "screen3_model5_plot_title_sim2": "Mô phỏng động: Tàu khu trục - Tàu ngầm", # <<< Sửa >>>

    "screen3_model5_plot_xlabel_sim1": "Tọa độ X (m)",
    "screen3_model5_plot_ylabel_sim1": "Tọa độ Y (m)",
    "screen3_legend_m5s1_path": "Quỹ đạo thuyền",
    "screen3_legend_m5s1_boat": "Con thuyền",
    "screen3_legend_m5s1_water_current": "Hướng dòng nước",

    "screen3_model5_plot_xlabel_sim2": "Tọa độ X (m)",
    "screen3_model5_plot_ylabel_sim2": "Tọa độ Y (m)",
    "screen3_legend_m5s2_submarine": "Tàu ngầm",
    "screen3_legend_m5s2_destroyer": "Tàu khu trục",
    "screen3_legend_m5s2_path_submarine": "Quỹ đạo tàu ngầm",
    "screen3_legend_m5s2_path_destroyer": "Quỹ đạo tàu khu trục",
    "screen3_legend_m5s2_catch_point": "Điểm bắt được",
    # <<< THÊM KEY CHO MODEL 3 (NẾU CẦN CHO LOGIC ĐỔI LABEL CỦA BẠN) >>>
    "screen3_m5_time_when_caught_label": "Thời gian bắt được tàu ngầm:",
}

# ========================================================================================================

LANG_EN = {
    "app_title": "Multi-step methods simulation application - FMS TDTU", # <<< Sửa
    # Welcome Screen
    "welcome_uni": "TON DUC THANG UNIVERSITY",
    "welcome_faculty": "FACULTY OF MATHEMATICS - STATISTICS",
    "welcome_project_title": "Multi-step methods and applications\n in simulating some real-life models", # <<< Sửa
    "welcome_authors_title": "Authors",
    "welcome_authors_names": "Tan Dat Khuu – Nhut Truong Huynh – Nhat Gia An Dao",
    "welcome_advisors_title": "Advisors",
    "welcome_advisor1": "Assoc. Prof. Minh Phuong Tran",
    "welcome_advisor2": "PhD. Huu Can Nguyen",
    "lang_vi": "Tiếng Việt", # Sẽ là tiếng Việt ở đây
    "lang_en": "English",
    "start_button": "Start",
    # Screen 1
    "screen1_title": "Select a real-life model", # <<< Sửa
    "screen1_model_info_group_title": "Model information", # <<< Sửa
    "screen1_model_application_group_title": "Model application", # <<< Sửa
    "screen1_equation_label": "Differential equation / Analytical solution:", # <<< Sửa
    "screen1_description_label": "Description and parameters:", # <<< Sửa
    "screen1_continue_button": "Continue with this model", # <<< Sửa
    # ================== MODEL 1: Energy Demand ==================
    "model1_name": "Model 1: Energy demand", # <<< Sửa
    "model1_eq": "dO/dt = kO<br>O(t) = O<sub>0</sub>e<sup>kt</sup>",#-t<sub>0</sub>
    "model1_desc": ("Exponential growth model describing energy consumption over time.<br>"
                   "O(t): Energy consumption level at time t.<br>"
                   "dO/dt: Rate of growth of energy consumption.<br>"
                   "O<sub>0</sub>: Initial energy consumption level at time t<sub>0</sub>.<br>"
                   "k: Constant representing the growth rate.<br>"),
                   #"t<sub>0</sub>: Initial time."),
    "model1_param1": "Initial energy consumption (O₀)",
    "model1_param2": "Growth rate constant (k)",
    "model1_param3": "Initial time (t₀)",
    "model1_param4": "End time (t₁)",
    # ================== MODEl 2 ==================
    "model2_name": "Model 2: Cell growth", # <<< Sửa
    "model2_eq": "dx/dt = cx<sup>2/3</sup><br>x(t) = (x<sub>0</sub><sup>1/3</sup> + ct/3)<sup>3</sup>",
    "model2_desc": ("Model simulating the growth of cell mass.<br>"
                   "x(t): Mass of the cell at time t.<br>"
                   "c: Constant representing the cell growth rate.<br>"
                   "dx/dt: Rate of change of cell mass over time.<br>"
                   "x<sub>0</sub>: Initial mass of the cell (at t=0 if solution is ct/3)."),
    "model2_param1": "Initial mass (x₀)",
    "model2_param3": "Initial time (t₀)",
    "model2_param4": "End time (t₁)",
    "model2_calculated_c_label": "Growth rate constant (c):",
    # ================== MODEL 3: Spread of epidemic ==================
    "model3_name": "Model 3: Spread of epidemic", # <<< Sửa
    "model3_eq": "y'(t) = -r*y(t)*(n+1-y(t))<br>y(t)  = n(n+1)e<sup>-r(n+1)(t-t<sub>0</sub>)</sup>/(1+ne<sup>-r(n+1)(t-t<sub>0</sub>)</sup>)",
    "model3_desc": ("Model simulating the change in the number of uninfected individuals in a community over time.<br>"
                   "x(t): Number of uninfected individuals at time t.<br>"
                   "n: Initial number of susceptible individuals.<br>"
                   "r: Positive constant measuring the rate of infection.<br>"
                   "dx/dt: Rate of decrease of uninfected individuals (infection rate).<br>"
                   "t<sub>0</sub>: Initial time."),
    "model3_param2": "Initial number of susceptible individuals (n)",
    "model3_param4": "Initial time (t₀)",
    "model3_param5": "End time (t₁)",
    "model3_calculated_r_label": "Infection rate constant (r):",
    # ================== MODEL 4: National Economy ==================
    "model4_name": "Model 4: National economy", # <<< Sửa
    "model4_eq": "Y''(t) + αY'(t) + βY(t) = mlG",
    "model4_desc": ("The model simulates economic changes over time based on macroeconomic variables.<br>"
                   "Y(t): National income.<br>"
                   "Y'(t): Rate of change of income.<br>"
                   "α: Coefficient related to propensity to consume/invest (α = m + ls - lma).<br>"
                   "β: Investment response to income change (β = lms).<br>"
                   "m: Government spending multiplier.<br>"
                   "l: Parameter related to money demand.<br>"
                   "a: Investment sensitivity to interest rate.<br>"
                   "s: Money demand sensitivity to interest rate.<br>"
                   "G: Government spending (constant)."),
    "model4_param_alpha": "Coefficient α", # <<< Sửa
    "model4_param_beta": "Coefficient β", # <<< Sửa
    "model4_param_a": "Parameter a",
    "model4_param_s": "Parameter s",
    "model4_param_m": "Multiplier m",
    "model4_param_G": "Spending G",
    "model4_param_l": "Parameter l",
    "model4_param_Y0": "Y(t₀)",
    "model4_param_dY0": "Y'(t₀)",
    "model4_param_t0": "Time t₀",
    "model4_param_t1": "Time t₁",
    # ================== MODEL 5: Pursuit Curve ==================
    "model5_name": "Model 5: Pursuit curve", # <<< Sửa
    "model5_eq": "dx/dt = -v * x / √(x<sup>2</sup>+y<sup>2</sup>)<br>dy/dt = -v * y / √(x<sup>2</sup>+y<sup>2</sup>) - u",
    "model5_desc": ("Model to find the trajectory of a boat moving under the influence of a current.<br>"
                   "(x(t), y(t)): Coordinates of the boat at time t.<br>"
                   "v: Velocity of the boat (relative to water).<br>"
                   "u: Velocity of the current (in the negative y-direction).<br>"
                   "x<sub>0</sub>, y<sub>0</sub>: Initial coordinates of the boat.<br>"
                   "t<sub>0</sub>, t<sub>1</sub>: Simulation time interval."),
    "model5_param_x0": "Initial x-coordinate (x₀)",
    "model5_param_y0": "Initial y-coordinate (y₀)",
    "model5_param_u": "Current velocity (u)",
    "model5_param_v": "Boat velocity (v)",
    "model5_param_t0": "Start time (t₀)",
    "model5_param_t1": "End time (t₁)",
    "model5_select_component": "Select component to display:",
    "model5_component_x": "X-Component",
    "model5_component_y": "Y-Component",

    # Screen 2
    #"screen2_back_button": "⬅ Back to model selection", # <<< Sửa
    #"screen2_goto_screen3_button": "View dynamic simulation ➡", # <<< Sửa
    "screen2_back_button": "Back to model selection", # <<< Sửa
    "screen2_goto_screen3_button": "View dynamic simulation", # <<< Sửa
    "screen2_goto_screen3_tooltip": "Switch to the dynamic simulation screen (if available)",
    "screen2_method_group": "1. Select main method",
    "screen2_method_ab": "Adams-Bashforth (AB)",
    "screen2_method_am": "Adams-Moulton (AM)",
    "screen2_details_group_ab": "2. Adams-Bashforth details", # <<< Sửa
    "screen2_details_group_am": "2. Adams-Moulton details", # <<< Sửa
    "screen2_steps_label": "Number of steps:",
    "screen2_select_all_steps_cb": "All",
    "screen2_step2": "2-step",
    "screen2_step3": "3-step",
    "screen2_step4": "4-step",
    "screen2_step5": "5-step",
    "param_placeholder": "Enter numeric value...",
    "screen2_h_label": "Step size (h):",
    "screen2_sim_toggle": "Show separate dynamic simulation window",
    "screen2_params_group": "3. Model input parameters", # <<< Sửa
    "screen2_actions_group": "4. Execute and save", # <<< Sửa
    "screen2_init_button": "🚀 Initialize and plot graphs", # <<< Sửa
    "screen2_refresh_button": "🔄 Refresh parameters", # <<< Sửa
    "screen2_show_data_button": "📊 View numerical data", # <<< Sửa
    "screen2_save_button": "💾 Save plot images", # <<< Sửa
    "screen2_plot_solution_title": "Solution plot", # <<< Sửa
    "screen2_plot_error_title": "L∞ error plot", # <<< Sửa
    "screen2_plot_order_title": "Convergence order plot", # <<< Sửa
    "screen2_plot_t_axis": "Time (t)",
    "screen2_plot_value_axis": "Solution value",
    "screen2_plot_n_axis": "Number of subintervals (N)",
    "screen2_plot_h_axis": "Step size (h)",
    "screen2_plot_error_axis": "L∞ Error",
    "screen2_plot_log_h_axis": "log(h)",
    "screen2_plot_log_error_axis": "log(L∞ Error)",
    "screen2_plot_exact_label": "Exact solution / Reference",
    "screen2_plot_error_label_prefix": "Error ",
    "screen2_plot_order_data_label_suffix": " (data)",
    "screen2_plot_order_fit_label_suffix": " Fit: O(h<sup>{:.2f}</sup>)",
    "screen2_info_area_init": "Press 'Initialize and plot graphs' to start the simulation.",
    "screen2_info_area_running": "Processing, please wait...",
    "screen2_info_area_error": "Error: ",
    "screen2_info_area_no_results": "No simulation results to display.",
    "screen2_info_area_no_show_data": "No data available. Please run a simulation first.",
    "screen2_info_area_show_data_method": "Method:",
    "screen2_info_area_show_data_textCont1": "-step",
    "screen2_info_area_show_data_textCont2": "with h =",
    "screen2_info_area_show_data_order": "Estimated convergence order:",
    "screen2_info_area_show_data_points_header": "Table of error",
    "screen2_info_area_show_data_time": "t", # Shorten
    "screen2_info_area_show_data_approx": "Approximate", # Shorten
    "screen2_info_area_show_data_exact": "Exact", # Shorten
    "screen2_info_area_show_data_error": "Error",
    "screen2_info_area_show_data_more": "(and other points...)",
    "screen2_info_area_show_data_no_points": "(No point data)",
    "screen2_info_area_refreshed": "Fields refreshed. Ready for new simulation.",
    "screen2_info_area_complete": "Completed!",
    "screen2_legend_title": "Legend",
    "screen2_legend_order_title": "Convergence order:", # <<< Sửa
    "screen2_plot_value_axis_base": "Value",
    "screen2_plot_value_axis_x": "Value (X-component)", # <<< Sửa
    "screen2_plot_value_axis_y": "Value (Y-component)", # <<< Sửa
    "screen2_plot_error_axis_base": "L∞ Error",
    "screen2_plot_error_axis_x": "L∞ Error (X-component)", # <<< Sửa
    "screen2_plot_error_axis_y": "L∞ Error (Y-component)", # <<< Sửa
    "screen2_plot_log_error_axis_base": "log(L∞ Error)",
    "screen2_plot_log_error_axis_x": "log(L∞ Error X)",
    "screen2_plot_log_error_axis_y": "log(L∞ Error Y)",
    "screen2_info_area_show_data_approx_x": "Approximate",
    "screen2_info_area_show_data_approx_y": "Approximate",
    "screen2_info_area_show_data_exact_x": "Reference",
    "screen2_info_area_show_data_exact_y": "Reference",
    "screen2_info_area_show_data_error_x": "Error",
    "screen2_info_area_show_data_error_y": "Error",

    # Simulation Plot Window
    "sim_window_title": "Dynamic simulation plot window", # <<< Sửa
    "sim_window_plot_title": "Solution simulation over time", # <<< Sửa
    "sim_window_t_axis": "Time (t)",
    "sim_window_value_axis": "Solution Value",
    "sim_window_no_data": "No valid data to plot dynamically",

    # Messages
    "msg_error": "Error",
    "msg_warning": "Warning",
    "msg_info": "Information",
    "msg_select_method": "Please select a method.",
    "msg_select_step": "Please select at least one number of steps.",
    "msg_select_h": "Please select a step size (h).",
    "msg_invalid_h": "Invalid step size h: '{}'.",
    "msg_invalid_input_title": "Input error", # <<< Sửa
    "msg_invalid_input_text": "Please check the parameters highlighted in red.",
    "msg_invalid_param_value": "Parameter '{}' is not a valid number (received value: '{}').",
    "msg_missing_param_value": "Parameter '{}' cannot be empty.",
    "msg_model_error_title": "Model error", # <<< Sửa
    "msg_model_no_ode": "Model '{}' does not have an ODE function defined.",
    "msg_param_error_title": "Parameter error", # <<< Sửa
    "msg_missing_keys": "Missing required parameters: {}",
    "msg_missing_y0": "Missing initial condition (e.g., O₀, x₀, Y(t₀)).",
    "msg_param_value_error_title": "Parameter value error", # <<< Sửa
    "msg_param_value_error_text": "Value error in parameter: {}",
    "msg_t_end_error": "End time t₁ must be greater than start time t₀.",
    "msg_unknown_error_title": "Unknown error", # <<< Sửa
    "msg_unknown_error_prep": "An error occurred while preparing for the simulation: {}",
    "msg_internal_error_title": "Internal error", # <<< Sửa
    "msg_internal_error_steps": "Invalid number of steps: {}",
    "msg_simulation_error_title": "Simulation error", # <<< Sửa
    "msg_simulation_error_text": "An error occurred during the simulation process: {}",
    "msg_no_results_title": "No results", # <<< Sửa
    "msg_no_results_text": "No valid simulation results were generated.",
    "msg_sim_window_no_data": "No data available to display in the dynamic simulation window.",
    "msg_show_data_no_data": "No simulation data has been generated yet.",
    "msg_save_no_plots": "No plots have been generated to save.",
    "msg_save_select_dir": "Please select a directory to save images",
    "msg_save_cancelled": "Directory selection was cancelled.",
    "msg_save_success_title": "Save successful", # <<< Sửa
    "msg_save_success_text": "Saved {} image(s) to the directory:\n{}",
    "msg_save_error_title": "Save error", # <<< Sửa
    "msg_save_error_text": "Saved {} image(s) but encountered some errors:\n{}",
    "msg_save_fail_title": "Save failed", # <<< Sửa
    "msg_save_fail_text": "Could not save images due to an error:\n{}",
    "msg_saving_plot_error": "Error saving plot '{}': {}",
    "msg_skipping_save": "Skipping save for plot '{}' (no data).",

    #Screen 3
    "screen3_back_button": "Back to parameters", # <<< Sửa
    "screen3_double_back_button": "Back to model selection", # <<< Sửa
    "screen3_dyn_only_title": "Dynamic model simulation", # <<< Sửa
    "screen3_dyn_back_tooltip": "Back to the input and static results screen",
    "screen3_settings_group_title": "Dynamic simulation settings", # <<< Sửa
    "screen3_speed_label": "Playback speed:",
    "screen3_results_group_title": "Dynamic simulation information", # <<< Sửa
    "screen3_unified_results_title": "Simulation information", # <<< Sửa
    "screen3_stop_button": "⏹ Pause/Resume simulation", # <<< Sửa
    "screen3_result_time": "Simulation time (t):",
    "screen3_result_c": "Growth constant (c):",
    "screen3_result_mass": "Cell count (or mass):",
    "screen3_legend_model2_cell": "Cell",
    "screen3_waiting_for_data": "Waiting for data or to start simulation...",
    "screen3_result_r_param": "Infection rate parameter (r):",
    "screen3_model3_simulation_time_label": "ABM simulation time (steps):",
    "screen3_actual_time": "Real time elapsed (seconds):",
    "screen3_total_pop": "Initial total population:",
    "screen3_infected_pop": "Number of infected individuals:",
    "screen3_susceptible_pop": "Number of susceptible individuals:",
    "screen3_legend_abm_susceptible": "Susceptible",
    "screen3_legend_abm_infected": "Infected",

    "screen3_sim_list_group_title": "Simulation List",
    "screen3_sim1_name_m5": "Simulation 1: Boat crossing river to a fixed target",
    "screen3_sim2_name_m5": "Simulation 2: Destroyer hunting submarine (In fog)",

    "screen3_info_m5_sim1_title": "Simulation 1 information (boat crossing)", # <<< Sửa
    "screen3_m5_boat_speed": "Boat velocity (v):",
    "screen3_m5_water_speed": "Current velocity (u):",
    "screen3_m5_crossing_time": "Simulation time (t):",
    "screen3_m5_start_point_boat": "Boat's starting point:",
    "screen3_m5_boat_reaches_target": "Does the boat reach the target?",
    "screen3_m5_boat_final_pos": "Boat's final position:",
    "screen3_m5_determining_status": "Determining...",
    "answer_yes": "Yes",
    "answer_no": "No",

    "screen3_info_m5_sim2_title": "Simulation 2 information (destroyer vs. submarine)", # <<< Sửa
    "screen3_m5_submarine_speed": "Submarine velocity (v<sub>target</sub>):",
    "screen3_m5_destroyer_speed": "Destroyer velocity (v<sub>pursuer</sub>):",
    "screen3_legend_m5s2_tn_avoid_radius": "Submarine radar zone", # <<< Sửa
    "screen3_legend_m5s2_kt_radar_radius": "Destroyer radar zone", # <<< Sửa
    "screen3_m5_submarine_trajectory": "Submarine base trajectory equation:",
    "screen3_m5_start_point_submarine": "Submarine's starting point:",
    "screen3_m5_start_point_destroyer": "Destroyer's starting point:",
    "screen3_m5_destroyer_catches_submarine": "Does the destroyer catch the submarine?",
    "screen3_m5_catch_point": "Catch point (coordinates):",
    "screen3_m5_catch_time": "Simulation time:", # <<< SỬA >>>
    "screen3_model5_not_implemented_msg": "Simulation for this scenario is not yet implemented.",

    "screen3_model2_anim_plot_title": "Dynamic simulation: Cell growth", # <<< Sửa
    "screen3_abm_anim_plot_title": "Dynamic simulation: Epidemic spread (ABM)", # <<< Sửa

    "screen3_model5_plot_title_sim1": "Dynamic simulation: Boat crossing river", # <<< Sửa
    "screen3_model5_plot_title_sim2": "Dynamic simulation: Destroyer - Submarine", # <<< Sửa

    "screen3_model5_plot_xlabel_sim1": "X Position (m)",
    "screen3_model5_plot_ylabel_sim1": "Y Position (m)",
    "screen3_legend_m5s1_path": "Boat trajectory", # <<< Sửa
    "screen3_legend_m5s1_boat": "Boat",
    "screen3_legend_m5s1_water_current": "Water current direction", # <<< Sửa

    "screen3_model5_plot_xlabel_sim2": "X Position (m)",
    "screen3_model5_plot_ylabel_sim2": "Y Position (m)",
    "screen3_legend_m5s2_submarine": "Submarine",
    "screen3_legend_m5s2_destroyer": "Destroyer",
    "screen3_legend_m5s2_path_submarine": "Submarine trajectory", # <<< Sửa
    "screen3_legend_m5s2_path_destroyer": "Destroyer trajectory", # <<< Sửa
    "screen3_legend_m5s2_catch_point": "Catch point",
    "screen3_m5_time_when_caught_label": "Time to catch submarine:", # <<< THÊM >>>
}
# ==============================================
#           UTILITY CLASSES
# ==============================================

class RetranslatableWidget(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        if self.main_window:
            self.main_window.languageChanged.connect(self.retranslate_ui)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self):
        pass

    def tr(self, key, default_text=""):
        if self.main_window and hasattr(self.main_window, 'translations'):
            return self.main_window.translations.get(key, default_text if default_text else key)
        return default_text if default_text else key

# ==============================================
#           ODE Solver Methods
# ==============================================
#RK,AB,AM bậc 1
# Runge-Kutta 2nd order method (GIỐNG STANDALONE)
def RK2(f, t, y0):
    h = t[1] - t[0]
    y = [y0]
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        # Chú ý: Standalone gốc có thể đã dùng công thức Euler cho k2.
        # Bản chuẩn Heun's method (thường gọi là RK2) là:
        k2_std = h * f(t[i] + h, y[i] + k1)
        y_new = y[i] + (k1 + k2_std) / 2.0
        # Nếu standalone gốc thực sự dùng công thức RK2 hơi khác:
        # k2_standalone_like = h * f(t[i] + h, y[i] + k1) # Giống trên
        # y_new = y[i] + (k1 + k2_standalone_like) / 2 # Vẫn giống công thức chuẩn này
        y.append(y_new)
    return np.array(y) # Trả về array

# Runge-Kutta 3rd order method (GIỐNG STANDALONE)
def RK3(f, t, y0):
    h = t[1] - t[0]
    y = [y0]
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 2.0, y[i] + k1 / 2.0)
        k3 = h * f(t[i] + h, y[i] - k1 + 2.0 * k2)
        y_new = y[i] + (k1 + 4.0 * k2 + k3) / 6.0
        y.append(y_new)
    return np.array(y) # Trả về array

# Runge-Kutta 4th order method (GIỐNG STANDALONE)
def RK4(f, t, y0):
    h = t[1] - t[0]
    y = [y0]
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 2.0, y[i] + k1 / 2.0)
        k3 = h * f(t[i] + h / 2.0, y[i] + k2 / 2.0)
        k4 = h * f(t[i] + h, y[i] + k3)
        y_new = y[i] + (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        y.append(y_new)
    return np.array(y) # Trả về array

# Runge-Kutta 5th order method (GIỐNG STANDALONE)
def RK5(f, t, y0):
    h = t[1] - t[0]
    y = [y0]
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 4.0, y[i] + k1 / 4.0)
        k3 = h * f(t[i] + h / 4.0, y[i] + k1 / 8.0 + k2 / 8.0)
        k4 = h * f(t[i] + h / 2.0, y[i] - k2 / 2.0 + k3)
        k5 = h * f(t[i] + 3.0 * h / 4.0, y[i] + 3.0 * k1 / 16.0 + 9.0 * k4 / 16.0)
        k6 = h * f(t[i] + h, y[i] - 3.0 * k1 / 7.0 + 2.0 * k2 / 7.0 + 12.0 * k3 / 7.0 - 12.0 * k4 / 7.0 + 8.0 * k5 / 7.0)
        y_new = y[i] + (7.0 * k1 + 32.0 * k3 + 12.0 * k4 + 32.0 * k5 + 7.0 * k6) / 90.0
        y.append(y_new)
    return np.array(y) # Trả về array

# --- Các hàm ABx, AMx giữ nguyên cách gọi RKx đã sửa ở trên ---
def AB2(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK2 đã sửa
    y_start = RK2(f,t[:2],y0) if len(t)>=2 else np.array([y0])
    y = list(y_start) # Chuyển thành list để append
    # Vòng lặp AB2 chính
    for i in range(1, len(t) - 1):
         # Đảm bảo index không vượt quá giới hạn của y đã tính
         if i < len(y) and i-1 < len(y):
             y_new = y[i] + h / 2.0 * (3.0 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
             y.append(y_new)
         else:
             print(f"Warning (AB2): Index out of bounds at i={i}, len(y)={len(y)}")
             break # Thoát nếu có lỗi index
    return np.array(y)

def AB3(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK3 đã sửa
    y_start = RK3(f, t[:3], y0) if len(t) >= 3 else AB2(f, t, y0) # Fallback nếu không đủ điểm
    y = list(y_start)
    # Vòng lặp AB3 chính
    for i in range(2, len(t) - 1):
        if i < len(y) and i-1 < len(y) and i-2 < len(y):
             y_new = y[i] + h / 12.0 * (23.0 * f(t[i], y[i]) - 16.0 * f(t[i-1], y[i-1]) + 5.0 * f(t[i-2], y[i-2]))
             y.append(y_new)
        else:
             print(f"Warning (AB3): Index out of bounds at i={i}, len(y)={len(y)}")
             break
    return np.array(y)

def AB4(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK4 đã sửa
    y_start = RK4(f, t[:4], y0) if len(t) >= 4 else AB3(f, t, y0)
    y = list(y_start)
    # Vòng lặp AB4 chính
    for i in range(3, len(t) - 1):
         if i < len(y) and i-1 < len(y) and i-2 < len(y) and i-3 < len(y):
             y_new = y[i] + h / 24.0 * (55.0 * f(t[i], y[i]) - 59.0 * f(t[i-1], y[i-1]) + 37.0 * f(t[i-2], y[i-2]) - 9.0 * f(t[i-3], y[i-3]))
             y.append(y_new)
         else:
             print(f"Warning (AB4): Index out of bounds at i={i}, len(y)={len(y)}")
             break
    return np.array(y)

def AB5(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK5 đã sửa
    y_start = RK5(f, t[:5], y0) if len(t) >= 5 else AB4(f, t, y0)
    y = list(y_start)
    # Vòng lặp AB5 chính
    for i in range(4, len(t) - 1):
         if i < len(y) and i-1 < len(y) and i-2 < len(y) and i-3 < len(y) and i-4 < len(y):
             y_new = y[i] + h / 720.0 * (1901.0 * f(t[i], y[i]) - 2774.0 * f(t[i-1], y[i-1]) + 2616.0 * f(t[i-2], y[i-2]) - 1274.0 * f(t[i-3], y[i-3]) + 251.0 * f(t[i-4], y[i-4]))
             y.append(y_new)
         else:
             print(f"Warning (AB5): Index out of bounds at i={i}, len(y)={len(y)}")
             break
    return np.array(y)

def AM2(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK2 đã sửa
    y_start = RK2(f, t[:2], y0) if len(t) >= 2 else np.array([y0])
    y = list(y_start)
    # Vòng lặp AM2
    for i in range(1, len(t) - 1):
         if i < len(y) and i-1 < len(y):
             # Predictor (AB2 step)
             y_pred = y[i] + h / 2.0 * (3.0 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
             # Corrector (AM2 step)
             # Kiểm tra index t[i+1]
             if i + 1 < len(t):
                 y_new = y[i] + h / 12.0 * (5.0 * f(t[i+1], y_pred) + 8.0 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
                 y.append(y_new)
             else:
                 print(f"Warning (AM2): Index t[i+1] out of bounds at i={i}")
                 break
         else:
             print(f"Warning (AM2): Index out of bounds at i={i}, len(y)={len(y)}")
             break
    return np.array(y)

def AM3(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK3 đã sửa
    y_start = RK3(f, t[:3], y0) if len(t) >= 3 else AM2(f, t, y0)
    y = list(y_start)
    # Vòng lặp AM3
    for i in range(2, len(t) - 1):
         if i < len(y) and i-1 < len(y) and i-2 < len(y):
             # Predictor (AB3 step)
             y_pred = y[i] + h / 12.0 * (23.0 * f(t[i], y[i]) - 16.0 * f(t[i-1], y[i-1]) + 5.0 * f(t[i-2], y[i-2]))
             # Corrector (AM3 step)
             if i + 1 < len(t):
                 y_new = y[i] + h / 24.0 * (9.0 * f(t[i+1], y_pred) + 19.0 * f(t[i], y[i]) - 5.0 * f(t[i-1], y[i-1]) + f(t[i-2], y[i-2]))
                 y.append(y_new)
             else:
                 print(f"Warning (AM3): Index t[i+1] out of bounds at i={i}")
                 break
         else:
             print(f"Warning (AM3): Index out of bounds at i={i}, len(y)={len(y)}")
             break
    return np.array(y)

def AM4(f, t, y0):
    h = t[1]-t[0]
    # Gọi RK4 đã sửa
    y_start = RK4(f, t[:4], y0) if len(t) >= 4 else AM3(f, t, y0)
    y = list(y_start)
    # Vòng lặp AM4
    for i in range(3, len(t) - 1):
         if i < len(y) and i-1 < len(y) and i-2 < len(y) and i-3 < len(y):
             # Predictor (AB4 step)
             y_pred = y[i] + h / 24.0 * (55.0 * f(t[i], y[i]) - 59.0 * f(t[i-1], y[i-1]) + 37.0 * f(t[i-2], y[i-2]) - 9.0 * f(t[i-3], y[i-3]))
             # Corrector (AM4 step)
             if i + 1 < len(t):
                 y_new = y[i] + h / 720.0 * (251.0 * f(t[i+1], y_pred) + 646.0 * f(t[i], y[i]) - 264.0 * f(t[i-1], y[i-1]) + 106.0 * f(t[i-2], y[i-2]) - 19.0 * f(t[i-3], y[i-3]))
                 y.append(y_new)
             else:
                 print(f"Warning (AM4): Index t[i+1] out of bounds at i={i}")
                 break
         else:
             print(f"Warning (AM4): Index out of bounds at i={i}, len(y)={len(y)}")
             break
    return np.array(y)
    h = t[1]-t[0]
    y = list(RK4(f,t[:4],y0)) if len(t)>=4 else list(AM3(f,t,y0))
    [y.append(y[i]+h/720*(251*f(t[i+1],y[i]+h/24*(55*f(t[i],y[i])-59*f(t[i-1],y[i-1])+37*f(t[i-2],y[i-2])-9*f(t[i-3],y[i-3])))+646*f(t[i],y[i])-264*f(t[i-1],y[i-1])+106*f(t[i-2],y[i-2])-19*f(t[i-3],y[i-3]))) for i in range(3,len(t)-1)]
    return np.array(y)

#RK,AB,AM bậc 2
# Runge-Kutta 2nd order method for SYSTEMS
def RK2_system(F, t_array, u10, u20): # F trả về [f1, f2]
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        k1_vec = F(t, u1[i-1], u2[i-1]) # k1_vec is [k1_u1, k1_u2]
        k2_vec = F(t + h, u1[i-1] + h*k1_vec[0], u2[i-1] + h*k1_vec[1])
        u1[i] = u1[i-1] + h/2.0 * (k1_vec[0] + k2_vec[0])
        u2[i] = u2[i-1] + h/2.0 * (k1_vec[1] + k2_vec[1])
    return u1, u2

# Runge-Kutta 3rd order method for SYSTEMS
def RK3_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        k1_vec = F(t, u1[i-1], u2[i-1])
        k2_vec = F(t + h/2.0, u1[i-1] + h/2.0*k1_vec[0], u2[i-1] + h/2.0*k1_vec[1])
        k3_vec = F(t + h, u1[i-1] - h*k1_vec[0] + 2.0*h*k2_vec[0], u2[i-1] - h*k1_vec[1] + 2.0*h*k2_vec[1])
        u1[i] = u1[i-1] + h/6.0 * (k1_vec[0] + 4.0*k2_vec[0] + k3_vec[0])
        u2[i] = u2[i-1] + h/6.0 * (k1_vec[1] + 4.0*k2_vec[1] + k3_vec[1])
    return u1, u2

# Runge-Kutta 4th order method for SYSTEMS
def RK4_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        k1_vec = F(t, u1[i-1], u2[i-1])
        k2_vec = F(t + h/2.0, u1[i-1] + h/2.0*k1_vec[0], u2[i-1] + h/2.0*k1_vec[1])
        k3_vec = F(t + h/2.0, u1[i-1] + h/2.0*k2_vec[0], u2[i-1] + h/2.0*k2_vec[1])
        k4_vec = F(t + h, u1[i-1] + h*k3_vec[0], u2[i-1] + h*k3_vec[1])
        u1[i] = u1[i-1] + h/6.0 * (k1_vec[0] + 2.0*k2_vec[0] + 2.0*k3_vec[0] + k4_vec[0])
        u2[i] = u2[i-1] + h/6.0 * (k1_vec[1] + 2.0*k2_vec[1] + 2.0*k3_vec[1] + k4_vec[1])
    return u1, u2

# Runge-Kutta 5th order method for SYSTEMS (Cash-Karp based coefficients)
def RK5_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20

    for i in range(len(t_array) - 1):
        t = t_array[i]
        u1_i = u1[i]
        u2_i = u2[i]

        k1_vec = F(t, u1_i, u2_i)
        k1_u1, k1_u2 = k1_vec[0], k1_vec[1]

        k2_vec = F(t + h / 4.0, u1_i + h / 4.0 * k1_u1, u2_i + h / 4.0 * k1_u2)
        k2_u1, k2_u2 = k2_vec[0], k2_vec[1]

        k3_vec = F(t + h / 4.0, u1_i + h / 8.0 * k1_u1 + h / 8.0 * k2_u1, u2_i + h / 8.0 * k1_u2 + h / 8.0 * k2_u2)
        k3_u1, k3_u2 = k3_vec[0], k3_vec[1]

        k4_vec = F(t + h / 2.0, u1_i - h / 2.0 * k2_u1 + h * k3_u1, u2_i - h / 2.0 * k2_u2 + h * k3_u2)
        k4_u1, k4_u2 = k4_vec[0], k4_vec[1]

        k5_vec = F(t + 3.0 * h / 4.0, u1_i + 3.0 * h / 16.0 * k1_u1 + 9.0 * h / 16.0 * k4_u1, u2_i + 3.0 * h / 16.0 * k1_u2 + 9.0 * h / 16.0 * k4_u2)
        k5_u1, k5_u2 = k5_vec[0], k5_vec[1]

        k6_vec = F(t + h, u1_i - 3.0 * h / 7.0 * k1_u1 + 2.0 * h / 7.0 * k2_u1 + 12.0 * h / 7.0 * k3_u1 - 12.0 * h / 7.0 * k4_u1 + 8.0 * h / 7.0 * k5_u1,
                        u2_i - 3.0 * h / 7.0 * k1_u2 + 2.0 * h / 7.0 * k2_u2 + 12.0 * h / 7.0 * k3_u2 - 12.0 * h / 7.0 * k4_u2 + 8.0 * h / 7.0 * k5_u2)
        k6_u1, k6_u2 = k6_vec[0], k6_vec[1]

        # Cập nhật giá trị u1 và u2
        u1[i + 1] = u1_i + h / 90.0 * (7.0 * k1_u1 + 32.0 * k3_u1 + 12.0 * k4_u1 + 32.0 * k5_u1 + 7.0 * k6_u1)
        u2[i + 1] = u2_i + h / 90.0 * (7.0 * k1_u2 + 32.0 * k3_u2 + 12.0 * k4_u2 + 32.0 * k5_u2 + 7.0 * k6_u2)

    return u1, u2

# Adams-Bashforth 2nd order method for SYSTEMS
def AB2_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    # Khởi tạo bằng RK bậc phù hợp (RK2)
    u1_start, u2_start = RK2_system(F, t_array[:2], u10, u20)
    u1[:2] = u1_start
    u2[:2] = u2_start

    # Vòng lặp AB2
    for i in range(2, len(t_array)):
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])

        u1[i] = u1[i-1] + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2[i] = u2[i-1] + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])
    return u1, u2

# Adams-Bashforth 3rd order method for SYSTEMS
def AB3_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    u1_start, u2_start = RK3_system(F, t_array[:3], u10, u20)
    u1[:3] = u1_start
    u2[:3] = u2_start

    for i in range(3, len(t_array)):
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        t_prev3 = t_array[i-3]
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])

        u1[i] = u1[i-1] + h/12.0 * (23.0*F_prev1[0] - 16.0*F_prev2[0] + 5.0*F_prev3[0])
        u2[i] = u2[i-1] + h/12.0 * (23.0*F_prev1[1] - 16.0*F_prev2[1] + 5.0*F_prev3[1])
    return u1, u2

# Adams-Bashforth 4th order method for SYSTEMS
def AB4_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    u1_start, u2_start = RK4_system(F, t_array[:4], u10, u20)
    u1[:4] = u1_start
    u2[:4] = u2_start

    for i in range(4, len(t_array)):
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        t_prev3 = t_array[i-3]
        t_prev4 = t_array[i-4]
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])
        F_prev4 = F(t_prev4, u1[i-4], u2[i-4])

        u1[i] = u1[i-1] + h/24.0 * (55.0*F_prev1[0] - 59.0*F_prev2[0] + 37.0*F_prev3[0] - 9.0*F_prev4[0])
        u2[i] = u2[i-1] + h/24.0 * (55.0*F_prev1[1] - 59.0*F_prev2[1] + 37.0*F_prev3[1] - 9.0*F_prev4[1])
    return u1, u2

# Adams-Bashforth 5th order method for SYSTEMS
def AB5_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    # Khởi tạo bằng RK5 đã cập nhật
    u1_start, u2_start = RK5_system(F, t_array[:5], u10, u20) # Gọi hàm RK5 mới
    if len(u1_start) < 5: # Xử lý trường hợp RK5 dừng sớm (nếu có)
         print(f"Warning (AB5_system): RK5 initializer returned fewer than 5 points ({len(u1_start)}). Cannot proceed.")
         # Trả về kết quả khởi tạo hoặc mảng rỗng tùy theo cách muốn xử lý lỗi
         return u1_start, u2_start # Hoặc return np.array([]), np.array([])
    u1[:5] = u1_start
    u2[:5] = u2_start

    for i in range(5, len(t_array)):
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        t_prev3 = t_array[i-3]
        t_prev4 = t_array[i-4]
        t_prev5 = t_array[i-5]
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])
        F_prev4 = F(t_prev4, u1[i-4], u2[i-4])
        F_prev5 = F(t_prev5, u1[i-5], u2[i-5])

        u1[i] = u1[i-1] + h/720.0 * (1901.0*F_prev1[0] - 2774.0*F_prev2[0] + 2616.0*F_prev3[0] - 1274.0*F_prev4[0] + 251.0*F_prev5[0])
        u2[i] = u2[i-1] + h/720.0 * (1901.0*F_prev1[1] - 2774.0*F_prev2[1] + 2616.0*F_prev3[1] - 1274.0*F_prev4[1] + 251.0*F_prev5[1])
    return u1, u2

# Adams-Moulton 2nd order method for SYSTEMS
def AM2_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    # Khởi tạo bằng RK bậc 2 (hoặc 3 theo standalone gốc?)
    # Standalone dùng RK3 cho AM2, AM3? Kiểm tra lại code gốc.
    # Theo lý thuyết, AM2 (bậc 2) nên dùng RK2 khởi tạo.
    # Nếu dùng RK3:
    # u1_start, u2_start = RK3_system(F, t_array[:2], u10, u20) # Standalone AM2 dùng RK3? Bất thường
    # Dùng RK2 hợp lý hơn:
    u1_start, u2_start = RK2_system(F, t_array[:2], u10, u20)
    u1[:2] = u1_start
    u2[:2] = u2_start

    for i in range(2, len(t_array)):
        t_curr = t_array[i]
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]

        # Predictor (AB2 step)
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        u1_pred = u1[i-1] + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2_pred = u2[i-1] + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])

        # Corrector (AM2 step)
        F_pred = F(t_curr, u1_pred, u2_pred) # F ở điểm dự đoán t_i
        u1[i] = u1[i-1] + h/12.0*(5.0*F_pred[0] + 8.0*F_prev1[0] - F_prev2[0])
        u2[i] = u2[i-1] + h/12.0*(5.0*F_pred[1] + 8.0*F_prev1[1] - F_prev2[1])
    return u1, u2

# Adams-Moulton 3rd order method for SYSTEMS
def AM3_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    u1_start, u2_start = RK3_system(F, t_array[:3], u10, u20)
    u1[:3] = u1_start
    u2[:3] = u2_start

    for i in range(3, len(t_array)):
        t_curr = t_array[i]
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        t_prev3 = t_array[i-3]

        # Predictor (AB3 step)
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])
        u1_pred = u1[i-1] + h/12.0 * (23.0*F_prev1[0] - 16.0*F_prev2[0] + 5.0*F_prev3[0])
        u2_pred = u2[i-1] + h/12.0 * (23.0*F_prev1[1] - 16.0*F_prev2[1] + 5.0*F_prev3[1])

        # Corrector (AM3 step)
        F_pred = F(t_curr, u1_pred, u2_pred)
        u1[i] = u1[i-1] + h/24.0*(9.0*F_pred[0] + 19.0*F_prev1[0] - 5.0*F_prev2[0] + F_prev3[0])
        u2[i] = u2[i-1] + h/24.0*(9.0*F_pred[1] + 19.0*F_prev1[1] - 5.0*F_prev2[1] + F_prev3[1])
    return u1, u2

# Adams-Moulton 4th order method for SYSTEMS
def AM4_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))

    u1_start, u2_start = RK4_system(F, t_array[:4], u10, u20)
    u1[:4] = u1_start
    u2[:4] = u2_start

    for i in range(4, len(t_array)):
        t_curr = t_array[i]
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        t_prev3 = t_array[i-3]
        t_prev4 = t_array[i-4]

        # Predictor (AB4 step)
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])
        F_prev4 = F(t_prev4, u1[i-4], u2[i-4])
        u1_pred = u1[i-1] + h/24.0 * (55.0*F_prev1[0] - 59.0*F_prev2[0] + 37.0*F_prev3[0] - 9.0*F_prev4[0])
        u2_pred = u2[i-1] + h/24.0 * (55.0*F_prev1[1] - 59.0*F_prev2[1] + 37.0*F_prev3[1] - 9.0*F_prev4[1])

        # Corrector (AM4 step)
        F_pred = F(t_curr, u1_pred, u2_pred)
        u1[i] = u1[i-1] + h/720.0*(251.0*F_pred[0] + 646.0*F_prev1[0] - 264.0*F_prev2[0] + 106.0*F_prev3[0] - 19.0*F_prev4[0])
        u2[i] = u2[i-1] + h/720.0*(251.0*F_pred[1] + 646.0*F_prev1[1] - 264.0*F_prev2[1] + 106.0*F_prev3[1] - 19.0*F_prev4[1])
    return u1, u2

# ==============================================
#   Solver Methods for Model 5 (with break)
# ==============================================

# --- RK Methods with Break ---
def RK2_original_system_M5(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        # ================== HIGHLIGHT START: Kiểm tra giá trị trước khi gọi F ==================
        # Nếu u1 hoặc u2 đã không hợp lệ, không cần tính tiếp
        if not np.isfinite(u1[i-1]) or not np.isfinite(u2[i-1]):
             print(f"RK2_M5 stopping at i={i}: Non-finite input u1={u1[i-1]}, u2={u2[i-1]}")
             return u1[:i], u2[:i]
        # ================== HIGHLIGHT END ==================
        try:
            k1_vec = F(t, u1[i-1], u2[i-1])
            # Thêm kiểm tra giá trị trung gian (ví dụ, k1)
            if not np.all(np.isfinite(k1_vec)):
                 print(f"RK2_M5 stopping at i={i}: Non-finite k1_vec={k1_vec}")
                 return u1[:i], u2[:i]

            u1_k2_in = u1[i-1] + h*k1_vec[0]
            u2_k2_in = u2[i-1] + h*k1_vec[1]
            if not np.isfinite(u1_k2_in) or not np.isfinite(u2_k2_in):
                 print(f"RK2_M5 stopping at i={i}: Non-finite input for k2")
                 return u1[:i], u2[:i]

            k2_vec = F(t + h, u1_k2_in, u2_k2_in)
            if not np.all(np.isfinite(k2_vec)):
                 print(f"RK2_M5 stopping at i={i}: Non-finite k2_vec={k2_vec}")
                 return u1[:i], u2[:i]

        except Exception as e_fcall:
            print(f"RK2_M5 stopping at i={i}: Error calling F -> {e_fcall}")
            return u1[:i], u2[:i] # Trả về kết quả tính được đến giờ

        u1_new = u1[i-1] + h/2.0 * (k1_vec[0] + k2_vec[0])
        u2_new = u2[i-1] + h/2.0 * (k1_vec[1] + k2_vec[1])

        # Kiểm tra giá trị cuối cùng trước khi gán
        if not np.isfinite(u1_new) or not np.isfinite(u2_new):
            print(f"RK2_M5 stopping at i={i}: Non-finite result u1_new={u1_new}, u2_new={u2_new}")
            return u1[:i], u2[:i]

        u1[i] = u1_new
        u2[i] = u2_new

        # ================== HIGHLIGHT: Điều kiện break giống standalone ==================
        if u1[i] <= 0.5:
            # print(f"RK2_M5 terminated early at t={t_array[i]:.4f} (u1={u1[i]:.4f} <= 0.01)")
            return u1[:i+1], u2[:i+1]
        # ================== HIGHLIGHT END ==================
    return u1, u2

def RK3_original_system_M5(F, t_array, u10, u20): # Copy từ RK3_system và thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        if not np.isfinite(u1[i-1]) or not np.isfinite(u2[i-1]): return u1[:i], u2[:i]
        try:
            k1_vec = F(t, u1[i-1], u2[i-1]);                                         
            if not np.all(np.isfinite(k1_vec)): return u1[:i], u2[:i]
            u1_k2_in, u2_k2_in = u1[i-1] + h/2.0*k1_vec[0], u2[i-1] + h/2.0*k1_vec[1]; 
            if not (np.isfinite(u1_k2_in) and np.isfinite(u2_k2_in)): return u1[:i],u2[:i]
            k2_vec = F(t + h/2.0, u1_k2_in, u2_k2_in);                                
            if not np.all(np.isfinite(k2_vec)): return u1[:i], u2[:i]
            u1_k3_in, u2_k3_in = u1[i-1]-h*k1_vec[0]+2.0*h*k2_vec[0], u2[i-1]-h*k1_vec[1]+2.0*h*k2_vec[1]; 
            if not (np.isfinite(u1_k3_in) and np.isfinite(u2_k3_in)): return u1[:i],u2[:i]
            k3_vec = F(t + h, u1_k3_in, u2_k3_in);                                    
            if not np.all(np.isfinite(k3_vec)): return u1[:i], u2[:i]
        except Exception as e_fcall: print(f"RK3_M5 err @ i={i}: {e_fcall}"); return u1[:i], u2[:i]

        u1_new = u1[i-1] + h/6.0 * (k1_vec[0] + 4.0*k2_vec[0] + k3_vec[0])
        u2_new = u2[i-1] + h/6.0 * (k1_vec[1] + 4.0*k2_vec[1] + k3_vec[1])
        if not np.isfinite(u1_new) or not np.isfinite(u2_new): return u1[:i], u2[:i]
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: return u1[:i+1], u2[:i+1]
    return u1, u2

def RK4_original_system_M5(F, t_array, u10, u20): # Copy từ RK4_system và thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        if not np.isfinite(u1[i-1]) or not np.isfinite(u2[i-1]): return u1[:i], u2[:i]
        try:
            k1_vec = F(t, u1[i-1], u2[i-1]);                                         
            if not np.all(np.isfinite(k1_vec)): 
                return u1[:i], u2[:i]
            u1_k2_in, u2_k2_in = u1[i-1] + h/2.0*k1_vec[0], u2[i-1] + h/2.0*k1_vec[1]; 
            if not (np.isfinite(u1_k2_in) and np.isfinite(u2_k2_in)): 
                return u1[:i],u2[:i]
            k2_vec = F(t + h/2.0, u1_k2_in, u2_k2_in);                                
            if not np.all(np.isfinite(k2_vec)): 
                return u1[:i], u2[:i]
            u1_k3_in, u2_k3_in = u1[i-1] + h/2.0*k2_vec[0], u2[i-1] + h/2.0*k2_vec[1]; 
            if not (np.isfinite(u1_k3_in) and np.isfinite(u2_k3_in)): 
                return u1[:i],u2[:i]
            k3_vec = F(t + h/2.0, u1_k3_in, u2_k3_in);                                
            if not np.all(np.isfinite(k3_vec)): 
                return u1[:i], u2[:i]
            u1_k4_in, u2_k4_in = u1[i-1] + h*k3_vec[0], u2[i-1] + h*k3_vec[1];        
            if not (np.isfinite(u1_k4_in) and np.isfinite(u2_k4_in)): 
                return u1[:i],u2[:i]
            k4_vec = F(t + h, u1_k4_in, u2_k4_in);                                    
            if not np.all(np.isfinite(k4_vec)): 
                return u1[:i], u2[:i]
        except Exception as e_fcall: print(f"RK4_M5 err @ i={i}: {e_fcall}"); return u1[:i], u2[:i]

        u1_new = u1[i-1] + h/6.0 * (k1_vec[0] + 2.0*k2_vec[0] + 2.0*k3_vec[0] + k4_vec[0])
        u2_new = u2[i-1] + h/6.0 * (k1_vec[1] + 2.0*k2_vec[1] + 2.0*k3_vec[1] + k4_vec[1])
        if not np.isfinite(u1_new) or not np.isfinite(u2_new): return u1[:i], u2[:i]
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: return u1[:i+1], u2[:i+1]
    return u1, u2

def RK5_original_system_M5(F, t_array, u10, u20): # Copy từ RK5_system và thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(len(t_array) - 1):
        t = t_array[i]
        u1_i, u2_i = u1[i], u2[i]
        if not np.isfinite(u1_i) or not np.isfinite(u2_i): return u1[:i], u2[:i]
        try:
            k1_vec=F(t, u1_i, u2_i); k1_u1,k1_u2=k1_vec[0],k1_vec[1]; 
            if not np.all(np.isfinite(k1_vec)): return u1[:i], u2[:i]
            k2_vec=F(t + h/4, u1_i+h/4*k1_u1, u2_i+h/4*k1_u2); k2_u1,k2_u2=k2_vec[0],k2_vec[1]; 
            if not np.all(np.isfinite(k2_vec)): return u1[:i], u2[:i]
            k3_vec=F(t + h/4, u1_i+h/8*k1_u1+h/8*k2_u1, u2_i+h/8*k1_u2+h/8*k2_u2); k3_u1,k3_u2=k3_vec[0],k3_vec[1]; 
            if not np.all(np.isfinite(k3_vec)): return u1[:i], u2[:i]
            k4_vec=F(t + h/2, u1_i-h/2*k2_u1+h*k3_u1, u2_i-h/2*k2_u2+h*k3_u2); k4_u1,k4_u2=k4_vec[0],k4_vec[1]; 
            if not np.all(np.isfinite(k4_vec)): return u1[:i], u2[:i]
            k5_vec=F(t + 3*h/4, u1_i+3*h/16*k1_u1+9*h/16*k4_u1, u2_i+3*h/16*k1_u2+9*h/16*k4_u2); k5_u1,k5_u2=k5_vec[0],k5_vec[1]; 
            if not np.all(np.isfinite(k5_vec)): return u1[:i], u2[:i]
            k6_vec=F(t+h, u1_i-3*h/7*k1_u1+2*h/7*k2_u1+12*h/7*k3_u1-12*h/7*k4_u1+8*h/7*k5_u1, u2_i-3*h/7*k1_u2+2*h/7*k2_u2+12*h/7*k3_u2-12*h/7*k4_u2+8*h/7*k5_u2); k6_u1,k6_u2=k6_vec[0],k6_vec[1]; 
            if not np.all(np.isfinite(k6_vec)): return u1[:i], u2[:i]
        except Exception as e_fcall: print(f"RK5_M5 err @ i={i}: {e_fcall}"); return u1[:i], u2[:i]

        u1_new = u1_i + h/90.0*(7*k1_u1+32*k3_u1+12*k4_u1+32*k5_u1+7*k6_u1)
        u2_new = u2_i + h/90.0*(7*k1_u2+32*k3_u2+12*k4_u2+32*k5_u2+7*k6_u2)
        if not np.isfinite(u1_new) or not np.isfinite(u2_new): return u1[:i], u2[:i]
        u1[i+1], u2[i+1] = u1_new, u2_new
        if u1[i+1] <= 0.5: return u1[:i+2], u2[:i+2] # Chú ý index ở đây là i+1
    return u1, u2

# --- AB Methods with Break ---
def AB2_original_system_M5(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0], u2[0] = u10, u20
    try:
        u1_start, u2_start = RK2_system_M5(F, t_array[:2], u10, u20) # Gọi bản M5
        start_len = len(u1_start)
        if start_len < 2: return u1[:start_len], u2[:start_len]
        u1[:start_len] = u1_start
        u2[:start_len] = u2_start
    except Exception as e_init: print(f"AB2_M5 init err: {e_init}"); return u1[:1], u2[:1]

    actual_len = len(t_array)
    for i in range(2, len(t_array)): # Bắt đầu từ index 2
        t_prev1, u1_prev1, u2_prev1 = t_array[i-1], u1[i-1], u2[i-1]
        t_prev2, u1_prev2, u2_prev2 = t_array[i-2], u1[i-2], u2[i-2]
        if not (np.isfinite(u1_prev1) and np.isfinite(u2_prev1) and np.isfinite(u1_prev2) and np.isfinite(u2_prev2)): actual_len=i; break
        try:
            F_prev1 = F(t_prev1, u1_prev1, u2_prev1); 
            if not np.all(np.isfinite(F_prev1)): actual_len=i; break
            F_prev2 = F(t_prev2, u1_prev2, u2_prev2); 
            if not np.all(np.isfinite(F_prev2)): actual_len=i; break
        except Exception as e_fcall: print(f"AB2_M5 F err @ i={i}: {e_fcall}"); actual_len=i; break

        u1_new = u1_prev1 + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2_new = u2_prev1 + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AB3_original_system_M5(F, t_array, u10, u20): # Copy từ AB3_system, sửa gọi RK3_M5, thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK3_system_M5(F, t_array[:3], u10, u20); start_len=len(u1_start)
        if start_len < 3: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AB3_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(3, len(t_array)):
        t0, x0, y0 = t_array[i-1], u1[i-1], u2[i-1]
        t1, x1, y1 = t_array[i-2], u1[i-2], u2[i-2]
        t2, x2, y2 = t_array[i-3], u1[i-3], u2[i-3]
        if not all(np.isfinite(v) for v in [x0, y0, x1, y1, x2, y2]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2)
            if not (np.all(np.isfinite(F0)) and np.all(np.isfinite(F1)) and np.all(np.isfinite(F2))): actual_len=i; break
        except Exception as e: print(f"AB3_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/12.0 * (23.0*F0[0] - 16.0*F1[0] + 5.0*F2[0])
        u2_new = y0 + h/12.0 * (23.0*F0[1] - 16.0*F1[1] + 5.0*F2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AB4_original_system_M5(F, t_array, u10, u20): # Copy từ AB4_system, sửa gọi RK4_M5, thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK4_system_M5(F, t_array[:4], u10, u20); start_len=len(u1_start)
        if start_len < 4: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AB4_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(4, len(t_array)):
        t0,x0,y0=t_array[i-1],u1[i-1],u2[i-1]; t1,x1,y1=t_array[i-2],u1[i-2],u2[i-2]
        t2,x2,y2=t_array[i-3],u1[i-3],u2[i-3]; t3,x3,y3=t_array[i-4],u1[i-4],u2[i-4]
        if not all(np.isfinite(v) for v in [x0,y0,x1,y1,x2,y2,x3,y3]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2); F3=F(t3,x3,y3)
            if not all(np.all(np.isfinite(f)) for f in [F0, F1, F2, F3]): actual_len=i; break
        except Exception as e: print(f"AB4_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/24.0 * (55.0*F0[0] - 59.0*F1[0] + 37.0*F2[0] - 9.0*F3[0])
        u2_new = y0 + h/24.0 * (55.0*F0[1] - 59.0*F1[1] + 37.0*F2[1] - 9.0*F3[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AB5_original_system_M5(F, t_array, u10, u20): # Copy từ AB5_system, sửa gọi RK5_M5, thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK5_system_M5(F, t_array[:5], u10, u20); start_len=len(u1_start)
        if start_len < 5: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AB5_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(5, len(t_array)):
        t0,x0,y0=t_array[i-1],u1[i-1],u2[i-1]; t1,x1,y1=t_array[i-2],u1[i-2],u2[i-2]
        t2,x2,y2=t_array[i-3],u1[i-3],u2[i-3]; t3,x3,y3=t_array[i-4],u1[i-4],u2[i-4]
        t4,x4,y4=t_array[i-5],u1[i-5],u2[i-5]
        if not all(np.isfinite(v) for v in [x0,y0,x1,y1,x2,y2,x3,y3,x4,y4]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2); F3=F(t3,x3,y3); F4=F(t4,x4,y4)
            if not all(np.all(np.isfinite(f)) for f in [F0, F1, F2, F3, F4]): actual_len=i; break
        except Exception as e: print(f"AB5_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/720.0*(1901*F0[0]-2774*F1[0]+2616*F2[0]-1274*F3[0]+251*F4[0])
        u2_new = y0 + h/720.0*(1901*F0[1]-2774*F1[1]+2616*F2[1]-1274*F3[1]+251*F4[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

# --- AM Methods with Break ---
def AM2_original_system_M5(F, t_array, u10, u20): # Copy từ AM2_system, sửa gọi RK2_M5, thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK2_system_M5(F, t_array[:2], u10, u20); start_len=len(u1_start)
        if start_len < 2: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AM2_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(2, len(t_array)): # Start from index 2 for AM2
        t_curr = t_array[i] # Note: AM corrector uses t_curr for F_pred
        t_prev1, u1_prev1, u2_prev1 = t_array[i-1], u1[i-1], u2[i-1]
        t_prev2, u1_prev2, u2_prev2 = t_array[i-2], u1[i-2], u2[i-2]
        if not all(np.isfinite(v) for v in [u1_prev1, u2_prev1, u1_prev2, u2_prev2]): actual_len=i; break
        try:
            F_prev1 = F(t_prev1, u1_prev1, u2_prev1); 
            if not np.all(np.isfinite(F_prev1)): actual_len=i; break
            F_prev2 = F(t_prev2, u1_prev2, u2_prev2); 
            if not np.all(np.isfinite(F_prev2)): actual_len=i; break
        except Exception as e: print(f"AM2_M5 F err @ i={i}: {e}"); actual_len=i; break
        # Predictor (AB2) - Calculate predicted values at t_curr
        u1_pred = u1_prev1 + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2_pred = u2_prev1 + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])
        if not (np.isfinite(u1_pred) and np.isfinite(u2_pred)): actual_len=i; break
        # Corrector (AM2) - Needs F at predicted point
        try:
            F_pred = F(t_curr, u1_pred, u2_pred); 
            if not np.all(np.isfinite(F_pred)): actual_len=i; break
        except Exception as e: print(f"AM2_M5 F_pred err @ i={i}: {e}"); actual_len=i; break
        u1_new = u1_prev1 + h/12.0*(5.0*F_pred[0] + 8.0*F_prev1[0] - F_prev2[0])
        u2_new = u2_prev1 + h/12.0*(5.0*F_pred[1] + 8.0*F_prev1[1] - F_prev2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AM3_original_system_M5(F, t_array, u10, u20): # Copy từ AM3_system, sửa gọi RK3_M5, thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK3_system_M5(F, t_array[:3], u10, u20); start_len=len(u1_start)
        if start_len < 3: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AM3_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(3, len(t_array)):
        t_curr = t_array[i]
        t0, x0, y0 = t_array[i-1], u1[i-1], u2[i-1]
        t1, x1, y1 = t_array[i-2], u1[i-2], u2[i-2]
        t2, x2, y2 = t_array[i-3], u1[i-3], u2[i-3]
        if not all(np.isfinite(v) for v in [x0, y0, x1, y1, x2, y2]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2)
            if not (np.all(np.isfinite(F0)) and np.all(np.isfinite(F1)) and np.all(np.isfinite(F2))): actual_len=i; break
        except Exception as e: print(f"AM3_M5 F err @ i={i}: {e}"); actual_len=i; break
        # Predictor (AB3)
        u1_pred = x0 + h/12.0 * (23.0*F0[0] - 16.0*F1[0] + 5.0*F2[0])
        u2_pred = y0 + h/12.0 * (23.0*F0[1] - 16.0*F1[1] + 5.0*F2[1])
        if not (np.isfinite(u1_pred) and np.isfinite(u2_pred)): actual_len=i; break
        # Corrector (AM3)
        try:
            F_pred = F(t_curr, u1_pred, u2_pred); 
            if not np.all(np.isfinite(F_pred)): actual_len=i; break
        except Exception as e: print(f"AM3_M5 F_pred err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/24.0*(9.0*F_pred[0] + 19.0*F0[0] - 5.0*F1[0] + F2[0])
        u2_new = y0 + h/24.0*(9.0*F_pred[1] + 19.0*F0[1] - 5.0*F1[1] + F2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AM4_original_system_M5(F, t_array, u10, u20): # Copy từ AM4_system, sửa gọi RK4_M5, thêm break
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK4_system_M5(F, t_array[:4], u10, u20); start_len=len(u1_start)
        if start_len < 4: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AM4_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(4, len(t_array)):
        t_curr=t_array[i]
        t0,x0,y0=t_array[i-1],u1[i-1],u2[i-1]; t1,x1,y1=t_array[i-2],u1[i-2],u2[i-2]
        t2,x2,y2=t_array[i-3],u1[i-3],u2[i-3]; t3,x3,y3=t_array[i-4],u1[i-4],u2[i-4]
        if not all(np.isfinite(v) for v in [x0,y0,x1,y1,x2,y2,x3,y3]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2); F3=F(t3,x3,y3)
            if not all(np.all(np.isfinite(f)) for f in [F0, F1, F2, F3]): actual_len=i; break
        except Exception as e: print(f"AM4_M5 F err @ i={i}: {e}"); actual_len=i; break
        # Predictor (AB4)
        u1_pred = x0 + h/24.0 * (55.0*F0[0] - 59.0*F1[0] + 37.0*F2[0] - 9.0*F3[0])
        u2_pred = y0 + h/24.0 * (55.0*F0[1] - 59.0*F1[1] + 37.0*F2[1] - 9.0*F3[1])
        if not (np.isfinite(u1_pred) and np.isfinite(u2_pred)): actual_len=i; break
        # Corrector (AM4)
        try:
            F_pred = F(t_curr, u1_pred, u2_pred); 
            if not np.all(np.isfinite(F_pred)): actual_len=i; break
        except Exception as e: print(f"AM4_M5 F_pred err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/720.0*(251.0*F_pred[0] + 646.0*F0[0] - 264.0*F1[0] + 106.0*F2[0] - 19.0*F3[0])
        u2_new = y0 + h/720.0*(251.0*F_pred[1] + 646.0*F0[1] - 264.0*F1[1] + 106.0*F2[1] - 19.0*F3[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

# ==============================================
#   NEW Solver Methods for Model 5 - SIMULATION 1
#   (Break condition similar to standalone rk4)
# ==============================================

# --- RK Methods with Break (Simplified Break for RK initializers) ---
def RK2_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None): # Signature nhận params
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        if not np.isfinite(u1[i-1]) or not np.isfinite(u2[i-1]):
             print(f"RK2_M5 stopping at i={i}: Non-finite input u1={u1[i-1]}, u2={u2[i-1]}")
             return u1[:i], u2[:i]
        try:
            k1_vec = F(t, u1[i-1], u2[i-1])
            if not np.all(np.isfinite(k1_vec)):
                 print(f"RK2_M5 stopping at i={i}: Non-finite k1_vec={k1_vec}")
                 return u1[:i], u2[:i]

            u1_k2_in = u1[i-1] + h*k1_vec[0]
            u2_k2_in = u2[i-1] + h*k1_vec[1]
            if not np.isfinite(u1_k2_in) or not np.isfinite(u2_k2_in):
                 print(f"RK2_M5 stopping at i={i}: Non-finite input for k2")
                 return u1[:i], u2[:i]

            k2_vec = F(t + h, u1_k2_in, u2_k2_in)
            if not np.all(np.isfinite(k2_vec)):
                 print(f"RK2_M5 stopping at i={i}: Non-finite k2_vec={k2_vec}")
                 return u1[:i], u2[:i]
        except Exception as e_fcall:
            print(f"RK2_M5 stopping at i={i}: Error calling F -> {e_fcall}")
            return u1[:i], u2[:i]

        u1_new = u1[i-1] + h/2.0 * (k1_vec[0] + k2_vec[0])
        u2_new = u2[i-1] + h/2.0 * (k1_vec[1] + k2_vec[1])

        if not np.isfinite(u1_new) or not np.isfinite(u2_new):
            print(f"RK2_M5 stopping at i={i}: Non-finite result u1_new={u1_new}, u2_new={u2_new}")
            return u1[:i], u2[:i]

        u1[i] = u1_new
        u2[i] = u2_new

        # ================== HIGHLIGHT: Giữ điều kiện break đơn giản cho RK initializer ==================
        if u1[i] <= 0.01: # Điều kiện break cũ của app cho RK
            # print(f"RK2_M5 (initializer break) terminated early at t={t_array[i]:.4f} (u1={u1[i]:.4f} <= 0.01)")
            return u1[:i+1], u2[:i+1]
        # ================== HIGHLIGHT END ==================
    return u1, u2

def RK3_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None): # Signature nhận params
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        if not np.isfinite(u1[i-1]) or not np.isfinite(u2[i-1]): return u1[:i], u2[:i]
        try:
            k1_vec = F(t, u1[i-1], u2[i-1]);
            if not np.all(np.isfinite(k1_vec)): return u1[:i], u2[:i]
            u1_k2_in, u2_k2_in = u1[i-1] + h/2.0*k1_vec[0], u2[i-1] + h/2.0*k1_vec[1];
            if not (np.isfinite(u1_k2_in) and np.isfinite(u2_k2_in)): return u1[:i],u2[:i]
            k2_vec = F(t + h/2.0, u1_k2_in, u2_k2_in);
            if not np.all(np.isfinite(k2_vec)): return u1[:i], u2[:i]
            u1_k3_in, u2_k3_in = u1[i-1]-h*k1_vec[0]+2.0*h*k2_vec[0], u2[i-1]-h*k1_vec[1]+2.0*h*k2_vec[1];
            if not (np.isfinite(u1_k3_in) and np.isfinite(u2_k3_in)): return u1[:i],u2[:i]
            k3_vec = F(t + h, u1_k3_in, u2_k3_in);
            if not np.all(np.isfinite(k3_vec)): return u1[:i], u2[:i]
        except Exception as e_fcall: print(f"RK3_M5 err @ i={i}: {e_fcall}"); return u1[:i], u2[:i]

        u1_new = u1[i-1] + h/6.0 * (k1_vec[0] + 4.0*k2_vec[0] + k3_vec[0])
        u2_new = u2[i-1] + h/6.0 * (k1_vec[1] + 4.0*k2_vec[1] + k3_vec[1])
        if not np.isfinite(u1_new) or not np.isfinite(u2_new): return u1[:i], u2[:i]
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT: Giữ điều kiện break đơn giản ==================
        if u1[i] <= 0.01: return u1[:i+1], u2[:i+1]
        # ================== HIGHLIGHT END ==================
    return u1, u2

def RK4_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None): # Signature nhận params
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        if not np.isfinite(u1[i-1]) or not np.isfinite(u2[i-1]): return u1[:i], u2[:i]
        try:
            k1_vec = F(t, u1[i-1], u2[i-1]);
            if not np.all(np.isfinite(k1_vec)): return u1[:i], u2[:i]
            u1_k2_in, u2_k2_in = u1[i-1] + h/2.0*k1_vec[0], u2[i-1] + h/2.0*k1_vec[1];
            if not (np.isfinite(u1_k2_in) and np.isfinite(u2_k2_in)): return u1[:i],u2[:i]
            k2_vec = F(t + h/2.0, u1_k2_in, u2_k2_in);
            if not np.all(np.isfinite(k2_vec)): return u1[:i], u2[:i]
            u1_k3_in, u2_k3_in = u1[i-1] + h/2.0*k2_vec[0], u2[i-1] + h/2.0*k2_vec[1];
            if not (np.isfinite(u1_k3_in) and np.isfinite(u2_k3_in)): return u1[:i],u2[:i]
            k3_vec = F(t + h/2.0, u1_k3_in, u2_k3_in);
            if not np.all(np.isfinite(k3_vec)): return u1[:i], u2[:i]
            u1_k4_in, u2_k4_in = u1[i-1] + h*k3_vec[0], u2[i-1] + h*k3_vec[1];
            if not (np.isfinite(u1_k4_in) and np.isfinite(u2_k4_in)): return u1[:i],u2[:i]
            k4_vec = F(t + h, u1_k4_in, u2_k4_in);
            if not np.all(np.isfinite(k4_vec)): return u1[:i], u2[:i]
        except Exception as e_fcall: print(f"RK4_M5 err @ i={i}: {e_fcall}"); return u1[:i], u2[:i]

        u1_new = u1[i-1] + h/6.0 * (k1_vec[0] + 2.0*k2_vec[0] + 2.0*k3_vec[0] + k4_vec[0])
        u2_new = u2[i-1] + h/6.0 * (k1_vec[1] + 2.0*k2_vec[1] + 2.0*k3_vec[1] + k4_vec[1])
        if not np.isfinite(u1_new) or not np.isfinite(u2_new): return u1[:i], u2[:i]
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT: Giữ điều kiện break đơn giản ==================
        if u1[i] <= 0.01: return u1[:i+1], u2[:i+1]
        # ================== HIGHLIGHT END ==================
    return u1, u2

def RK5_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20

    for i in range(len(t_array) - 1): # Vòng lặp đến len - 1 để tính cho i+1
        t = t_array[i]
        u1_i, u2_i = u1[i], u2[i]

        # Kiểm tra giá trị đầu vào cho bước hiện tại
        if not np.isfinite(u1_i) or not np.isfinite(u2_i):
            print(f"RK5_M5 stopping at step i={i} due to non-finite input u1_i, u2_i.")
            return u1[:i], u2[:i] # Trả về các giá trị đã tính được đến giờ

        try:
            # Tính các hệ số k
            k1_vec = F(t, u1_i, u2_i)
            if not np.all(np.isfinite(k1_vec)): return u1[:i], u2[:i]
            k1_u1, k1_u2 = k1_vec[0], k1_vec[1]

            k2_input_u1 = u1_i + h / 4.0 * k1_u1
            k2_input_u2 = u2_i + h / 4.0 * k1_u2
            if not (np.isfinite(k2_input_u1) and np.isfinite(k2_input_u2)): return u1[:i], u2[:i]
            k2_vec = F(t + h / 4.0, k2_input_u1, k2_input_u2)
            if not np.all(np.isfinite(k2_vec)): return u1[:i], u2[:i]
            k2_u1, k2_u2 = k2_vec[0], k2_vec[1]

            k3_input_u1 = u1_i + h / 8.0 * k1_u1 + h / 8.0 * k2_u1
            k3_input_u2 = u2_i + h / 8.0 * k1_u2 + h / 8.0 * k2_u2
            if not (np.isfinite(k3_input_u1) and np.isfinite(k3_input_u2)): return u1[:i], u2[:i]
            k3_vec = F(t + h / 4.0, k3_input_u1, k3_input_u2)
            if not np.all(np.isfinite(k3_vec)): return u1[:i], u2[:i]
            k3_u1, k3_u2 = k3_vec[0], k3_vec[1]

            k4_input_u1 = u1_i - h / 2.0 * k2_u1 + h * k3_u1
            k4_input_u2 = u2_i - h / 2.0 * k2_u2 + h * k3_u2
            if not (np.isfinite(k4_input_u1) and np.isfinite(k4_input_u2)): return u1[:i], u2[:i]
            k4_vec = F(t + h / 2.0, k4_input_u1, k4_input_u2)
            if not np.all(np.isfinite(k4_vec)): return u1[:i], u2[:i]
            k4_u1, k4_u2 = k4_vec[0], k4_vec[1]

            k5_input_u1 = u1_i + 3.0 * h / 16.0 * k1_u1 + 9.0 * h / 16.0 * k4_u1
            k5_input_u2 = u2_i + 3.0 * h / 16.0 * k1_u2 + 9.0 * h / 16.0 * k4_u2
            if not (np.isfinite(k5_input_u1) and np.isfinite(k5_input_u2)): return u1[:i], u2[:i]
            k5_vec = F(t + 3.0 * h / 4.0, k5_input_u1, k5_input_u2)
            if not np.all(np.isfinite(k5_vec)): return u1[:i], u2[:i]
            k5_u1, k5_u2 = k5_vec[0], k5_vec[1]

            k6_input_u1 = u1_i - 3.0*h/7.0*k1_u1 + 2.0*h/7.0*k2_u1 + 12.0*h/7.0*k3_u1 - 12.0*h/7.0*k4_u1 + 8.0*h/7.0*k5_u1
            k6_input_u2 = u2_i - 3.0*h/7.0*k1_u2 + 2.0*h/7.0*k2_u2 + 12.0*h/7.0*k3_u2 - 12.0*h/7.0*k4_u2 + 8.0*h/7.0*k5_u2
            if not (np.isfinite(k6_input_u1) and np.isfinite(k6_input_u2)): return u1[:i], u2[:i]
            k6_vec = F(t + h, k6_input_u1, k6_input_u2)
            if not np.all(np.isfinite(k6_vec)): return u1[:i], u2[:i]
            k6_u1, k6_u2 = k6_vec[0], k6_vec[1]

        except Exception as e_fcall:
            print(f"RK5_M5 stopping at step i={i}: Error calling F -> {e_fcall}")
            return u1[:i], u2[:i]

        # Cập nhật giá trị u1 và u2 cho điểm tiếp theo (i+1)
        u1_new_rk5 = u1_i + h / 90.0 * (7.0 * k1_u1 + 32.0 * k3_u1 + 12.0 * k4_u1 + 32.0 * k5_u1 + 7.0 * k6_u1)
        u2_new_rk5 = u2_i + h / 90.0 * (7.0 * k1_u2 + 32.0 * k3_u2 + 12.0 * k4_u2 + 32.0 * k5_u2 + 7.0 * k6_u2)

        if not np.isfinite(u1_new_rk5) or not np.isfinite(u2_new_rk5):
            print(f"RK5_M5 stopping at step i={i}: Non-finite result u1_new, u2_new.")
            return u1[:i], u2[:i] # Trả về các giá trị đã tính được đến giờ

        u1[i+1] = u1_new_rk5
        u2[i+1] = u2_new_rk5

        # --- ĐIỀU KIỆN BREAK PHỨC TẠP TỪ STANDALONE (áp dụng cho điểm u1[i+1], u2[i+1]) ---
        new_z_vec_for_break_rk5 = np.array([u1[i+1], u2[i+1]])
        break_occurred_rk5 = False

        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_rk5[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_rk5) < 0.5:
                    # Điểm gây break VẪN được bao gồm trong kết quả trả về
                    # u1[i+1] và u2[i+1] đã được gán.
                    break_occurred_rk5 = True
            else:
                if np.linalg.norm(new_z_vec_for_break_rk5) < 0.001:
                    # Standalone: điểm gây break KHÔNG được thêm.
                    # Trả về mảng cắt bỏ đi điểm i+1.
                    # print(f"RK5_M5 standalone-like break (norm < 0.001) at t={t_array[i+1]:.4f}")
                    return u1[:i+1], u2[:i+1] # Trả về đến u1[i], u2[i] (tức là i+1 phần tử)

            if break_occurred_rk5:
                # print(f"RK5_M5 standalone-like break (special v_n/v_t or x<d or norm<0.5) at t={t_array[i+1]:.4f}")
                return u1[:i+2], u2[:i+2] # Trả về bao gồm cả điểm u1[i+1], u2[i+1] (tức là i+2 phần tử)
        else:
            # Fallback: Nếu v_t_param, v_n_param, d_param không được cung cấp, dùng break đơn giản cũ
            if u1[i+1] <= 0.01: # Điều kiện break cũ của app
                # print(f"RK5_M5 (initializer/fallback break) terminated at t={t_array[i+1]:.4f} (u1={u1[i+1]:.4f} <= 0.01)")
                return u1[:i+2], u2[:i+2] # Bao gồm điểm hiện tại
        # --- KẾT THÚC ĐIỀU KIỆN BREAK ---
    return u1, u2

def AB2_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0], u2[0] = u10, u20
    try:
        # Gọi RK2_system_M5 (với break đơn giản của nó) để khởi tạo
        u1_start, u2_start = RK2_system_M5(F, t_array[:2], u10, u20, v_t_param, v_n_param, d_param)
        start_len = len(u1_start)
        if start_len < 2: return u1[:start_len], u2[:start_len]
        u1[:start_len] = u1_start
        u2[:start_len] = u2_start
    except Exception as e_init: print(f"AB2_M5 init err: {e_init}"); return u1[:1], u2[:1]

    actual_len = len(t_array)
    for i in range(2, len(t_array)):
        t_prev1, u1_prev1, u2_prev1 = t_array[i-1], u1[i-1], u2[i-1]
        t_prev2, u1_prev2, u2_prev2 = t_array[i-2], u1[i-2], u2[i-2]
        if not (np.isfinite(u1_prev1) and np.isfinite(u2_prev1) and np.isfinite(u1_prev2) and np.isfinite(u2_prev2)):
            actual_len=i; break
        try:
            F_prev1 = F(t_prev1, u1_prev1, u2_prev1);
            if not np.all(np.isfinite(F_prev1)): actual_len=i; break
            F_prev2 = F(t_prev2, u1_prev2, u2_prev2);
            if not np.all(np.isfinite(F_prev2)): actual_len=i; break
        except Exception as e_fcall: print(f"AB2_M5 F err @ i={i}: {e_fcall}"); actual_len=i; break

        u1_new = u1_prev1 + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2_new = u2_prev1 + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new

        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AB2 ==================
        new_z_vec_for_break_ab = np.array([u1[i], u2[i]])
        break_occurred_ab = False

        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_ab[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_ab) < 0.5:
                    actual_len = i + 1 # Bao gồm điểm break
                    break_occurred_ab = True
            else:
                if np.linalg.norm(new_z_vec_for_break_ab) < 0.001:
                    actual_len = i # KHÔNG bao gồm điểm break
                    break_occurred_ab = True
            if break_occurred_ab: break
        else: # Fallback (nếu không có params, dùng break đơn giản)
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

def AB3_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK3_system_M5(F, t_array[:3], u10, u20, v_t_param, v_n_param, d_param)
        start_len=len(u1_start)
        if start_len < 3: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AB3_M5 init err: {e}"); return u1[:1],u2[:1]

    actual_len=len(t_array)
    for i in range(3, len(t_array)):
        t0, x0, y0 = t_array[i-1], u1[i-1], u2[i-1]
        t1, x1, y1 = t_array[i-2], u1[i-2], u2[i-2]
        t2, x2, y2 = t_array[i-3], u1[i-3], u2[i-3]
        if not all(np.isfinite(v) for v in [x0, y0, x1, y1, x2, y2]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2)
            if not (np.all(np.isfinite(F0)) and np.all(np.isfinite(F1)) and np.all(np.isfinite(F2))): actual_len=i; break
        except Exception as e: print(f"AB3_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/12.0 * (23.0*F0[0] - 16.0*F1[0] + 5.0*F2[0])
        u2_new = y0 + h/12.0 * (23.0*F0[1] - 16.0*F1[1] + 5.0*F2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new

        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AB3 ==================
        new_z_vec_for_break_ab = np.array([u1[i], u2[i]])
        break_occurred_ab = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_ab[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_ab) < 0.5:
                    actual_len = i + 1; break_occurred_ab = True
            else:
                if np.linalg.norm(new_z_vec_for_break_ab) < 0.001:
                    actual_len = i; break_occurred_ab = True
            if break_occurred_ab: break
        else:
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

def AB4_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK4_system_M5(F, t_array[:4], u10, u20, v_t_param, v_n_param, d_param)
        start_len=len(u1_start)
        if start_len < 4: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AB4_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(4, len(t_array)):
        t0,x0,y0=t_array[i-1],u1[i-1],u2[i-1]; t1,x1,y1=t_array[i-2],u1[i-2],u2[i-2]
        t2,x2,y2=t_array[i-3],u1[i-3],u2[i-3]; t3,x3,y3=t_array[i-4],u1[i-4],u2[i-4]
        if not all(np.isfinite(v) for v in [x0,y0,x1,y1,x2,y2,x3,y3]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2); F3=F(t3,x3,y3)
            if not all(np.all(np.isfinite(f)) for f in [F0, F1, F2, F3]): actual_len=i; break
        except Exception as e: print(f"AB4_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/24.0 * (55.0*F0[0] - 59.0*F1[0] + 37.0*F2[0] - 9.0*F3[0])
        u2_new = y0 + h/24.0 * (55.0*F0[1] - 59.0*F1[1] + 37.0*F2[1] - 9.0*F3[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AB4 ==================
        new_z_vec_for_break_ab = np.array([u1[i], u2[i]])
        break_occurred_ab = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_ab[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_ab) < 0.5:
                    actual_len = i + 1; break_occurred_ab = True
            else:
                if np.linalg.norm(new_z_vec_for_break_ab) < 0.001:
                    actual_len = i; break_occurred_ab = True
            if break_occurred_ab: break
        else:
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

def AB5_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK5_system_M5(F, t_array[:5], u10, u20, v_t_param, v_n_param, d_param)
        start_len=len(u1_start)
        if start_len < 5: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AB5_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(5, len(t_array)):
        t0,x0,y0=t_array[i-1],u1[i-1],u2[i-1]; t1,x1,y1=t_array[i-2],u1[i-2],u2[i-2]
        t2,x2,y2=t_array[i-3],u1[i-3],u2[i-3]; t3,x3,y3=t_array[i-4],u1[i-4],u2[i-4]
        t4,x4,y4=t_array[i-5],u1[i-5],u2[i-5]
        if not all(np.isfinite(v) for v in [x0,y0,x1,y1,x2,y2,x3,y3,x4,y4]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2); F3=F(t3,x3,y3); F4=F(t4,x4,y4)
            if not all(np.all(np.isfinite(f)) for f in [F0, F1, F2, F3, F4]): actual_len=i; break
        except Exception as e: print(f"AB5_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/720.0*(1901*F0[0]-2774*F1[0]+2616*F2[0]-1274*F3[0]+251*F4[0])
        u2_new = y0 + h/720.0*(1901*F0[1]-2774*F1[1]+2616*F2[1]-1274*F3[1]+251*F4[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AB5 ==================
        new_z_vec_for_break_ab = np.array([u1[i], u2[i]])
        break_occurred_ab = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_ab[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_ab) < 0.5:
                    actual_len = i + 1; break_occurred_ab = True
            else:
                if np.linalg.norm(new_z_vec_for_break_ab) < 0.001:
                    actual_len = i; break_occurred_ab = True
            if break_occurred_ab: break
        else:
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

def AM2_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK2_system_M5(F, t_array[:2], u10, u20, v_t_param, v_n_param, d_param)
        start_len=len(u1_start)
        if start_len < 2: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AM2_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(2, len(t_array)):
        t_curr = t_array[i]
        t_prev1, u1_prev1, u2_prev1 = t_array[i-1], u1[i-1], u2[i-1]
        t_prev2, u1_prev2, u2_prev2 = t_array[i-2], u1[i-2], u2[i-2]
        if not all(np.isfinite(v) for v in [u1_prev1, u2_prev1, u1_prev2, u2_prev2]): actual_len=i; break
        try:
            F_prev1 = F(t_prev1, u1_prev1, u2_prev1);
            if not np.all(np.isfinite(F_prev1)): actual_len=i; break
            F_prev2 = F(t_prev2, u1_prev2, u2_prev2);
            if not np.all(np.isfinite(F_prev2)): actual_len=i; break
        except Exception as e: print(f"AM2_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_pred = u1_prev1 + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2_pred = u2_prev1 + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])
        if not (np.isfinite(u1_pred) and np.isfinite(u2_pred)): actual_len=i; break
        try:
            F_pred = F(t_curr, u1_pred, u2_pred);
            if not np.all(np.isfinite(F_pred)): actual_len=i; break
        except Exception as e: print(f"AM2_M5 F_pred err @ i={i}: {e}"); actual_len=i; break
        u1_new = u1_prev1 + h/12.0*(5.0*F_pred[0] + 8.0*F_prev1[0] - F_prev2[0])
        u2_new = u2_prev1 + h/12.0*(5.0*F_pred[1] + 8.0*F_prev1[1] - F_prev2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AM2 ==================
        new_z_vec_for_break_am = np.array([u1[i], u2[i]])
        break_occurred_am = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_am[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_am) < 0.5:
                    actual_len = i + 1; break_occurred_am = True
            else:
                if np.linalg.norm(new_z_vec_for_break_am) < 0.001:
                    actual_len = i; break_occurred_am = True
            if break_occurred_am: break
        else:
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

def AM3_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK3_system_M5(F, t_array[:3], u10, u20, v_t_param, v_n_param, d_param)
        start_len=len(u1_start)
        if start_len < 3: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AM3_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(3, len(t_array)):
        t_curr = t_array[i]
        t0, x0, y0 = t_array[i-1], u1[i-1], u2[i-1]
        t1, x1, y1 = t_array[i-2], u1[i-2], u2[i-2]
        t2, x2, y2 = t_array[i-3], u1[i-3], u2[i-3]
        if not all(np.isfinite(v) for v in [x0, y0, x1, y1, x2, y2]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2)
            if not (np.all(np.isfinite(F0)) and np.all(np.isfinite(F1)) and np.all(np.isfinite(F2))): actual_len=i; break
        except Exception as e: print(f"AM3_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_pred = x0 + h/12.0 * (23.0*F0[0] - 16.0*F1[0] + 5.0*F2[0])
        u2_pred = y0 + h/12.0 * (23.0*F0[1] - 16.0*F1[1] + 5.0*F2[1])
        if not (np.isfinite(u1_pred) and np.isfinite(u2_pred)): actual_len=i; break
        try:
            F_pred = F(t_curr, u1_pred, u2_pred);
            if not np.all(np.isfinite(F_pred)): actual_len=i; break
        except Exception as e: print(f"AM3_M5 F_pred err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/24.0*(9.0*F_pred[0] + 19.0*F0[0] - 5.0*F1[0] + F2[0])
        u2_new = y0 + h/24.0*(9.0*F_pred[1] + 19.0*F0[1] - 5.0*F1[1] + F2[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AM3 ==================
        new_z_vec_for_break_am = np.array([u1[i], u2[i]])
        break_occurred_am = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_am[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_am) < 0.5:
                    actual_len = i + 1; break_occurred_am = True
            else:
                if np.linalg.norm(new_z_vec_for_break_am) < 0.001:
                    actual_len = i; break_occurred_am = True
            if break_occurred_am: break
        else:
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

def AM4_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK4_system_M5(F, t_array[:4], u10, u20, v_t_param, v_n_param, d_param)
        start_len=len(u1_start)
        if start_len < 4: return u1[:start_len], u2[:start_len]
        u1[:start_len], u2[:start_len] = u1_start, u2_start
    except Exception as e: print(f"AM4_M5 init err: {e}"); return u1[:1],u2[:1]
    actual_len=len(t_array)
    for i in range(4, len(t_array)):
        t_curr=t_array[i]
        t0,x0,y0=t_array[i-1],u1[i-1],u2[i-1]; t1,x1,y1=t_array[i-2],u1[i-2],u2[i-2]
        t2,x2,y2=t_array[i-3],u1[i-3],u2[i-3]; t3,x3,y3=t_array[i-4],u1[i-4],u2[i-4]
        if not all(np.isfinite(v) for v in [x0,y0,x1,y1,x2,y2,x3,y3]): actual_len=i; break
        try:
            F0=F(t0,x0,y0); F1=F(t1,x1,y1); F2=F(t2,x2,y2); F3=F(t3,x3,y3)
            if not all(np.all(np.isfinite(f)) for f in [F0, F1, F2, F3]): actual_len=i; break
        except Exception as e: print(f"AM4_M5 F err @ i={i}: {e}"); actual_len=i; break
        u1_pred = x0 + h/24.0 * (55.0*F0[0] - 59.0*F1[0] + 37.0*F2[0] - 9.0*F3[0])
        u2_pred = y0 + h/24.0 * (55.0*F0[1] - 59.0*F1[1] + 37.0*F2[1] - 9.0*F3[1])
        if not (np.isfinite(u1_pred) and np.isfinite(u2_pred)): actual_len=i; break
        try:
            F_pred = F(t_curr, u1_pred, u2_pred);
            if not np.all(np.isfinite(F_pred)): actual_len=i; break
        except Exception as e: print(f"AM4_M5 F_pred err @ i={i}: {e}"); actual_len=i; break
        u1_new = x0 + h/720.0*(251.0*F_pred[0] + 646.0*F0[0] - 264.0*F1[0] + 106.0*F2[0] - 19.0*F3[0])
        u2_new = y0 + h/720.0*(251.0*F_pred[1] + 646.0*F0[1] - 264.0*F1[1] + 106.0*F2[1] - 19.0*F3[1])
        if not (np.isfinite(u1_new) and np.isfinite(u2_new)): actual_len=i; break
        u1[i], u2[i] = u1_new, u2_new
        # ================== HIGHLIGHT START: Điều kiện break phức tạp cho AM4 ==================
        new_z_vec_for_break_am = np.array([u1[i], u2[i]])
        break_occurred_am = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_am[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_am) < 0.5:
                    actual_len = i + 1; break_occurred_am = True
            else:
                if np.linalg.norm(new_z_vec_for_break_am) < 0.001:
                    actual_len = i; break_occurred_am = True
            if break_occurred_am: break
        else:
            if u1[i] <= 0.01: actual_len = i + 1; break
        # ================== HIGHLIGHT END ==================
    return u1[:actual_len], u2[:actual_len]

# =================================================================
#  NEW SOLVERS for Model 5, Simulation 2 (Combined Logic)
# =================================================================

# --- RK Methods (Initializer for AB/AM) ---
def RK2_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    # t_array_initial_segment sẽ là t_array_full_potential[:2]
    # initial_state_combined là [x_kt0, y_kt0, x_tn0, y_tn0]
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1] # Thời gian cuối của segment này

    # Chỉ cần tính một bước cho RK2 để lấy điểm thứ hai
    t_curr, current_st = t_array_initial_segment[0], initial_state_combined
    try:
        k1 = f_combined_ode_func(t_curr, current_st)
        k2 = f_combined_ode_func(t_curr + h_step / 2.0, current_st + h_step / 2.0 * k1)
        # Chú ý: Công thức RK2 chuẩn (Heun) thường dùng k2 = f(t+h, y+h*k1)
        # Nếu bạn muốn RK2 (midpoint/improved Euler):
        # k2_midpoint = f_combined_ode_func(t_curr + h_step/2.0, current_st + h_step/2.0 * k1)
        # new_st = current_st + h_step * k2_midpoint
        # Dưới đây là công thức Heun's method / RK2 phổ biến:
        k2_heun = f_combined_ode_func(t_curr + h_step, current_st + h_step * k1)
        new_st = current_st + h_step / 2.0 * (k1 + k2_heun)
    except Exception as e:
        print(f"RK2_Sim2_Combined: Error in f_combined_ode_func call: {e}")
        return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

    time_points_list.append(t_array_initial_segment[1])
    state_history_list.append(new_st)

    if np.linalg.norm(new_st[2:4] - new_st[0:2]) <= catch_dist_threshold:
        caught_flag_main = True
        time_of_catch_main = t_array_initial_segment[1]
        # Không cần break vì đây chỉ là một bước

    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def RK3_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    # t_array_initial_segment sẽ là t_array_full_potential[:3]
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]

    current_st_loop = initial_state_combined
    for i in range(len(t_array_initial_segment) - 1): # Loop 2 lần để ra 3 điểm (t0, t1, t2)
        t_curr = t_array_initial_segment[i]
        try:
            k1 = f_combined_ode_func(t_curr, current_st_loop)
            k2 = f_combined_ode_func(t_curr + h_step / 2.0, current_st_loop + h_step / 2.0 * k1)
            k3 = f_combined_ode_func(t_curr + h_step, current_st_loop - h_step * k1 + 2.0 * h_step * k2)
            new_st = current_st_loop + h_step / 6.0 * (k1 + 4.0 * k2 + k3)
        except Exception as e:
            print(f"RK3_Sim2_Combined: Error in f_combined_ode_func call at t={t_curr:.2f}: {e}")
            return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

        time_points_list.append(t_array_initial_segment[i+1])
        state_history_list.append(new_st)
        current_st_loop = new_st # Cập nhật state cho vòng lặp tiếp theo

        if np.linalg.norm(new_st[2:4] - new_st[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_initial_segment[i+1]
            break # Dừng khởi tạo nếu đã bắt được
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def RK4_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    # t_array_initial_segment sẽ là t_array_full_potential[:4]
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]

    current_st_loop = initial_state_combined
    for i in range(len(t_array_initial_segment) - 1): # Loop 3 lần để ra 4 điểm
        t_curr = t_array_initial_segment[i]
        try:
            k1 = f_combined_ode_func(t_curr, current_st_loop)
            k2 = f_combined_ode_func(t_curr + h_step / 2.0, current_st_loop + h_step / 2.0 * k1)
            k3 = f_combined_ode_func(t_curr + h_step / 2.0, current_st_loop + h_step / 2.0 * k2)
            k4 = f_combined_ode_func(t_curr + h_step, current_st_loop + h_step * k3)
            new_st = current_st_loop + h_step / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        except Exception as e:
            print(f"RK4_Sim2_Combined: Error in f_combined_ode_func call at t={t_curr:.2f}: {e}")
            return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

        time_points_list.append(t_array_initial_segment[i+1])
        state_history_list.append(new_st)
        current_st_loop = new_st

        if np.linalg.norm(new_st[2:4] - new_st[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_initial_segment[i+1]
            break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def RK5_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    # t_array_initial_segment sẽ là t_array_full_potential[:5]
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]

    current_st_loop = initial_state_combined
    for i in range(len(t_array_initial_segment) - 1): # Loop 4 lần để ra 5 điểm
        t_curr = t_array_initial_segment[i]
        try:
            k1 = f_combined_ode_func(t_curr, current_st_loop)
            k2 = f_combined_ode_func(t_curr + h_step/4.0, current_st_loop + h_step/4.0 * k1)
            k3 = f_combined_ode_func(t_curr + h_step/4.0, current_st_loop + h_step/8.0 * k1 + h_step/8.0 * k2)
            k4 = f_combined_ode_func(t_curr + h_step/2.0, current_st_loop - h_step/2.0 * k2 + h_step * k3)
            k5 = f_combined_ode_func(t_curr + 3.0*h_step/4.0, current_st_loop + 3.0*h_step/16.0 * k1 + 9.0*h_step/16.0 * k4)
            k6 = f_combined_ode_func(t_curr + h_step, current_st_loop - 3.0*h_step/7.0 * k1 + 2.0*h_step/7.0 * k2 + 12.0*h_step/7.0 * k3 - 12.0*h_step/7.0 * k4 + 8.0*h_step/7.0 * k5)
            new_st = current_st_loop + h_step/90.0 * (7.0*k1 + 32.0*k3 + 12.0*k4 + 32.0*k5 + 7.0*k6)
        except Exception as e:
            print(f"RK5_Sim2_Combined: Error in f_combined_ode_func call at t={t_curr:.2f}: {e}")
            return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

        time_points_list.append(t_array_initial_segment[i+1])
        state_history_list.append(new_st)
        current_st_loop = new_st

        if np.linalg.norm(new_st[2:4] - new_st[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_initial_segment[i+1]
            break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main


# --- Adams-Bashforth Methods ---
def AB2_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 2 # AB2 cần y_0, y_1
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK2_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)

    if caught_init or len(states_init) < num_initial_points:
        return time_points_list, states_init, caught_init, time_catch_init

    # Chuyển thành list để có thể append
    time_points_list = list(time_points_list)
    state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]
    caught_flag_main = False
    time_of_catch_main = t_array_full_potential[-1]

    # f_values_history[j] lưu f(t_j, y_j)
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]

    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        # y_ip1 = y_i + h/2 * (3*f_i - f_im1)
        # i là chỉ số của y_i (điểm hiện tại)
        # f_i là f_values_history[i]
        # f_im1 là f_values_history[i-1]
        try:
            y_i = state_history_list[i]
            f_i = f_values_history[i]
            f_im1 = f_values_history[i-1]
            y_ip1 = y_i + (h_step / 2.0) * (3.0 * f_i - 1.0 * f_im1)
        except Exception as e:
            print(f"AB2_Sim2_Combined: Error calculating y_ip1 at t={time_points_list[i]:.2f}: {e}")
            break # Dừng nếu có lỗi tính toán

        state_history_list.append(y_ip1)
        time_points_list.append(t_array_full_potential[i+1])

        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_full_potential[i+1]
            break # Bắt được, dừng mô phỏng

        # Tính f_ip1 cho bước tiếp theo và lưu vào history
        try:
            f_ip1 = f_combined_like(t_array_full_potential[i+1], y_ip1)
            f_values_history.append(f_ip1)
        except Exception as e:
            print(f"AB2_Sim2_Combined: Error calculating f_ip1 at t={t_array_full_potential[i+1]:.2f}: {e}")
            # Có thể quyết định dừng ở đây hoặc cho phép nó tiếp tục với f_values cũ (không khuyến khích)
            break

    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AB3_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 3 # AB3 cần y_0, y_1, y_2
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK3_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)

    if caught_init or len(states_init) < num_initial_points:
        return time_points_list, states_init, caught_init, time_catch_init

    time_points_list = list(time_points_list)
    state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]
    caught_flag_main = False
    time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]

    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        # y_ip1 = y_i + h/12 * (23*f_i - 16*f_im1 + 5*f_im2)
        try:
            y_i = state_history_list[i]
            f_i = f_values_history[i]
            f_im1 = f_values_history[i-1]
            f_im2 = f_values_history[i-2]
            y_ip1 = y_i + (h_step / 12.0) * (23.0 * f_i - 16.0 * f_im1 + 5.0 * f_im2)
        except Exception as e:
            print(f"AB3_Sim2_Combined: Error calculating y_ip1 at t={time_points_list[i]:.2f}: {e}")
            break

        state_history_list.append(y_ip1)
        time_points_list.append(t_array_full_potential[i+1])
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold:
            caught_flag_main = True; time_of_catch_main = t_array_full_potential[i+1]; break
        try:
            f_ip1 = f_combined_like(t_array_full_potential[i+1], y_ip1)
            f_values_history.append(f_ip1)
        except Exception as e:
            print(f"AB3_Sim2_Combined: Error calculating f_ip1 at t={t_array_full_potential[i+1]:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AB4_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 4 # AB4
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK4_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points: return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list); state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]; caught_flag_main = False; time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]
    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        try:
            y_i = state_history_list[i]; f_i = f_values_history[i]; f_im1 = f_values_history[i-1]; f_im2 = f_values_history[i-2]; f_im3 = f_values_history[i-3]
            y_ip1 = y_i + (h_step / 24.0) * (55.0 * f_i - 59.0 * f_im1 + 37.0 * f_im2 - 9.0 * f_im3)
        except Exception as e: print(f"AB4_Sim2_Combined: Error y_ip1 t={time_points_list[i]:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_array_full_potential[i+1])
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_array_full_potential[i+1]; break
        try: f_ip1 = f_combined_like(t_array_full_potential[i+1], y_ip1); f_values_history.append(f_ip1)
        except Exception as e: print(f"AB4_Sim2_Combined: Error f_ip1 t={t_array_full_potential[i+1]:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AB5_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 5 # AB5
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK5_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points: return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list); state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]; caught_flag_main = False; time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]
    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        try:
            y_i = state_history_list[i]; f_i = f_values_history[i]; f_im1 = f_values_history[i-1]; f_im2 = f_values_history[i-2]; f_im3 = f_values_history[i-3]; f_im4 = f_values_history[i-4]
            y_ip1 = y_i + (h_step / 720.0) * (1901.0 * f_i - 2774.0 * f_im1 + 2616.0 * f_im2 - 1274.0 * f_im3 + 251.0 * f_im4)
        except Exception as e: print(f"AB5_Sim2_Combined: Error y_ip1 t={time_points_list[i]:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_array_full_potential[i+1])
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_array_full_potential[i+1]; break
        try: f_ip1 = f_combined_like(t_array_full_potential[i+1], y_ip1); f_values_history.append(f_ip1)
        except Exception as e: print(f"AB5_Sim2_Combined: Error f_ip1 t={t_array_full_potential[i+1]:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

# --- Adams-Moulton Methods ---
def AM2_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 2 # AM2 predictor (AB2) needs y_i, y_im1. Corrector AM2 uses y_i, y_im1, y_pred_ip1
    t_init_segment = t_array_full_potential[:num_initial_points] # => [t0, t1]
    time_points_list, states_init, caught_init, time_catch_init = RK2_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points: return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list); state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]; caught_flag_main = False; time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)] # f0, f1

    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1): # i là chỉ số của y_i
        try:
            y_i = state_history_list[i]; t_i = time_points_list[i]
            f_i = f_values_history[i]
            f_im1 = f_values_history[i-1] # f(t_{i-1}, y_{i-1})
            # Predictor (AB2): y_pred_ip1 = y_i + h/2 * (3*f_i - f_im1)
            y_pred_ip1 = y_i + (h_step / 2.0) * (3.0 * f_i - 1.0 * f_im1)
            t_ip1 = t_array_full_potential[i+1]
            f_pred_ip1 = f_combined_like(t_ip1, y_pred_ip1) # f(t_{i+1}, y_pred_{i+1})
            # Corrector (AM2): y_ip1 = y_i + h/12 * (5*f_pred_ip1 + 8*f_i - f_im1)
            y_ip1 = y_i + (h_step / 12.0) * (5.0 * f_pred_ip1 + 8.0 * f_i - 1.0 * f_im1)
        except Exception as e: print(f"AM2_Sim2_Combined: Error y_ip1 t={t_i:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_ip1)
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_ip1; break
        try: f_ip1_corrected = f_combined_like(t_ip1, y_ip1); f_values_history.append(f_ip1_corrected)
        except Exception as e: print(f"AM2_Sim2_Combined: Error f_ip1_corr t={t_ip1:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AM3_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 3 # AM3 predictor (AB3) needs y_i, y_im1, y_im2.
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK3_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points: return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list); state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]; caught_flag_main = False; time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]
    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        try:
            y_i = state_history_list[i]; t_i = time_points_list[i]
            f_i = f_values_history[i]; f_im1 = f_values_history[i-1]; f_im2 = f_values_history[i-2]
            # Predictor (AB3)
            y_pred_ip1 = y_i + (h_step / 12.0) * (23.0 * f_i - 16.0 * f_im1 + 5.0 * f_im2)
            t_ip1 = t_array_full_potential[i+1]
            f_pred_ip1 = f_combined_like(t_ip1, y_pred_ip1)
            # Corrector (AM3): y_ip1 = y_i + h/24 * (9*f_pred_ip1 + 19*f_i - 5*f_im1 + f_im2)
            y_ip1 = y_i + (h_step / 24.0) * (9.0 * f_pred_ip1 + 19.0 * f_i - 5.0 * f_im1 + 1.0 * f_im2)
        except Exception as e: print(f"AM3_Sim2_Combined: Error y_ip1 t={t_i:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_ip1)
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_ip1; break
        try: f_ip1_corrected = f_combined_like(t_ip1, y_ip1); f_values_history.append(f_ip1_corrected)
        except Exception as e: print(f"AM3_Sim2_Combined: Error f_ip1_corr t={t_ip1:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AM4_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 4 # AM4
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK4_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points: return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list); state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]; caught_flag_main = False; time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]
    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        try:
            y_i = state_history_list[i]; t_i = time_points_list[i]
            f_i = f_values_history[i]; f_im1 = f_values_history[i-1]; f_im2 = f_values_history[i-2]; f_im3 = f_values_history[i-3]
            # Predictor (AB4)
            y_pred_ip1 = y_i + (h_step / 24.0) * (55.0 * f_i - 59.0 * f_im1 + 37.0 * f_im2 - 9.0 * f_im3)
            t_ip1 = t_array_full_potential[i+1]
            f_pred_ip1 = f_combined_like(t_ip1, y_pred_ip1)
            # Corrector (AM4): y_ip1 = y_i + h/720 * (251*f_pred_ip1 + 646*f_i - 264*f_im1 + 106*f_im2 - 19*f_im3)
            y_ip1 = y_i + (h_step / 720.0) * (251.0 * f_pred_ip1 + 646.0 * f_i - 264.0 * f_im1 + 106.0 * f_im2 - 19.0 * f_im3)
        except Exception as e: print(f"AM4_Sim2_Combined: Error y_ip1 t={t_i:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_ip1)
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_ip1; break
        try: f_ip1_corrected = f_combined_like(t_ip1, y_ip1); f_values_history.append(f_ip1_corrected)
        except Exception as e: print(f"AM4_Sim2_Combined: Error f_ip1_corr t={t_ip1:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

# --- Các hằng số cần cho ABM (Lấy từ file simulation gốc) ---
# Ví dụ:
AGENT_DIRECTION_CHANGE_PROB = 0.02
AGENT_MAX_ANGLE_PERTURBATION_DEG = 10
MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY = 150 # Ngưỡng hiển thị đầy đủ
SAMPLE_SIZE_FOR_LARGE_POPULATION = 100 # Kích thước mẫu hiển thị
# Các hằng số mặc định khác nếu cần
ABM_ROOM_DIMENSION_DEFAULT = 10.0
ABM_AGENT_SPEED_DEFAULT = 0.05
ABM_CONTACT_RADIUS_DEFAULT = 0.55
ABM_R_FACTOR_DEFAULT = 1000
ABM_PTRANS_MIN = 0.01
ABM_PTRANS_MAX = 0.9
ABM_MAX_STEPS_DEFAULT = 400
ABM_INTERVAL_DEFAULT = 120

# --- Class Mô phỏng ABM (Copy toàn bộ class từ file simulation) ---
class DiseaseSimulationABM:
    def __init__(self, total_population, initial_infected_count_for_abm, room_dimension,
                 contact_radius, transmission_prob, agent_speed):
        self.n_total_population_initial = total_population
        self.n_total_population = total_population
        self.n_infected_initial_abm = initial_infected_count_for_abm
        self.room_dimension = room_dimension
        self.contact_radius = contact_radius
        self.transmission_prob = transmission_prob # P_trans giờ được truyền trực tiếp
        self.agent_speed = agent_speed
        self.susceptible_coords = np.zeros((0,2))
        self.infected_coords = np.zeros((0,2))
        self.susceptible_velocities = np.zeros((0,2))
        self.infected_velocities = np.zeros((0,2))
        self.current_time_step = 0
        self.contact_radius_patches = []
        self._initialize_agents()

    def _initialize_agents(self):
        if self.n_infected_initial_abm > self.n_total_population:
            raise ValueError("Số nhiễm ban đầu không thể lớn hơn tổng dân số.")
        all_coords = np.random.rand(self.n_total_population, 2) * self.room_dimension
        actual_initial_infected = min(self.n_infected_initial_abm, self.n_total_population)
        # Đảm bảo số lượng nhiễm không vượt quá tổng dân số khi chọn ngẫu nhiên
        if actual_initial_infected > self.n_total_population:
            actual_initial_infected = self.n_total_population
        
        if self.n_total_population > 0 and actual_initial_infected > 0 :
             infected_indices = np.random.choice(self.n_total_population, actual_initial_infected, replace=False)
        elif actual_initial_infected == 0:
             infected_indices = np.array([], dtype=int)
        else: # n_total_population = 0
             infected_indices = np.array([], dtype=int)


        susceptible_mask = np.ones(self.n_total_population, dtype=bool)
        if len(infected_indices) > 0:
            susceptible_mask[infected_indices] = False
        
        self.infected_coords = all_coords[infected_indices]
        self.susceptible_coords = all_coords[susceptible_mask]

        num_susceptible = self.susceptible_coords.shape[0]
        if num_susceptible > 0:
            angles_s = np.random.rand(num_susceptible) * 2 * np.pi
            self.susceptible_velocities = self.agent_speed * np.array([np.cos(angles_s), np.sin(angles_s)]).T
        else:
            self.susceptible_velocities = np.zeros((0,2))

        num_infected = self.infected_coords.shape[0]
        if num_infected > 0:
            angles_i = np.random.rand(num_infected) * 2 * np.pi
            self.infected_velocities = self.agent_speed * np.array([np.cos(angles_i), np.sin(angles_i)]).T
        else:
            self.infected_velocities = np.zeros((0,2))

    def _move_agents(self, coords_array, velocities_array):
        if coords_array.shape[0] == 0: return coords_array, velocities_array
        coords_array += velocities_array
        for i in range(coords_array.shape[0]):
            for dim in range(2):
                if coords_array[i, dim] < 0:
                    coords_array[i, dim] = 0
                    velocities_array[i, dim] *= -1
                elif coords_array[i, dim] > self.room_dimension:
                    coords_array[i, dim] = self.room_dimension
                    velocities_array[i, dim] *= -1
        for i in range(velocities_array.shape[0]):
            if np.random.rand() < AGENT_DIRECTION_CHANGE_PROB:
                angle_perturbation_rad = np.deg2rad((np.random.rand() - 0.5) * 2 * AGENT_MAX_ANGLE_PERTURBATION_DEG)
                vx, vy = velocities_array[i, 0], velocities_array[i, 1]
                current_speed_sq = vx**2 + vy**2
                if current_speed_sq < 1e-12 :
                    new_angle = np.random.rand() * 2 * np.pi; speed_to_use = self.agent_speed
                else:
                    current_angle = np.arctan2(vy, vx); new_angle = current_angle + angle_perturbation_rad; speed_to_use = self.agent_speed
                velocities_array[i, 0] = speed_to_use * np.cos(new_angle)
                velocities_array[i, 1] = speed_to_use * np.sin(new_angle)
        return coords_array, velocities_array

    def _check_infections(self):
        # (Giữ nguyên)
        if self.susceptible_coords.shape[0] == 0 or self.infected_coords.shape[0] == 0: return
        newly_infected_indices = []
        for i, s_pos in enumerate(self.susceptible_coords):
            if self.infected_coords.shape[0] > 0:
                distances_sq = np.sum((self.infected_coords - s_pos)**2, axis=1)
                min_dist_sq_to_infected = np.min(distances_sq)
                if min_dist_sq_to_infected < self.contact_radius**2:
                    if np.random.rand() < self.transmission_prob: newly_infected_indices.append(i)
        if newly_infected_indices:
            newly_infected_indices_np = np.array(sorted(list(set(newly_infected_indices)), reverse=True))
            agents_coords_to_move = self.susceptible_coords[newly_infected_indices_np]
            agents_velocities_to_move = self.susceptible_velocities[newly_infected_indices_np]
            if agents_coords_to_move.shape[0] > 0:
                 self.infected_coords = np.vstack((self.infected_coords, agents_coords_to_move))
                 self.infected_velocities = np.vstack((self.infected_velocities, agents_velocities_to_move))
            self.susceptible_coords = np.delete(self.susceptible_coords, newly_infected_indices_np, axis=0)
            self.susceptible_velocities = np.delete(self.susceptible_velocities, newly_infected_indices_np, axis=0)


    def step(self):
        self.current_time_step += 1
        self.susceptible_coords, self.susceptible_velocities = self._move_agents(self.susceptible_coords, self.susceptible_velocities)
        self.infected_coords, self.infected_velocities = self._move_agents(self.infected_coords, self.infected_velocities)
        self._check_infections()
        current_total_pop = len(self.susceptible_coords) + len(self.infected_coords)
        if abs(current_total_pop - self.n_total_population_initial) > 0 and self.current_time_step > 1 : # Cho phép sai số nhỏ
             # print(f"CẢNH BÁO: Tổng dân số thay đổi! Ban đầu: {self.n_total_population_initial}, Hiện tại: {current_total_pop} tại bước {self.current_time_step}")
             pass
        num_susceptible = len(self.susceptible_coords); num_infected = len(self.infected_coords)
        if num_susceptible == 0 and self.n_total_population_initial > 0: # Chỉ kiểm tra số lượng chưa nhiễm
            print(f"Tất cả {self.n_total_population_initial} người đã bị nhiễm tại bước thời gian {self.current_time_step}.")
            return True
        return False

    def update_contact_circles(self, ax, coords_to_display):
        for patch in self.contact_radius_patches: patch.remove()
        self.contact_radius_patches.clear()
        for i_pos in coords_to_display:
            circle = Circle((i_pos[0], i_pos[1]), self.contact_radius, edgecolor='red', facecolor='none', alpha=0.2, linewidth=0.8, linestyle='--'); ax.add_patch(circle); self.contact_radius_patches.append(circle)

    def get_current_stats(self):
        # Trả về dictionary chứa trạng thái hiện tại
        return {
            "time_step": self.current_time_step,
            "susceptible_count": len(self.susceptible_coords),
            "infected_count": len(self.infected_coords),
            "total_population": self.n_total_population_initial
        }

# --- Hàm helper cho hiển thị ABM (Copy từ file simulation) ---
def get_display_coords_mixed(s_coords, i_coords, max_total_full, sample_size_large):
    """Quyết định cách hiển thị dựa trên tổng số lượng."""
    total_current_agents = s_coords.shape[0] + i_coords.shape[0]
    
    if total_current_agents <= max_total_full:
        # Hiển thị tất cả
        return s_coords, i_coords
    else:
        # Hiển thị mẫu
        s_display = s_coords
        i_display = i_coords
        
        # Tính tỷ lệ S và I để lấy mẫu tương ứng
        ratio_s = s_coords.shape[0] / total_current_agents if total_current_agents > 0 else 0
        ratio_i = i_coords.shape[0] / total_current_agents if total_current_agents > 0 else 0
        
        num_s_to_sample = int(sample_size_large * ratio_s)
        num_i_to_sample = sample_size_large - num_s_to_sample # Đảm bảo tổng là sample_size_large

        if s_coords.shape[0] > num_s_to_sample:
            s_indices = np.random.choice(s_coords.shape[0], num_s_to_sample, replace=False)
            s_display = s_coords[s_indices]
        
        if i_coords.shape[0] > num_i_to_sample:
            i_indices = np.random.choice(i_coords.shape[0], num_i_to_sample, replace=False)
            i_display = i_coords[i_indices]
            
        return s_display, i_display
ABM_AVAILABLE = True
print("ABM components included directly in the script.")
# ==============================================
#           Models Data
# ==============================================
MODELS_DATA = {
    #Model 1: Energy demand
    LANG_VI["model1_name"]: {
        "id": "model1",
        "equation_key": "model1_eq",
        "description_key": "model1_desc",
        "param_keys_vi": [LANG_VI["model1_param1"], LANG_VI["model1_param2"], LANG_VI["model1_param3"], LANG_VI["model1_param4"]],
        "param_keys_en": [LANG_EN["model1_param1"], LANG_EN["model1_param2"], LANG_EN["model1_param3"], LANG_EN["model1_param4"]],
        "internal_param_keys": ["O₀", "k", "t₀", "t₁"],
        "ode_func": lambda k: (lambda t, y: k * y),
        "exact_func": lambda O0, k, t0: (lambda t: O0 * np.exp(k * (np.asarray(t) - t0))),
    },
    #Model 2: CCell growth
    LANG_VI["model2_name"]: {
        "id": "model2",
        "equation_key": "model2_eq",
        "description_key": "model2_desc",
        "param_keys_vi": [LANG_VI["model2_param1"], LANG_VI["model2_param3"], LANG_VI["model2_param4"]],
        "param_keys_en": [LANG_EN["model2_param1"], LANG_EN["model2_param3"], LANG_EN["model2_param4"]],
        "internal_param_keys": ["x₀", "t₀", "t₁"],
        "ode_func": lambda c: (lambda t, y: c * (y**(2.0/3.0) + 1e-15)),
        "exact_func": lambda x0, c, t0: (lambda t: (x0**(1.0/3.0) + c * (np.asarray(t) - t0) / 3.0)**3),
    },
    #Model 3: Spread of epidemicepidemic
    LANG_VI["model3_name"]: {
        "id": "model3", # Giữ id là model3
        "can_run_abm_on_screen3": True,
        "equation_key": "model3_eq",
        "description_key": "model3_desc",
        # Chỉ cần nhập n (giá trị ban đầu), t0, t1
        "param_keys_vi": [LANG_VI["model3_param2"], LANG_VI["model3_param4"], LANG_VI["model3_param5"]],
        "param_keys_en": [LANG_EN["model3_param2"], LANG_EN["model3_param4"], LANG_EN["model3_param5"]],
        "internal_param_keys": ["n", "t₀", "t₁"], # Key nội bộ là 'n' cho giá trị ban đầu
        # Hàm ODE: y' = -r * y * (n + 1 - y)
        # Lưu ý: tham số thứ hai của lambda là 'n_initial' để phân biệt với biến 'n' trong namespace khác
        "ode_func": lambda r, n_initial: (lambda t, y: -r * y * (n_initial + 1.0 - y)),
        # Hàm nghiệm chính xác: y(t) = n(n+1)exp(...) / (1 + n*exp(...))
        "exact_func": lambda n_initial, r, t0: (
            lambda t: (n_initial * (n_initial + 1.0) * np.exp(-r * (n_initial + 1.0) * (np.asarray(t) - t0))) / \
                      (1.0 + n_initial * np.exp(-r * (n_initial + 1.0) * (np.asarray(t) - t0))) if n_initial > 0 else
            (lambda t: np.zeros_like(np.asarray(t))) # Nếu n=0, nghiệm là 0
        ),
        "abm_defaults": {
            # "total_population": ..., # Đã xóa
            "initial_infected": 1,
            "room_dimension": ABM_ROOM_DIMENSION_DEFAULT, # 10.0

            # --- Tham số cũ ---
            # "agent_speed": ABM_AGENT_SPEED_DEFAULT, # 0.05 (Sẽ tính động)
            # "contact_radius": ABM_CONTACT_RADIUS_DEFAULT, # 0.55 (Sẽ tính động)
            "r_to_ptrans_factor": 5000, # Giữ cố định giá trị đã tăng ở lần trước (hoặc giá trị bạn thấy hợp lý)
            "ptrans_min": ABM_PTRANS_MIN, # 0.01
            "ptrans_max": ABM_PTRANS_MAX, # 0.9

            "base_agent_speed": 0.04,
            "speed_scaling_factor": 0.5,
            "min_agent_speed": 0.02,
            "max_agent_speed": 0.20,

            "base_contact_radius": 0.5,
            "radius_scaling_factor": 3.0,
            "min_contact_radius": 0.3,
            "max_contact_radius": 1.5,
            "seconds_per_step": 0.1,

            "max_steps": ABM_MAX_STEPS_DEFAULT, # 400
            "interval_ms": ABM_INTERVAL_DEFAULT, # 120
            "display_max_total": MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY, # 150
            "display_sample_size": SAMPLE_SIZE_FOR_LARGE_POPULATION # 100
        }
    },
    #Model 4: National economy
    LANG_VI["model4_name"]: {
        "id": "model4",
        "is_system": True,
        "equation_key": "model4_eq",
        "description_key": "model4_desc",
        # <<< HIGHLIGHT START: Cập nhật danh sách tham số cho Model 4 >>>
        "param_keys_vi": [
            # Chỉ các nhãn cho các ô sẽ hiển thị/nhập
            LANG_VI["model4_param_m"], LANG_VI["model4_param_l"],
            LANG_VI["model4_param_a"], LANG_VI["model4_param_s"], # Nhãn cho ô nhập a, s
            LANG_VI["model4_param_G"],
            LANG_VI["model4_param_alpha"], LANG_VI["model4_param_beta"], # Nhãn cho ô hiển thị alpha, beta
            LANG_VI["model4_param_dY0"], LANG_VI["model4_param_Y0"], # Đảo lại vị trí Y', Y cho giống hình ảnh
            LANG_VI["model4_param_t0"], LANG_VI["model4_param_t1"]
        ],
        "param_keys_en": [
            LANG_EN["model4_param_m"], LANG_EN["model4_param_l"],
            LANG_EN["model4_param_a"], LANG_EN["model4_param_s"], # Labels for input a, s
            LANG_EN["model4_param_G"],
            LANG_EN["model4_param_alpha"], LANG_EN["model4_param_beta"], # Labels for display alpha, beta
            LANG_EN["model4_param_dY0"], LANG_EN["model4_param_Y0"], # Keep order Y', Y
            LANG_EN["model4_param_t0"], LANG_EN["model4_param_t1"]
        ],
        # Các key nội bộ cần để LẤY GIÁ TRỊ NHẬP TỪ USER
        "internal_param_keys": ["m", "l", "a", "s", "G", "Y0", "dY0", "t₀", "t₁"], # alpha, beta không còn là input trực tiếp
        # Hàm ODE và Exact vẫn nhận alpha, beta đã tính toán
        "ode_func": lambda alpha, beta, m, G, l: (
            lambda t, u1, u2: np.array([u2, m * l * G - alpha * u2 - beta * u1])
        ),
        "exact_func": lambda alpha, beta, m, G, l, n, k, t0: (
            lambda t_arr: _model4_exact_solution(alpha, beta, m, G, l, n, k, t0, t_arr)
        ),
        # <<< HIGHLIGHT END >>>
    },
    #Model 5: Pursuit curve
    LANG_VI["model5_name"]: {
        "id": "model5",
        "is_system": True,                 # Đánh dấu là hệ PTVP
        "uses_rk5_reference": True,      # <<< Flag mới để biết dùng RK5 làm chuẩn >>>
        "equation_key": "model5_eq",
        "description_key": "model5_desc",
        "param_keys_vi": [
            LANG_VI["model5_param_x0"], LANG_VI["model5_param_y0"],
            LANG_VI["model5_param_u"], LANG_VI["model5_param_v"] ,
            LANG_VI["model5_param_t0"], LANG_VI["model5_param_t1"],
            # Không thêm key của combobox chọn component vào đây
        ],
        "param_keys_en": [
            LANG_EN["model5_param_x0"], LANG_EN["model5_param_y0"],
             LANG_EN["model5_param_u"], LANG_EN["model5_param_v"],
            LANG_EN["model5_param_t0"], LANG_EN["model5_param_t1"],
        ],
        "internal_param_keys": ["x0", "y0", "u", "v", "t₀", "t₁"], # Chỉ các tham số cần nhập
        # Hàm tạo ra F(t, x, y) -> [dx/dt, dy/dt]
        "ode_func": lambda u_param, v_param: (
            lambda t, x, y: _model5_ode_system(t, x, y, u_param, v_param)
        ),
        # Không có nghiệm giải tích, RK5 sẽ được tính trong _perform_single_simulation
        "exact_func": None, # Hoặc lambda *args: None
    },
}
#Solve model 4
def _model4_exact_solution(alpha, beta, m, G, l, n, k, t0, t_arr):
    """
    Calculates the exact solution Y(t) and Y'(t) for Model 4.
    n = Y(t0), k = Y'(t0)
    Returns a tuple: (Y_exact_values, dY_exact_values)
    """
    t_rel = np.asarray(t_arr) - t0 # Time relative to t0
    Y_vals = np.zeros_like(t_rel)
    dY_vals = np.zeros_like(t_rel)

    # Handle beta = 0 case separately to avoid division by zero later
    if abs(beta) < 1e-15:
        if abs(alpha) < 1e-15: # Should not happen with alpha > 0 constraint
             # If alpha is also zero, it's just Y'' = m*l*G
             c = m * l * G
             Y_vals = n + k * t_rel + 0.5 * c * t_rel**2
             dY_vals = k + c * t_rel
             return Y_vals, dY_vals
        else:
             # Y'' + alpha*Y' = m*l*G
             c = m * l * G
             # General solution: A + B*exp(-alpha*t) + (c/alpha)*t
             # Apply ICs:
             # Y(0) = n => A + B = n
             # Y'(0) = k => -alpha*B + c/alpha = k => B = (c/alpha - k)/alpha
             # A = n - B
             B = (c / alpha - k) / alpha
             A = n - B
             Y_vals = A + B * np.exp(-alpha * t_rel) + (c / alpha) * t_rel
             dY_vals = -alpha * B * np.exp(-alpha * t_rel) + (c / alpha)
             return Y_vals, dY_vals

    # Case beta != 0
    steady_state = (m * l * G) / beta
    delta = alpha**2 - 4 * beta

    if delta > 1e-15: # Overdamped
        r1 = (-alpha + np.sqrt(delta)) / 2.0
        r2 = (-alpha - np.sqrt(delta)) / 2.0
        # Y(t) = C1*exp(r1*t_rel) + C2*exp(r2*t_rel) + steady_state
        # Y(0) = n => C1 + C2 + steady_state = n => C1 + C2 = n - steady_state
        # Y'(0) = k => C1*r1 + C2*r2 = k
        # Solve for C1, C2
        if abs(r1 - r2) > 1e-15:
            C2 = (k - r1 * (n - steady_state)) / (r2 - r1)
            C1 = (n - steady_state) - C2
        else: # Should not happen if delta > 0
             C1, C2 = 0, 0 # Fallback
        Y_vals = C1 * np.exp(r1 * t_rel) + C2 * np.exp(r2 * t_rel) + steady_state
        dY_vals = C1 * r1 * np.exp(r1 * t_rel) + C2 * r2 * np.exp(r2 * t_rel)

    elif delta < -1e-15: # Underdamped
        omega = np.sqrt(-delta) / 2.0
        zeta = -alpha / 2.0
        # Y(t) = exp(zeta*t_rel)*(C1*cos(omega*t_rel) + C2*sin(omega*t_rel)) + steady_state
        # Y(0) = n => C1 + steady_state = n => C1 = n - steady_state
        # Y'(0) = k => zeta*C1 + omega*C2 = k => C2 = (k - zeta*C1)/omega
        C1 = n - steady_state
        if abs(omega)>1e-15:
            C2 = (k - zeta * C1) / omega
        else: # Should not happen if delta < 0
            C2 = 0 # Fallback
        exp_term = np.exp(zeta * t_rel)
        cos_term = np.cos(omega * t_rel)
        sin_term = np.sin(omega * t_rel)
        Y_vals = exp_term * (C1 * cos_term + C2 * sin_term) + steady_state
        dY_vals = zeta * exp_term * (C1 * cos_term + C2 * sin_term) + \
                  exp_term * (-C1 * omega * sin_term + C2 * omega * cos_term)

    else: # Critically damped (delta is very close to 0)
        r = -alpha / 2.0
        # Y(t) = (C1 + C2*t_rel)*exp(r*t_rel) + steady_state
        # Y(0) = n => C1 + steady_state = n => C1 = n - steady_state
        # Y'(0) = k => C2 + r*C1 = k => C2 = k - r*C1
        C1 = n - steady_state
        C2 = k - r * C1
        Y_vals = (C1 + C2 * t_rel) * np.exp(r * t_rel) + steady_state
        dY_vals = C2 * np.exp(r * t_rel) + (C1 + C2 * t_rel) * r * np.exp(r * t_rel)

    return Y_vals, dY_vals
#Solve model 5
def _model5_ode_system(t, x, y, u, v):
    """Hệ PTVP cho Model 5."""
    # Thêm epsilon nhỏ để tránh chia cho 0 nếu x và y cùng bằng 0
    r = np.sqrt(x**2 + y**2) + 1e-15
    dxdt = -v * x / r
    dydt = -v * y / r - u
    return np.array([dxdt, dydt])

# ==============================================
#           Matplotlib Canvas Widget
# ==============================================
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

        if parent:
            self.setParent(parent)

        # 🔧 Set policy mở rộng toàn phần
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        size_policy.setHorizontalStretch(1)  # (không bắt buộc, giúp khi trong layout có nhiều cột)
        size_policy.setVerticalStretch(1)
        self.setSizePolicy(size_policy)

        self.setMinimumSize(10, 10)  # Tránh bị co quá nhỏ
        self.updateGeometry()

# ==============================================
#           Welcome Screen Widget
# ==============================================
class WelcomeScreenWidget(RetranslatableWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        image_path = os.path.join(base_path, "back@2.png")
        self.background_pixmap = QPixmap(image_path)
        if self.background_pixmap.isNull():
            self.setStyleSheet("background-color: #e0f0ff;")
        else:
            self._setup_background()
        self._init_ui()
        self._connect_signals()
        self.retranslate_ui()

    def _setup_background(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        scaled = self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled))
        self.setPalette(palette)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30,30,30,30)
        main_layout.setSpacing(15)
        # --- Top Logos and Titles ---
        top_layout = QHBoxLayout()
        self.logo_tdtu_label = QLabel()
        self.logo_faculty_label = QLabel()
        try:
            self.logo_tdtu_label.setPixmap(QPixmap(os.path.join(base_path, "logotdtu1.png")).scaled(150, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
            self.logo_tdtu_label.setText("[TDTU Logo Error]")
        try:
            self.logo_faculty_label.setPixmap(QPixmap(os.path.join(base_path, "logokhoa1@2.png")).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
            self.logo_faculty_label.setText("[Faculty Logo Error]")
        self.logo_tdtu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_faculty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout = QVBoxLayout()
        self.uni_label = QLabel()
        self.faculty_label = QLabel()
        self.uni_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.uni_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uni_label.setStyleSheet("color: #000080;")
        self.faculty_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.faculty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.faculty_label.setStyleSheet("color: #000080;")
        title_layout.addWidget(self.uni_label)
        title_layout.addWidget(self.faculty_label)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.logo_tdtu_label, 1)
        top_layout.addLayout(title_layout, 3)
        top_layout.addWidget(self.logo_faculty_label, 1)
        main_layout.addLayout(top_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        # --- Project Title ---
        self.project_title_label = QLabel()
        self.project_title_label.setFont(QFont("Times New Roman", 24, QFont.Weight.Bold))
        self.project_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.project_title_label.setStyleSheet("color: #990000;")
        #main_layout.addWidget(self.project_title_label)
        project_title_wrapper_layout = QHBoxLayout()
        project_title_wrapper_layout.addStretch()
        project_title_wrapper_layout.addWidget(self.project_title_label)
        project_title_wrapper_layout.addStretch()
        main_layout.addLayout(project_title_wrapper_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        grouped_elements_layout = QVBoxLayout()
        grouped_elements_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # Để căn giữa các phần tử con bên trong nó
        grouped_elements_layout.setSpacing(15)
        # --- Info Layout ---
        info_style = "color: #333333;"
        info_font_size = 12
        bold_info_font_size = 14
        info_layout = QVBoxLayout()
        #info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.setSpacing(8)
        self.author_title_label = QLabel()
        self.author_names_label = QLabel()
        self.advisor_title_label = QLabel()
        self.advisor1_label = QLabel()
        self.advisor2_label = QLabel()
        self.author_title_label.setFont(QFont("Arial", bold_info_font_size, QFont.Weight.Bold))
        self.author_title_label.setStyleSheet(info_style)
        self.author_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.author_names_label.setFont(QFont("Arial", info_font_size))
        self.author_names_label.setStyleSheet(info_style)
        self.author_names_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advisor_title_label.setFont(QFont("Arial", bold_info_font_size, QFont.Weight.Bold))
        self.advisor_title_label.setStyleSheet(info_style)
        self.advisor_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advisor1_label.setFont(QFont("Arial", info_font_size))
        self.advisor1_label.setStyleSheet(info_style)
        self.advisor1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advisor2_label.setFont(QFont("Arial", info_font_size))
        self.advisor2_label.setStyleSheet(info_style)
        self.advisor2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.author_title_label)
        info_layout.addWidget(self.author_names_label)
        info_layout.addSpacerItem(QSpacerItem(10, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        info_layout.addWidget(self.advisor_title_label)
        info_layout.addWidget(self.advisor1_label)
        info_layout.addWidget(self.advisor2_label)
        grouped_elements_layout.addLayout(info_layout)

        #main_layout.addLayout(info_layout)
        #info_wrapper_layout = QHBoxLayout()
        #info_wrapper_layout.addStretch()
        #info_wrapper_layout.addLayout(info_layout) # info_layout là QVBoxLayout chứa các QLabel thông tin
        #info_wrapper_layout.addStretch()
        #main_layout.addLayout(info_wrapper_layout)
        #main_layout.addSpacerItem(QSpacerItem(20, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # --- Language Selector (ComboBox) ---
        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        self.language_combo = QComboBox()
        self.language_combo.setFont(QFont("Arial", 11))
        self.language_combo.setMinimumWidth(150)
        self.language_combo.setMinimumHeight(35) # Đặt chiều cao tối thiểu

        # Tạo và set LineEdit để hiển thị và căn giữa
        line_edit_welcome = QLineEdit()
        line_edit_welcome.setAlignment(Qt.AlignCenter) # Căn giữa bằng code Qt
        line_edit_welcome.setReadOnly(True)
        self.language_combo.setLineEdit(line_edit_welcome)

        # Cài đặt Event Filter cho LineEdit
        line_edit_welcome.installEventFilter(self) # 'self' (WelcomeScreenWidget) sẽ lọc sự kiện
        self.welcome_combo_line_edit = line_edit_welcome
        self.language_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #aabbcc;       /* Viền ngoài */
                border-radius: 17px;      /* Bo tròn (17.5 là nửa của 35px) */
                padding: 5px 5px 5px 5px; /* Giảm padding trái/phải */
                background-color: rgba(248, 248, 248, 0.95); /* Nền gần trắng */
                color: #333333;           /* Màu chữ */
            }

            QComboBox::drop-down {
                /* Ẩn phần mũi tên và đường kẻ */
                width: 0px;
                border: none;
            }

            /* Đảm bảo LineEdit được set không có nền/viền riêng */
            QComboBox > QLineEdit {
                 background-color: transparent;
                 border: none;
                 padding: 0px;
                 margin: 0px;
            }

            QComboBox QAbstractItemView { /* Style cho danh sách thả xuống */
                border: 1px solid darkgray;
                background-color: white;
                selection-background-color: #ddeeff;
                color: #333333;
                padding: 5px;
                min-width: 130px; /* Đảm bảo danh sách không quá hẹp */
                text-align: left; /* Căn trái trong danh sách thả xuống */
            }
        """)
        # Populate items in retranslate_ui
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        grouped_elements_layout.addLayout(lang_layout)
        #main_layout.addLayout(lang_layout)

        # --- Start Button ---
        main_layout.addSpacerItem(QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.start_button = QPushButton()
        self.start_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.start_button.setFixedSize(QSize(130, 45))
        self.start_button.setStyleSheet(""" QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ddeeff, stop:1 #3388cc); border: 2px solid #aabbcc; border-radius:10px; color:white; font-weight:bold; font-size:16px; padding:5px 10px;} QPushButton:hover{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeffff, stop:1 #4499dd); border-color:#cceeff;} QPushButton:pressed{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aaddff, stop:1 #2277bb); border-color:#88aabb; padding-top:6px; padding-bottom:4px;} """)
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        grouped_elements_layout.addLayout(button_layout)

        # Bây giờ, bọc grouped_elements_layout vào một QHBoxLayout với stretch hai bên để căn giữa nó
        # Đây chính là "info_wrapper_layout" mà bạn đề cập
        group_wrapper_layout = QHBoxLayout()
        group_wrapper_layout.addStretch()
        group_wrapper_layout.addLayout(grouped_elements_layout)
        group_wrapper_layout.addStretch()
        
        main_layout.addLayout(group_wrapper_layout)
        main_layout.addStretch(1)
    def eventFilter(self, watched, event):
        """Lọc sự kiện cho LineEdit của ComboBox ngôn ngữ trên Welcome Screen."""
        # Kiểm tra xem sự kiện có phải là cho LineEdit của Welcome Screen không
        if watched == getattr(self, 'welcome_combo_line_edit', None) and \
           event.type() == QEvent.MouseButtonPress and \
           event.button() == Qt.MouseButton.LeftButton:
            # Nếu đúng, yêu cầu ComboBox hiển thị popup
            if self.language_combo: # Kiểm tra ComboBox của Welcome Screen tồn tại
                self.language_combo.showPopup()
                return True # Đã xử lý sự kiện

        # Gọi eventFilter của lớp cha cho các sự kiện khác
        return super().eventFilter(watched, event)
    def _connect_signals(self):
        self.start_button.clicked.connect(self._go_to_screen1)
        # Connect ComboBox signal
        self.language_combo.currentIndexChanged.connect(self._language_selected)

    def retranslate_ui(self):
        # --- Retranslate static text ---
        self.uni_label.setText(self.tr("welcome_uni"))
        self.faculty_label.setText(self.tr("welcome_faculty"))
        self.project_title_label.setText(self.tr("welcome_project_title"))
        self.author_title_label.setText(self.tr("welcome_authors_title"))
        self.author_names_label.setText(self.tr("welcome_authors_names"))
        self.advisor_title_label.setText(self.tr("welcome_advisors_title"))
        self.advisor1_label.setText(self.tr("welcome_advisor1"))
        self.advisor2_label.setText(self.tr("welcome_advisor2"))
        self.start_button.setText(self.tr("start_button"))

        # --- Repopulate and set ComboBox ---
        self.language_combo.blockSignals(True) # Block signals during update
        self.language_combo.clear()
        # Add items with language codes as data
        self.language_combo.addItem(self.tr("lang_vi"), "vi")
        self.language_combo.addItem(self.tr("lang_en"), "en")
        # Set current index based on main window's language
        current_lang_code = self.main_window.current_language
        index_to_set = self.language_combo.findData(current_lang_code)
        if index_to_set >= 0:
            self.language_combo.setCurrentIndex(index_to_set)
        self.language_combo.blockSignals(False) # Unblock signals

        super().retranslate_ui()

    @Slot(int) # Accept index argument from signal
    def _language_selected(self, index):
        """Called when the language combo box selection changes."""
        selected_lang_code = self.language_combo.itemData(index)
        if selected_lang_code and selected_lang_code != self.main_window.current_language:
            self.main_window.set_language(selected_lang_code)

    @Slot()
    def _go_to_screen1(self):
        self.main_window.switch_to_screen1()

    def resizeEvent(self, event):
         if not self.background_pixmap.isNull():
             palette = self.palette()
             scaled = self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
             palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled))
             self.setPalette(palette)
         super().resizeEvent(event)

# ==============================================
#           Screen 1: Model Selection
# ==============================================
# (Screen1Widget không thay đổi nhiều, chỉ cần kế thừa RetranslatableWidget)
class Screen1Widget(RetranslatableWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.left_info_group = None
        self.right_application_group = None
        self.equation_static_label = None
        self.description_static_label = None
        self.model_combo = None
        self.title_label = None
        self.equation_display = None
        self.description_display = None
        self.application_image_label = None
        self.continue_button = None
        self.language_combo_screen1 = None
        self._init_ui()
        self._connect_signals()
        self._populate_model_combo()
        self.retranslate_ui()

    def _init_ui(self):
        #self.setStyleSheet(""" QWidget{...} ... """) # Giữ nguyên style sheet
        self.setStyleSheet("""
            QWidget#Screen1Widget { /* Đặt objectName cho widget chính của Screen1 */
                background-color: #f0f0f0;
            }
            QGroupBox {
                /* font-weight: bold; -- Sẽ đặt font trực tiếp bằng QFont */
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 1em; /* Tăng margin-top để có không gian cho title lớn hơn */
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px 0 5px; /* Tăng padding cho title */
                left: 10px;
                background-color: #f0f0f0; /* Để nền title trùng với nền chính của Screen1 */
                border-radius: 3px; /* Bo góc nhẹ cho nền title */
            }
            QLabel#titleLabelScreen1 { /* Đặt objectName cho title chính của Screen1 */
                color: #333333;
                padding: 5px;
                background-color: transparent;
            }
            QLabel#equationDisplayLabel {
                background-color: #ffffff; /* Nền trắng */
                border: 1px solid #ced4da; /* Giữ lại border */
                border-radius: 4px;
                padding: 10px;
                /* font-size và font-family sẽ đặt bằng QFont */
            }
            QLabel#descriptionDisplay { /* << THÊM HOẶC SỬA MỤC NÀY */
                background-color: #ffffff; /* Nền trắng */
                border: 1px solid #ced4da; /* Khung viền giống equationDisplayLabel */
                border-radius: 4px;        /* Bo góc giống equationDisplayLabel */
                padding: 8px;              /* Padding bên trong */
                /* font-size sẽ đặt bằng QFont */
            }
            QComboBox#modelSelectionCombo { /* Đặt objectName cho ComboBox */
                border: 1px solid #adb5bd; /* Border xám nhạt hơn */
                border-radius: 4px;
                padding: 5px 10px; /* Padding cho ComboBox */
                background-color: #f8f9fa; /* Màu nền xám rất nhạt, gần như trắng */
                color: #212529; /* Màu chữ tối */
                /* font-size sẽ đặt bằng QFont */
            }
            QComboBox#modelSelectionCombo {
                padding: 5px 25px 5px 10px; /* Tăng padding-right để có chỗ cho mũi tên mặc định nếu ::drop-down không hoạt động */
                min-height: 35px;
                border: 1px solid #adb5bd;
                background-color: #f8f9fa;
            }
            QComboBox#modelSelectionCombo {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 25px 6px 12px; /* Right padding lớn hơn để chừa chỗ cho mũi tên */
                min-height: 28px; /* Điều chỉnh cho phù hợp với font */
                background-color: white; /* Hoặc màu bạn muốn */
                /* selection-background-color: #007bff; -- Áp dụng cho phần text được chọn, không phải mũi tên */
            }
                           QComboBox#modelSelectionCombo {
                padding: 5px 25px 5px 10px; /* Tăng padding-right để có chỗ cho mũi tên mặc định nếu ::drop-down không hoạt động */
                min-height: 35px;
                border: 1px solid #adb5bd;
                background-color: #f8f9fa;
            }
            QComboBox#modelSelectionCombo::drop-down {
                /* Không cần style nhiều ở đây nếu chỉ muốn mũi tên mặc định */
                border: none; /* Quan trọng: Thử bỏ border của drop-down */
                width: 20px; /* Đảm bảo đủ rộng */
                /* background: transparent; */ /* Thử nền trong suốt */
            }
            QComboBox#modelSelectionCombo QAbstractItemView {
                border: 1px solid #ced4da;
                background-color: white;
                selection-background-color: #007bff;
                selection-color: white;
                color: #212529;
                padding: 4px;
            }
        """)

        self.setObjectName("Screen1Widget") # Đặt objectName cho widget chính
        layout=QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15) # Giảm spacing

        # Layout riêng cho tiêu đề chính, đảm bảo nó được căn giữa
        title_and_lang_layout = QHBoxLayout()
        title_and_lang_layout.setSpacing(10) # Giữ khoảng cách giữa title và combo

        # Tiêu đề chính
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabelScreen1")
        self.title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Căn giữa text bên trong QLabel

        # ComboBox ngôn ngữ
        self.language_combo_screen1 = QComboBox()
        self.language_combo_screen1.setFont(QFont("Arial", 11))
        self.language_combo_screen1.setMinimumWidth(150) # Giữ kích thước tối thiểu
        self.language_combo_screen1.setMinimumHeight(35)
        # ... (code set LineEdit và stylesheet cho language_combo_screen1 như cũ) ...
        line_edit_display = QLineEdit()
        line_edit_display.setAlignment(Qt.AlignCenter)
        line_edit_display.setReadOnly(True)
        line_edit_display.installEventFilter(self)
        self.language_combo_screen1_line_edit = line_edit_display
        self.language_combo_screen1.setLineEdit(line_edit_display)
        self.language_combo_screen1.setStyleSheet("""
            QComboBox {
                border: 1px solid #aabbcc;
                border-radius: 17px;
                /* Quan trọng: Giảm padding trái/phải để LineEdit có thể căn giữa */
                /* Có thể cần thử padding: 5px 0px; nếu 5px 5px vẫn bị lệch */
                padding: 5px 5px 5px 5px;
                background-color: rgba(248, 248, 248, 0.95);
                color: #333333;
            }

            /* Bỏ phần style cho QComboBox QLineEdit vì đã set bằng code */
            /*
            QComboBox QLineEdit {
                 ...
            }
            */

            QComboBox::drop-down {
                width: 0px;
                border: none;
            }

            /* StyleSheet cho LineEdit được set làm display widget (nếu cần) */
            /* Đảm bảo LineEdit không có viền/nền riêng che lấp ComboBox */
            QComboBox > QLineEdit { /* Selector > chỉ áp dụng cho LineEdit con trực tiếp */
                 background-color: transparent;
                 border: none;
                 padding: 0px;
                 margin: 0px;
            }


            QComboBox QAbstractItemView {
                border: 1px solid darkgray;
                background-color: white;
                selection-background-color: #ddeeff;
                color: #333333;
                padding: 5px;
                min-width: 130px;
                text-align: left; /* Giữ căn trái trong danh sách thả xuống */
            }
        """)

        title_and_lang_layout.addStretch(3) # Stretch bên trái (ví dụ: giá trị lớn hơn)
        title_and_lang_layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter) # Title
        title_and_lang_layout.addStretch(2) # Stretch giữa title và combo (ví dụ: giá trị nhỏ hơn stretch trái)
        title_and_lang_layout.addWidget(self.language_combo_screen1, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter) # Combo

        layout.addLayout(title_and_lang_layout)

        self.model_combo=QComboBox()
        self.model_combo.setObjectName("modelSelectionCombo")
        self.model_combo.setFont(QFont("Arial",13,QFont.Weight.Bold))
        self.model_combo.setMinimumHeight(40)
        layout.addWidget(self.model_combo)

         # --- Layout chính cho phần thông tin và ứng dụng (QHBoxLayout) ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20) # Khoảng cách giữa 2 cột

           # --- Cột Trái: Thông tin mô hình (TEXT) ---
        self.left_info_group = QGroupBox()
        self.left_info_group.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        left_info_layout = QVBoxLayout(self.left_info_group)
        left_info_layout.setContentsMargins(15, 30, 15, 15)
        left_info_layout.setSpacing(10)
    
        # Label cho "Phương trình..."
        self.equation_static_label = QLabel() # Label tĩnh "Phương trình..."
        self.equation_static_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        left_info_layout.addWidget(self.equation_static_label)

        # Hiển thị phương trình (QLabel cho RichText)
        self.equation_display = QLabel()
        self.equation_display.setObjectName("equationDisplayLabel") # Để style riêng nếu cần
        self.equation_display.setFont(QFont("Courier New", 11))
        self.equation_display.setTextFormat(Qt.TextFormat.RichText) # Cho phép thẻ HTML như <sup>
        self.equation_display.setWordWrap(True)
        self.equation_display.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.equation_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # Giãn ngang, chiều cao tự động
        left_info_layout.addWidget(self.equation_display)

        # Label cho "Mô tả..."
        self.description_static_label = QLabel() # Label tĩnh "Mô tả..."
        self.description_static_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        left_info_layout.addWidget(self.description_static_label)

        # Hiển thị mô tả (QTextEdit cho phép scroll nếu text dài)
        self.description_display = QLabel() # Thay bằng QLabel
        self.description_display.setObjectName("descriptionDisplay")
        #self.description_display.setReadOnly(True) # QLabel không có thuộc tính này
        self.description_display.setFont(QFont("Arial", 12))
        self.description_display.setTextFormat(Qt.TextFormat.RichText) # Rất quan trọng cho QLabel
        self.description_display.setWordWrap(True) # Để tự động xuống dòng
        self.description_display.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # Căn lề
        self.description_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # Cho phép giãn chiều cao tự động
        left_info_layout.addWidget(self.description_display, 1)

        content_layout.addWidget(self.left_info_group, 1) # Cột trái chiếm 1 phần

        #self.info_group=QGroupBox()
        #info_layout=QVBoxLayout(self.info_group)
        #info_layout.setSpacing(8) # Giảm spacing
        #self.equation_label=QLabel()
        #self.equation_label.setFont(QFont("Arial",11,QFont.Weight.Bold))
        #info_layout.addWidget(self.equation_label)
        #self.equation_display=QLabel()
        #self.equation_display.setObjectName("equationDisplayLabel")
        #self.equation_display.setFont(QFont("Courier New",13))
        #self.equation_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.equation_display.setTextFormat(Qt.TextFormat.RichText)
        #self.equation_display.setWordWrap(True)
        #info_layout.addWidget(self.equation_display)
        #self.description_label=QLabel()
        #self.description_label.setFont(QFont("Arial",11,QFont.Weight.Bold))
        #info_layout.addWidget(self.description_label)
        #self.description_display=QTextEdit()
        #self.description_display.setFont(QFont("Arial",11))
        #self.description_display.setReadOnly(True)
        #self.description_display.setMinimumHeight(100)
        #info_layout.addWidget(self.description_display)
        #self.description_image_label = QLabel() # Tạo QLabel mới cho ảnh
        #self.description_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Căn giữa ảnh
        #self.description_image_label.setMinimumWidth(100) # Ngăn không bị co quá nhỏ
        #self.description_image_label.setVisible(False) # Ẩn ban đầu
        #info_layout.addWidget(self.description_image_label) # Thêm vào layout SAU ô text
        # <<< KẾT THÚC THÊM CODE >>>

        # --- Cột Phải: Ứng dụng của mô hình ---
        self.right_application_group = QGroupBox() # Sẽ đặt title là "Ứng dụng của mô hình"
        self.right_application_group.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        right_application_layout = QVBoxLayout(self.right_application_group)
        right_application_layout.setContentsMargins(15, 30, 15, 15)
        right_application_layout.setSpacing(10)

        self.application_image_label = QLabel()
        self.application_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.application_image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.application_image_label.setScaledContents(True)
        right_application_layout.addWidget(self.application_image_label, 1) # Stretch factor 1

        content_layout.addWidget(self.right_application_group, 2) # Cột phải chiếm 2 phần (rộng hơn)

        layout.addLayout(content_layout, 1) # Layout nội dung chiếm phần lớn không gian
        #layout.addWidget(self.info_group)
        #layout.addStretch()
        #Button continuous
        button_layout=QHBoxLayout()
        button_layout.addStretch()
        self.continue_button=QPushButton()
        self.continue_button.setFont(QFont("Arial",12,QFont.Weight.Bold))
        self.continue_button.setStyleSheet(""" QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ddeeff, stop:1 #3388cc); border: 2px solid #aabbcc; border-radius:10px; color:white; font-weight:bold; font-size:16px; padding:5px 10px;} QPushButton:hover{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeffff, stop:1 #4499dd); border-color:#cceeff;} QPushButton:pressed{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aaddff, stop:1 #2277bb); border-color:#88aabb; padding-top:6px; padding-bottom:4px;} """)
        button_layout.addWidget(self.continue_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def eventFilter(self, watched, event):
        """Lọc sự kiện cho LineEdit của ComboBox ngôn ngữ."""
        # Kiểm tra xem sự kiện có phải là cho LineEdit chúng ta đang theo dõi không
        # và sự kiện có phải là Nhấp chuột trái không
        if watched == getattr(self, 'language_combo_screen1_line_edit', None) and \
           event.type() == QEvent.MouseButtonPress and \
           event.button() == Qt.MouseButton.LeftButton:
            # Nếu đúng, yêu cầu ComboBox hiển thị popup
            if self.language_combo_screen1: # Đảm bảo ComboBox tồn tại
                self.language_combo_screen1.showPopup()
                return True # Đã xử lý sự kiện, không cần lan truyền tiếp

        # Nếu không phải sự kiện chúng ta quan tâm, trả về False để xử lý mặc định
        return super().eventFilter(watched, event)
    
    def _connect_signals(self):
        self.model_combo.currentTextChanged.connect(self._update_model_info)
        self.continue_button.clicked.connect(self._on_continue_clicked)
        if self.language_combo_screen1: # Kiểm tra nếu widget đã được tạo
            self.language_combo_screen1.currentIndexChanged.connect(self._language_selected_screen1)
    
    @Slot(int) # Accept index argument from signal
    def _language_selected_screen1(self, index):
        """Called when the language combo box on Screen 1 selection changes."""
        if self.language_combo_screen1: # Kiểm tra widget tồn tại
            selected_lang_code = self.language_combo_screen1.itemData(index)
            if selected_lang_code and selected_lang_code != self.main_window.current_language:
                self.main_window.set_language(selected_lang_code)
    
    def _populate_model_combo(self):
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        model_keys_vi = list(MODELS_DATA.keys()) # Dùng key VI làm tham chiếu
        for vi_key in model_keys_vi:
            model_data = MODELS_DATA[vi_key]
            lang_key = f"{model_data['id']}_name"
            display_name = self.tr(lang_key, default_text=vi_key)
            self.model_combo.addItem(display_name, vi_key) # Lưu key VI gốc
        self.model_combo.blockSignals(False)
        if self.model_combo.count() > 0:
            #self._update_model_info(self.model_combo.currentText())
            self._update_model_info(self.model_combo.itemText(0))
            # HIGHLIGHT END
        else:
            # HIGHLIGHT START: Nếu không có model nào, xóa thông tin
            self._clear_model_info_display()

    def _clear_model_info_display(self):
        self.equation_display.setText("")
        self.description_display.setText("") # Dùng setPlainText cho QTextEdit
        self.application_image_label.clear()
    
    @Slot(str)
    def _update_model_info(self, current_display_name=None):
        self._clear_model_info_display()
        if current_display_name is None or self.model_combo.count()==0:
            vi_key = self.model_combo.currentData() if self.model_combo.count()>0 else None
        else:
            item_index = self.model_combo.findText(current_display_name)
            if item_index != -1:
                vi_key = self.model_combo.itemData(item_index)
            else:
                vi_key = None # Không tìm thấy item
        if vi_key and vi_key in MODELS_DATA:
            data = MODELS_DATA[vi_key]
            model_id = data.get("id")
            # Lấy và hiển thị phương trình (TEXT)
            eq_text_key = data.get("equation_key", "")
            eq_text = self.tr(eq_text_key, "N/A")
            self.equation_display.setText(eq_text) # setText cho QLabel

            # Lấy và hiển thị mô tả (TEXT)
            desc_text_key = data.get("description_key", "")
            desc_text = self.tr(desc_text_key, "...")
            #self.description_display.setHtml(desc_text)
            self.description_display.setText(desc_text) # 

            current_lang_code = self.main_window.current_language # 'vi' hoặc 'en'

            # Trích xuất số model từ model_id (ví dụ: "model1" -> "1")
            model_number_str = ""
            if model_id and model_id.startswith("model"):
                try:
                    model_number_str = model_id[5:] # Lấy phần sau "model"
                except IndexError:
                    print(f"Warning: Could not extract model number from id: {model_id}")

            if model_number_str:
                lang_suffix_for_file = "Vie" if current_lang_code == 'vi' else "Eng"
                # Tất cả các file của bạn đều là .png dựa trên hình ảnh
                application_image_filename = f"model_{model_number_str}_{lang_suffix_for_file}.png"
                
                actual_application_image_path = os.path.join(base_path, application_image_filename)

                if os.path.exists(actual_application_image_path):
                    pixmap_app = QPixmap(actual_application_image_path)
                    if not pixmap_app.isNull():
                        self.application_image_label.setPixmap(pixmap_app)
                        print(f"Displayed application image: {actual_application_image_path}")
                    else:
                        print(f"Warning: Failed to load application QPixmap from {actual_application_image_path}")
                        self.application_image_label.clear()
                else:
                    print(f"Application image not found: {actual_application_image_path}")
                    self.application_image_label.clear()
            else:
                # Nếu không trích xuất được model_number_str, xóa ảnh
                print(f"Could not determine image filename for model_id: {model_id}")
                self.application_image_label.clear()
            # HIGHLIGHT END
        else:
            self._clear_model_info_display()

    @Slot()
    def _on_continue_clicked(self):
        if self.model_combo.currentIndex()>=0:
            selected_vi_key = self.model_combo.currentData()
            self.main_window.switch_to_screen2(selected_vi_key)
        else:
            QMessageBox.warning(self, self.tr("msg_warning"), self.tr("msg_select_model", "Please select model"))

    def retranslate_ui(self):
        if hasattr(self, 'title_label') and self.title_label:
            self.title_label.setText(self.tr("screen1_title"))
        if hasattr(self, 'language_combo_screen1') and self.language_combo_screen1:
            self.language_combo_screen1.blockSignals(True) # Block signals during update
            self.language_combo_screen1.clear()
            # Add items with language codes as data
            self.language_combo_screen1.addItem(self.tr("lang_vi"), "vi")
            self.language_combo_screen1.addItem(self.tr("lang_en"), "en")
            # Set current index based on main window's language
            current_lang_code = self.main_window.current_language
            index_to_set = self.language_combo_screen1.findData(current_lang_code)
            if index_to_set >= 0:
                self.language_combo_screen1.setCurrentIndex(index_to_set)
            self.language_combo_screen1.blockSignals(False) # Unblock signals
        # HIGHLIGHT START: Sử dụng key dịch mới cho GroupBox titles
        if hasattr(self, 'left_info_group') and self.left_info_group:
            # Sử dụng key mới hoặc key cũ "screen1_info_group_title" tùy bạn chọn
            self.left_info_group.setTitle(self.tr("screen1_model_info_group_title")) 
        if hasattr(self, 'right_application_group') and self.right_application_group:
            self.right_application_group.setTitle(self.tr("screen1_model_application_group_title"))
        # HIGHLIGHT END

        if hasattr(self, 'equation_static_label') and self.equation_static_label:
            self.equation_static_label.setText(self.tr("screen1_equation_label"))
        if hasattr(self, 'description_static_label') and self.description_static_label:
            self.description_static_label.setText(self.tr("screen1_description_label"))
        
        if hasattr(self, 'continue_button') and self.continue_button:
            self.continue_button.setText(self.tr("screen1_continue_button"))

        current_vi_key = None
        if hasattr(self, 'model_combo') and self.model_combo:
            current_vi_key = self.model_combo.currentData()
            self._populate_model_combo() 

            if current_vi_key:
                index = self.model_combo.findData(current_vi_key)
                if index >= 0:
                    self.model_combo.setCurrentIndex(index)
                elif self.model_combo.count() > 0:
                    self.model_combo.setCurrentIndex(0)
            elif self.model_combo.count() > 0:
                self.model_combo.setCurrentIndex(0)
            else:
                if hasattr(self, '_clear_model_info_display'): # Kiểm tra _clear_model_info_display tồn tại
                    self._clear_model_info_display()
        elif hasattr(self, '_clear_model_info_display'): # Nếu model_combo không tồn tại, cũng clear
            self._clear_model_info_display()
        super().retranslate_ui()

# ==============================================
#           Simulation Plot Window
# ==============================================
# (Giữ nguyên SimulationPlotWindow như trước, đã kế thừa RetranslatableWidget)
class SimulationPlotWindow(RetranslatableWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setGeometry(200, 200, 700, 550)
        layout = QVBoxLayout(self)
        self.canvas = MplCanvas(self, width=6, height=4.5, dpi=100)
        layout.addWidget(self.canvas)
        self.retranslate_ui()
        self._setup_initial_plot()

    def _setup_initial_plot(self):
        ax = self.canvas.axes
        ax.clear()
        ax.set_title(self.tr("sim_window_plot_title"))
        ax.set_xlabel(self.tr("sim_window_t_axis"))
        ax.set_ylabel(self.tr("sim_window_value_axis"))
        ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.fig.tight_layout()
        self.canvas.draw()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("sim_window_title"))
        if hasattr(self.canvas,'axes') and self.canvas.axes.lines:
            ax=self.canvas.axes
            ax.set_title(self.tr("sim_window_plot_title"),fontsize=12,weight='bold')
            ax.set_xlabel(self.tr("sim_window_t_axis"),fontsize=10)
            ax.set_ylabel(self.tr("sim_window_value_axis"),fontsize=10)
            self.canvas.fig.tight_layout()
            self.canvas.draw()
        else:
            self._setup_initial_plot()
        super().retranslate_ui()

    def plot_data(self, t, sim_data_list, labels=None, title_key="sim_window_plot_title"):
        ax = self.canvas.axes
        ax.clear()
        plot_valid = False
        num_lines = len(sim_data_list)
        colors = plt.cm.viridis(np.linspace(0, 0.9, num_lines)) if num_lines > 1 else ['#1f77b4']
        if t is not None and sim_data_list:
            t_np = np.asarray(t)
            for i, sim_line in enumerate(sim_data_list):
                sim_line_np = np.asarray(sim_line)
                label = labels[i] if labels and i < len(labels) else f'Sim {i+1}'
                label = self.tr("screen2_plot_exact_label") if label.lower()=="exact" else label
                if isinstance(sim_line_np,np.ndarray) and len(t_np)==len(sim_line_np) and np.all(np.isfinite(sim_line_np)):
                    ax.plot(t_np, sim_line_np, label=label, color=colors[i%len(colors)], alpha=0.8, lw=1.8, marker='.', ms=4, ls='-')
                    plot_valid = True
        if not plot_valid:
            ax.text(0.5, 0.5, self.tr("sim_window_no_data"), ha='center', va='center', transform=ax.transAxes, wrap=True, fontsize=12, color='red')
        ax.set_title(self.tr(title_key),fontsize=12,weight='bold')
        ax.set_xlabel(self.tr("sim_window_t_axis"),fontsize=10)
        ax.set_ylabel(self.tr("sim_window_value_axis"),fontsize=10)
        ax.grid(True,ls='--',alpha=0.6)
        if plot_valid and labels:
            ax.legend(fontsize='small')
        self.canvas.fig.tight_layout()
        self.canvas.draw()

    def closeEvent(self, event):
        print("Closing sim window.")
        self.canvas.figure.clf()
        plt.close(self.canvas.figure)
        super().closeEvent(event)

# ==============================================
#           Screen 2: Simulation and Results
# ==============================================
class Screen2Widget(RetranslatableWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.component_selector_widget = None # <<< Thêm thuộc tính để lưu combobox
        self.component_selector_label = None
        self.current_model_vi_key = None
        self.current_model_data = {}
        self.param_inputs = {}
        self.simulation_window = None
        self.dynamic_plot_data = None
        self.last_results_dict = {}
        self.calculated_c_label_widget = None # Lưu label
        self.calculated_c_display_widget = None # Lưu QLineEdit
        self._last_calculated_c = None
        self.calculated_r_label_widget = None
        self.calculated_r_display_widget = None
        self._last_calculated_r = None 
        self.calculated_steady_state_label_widget = None
        self.calculated_steady_state_display_widget = None
        self._last_calculated_steady_state = None
        self.calculated_beta_label_widget = None
        self.calculated_beta_display_widget = None
        self._last_calculated_beta = None
        self.select_all_steps_checkbox = None
        self._init_ui()
        self._connect_signals()
        self.rb_adams_bashforth.setChecked(True)
        self.retranslate_ui() # Includes initial plot setup

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10) # Giảm margins
        main_layout.setSpacing(5) # Giảm spacing

        # Tạo layout chứa tiêu đề và nút
        title_bar_layout = QHBoxLayout()

        #Button
        self.btn_back = QPushButton()
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setFont(QFont("Arial", 9))
        self.btn_back.setStyleSheet(""" QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ddeeff, stop:1 #3388cc); border: 2px solid #aabbcc; border-radius:10px; color:white; font-weight:bold; font-size:16px; padding:5px 10px;} QPushButton:hover{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeffff, stop:1 #4499dd); border-color:#cceeff;} QPushButton:pressed{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aaddff, stop:1 #2277bb); border-color:#88aabb; padding-top:6px; padding-bottom:4px;} """)

        title_bar_layout.addWidget(self.btn_back)

        # Tiêu đề
        self.model_title_label = QLabel()
        self.model_title_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.model_title_label.setStyleSheet("color: #191970; padding: 4px;")

        # Căn giữa tiêu đề bằng cách dùng stretch
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self.model_title_label)
        title_bar_layout.addStretch()

        #Button to screen 3
        self.btn_go_to_screen3 = QPushButton()
        self.btn_go_to_screen3.setVisible(False) # <<< ẨN BAN ĐẦU
        self.btn_go_to_screen3.setEnabled(False)
        self.btn_go_to_screen3.setObjectName("btn_go_to_screen3_dyn")
        self.btn_go_to_screen3.setFont(QFont("Arial", 9)) # Cùng font với nút phụ khác
        #self.btn_go_to_screen3.setEnabled(False) # <<< BẮT ĐẦU VÔ HIỆU HÓA
        self.btn_go_to_screen3.setStyleSheet(""" QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ddeeff, stop:1 #3388cc); border: 2px solid #aabbcc; border-radius:10px; color:white; font-weight:bold; font-size:16px; padding:5px 10px;} QPushButton:hover{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeffff, stop:1 #4499dd); border-color:#cceeff;} QPushButton:pressed{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aaddff, stop:1 #2277bb); border-color:#88aabb; padding-top:6px; padding-bottom:4px;} """)

        title_bar_layout.addWidget(self.btn_go_to_screen3)
        # Thêm vào layout chính
        main_layout.addLayout(title_bar_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(8) # Thêm spacing giữa 2 panel
        main_layout.addLayout(content_layout, 1)


        # Thêm nút này vào layout, ví dụ hàng 2, cột 1 (hoặc hàng 3, cột 0 nếu muốn nó dưới nút save)
        # --- Left Panel (Controls) ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setStyleSheet(""" QWidget{...} QGroupBox{padding: 10px 5px 5px 5px; margin-top: 0.1ex;} ... """) # Giảm padding groupbox
        left_panel.setContentsMargins(7, 10, 9, 9)
        left_layout.setSpacing(10) # Giảm spacing/margins
        content_layout.addWidget(left_panel, 1) # *** THAY ĐỔI Stretch: Left=1 ***

        self.method_group = QGroupBox()
        method_layout = QHBoxLayout(self.method_group)
        self.method_button_group = QButtonGroup(self)
        self.method_button_group.setExclusive(True)
        self.rb_adams_bashforth = QRadioButton()
        self.rb_adams_moulton = QRadioButton()
        self.rb_adams_bashforth.setObjectName("Bashforth")
        self.rb_adams_moulton.setObjectName("Moulton")
        self.rb_adams_bashforth.setFont(QFont("Arial", 10))
        self.rb_adams_moulton.setFont(QFont("Arial", 10))
        self.method_button_group.addButton(self.rb_adams_bashforth)
        self.method_button_group.addButton(self.rb_adams_moulton)
        method_layout.addWidget(self.rb_adams_bashforth)
        method_layout.addWidget(self.rb_adams_moulton)
        left_layout.addWidget(self.method_group)

        self.details_group = QGroupBox()
        details_layout = QVBoxLayout(self.details_group)
        details_layout.setSpacing(6) # Giảm spacing
        steps_layout_container = QHBoxLayout()
        self.steps_label = QLabel()
        steps_layout_container.addWidget(self.steps_label)
        self.select_all_steps_checkbox = QCheckBox()
        self.select_all_steps_checkbox.setFont(QFont("Arial", 9)) # Đồng bộ font
        # self.select_all_steps_checkbox.setText("Tất cả") # Sẽ đặt text trong retranslate_ui
        steps_layout_container.addWidget(self.select_all_steps_checkbox)
        steps_layout_container.addStretch()
        details_layout.addLayout(steps_layout_container)
        self.step_checkboxes = {}
        self.step_buttons_container_layout = QHBoxLayout()
        step_keys_map = {"step2": "screen2_step2", "step3": "screen2_step3", "step4": "screen2_step4", "step5": "screen2_step5"}
        for int_key, lang_key in step_keys_map.items():
            cb = QCheckBox()
            cb.setFont(QFont("Arial", 9))
            cb.setObjectName(lang_key)
            self.step_buttons_container_layout.addWidget(cb)
            self.step_checkboxes[int_key] = cb
        details_layout.addLayout(self.step_buttons_container_layout)

        h_layout = QHBoxLayout()
        self.h_label = QLabel()
        h_layout.addWidget(self.h_label)
        h_layout.addStretch()
        details_layout.addLayout(h_layout)
        self.h_button_group = QButtonGroup(self)
        self.h_button_group.setExclusive(True)
        h_values = ["0.1", "0.05", "0.01", "0.005","0.001"]
        self.h_radio_buttons = {}
        h_radio_layout = QHBoxLayout()
        for val in h_values:
            rb = QRadioButton(val)
            rb.setFont(QFont("Arial", 9))
            self.h_button_group.addButton(rb)
            h_radio_layout.addWidget(rb)
            self.h_radio_buttons[val] = rb
        if "0.01" in self.h_radio_buttons:
            self.h_radio_buttons["0.01"].setChecked(True)
        details_layout.addLayout(h_radio_layout)

        #self.show_simulation_checkbox = QCheckBox()
        #self.show_simulation_checkbox.setFont(QFont("Arial", 9))
        #details_layout.addWidget(self.show_simulation_checkbox)
        left_layout.addWidget(self.details_group) # Giảm font sim toggle

        self.params_group = QGroupBox()
        self.params_form_layout = QFormLayout(self.params_group)
        #self.params_form_layout = None
        self.params_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.params_form_layout.setHorizontalSpacing(10)
        self.params_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.params_form_layout.setSpacing(0)
        left_layout.addWidget(self.params_group) # Giảm spacing form

        self.action_buttons_group = QGroupBox()
        buttons_layout = QGridLayout(self.action_buttons_group)
        buttons_layout.setSpacing(7) # Giảm spacing nút
        self.btn_initialize = QPushButton()
        self.btn_initialize.setObjectName("btn_initialize")
        self.btn_initialize.setFont(QFont("Arial", 10, QFont.Weight.Bold)) # Tăng đậm nút chính
        self.btn_refresh_data = QPushButton()
        self.btn_refresh_data.setFont(QFont("Arial", 9)) # Giảm font nút phụ
        self.btn_show_data = QPushButton()
        self.btn_show_data.setFont(QFont("Arial", 9))
        self.btn_save_data = QPushButton()
        self.btn_save_data.setFont(QFont("Arial", 9))
        buttons_layout.addWidget(self.btn_initialize, 0, 0, 1, 2)
        buttons_layout.addWidget(self.btn_refresh_data, 1, 0)
        buttons_layout.addWidget(self.btn_show_data, 1, 1)
        buttons_layout.addWidget(self.btn_save_data, 2, 0, 1, 2)
        left_layout.addWidget(self.action_buttons_group)

        left_layout.addWidget(self.method_group, 1)
        left_layout.addWidget(self.details_group, 2)
        left_layout.addWidget(self.params_group, 3)
        left_layout.addWidget(self.action_buttons_group, 1)

        # --- Right Panel (Plots) ---
        right_panel = QWidget()
        right_layout = QGridLayout(right_panel)
        right_layout.setVerticalSpacing(2.5)
        #right_layout.setSpacing(15);
        right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_panel.setStyleSheet("background-color: #ffffff; border: 1px solid #cccccc; border-radius: 5px;")
        content_layout.addWidget(right_panel, 3) # *** THAY ĐỔI Stretch: Right=2 ***
        #right_panel.setFixedHeight(600)

        self.canvas_solution = MplCanvas(self)
        self.canvas_error = MplCanvas(self)
        self.canvas_error_order = MplCanvas(self)
        plot_title_style = "QLabel { color: black; font-weight: bold; padding: 3px; background-color:#f0f0f0; border-bottom: 1px solid #ccc;}" # Giảm padding label plot
        self.label_sol = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_sol.setStyleSheet(plot_title_style)
        self.label_err = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_err.setStyleSheet(plot_title_style)
        self.label_ord = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_ord.setStyleSheet(plot_title_style)

        # ================== HIGHLIGHT START: Nested Layout Approach ==================
        # Sắp xếp Grid:
        # Row 0: Tiêu đề Nghiệm (0,0) | Tiêu đề Lỗi (0,1)
        # Row 1: Đồ thị Nghiệm (1,0) | Đồ thị Lỗi (1,1)
        # Row 2: Tiêu đề Bậc   (2,0) | **Nested Widget Container (2,1, span 2 rows)**
        # Row 3: Đồ thị Bậc    (3,0) | (Spanned by Nested Widget)

        # Thêm các widget chính vào grid
        right_layout.addWidget(self.label_sol, 0, 0)
        right_layout.addWidget(self.label_err, 0, 1)
        right_layout.addWidget(self.canvas_solution, 1, 0)
        right_layout.addWidget(self.canvas_error, 1, 1)
        right_layout.addWidget(self.label_ord, 2, 0)      # Title convergence plot
        right_layout.addWidget(self.canvas_error_order, 3, 0) # Convergence plot

        # --- Tạo Container Widget cho cột phải, phần dưới ---
        self.right_col_lower_widget = QWidget() # Đổi tên biến để rõ ràng hơn
        right_col_lower_layout = QVBoxLayout(self.right_col_lower_widget)
        self.right_col_lower_widget.setStyleSheet("border: none;")
        right_col_lower_layout.setContentsMargins(0, 0, 0, 0) # Không cần margin/padding nội bộ cho container này
        right_col_lower_layout.setSpacing(2) # Khoảng cách nhỏ giữa legend và info area

        # --- Khởi tạo Legend Container (như cũ nhưng thêm SizePolicy) ---
        self.method_legend_container = QWidget()
        self.method_legend_container.setObjectName("methodLegendContainer")
        self.method_legend_container.setStyleSheet("""
            QWidget#methodLegendContainer {
                background-color: #f8f8f8;
                border: 1px solid #dddddd;
                border-radius: 4px;
                padding: 2px 5px;
            }
        """)
        # *** Quan trọng: Set SizePolicy cho legend container ***
        legend_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred) # Ngang giãn, dọc vừa đủ
        self.method_legend_container.setSizePolicy(legend_policy)

        self.method_legend_layout = QHBoxLayout(self.method_legend_container)
        self.method_legend_layout.setContentsMargins(5, 5, 5, 0)
        self.method_legend_layout.setSpacing(8)
        self.method_legend_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.method_legend_container.setVisible(False) # Ẩn ban đầu

        # --- Khởi tạo Info Text Area (như cũ nhưng thêm SizePolicy) ---
        self.info_text_area = QTextEdit()
        self.info_text_area.setReadOnly(True)
        self.info_text_area.setFont(QFont("Consolas", 9))
        self.info_text_area.setStyleSheet("border: 1px solid #dddddd;")
        # Info area nên co giãn cả ngang và dọc
        info_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.info_text_area.setSizePolicy(info_policy)


        # --- Thêm Legend và Info Area vào Layout của Container Widget ---
        right_col_lower_layout.addWidget(self.method_legend_container, 0) # Legend không co giãn dọc (stretch 0)
        right_col_lower_layout.addWidget(self.info_text_area, 1)          # Info area co giãn dọc (stretch 1)

        # --- Thêm Container Widget vào Grid Layout chính ---
        # Bắt đầu từ hàng 2, cột 1, kéo dài 2 hàng (rows 2 & 3), 1 cột
        right_layout.addWidget(self.right_col_lower_widget, 2, 1, 2, 1) # row=2, col=1, rowSpan=2, colSpan=1

        # --- Điều chỉnh stretch factors cho Grid Layout chính ---
        right_layout.setRowStretch(0, 0) # Hàng tiêu đề sol/err
        right_layout.setRowStretch(1, 1) # Hàng đồ thị sol/err (chiếm không gian chính - stretch 2)
        right_layout.setRowStretch(2, 0) # Hàng tiêu đề ord / Bắt đầu nested widget
        right_layout.setRowStretch(3, 1) # Hàng đồ thị ord / Tiếp tục nested widget (cho info area co giãn - stretch 1)

        right_layout.setColumnStretch(0, 1) # Cột trái (đồ thị)
        right_layout.setColumnStretch(1, 1) # Cột phải (đồ thị/nested widget)
        # ================== HIGHLIGHT END ==================

    def _clear_layout(self, layout):
        """Xóa tất cả các widget và layout con khỏi một layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0) # Lấy item đầu tiên ra khỏi layout
                widget = item.widget()
                if widget is not None:
                    # Set parent=None TRƯỚC KHI gọi deleteLater
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        # Đệ quy để xóa nội dung của layout con
                        self._clear_layout(sub_layout)

    def matplotlib_color_to_qt_rgb_string(self, mpl_color):
        """Chuyển đổi màu Matplotlib (ví dụ: tuple RGBA 0-1) sang chuỗi 'rgb(r,g,b)' cho Qt."""
        try:
            # Matplotlib thường trả về tuple RGBA (hoặc RGB) trong khoảng 0-1
            r, g, b = int(mpl_color[0] * 255), int(mpl_color[1] * 255), int(mpl_color[2] * 255)
            return f"rgb({r},{g},{b})"
        except (IndexError, TypeError, ValueError): # Thêm ValueError phòng trường hợp màu không hợp lệ
            # Nếu không phải định dạng mong đợi, trả về màu mặc định (đen)
            print(f"Warning: Could not convert color {mpl_color}, using black.")
            return "rgb(0,0,0)"

    def _update_method_legend(self, results_dict, method_short, colors):
        """Cập nhật nội dung cho ô legend - 2 dòng, căn chỉnh bậc."""
        print("--- Attempting to update legend (2 Lines, Aligned Order) ---")

        container = self.method_legend_container
        layout = self.method_legend_layout

        if not all([container, layout]):
             print("Error: Legend layout or container not initialized.")
             return

        self._clear_layout(layout)
        print("  Cleared previous legend layout content.")

        has_data = bool(results_dict) and colors is not None and (not isinstance(colors, np.ndarray) or colors.size > 0)
        print(f"  Legend has_data: {has_data}")

        if not has_data:
            container.setVisible(False)
            print("  No data for legend, hiding container.")
            return

        # --- Định nghĩa chung ---
        font_legend = QFont("Arial", 8)
        font_title = QFont("Arial", 8, QFont.Weight.Bold) # Font riêng cho title
        line_width = 18  # Swatch width
        line_height = 2   # Swatch height
        item_spacing = 3  # Space between swatch and label text
        entry_group_spacing = 8 # Space between B2 group and B3 group

        # --- 1. Tạo và thêm khối Title (Vertical) ---
        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(0) # Khoảng cách nhỏ giữa 2 dòng title
        title_vbox.setContentsMargins(0, 2, 5, 2)

        legend_title_label = QLabel(self.tr("screen2_legend_title")) # "Chú thích:"
        legend_title_label.setFont(font_title)
        legend_title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        legend_title_label.setStyleSheet("border: none; background: transparent;")
        title_vbox.addWidget(legend_title_label)

        order_title_label = QLabel(self.tr("screen2_legend_order_title")) # <<< Key dịch mới "Bậc:"
        order_title_label.setFont(font_title)
        order_title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        order_title_label.setStyleSheet("border: none; background: transparent;")
        title_vbox.addWidget(order_title_label)

        # Thêm khối title vào layout chính (QHBoxLayout)
        layout.addLayout(title_vbox)
        print("  Added Title VBox")

        # --- 2. Lặp qua các bước để tạo Entry Blocks ---
        sorted_steps = sorted(results_dict.keys())
        legend_items_added = False
        color_idx = 0
        max_entry_height = 0 # Theo dõi chiều cao lớn nhất của một entry

        for i, step in enumerate(sorted_steps):
            method_base_text = f"A{method_short[0]}{step}"
            current_color_mpl = colors[color_idx % len(colors)]
            current_color_qt = self.matplotlib_color_to_qt_rgb_string(current_color_mpl)

            # Lấy slope
            res = results_dict.get(step, {})
            slope = res.get("order_slope", np.nan)

            # --- Tạo khối VBox cho Entry này ---
            entry_vbox = QVBoxLayout()
            entry_vbox.setSpacing(0) # Khoảng cách nhỏ giữa dòng swatch/name và dòng order
            entry_vbox.setContentsMargins(0, 2, 0, 2)

            # --- Dòng 1: Swatch + Method Name (QHBoxLayout) ---
            line1_hbox = QHBoxLayout()
            line1_hbox.setSpacing(item_spacing) # Khoảng cách giữa swatch và name
            line1_hbox.setContentsMargins(0, 0, 0, 0)

            # Swatch
            line_swatch = QLabel()
            line_swatch.setFixedSize(line_width, line_height)
            # *** HIGHLIGHT: Đảm bảo swatch chỉ có background ***
            line_swatch.setStyleSheet(f"background-color: {current_color_qt}; border: none;")
            line1_hbox.addWidget(line_swatch, 0, Qt.AlignmentFlag.AlignVCenter)
            # Method Name Label
            name_label = QLabel(method_base_text)
            name_label.setFont(font_legend)
            name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            name_label.setStyleSheet("border: none; background: transparent; padding: 0px 2px;")
            line1_hbox.addWidget(name_label, 1) # Cho phép label co giãn nếu cần
            line1_hbox.addStretch(0) # Đẩy về bên trái trong hbox này

            entry_vbox.addLayout(line1_hbox) # Thêm dòng 1 vào VBox của entry

            # --- Dòng 2: Spacer + Order Value (QHBoxLayout) ---
            line2_hbox = QHBoxLayout()
            line2_hbox.setSpacing(item_spacing) # Giữ spacing giống dòng 1 (cho spacer)
            line2_hbox.setContentsMargins(0, 0, 0, 0)

            # Spacer để căn lề (rộng bằng swatch + spacing)
            indent_spacer_width = line_width # Chỉ cần rộng bằng swatch là đủ để chữ Bậc nằm dưới chữ B2
            indent_spacer = QSpacerItem(indent_spacer_width, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed) # Cao 1 pixel là đủ
            line2_hbox.addSpacerItem(indent_spacer)

            # Order Value Label
            order_text = ""
            if np.isfinite(slope):
                # Dùng key dịch cũ nhưng bỏ dấu ngoặc đi nếu muốn
                order_format_str = "{:.4f}" # Chỉ hiển thị số
                order_text = order_format_str.format(slope)
            else:
                order_text = "N/A" # Hoặc để trống ""

            order_label = QLabel(order_text)
            order_label.setFont(font_legend)
            order_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            # Đặt chiều rộng tối thiểu để tránh bị co quá nếu text ngắn
            order_label.setMinimumWidth(name_label.fontMetrics().horizontalAdvance(method_base_text) + 5)
            order_label.setStyleSheet("border: none; background: transparent; padding: 0px 2px;")
            line2_hbox.addWidget(order_label, 1) # Cho phép label co giãn
            line2_hbox.addStretch(0) # Đẩy về bên trái

            entry_vbox.addLayout(line2_hbox) # Thêm dòng 2 vào VBox của entry

            # --- Thêm Spacer ngang LỚN vào layout chính TRƯỚC entry này (trừ cái đầu tiên sau title) ---
            if i == 0: # Spacer giữa Title và Entry đầu tiên
                 layout.addSpacerItem(QSpacerItem(entry_group_spacing, 1, QSizePolicy.Policy.Fixed))
            elif i > 0: # Spacer giữa các Entry
                 layout.addSpacerItem(QSpacerItem(entry_group_spacing, 1, QSizePolicy.Policy.Fixed))

            # --- Thêm VBox của entry này vào layout chính ---
            layout.addLayout(entry_vbox)
            print(f"    Added Entry VBox for {method_base_text}")
            legend_items_added = True
            color_idx += 1


        # --- Thêm Stretch cuối cùng vào layout chính ---
        layout.addStretch(1)
        print("  Added final stretch")

        # --- Hiển thị container và đặt chiều cao ---
        # --- Cập nhật visibility và yêu cầu tính toán lại layout ---
        if legend_items_added:
            container.setVisible(True)
            print("  Container visibility set to: True")
            # *** BỎ HOÀN TOÀN VIỆC SET CHIỀU CAO CỐ ĐỊNH/TỐI THIỂU Ở ĐÂY ***
            # Yêu cầu container tự tính lại kích thước đề xuất
            container.adjustSize()
            # Yêu cầu layout cha (QVBoxLayout) và widget chứa nó cập nhật
            if self.right_col_lower_widget:
                 # Invalidate layout để nó tính toán lại dựa trên size hint mới của legend
                 self.right_col_lower_widget.layout().invalidate()
                 # Yêu cầu widget cập nhật geometry của nó (kích hoạt lại layout)
                 self.right_col_lower_widget.updateGeometry()
                 print(f"  Requested geometry update for right_col_lower_widget.")

        else:
             container.setVisible(False)
             print("  No legend items added, hiding container.")
             # Cũng nên cập nhật layout cha khi ẩn legend
             if self.right_col_lower_widget:
                  self.right_col_lower_widget.layout().invalidate()
                  self.right_col_lower_widget.updateGeometry()


        print("--- Legend update finished (Nested Layout) ---")

    def _setup_initial_plots(self):
        plot_info = [
            (self.canvas_solution,self.tr("screen2_plot_t_axis"), self.tr("screen2_plot_value_axis"), 'linear', 'linear', False),
            (self.canvas_error, self.tr("screen2_plot_n_axis"), self.tr("screen2_plot_error_axis"), 'linear', 'log', False),
            (self.canvas_error_order, self.tr("screen2_plot_log_h_axis"), self.tr("screen2_plot_log_error_axis"), 'linear', 'linear', False)
        ]
        axis_label_fs = 7 # Giảm font label trục
        tick_label_fs = 7 # Giảm font số trên trục

        for canvas, xlabel_key, ylabel_key, xscale, yscale, invert_x in plot_info:
            ax = canvas.axes
            ax.clear()
            xlabel = self.tr(xlabel_key, xlabel_key) # Lấy text từ key dịch
            ylabel = self.tr(ylabel_key, ylabel_key) # Lấy text từ key dịch
            ax.set_xlabel(xlabel, fontsize=axis_label_fs)#labelpad=-0.2
            ax.set_ylabel(ylabel, fontsize=axis_label_fs)
            ax.grid(True, linestyle=':', alpha=0.7, which='major')
            ax.set_xscale(xscale) # Đặt scale X
            ax.set_yscale(yscale) # Đặt scale Y

            # Bật grid phụ nếu có trục log
            #if xscale == 'log' or yscale == 'log':
            #     ax.grid(True, which='minor', linestyle=':', alpha=0.3)
            # Đảo trục x chỉ khi được yêu cầu (không cần cho N hoặc log(h))
            # if invert_x:
            #    ax.invert_xaxis() # Bỏ invert cho N và log(h)

            ax.tick_params(axis='both', which='major', labelsize=tick_label_fs)
            try:
                canvas.fig.tight_layout(pad=0.8)
            except ValueError:
                print(f"Warning: tight_layout failed during initial setup for canvas of '{xlabel}'.")
            canvas.draw()
        # *** HIGHLIGHT END ***
        if hasattr(self, 'method_legend_container') and hasattr(self, 'method_legend_layout'):
             self.method_legend_container.setVisible(False) # Ẩn container
             # Gọi _clear_layout phiên bản đơn giản
             self._clear_layout(self.method_legend_layout)
    
    @Slot(int) 
    def _toggle_go_to_screen3_button(self, state):
        """Hiện hoặc ẩn nút 'Xem Đồ thị động' dựa vào checkbox."""
        # state có thể là Qt.CheckState.Checked (2) hoặc Qt.CheckState.Unchecked (0)
        # Cần import Qt từ PySide6.QtCore nếu chưa có: from PySide6.QtCore import Qt
        is_checked = (state == Qt.CheckState.Checked.value) # So sánh với giá trị của enum

        print(f"Checkbox state changed: {'Checked' if is_checked else 'Unchecked'}. Button visibility: {is_checked}")
        # Đảm bảo nút self.btn_go_to_screen3 đã được tạo trong _init_ui
        if hasattr(self, 'btn_go_to_screen3'):
            self.btn_go_to_screen3.setVisible(is_checked)

            # Quan trọng: Khi ẩn nút đi, cũng nên reset dữ liệu và vô hiệu hóa nó luôn
            if not is_checked:
                self.btn_go_to_screen3.setEnabled(False)
                self.dynamic_plot_data = None
        else:
            print("Warning: btn_go_to_screen3 does not exist when trying to toggle visibility.")
    
    def _connect_signals(self):
        self.btn_back.clicked.connect(self._go_back_to_screen1)
        #self.show_simulation_checkbox.stateChanged.connect(self._toggle_go_to_screen3_button)
        self.btn_go_to_screen3.clicked.connect(self._go_to_screen3_dynamic)
        self.method_button_group.buttonToggled.connect(self._update_method_details_options)
        self.btn_initialize.clicked.connect(self._run_simulation_and_plot)
        self.btn_refresh_data.clicked.connect(self._refresh_data)
        self.btn_save_data.clicked.connect(self._save_data)
        self.btn_show_data.clicked.connect(self._show_data)
        if self.select_all_steps_checkbox: # Kiểm tra nếu widget đã được tạo
            self.select_all_steps_checkbox.stateChanged.connect(self._toggle_all_steps)

        # (Tùy chọn) Kết nối tín hiệu của các checkbox con để cập nhật "Chọn tất cả"
        for cb in self.step_checkboxes.values():
            cb.stateChanged.connect(self._update_select_all_checkbox_status)
    
    @Slot(int)
    def _toggle_all_steps(self, state):
        """Khi checkbox 'Chọn tất cả' thay đổi trạng thái."""
        if not self.select_all_steps_checkbox.signalsBlocked(): # Chỉ xử lý nếu không bị block
            should_check_all = False
            if state == Qt.CheckState.Checked.value:
                should_check_all = True
            elif state == Qt.CheckState.Unchecked.value:
                should_check_all = False
            elif state == Qt.CheckState.PartiallyChecked.value: # Người dùng nhấp vào ô vuông đen
                # Quyết định: khi nhấp vào PartiallyChecked, nên chuyển thành Checked hay Unchecked?
                # Thông thường, người ta mong muốn nó chuyển thành Checked.
                should_check_all = True 
                # Cập nhật lại trạng thái của chính checkbox "All" thành Checked
                self.select_all_steps_checkbox.blockSignals(True)
                self.select_all_steps_checkbox.setCheckState(Qt.CheckState.Checked)
                self.select_all_steps_checkbox.blockSignals(False)

            print(f"_toggle_all_steps: User clicked. New state from signal: {state}. Decided should_check_all: {should_check_all}")
            for cb in self.step_checkboxes.values():
                if cb.isVisible(): # Chỉ tác động đến các checkbox đang hiển thị
                    cb.blockSignals(True)
                    cb.setChecked(should_check_all)
                    cb.blockSignals(False)
    
    @Slot()
    def _update_select_all_checkbox_status(self):
        """Cập nhật trạng thái của checkbox 'Chọn tất cả' dựa trên các checkbox con."""
        sender_widget = self.sender()
        if sender_widget is not None and sender_widget.signalsBlocked():
            return 
        
        if not hasattr(self, 'step_checkboxes') or not self.step_checkboxes: 
            if hasattr(self, 'select_all_steps_checkbox') and self.select_all_steps_checkbox:
                self.select_all_steps_checkbox.blockSignals(True)
                self.select_all_steps_checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.select_all_steps_checkbox.blockSignals(False)
            return

        all_visible_children_checked = True
        no_visible_children = True

        for cb in self.step_checkboxes.values():
            if cb.isVisible():
                no_visible_children = False # Đã tìm thấy ít nhất một checkbox con hiển thị
                if not cb.isChecked():
                    all_visible_children_checked = False
                    break # Chỉ cần một cái không check là đủ để "All" không phải là checked

        if not hasattr(self, 'select_all_steps_checkbox') or not self.select_all_steps_checkbox:
            return

        self.select_all_steps_checkbox.blockSignals(True)
        if no_visible_children: # Nếu không có checkbox con nào hiển thị
            self.select_all_steps_checkbox.setCheckState(Qt.CheckState.Unchecked)
            print("_update_select_all_checkbox_status: No visible children, setting 'All' to Unchecked.")
        elif all_visible_children_checked:
            self.select_all_steps_checkbox.setCheckState(Qt.CheckState.Checked)
            print("_update_select_all_checkbox_status: All visible children are checked, setting 'All' to Checked.")
        else: # Nếu có ít nhất một con không được check (và có con hiển thị)
            self.select_all_steps_checkbox.setCheckState(Qt.CheckState.Unchecked)
            print("_update_select_all_checkbox_status: Not all visible children are checked, setting 'All' to Unchecked.")
        self.select_all_steps_checkbox.blockSignals(False)
    
    def retranslate_ui(self):
        # Assuming 'screen2_base_title' exists in translations or provide default
        base_title = self.tr("screen2_base_title", "Simulation") # Add default text
        model_name_key = self.current_model_data.get('id', '') + "_name"
        current_model_name_tr = self.tr(model_name_key, default_text=self.current_model_vi_key or "N/A")
        self.model_title_label.setText(f"{base_title}: {current_model_name_tr}") # Use f-string
        self.btn_back.setText(self.tr("screen2_back_button"))
        self.method_group.setTitle(self.tr("screen2_method_group"))
        self.rb_adams_bashforth.setText(self.tr("screen2_method_ab"))
        self.rb_adams_moulton.setText(self.tr("screen2_method_am"))
        self.steps_label.setText(self.tr("screen2_steps_label"))
        if self.select_all_steps_checkbox: # Kiểm tra widget tồn tại
            self.select_all_steps_checkbox.setText(self.tr("screen2_select_all_steps_cb"))
        for cb in self.step_checkboxes.values():
            lang_key = cb.objectName()
            cb.setText(self.tr(lang_key))
        self.h_label.setText(self.tr("screen2_h_label"))
        #self.show_simulation_checkbox.setText(self.tr("screen2_sim_toggle"))
        self.params_group.setTitle(self.tr("screen2_params_group"))
        self.action_buttons_group.setTitle(self.tr("screen2_actions_group"))
        self.btn_initialize.setText(self.tr("screen2_init_button"))
        self.btn_refresh_data.setText(self.tr("screen2_refresh_button"))
        self.btn_show_data.setText(self.tr("screen2_show_data_button"))
        self.btn_save_data.setText(self.tr("screen2_save_button"))
        self.label_sol.setText(self.tr("screen2_plot_solution_title"))
        self.label_err.setText(self.tr("screen2_plot_error_title"))
        self.label_ord.setText(self.tr("screen2_plot_order_title"))
        self.btn_go_to_screen3.setText(self.tr("screen2_goto_screen3_button"))
        self.btn_go_to_screen3.setToolTip(self.tr("screen2_goto_screen3_tooltip"))
        self.info_text_area.setPlaceholderText(self.tr("screen2_info_area_init"))
        self._retranslate_parameter_labels()
        if self.calculated_c_label_widget:
             self.calculated_c_label_widget.setText(self.tr("model2_calculated_c_label"))
        if self.calculated_c_display_widget and not self.calculated_c_display_widget.text(): # Chỉ đặt lại placeholder nếu trống
             self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A", "N/A"))
        if self.calculated_r_label_widget: # Thêm cho r
            self.calculated_r_label_widget.setText(self.tr("model3_calculated_r_label"))
        if self.calculated_r_display_widget and not self.calculated_r_display_widget.text(): # Thêm cho r
            self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A", "N/A"))
        if self.calculated_steady_state_label_widget:
            self.calculated_steady_state_label_widget.setText(self.tr("model4_steady_label_short"))
        if self.calculated_steady_state_display_widget and not self.calculated_steady_state_display_widget.text():
            self.calculated_steady_state_display_widget.setPlaceholderText(self.tr("N/A", "N/A"))
        self._update_method_details_options()
        self._setup_initial_plots()
        super().retranslate_ui()

    def _retranslate_parameter_labels(self):
        current_layout = self.params_group.layout() # Lấy layout hiện tại đã được gán trong set_model
        if not current_layout or not self.current_model_data:
             print("Retranslate params: No current layout or model data.")
             return
        model_id = self.current_model_data.get("id") 
        internal_keys_input = self.current_model_data.get("internal_param_keys", [])
        current_lang = self.main_window.current_language
        param_labels_key = f"param_keys_{current_lang}"
        param_labels = self.current_model_data.get(param_labels_key, self.current_model_data.get("param_keys_vi", []))
        internal_key_to_label = {}
        if model_id == "model4":
            label_map_m4 = { # Lấy lại map từ set_model hoặc định nghĩa lại ở đây
                "m": self.tr("model4_param_m"), "l": self.tr("model4_param_l"),
                "a": self.tr("model4_param_a"), "s": self.tr("model4_param_s"),
                "G": self.tr("model4_param_G"), "alpha": self.tr("model4_param_alpha"),
                "beta": self.tr("model4_param_beta"), "dY0": self.tr("model4_param_dY0"),
                "Y0": self.tr("model4_param_Y0"), "t₀": self.tr("model4_param_t0"),
                "t₁": self.tr("model4_param_t1"),
            }
            internal_key_to_label = label_map_m4 # Dùng map này cho model 4
        elif len(param_labels) == len(internal_keys_input): # Các model khác
            internal_key_to_label = dict(zip(internal_keys_input, param_labels))
        else:
            print(f"Warning: Mismatch between param_labels and internal_keys for retranslation (Model {model_id}).")
            return

        print(f"Retranslating labels for layout type: {type(current_layout).__name__} (Model {model_id})")
        
         # ================== HIGHLIGHT START: Xử lý theo loại layout ==================
        if isinstance(current_layout, QFormLayout):
         for i in range(current_layout.rowCount()):
             try:
                 label_item = current_layout.itemAt(i, QFormLayout.ItemRole.LabelRole)
                 field_item = current_layout.itemAt(i, QFormLayout.ItemRole.FieldRole)
                 if label_item and label_item.widget() and field_item and field_item.widget():
                     label_widget = label_item.widget()
                     field_widget = field_item.widget()
                     if label_widget in [self.calculated_c_label_widget, self.calculated_r_label_widget, self.component_selector_label]: continue
                     found_key = None
                     for key, widget in self.param_inputs.items():
                         if widget == field_widget: found_key = key; break
                     if found_key in internal_key_to_label: # Dùng map của model hiện tại
                             label_widget.setText(f"{internal_key_to_label[found_key]}:")
             except Exception as e_retrans_form:
                  print(f"Error retranslating FormLayout row {i}: {e_retrans_form}")

        elif isinstance(current_layout, QGridLayout):
             processed_labels = set() # Tránh xử lý cùng một label nhiều lần
             for i in range(current_layout.count()):
                item = current_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QLineEdit): # Tìm field trước
                        found_key = None
                        # Xác định field này là input hay display
                        is_input_field = False
                        if widget in self.param_inputs.values(): # Là ô nhập
                            for key, input_widget in self.param_inputs.items():
                                if input_widget == widget:
                                    found_key = key
                                    is_input_field = True
                                    break
                        elif widget == self.calculated_alpha_display_widget:
                            found_key = 'alpha'
                        elif widget == self.calculated_beta_display_widget:
                            found_key = 'beta'

                        if found_key:
                            try:
                                row, col, _, _ = current_layout.getItemPosition(i)
                                # Tìm label ở cột bên trái (col - 1)
                                label_item = current_layout.itemAtPosition(row, col - 1)
                                if label_item and label_item.widget() and isinstance(label_item.widget(), QLabel) and label_item.widget() not in processed_labels:
                                    target_label_map = internal_key_to_label # Dùng map đã tạo ở đầu hàm
                                    if found_key in target_label_map:
                                        label_item.widget().setText(f"{target_label_map[found_key]}:")
                                        processed_labels.add(label_item.widget()) # Đánh dấu đã xử lý
                                    else:
                                        print(f"Warning: Key '{found_key}' not in label map during retranslation.")
                            except Exception as e_retrans_grid:
                                print(f"Error retranslating GridLayout for key {found_key}: {e_retrans_grid}")

        # --- Dịch các label tính toán (model 2, 3) ---
        if self.calculated_c_label_widget:
            self.calculated_c_label_widget.setText(self.tr("model2_calculated_c_label"))
        if self.calculated_r_label_widget:
            self.calculated_r_label_widget.setText(self.tr("model3_calculated_r_label"))
        if model_id == "model5":
            if hasattr(self, 'rb_component_x') and self.rb_component_x:
                self.rb_component_x.setText(self.tr("model5_component_x"))
            if hasattr(self, 'rb_component_y') and self.rb_component_y:
                self.rb_component_y.setText(self.tr("model5_component_y"))
    
    @Slot()
    def _go_back_to_screen1(self):
        if self.simulation_window and self.simulation_window.isVisible():
            self.simulation_window.close()
        self.simulation_window = None
        self.main_window.switch_to_screen1()

    @Slot()
    def _update_method_details_options(self):
        checked_button = self.method_button_group.checkedButton()
        if not checked_button:
            return
        cb_5_steps = self.step_checkboxes.get("step5")
        if not cb_5_steps:
            return
        model_id = self.current_model_data.get("id")
        is_model5 = (model_id == "model5")
        if checked_button == self.rb_adams_bashforth:
            self.details_group.setTitle(self.tr("screen2_details_group_ab"))
            if not is_model5:
                cb_5_steps.show()
            else:
                cb_5_steps.hide() # Ẩn đi cho model 5
                if cb_5_steps.isChecked():
                    cb_5_steps.setChecked(False)
        elif checked_button == self.rb_adams_moulton:
            self.details_group.setTitle(self.tr("screen2_details_group_am"))
            cb_5_steps.hide()
            if cb_5_steps.isChecked():
                cb_5_steps.setChecked(False)
                cb4 = self.step_checkboxes.get("step4")
                # Simplified logic: just set step 4 if it exists and is visible
                if cb4 and cb4.isVisible():
                     cb4.setChecked(True)
                else: # Fallback: check the first available step below 5
                     for key, cb in self.step_checkboxes.items():
                         if key != "step5" and cb.isVisible():
                             cb.setChecked(True)
                             break
        self._update_select_all_checkbox_status()
        self.details_group.update()

    def set_model(self, model_vi_key):
        self.current_model_vi_key = model_vi_key
        self.current_model_data = MODELS_DATA.get(model_vi_key, {})
        model_id = self.current_model_data.get("id", "")
        #can_run_ode_dynamic_animation = (model_id == "model2" or model_id == "model3") # <<< THAY ĐỔI Ở ĐÂY
        # Đặt lại cờ: chỉ Model 2 có PTVP động hình tròn mặc định
        #can_run_model2_dynamic_plot = (model_id == "model2")

        # Kiểm tra ABM (Model 3 sẽ vào đây nếu ABM_AVAILABLE)
        #can_run_abm = self.current_model_data.get("can_run_abm_on_screen3", False) and ABM_AVAILABLE

    # Kiểm tra ABM (sẽ không còn đúng cho Model 3 nếu đã sửa MODELS_DATA)
        can_run_abm = self.current_model_data.get("can_run_abm_on_screen3", False) and ABM_AVAILABLE
        if hasattr(self, 'btn_go_to_screen3'):
            self.btn_go_to_screen3.setVisible(False)
            self.btn_go_to_screen3.setEnabled(False)
        #model_id = self.current_model_data.get("id", "")
        model_name_tr = self.tr(f"{model_id}_name", model_vi_key)
        self.model_title_label.setText(f"{model_name_tr}") # Consider adding base title here too if needed
        # Clear previous param inputs
        print("Clearing old calculated/selector widgets...")
        widgets_to_clear = [
            'calculated_c_label_widget', 'calculated_c_display_widget',
            'calculated_r_label_widget', 'calculated_r_display_widget',
            # <<< HIGHLIGHT START: Thêm alpha/beta display vào danh sách xóa >>>
            'calculated_alpha_label_widget', 'calculated_alpha_display_widget',
            'calculated_beta_label_widget', 'calculated_beta_display_widget',
            # 'calculated_steady_state_label_widget', 'calculated_steady_state_display_widget', # Xóa steady state
            # <<< HIGHLIGHT END >>>
            'component_selector_label', 'component_selector_widget',
            'rb_component_x', 'rb_component_y'
        ]
        if hasattr(self, 'component_button_group') and self.component_button_group:
            # Không cần xóa group trực tiếp, Qt sẽ quản lý khi không còn widget nào tham chiếu
            self.component_button_group = None
        for attr_name in widgets_to_clear:
            widget = getattr(self, attr_name, None)
            if widget:
                # Quan trọng: Gỡ widget khỏi layout trước khi xóa
                layout = widget.parentWidget().layout() if widget.parentWidget() else None
                if layout:
                    layout.removeWidget(widget)
                widget.deleteLater()
                setattr(self, attr_name, None) # Reset thuộc tính

        # Reset giá trị lưu trữ
        self._last_calculated_c = None
        self._last_calculated_r = None
        self._last_calculated_alpha = None
        self._last_calculated_beta = None

        old_layout = self.params_group.layout()
        if old_layout is not None:
            print(f"Clearing old layout ({type(old_layout).__name__}) from params_group...")
            # Xóa sạch nội dung bên trong layout cũ
            self._clear_layout(old_layout)
            # Quan trọng: Gỡ layout cũ ra khỏi QGroupBox
            # Cách 1: Dùng widget tạm
            # QWidget().setLayout(old_layout)
            # Cách 2: Set layout của group thành None (an toàn hơn)
            QWidget().setLayout(old_layout)
            # Bây giờ có thể xóa đối tượng layout cũ nếu muốn (Qt thường tự quản lý khi set layout mới)
            # old_layout.deleteLater() # Thử thêm dòng này nếu cách trên vẫn lỗi
            print("Old layout cleared and detached.")
        else:
            print("No old layout found in params_group.")
        self.param_inputs.clear() # Xóa tham chiếu widget


         # --- Get parameter lists (unchanged) ---
        param_labels_key = f"param_keys_{self.main_window.current_language}"
        # Get ALL labels, including Beta's, for display purposes
        all_param_labels = self.current_model_data.get(param_labels_key, self.current_model_data.get("param_keys_vi", []))
        # Get only the keys for ACTUAL user inputs
        input_internal_keys = self.current_model_data.get("internal_param_keys", [])

        # --- Tạo layout và thêm widget dựa trên model_id ---
        new_layout = None
        if model_id == "model4":
            # <<< HIGHLIGHT START: Sử dụng QGridLayout cho Model 4 >>>
            grid_layout = QGridLayout()
            grid_layout.setHorizontalSpacing(15) # Khoảng cách ngang giữa các cột
            grid_layout.setVerticalSpacing(5)   # Khoảng cách dọc giữa các hàng
            # grid_layout.setContentsMargins(5, 5, 5, 5) # Thêm padding nếu cần

            label_map = {
                "m": self.tr("model4_param_m"),
                "l": self.tr("model4_param_l"),
                "a": self.tr("model4_param_a"), # Nhãn mới
                "s": self.tr("model4_param_s"), # Nhãn mới
                "G": self.tr("model4_param_G"),
                "alpha": self.tr("model4_param_alpha"), # Nhãn cho ô hiển thị
                "beta": self.tr("model4_param_beta"),   # Nhãn cho ô hiển thị
                "dY0": self.tr("model4_param_dY0"),
                "Y0": self.tr("model4_param_Y0"),
                "t₀": self.tr("model4_param_t0"),
                "t₁": self.tr("model4_param_t1"),
            }

            # Hàm trợ giúp tạo label và input/display
            def create_widget(key, is_input=True):
                lbl = QLabel(f"{label_map.get(key, key)}:")
                lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                lbl.setFont(QFont("Arial", 9))
                if is_input:
                    widget = QLineEdit()
                    widget.setFont(QFont("Arial", 9))
                    widget.setPlaceholderText(self.tr("param_placeholder", "..."))
                    self.param_inputs[key] = widget # Lưu tham chiếu ô nhập
                else: # Ô hiển thị
                    widget = QLineEdit()
                    widget.setFont(QFont("Arial", 9))
                    widget.setReadOnly(True)
                    widget.setStyleSheet("background-color: #f0f0f0; color: #555555; border: 1px solid #cccccc;")
                    widget.setPlaceholderText(self.tr("N/A", "N/A"))
                    # Lưu tham chiếu ô hiển thị vào self
                    if key == 'alpha': self.calculated_alpha_display_widget = widget
                    elif key == 'beta': self.calculated_beta_display_widget = widget
                return lbl, widget

            # --- Sắp xếp các widget theo layout mong muốn ---
            # Hàng 0: m, G
            lbl_m, input_m = create_widget('m')
            lbl_G, input_G = create_widget('G')
            grid_layout.addWidget(lbl_m, 0, 0)
            grid_layout.addWidget(input_m, 0, 1)
            grid_layout.addWidget(lbl_G, 0, 2)
            grid_layout.addWidget(input_G, 0, 3)

            # Hàng 1: l, a
            lbl_l, input_l = create_widget('l')
            lbl_a, input_a = create_widget('a') # Ô nhập a
            grid_layout.addWidget(lbl_l, 1, 0)
            grid_layout.addWidget(input_l, 1, 1)
            grid_layout.addWidget(lbl_a, 1, 2)
            grid_layout.addWidget(input_a, 1, 3)

            # Hàng 2: s (kéo dài), (trống)
            lbl_s, input_s = create_widget('s') # Ô nhập s
            grid_layout.addWidget(lbl_s, 2, 0)
            grid_layout.addWidget(input_s, 2, 1, 1, 3) # Kéo dài ô nhập s qua 3 cột

            # Hàng 3: alpha (display), beta (display) <-- Di chuyển lên trên Y', Y
            lbl_alpha, display_alpha = create_widget('alpha', is_input=False)
            lbl_beta, display_beta = create_widget('beta', is_input=False)
            self.calculated_alpha_label_widget = lbl_alpha # Lưu label alpha
            self.calculated_beta_label_widget = lbl_beta   # Lưu label beta
            grid_layout.addWidget(lbl_alpha, 3, 0)
            grid_layout.addWidget(display_alpha, 3, 1)
            grid_layout.addWidget(lbl_beta, 3, 2)
            grid_layout.addWidget(display_beta, 3, 3)

            # Hàng 4: Y'(t₀), Y(t₀)
            lbl_dY0, input_dY0 = create_widget('dY0')
            lbl_Y0, input_Y0 = create_widget('Y0')
            grid_layout.addWidget(lbl_dY0, 4, 0)
            grid_layout.addWidget(input_dY0, 4, 1)
            grid_layout.addWidget(lbl_Y0, 4, 2)
            grid_layout.addWidget(input_Y0, 4, 3)

            # Hàng 5: t₀, t₁
            lbl_t0, input_t0 = create_widget('t₀')
            lbl_t1, input_t1 = create_widget('t₁')
            grid_layout.addWidget(lbl_t0, 5, 0)
            grid_layout.addWidget(input_t0, 5, 1)
            grid_layout.addWidget(lbl_t1, 5, 2)
            grid_layout.addWidget(input_t1, 5, 3)

            # Set column stretches
            grid_layout.setColumnStretch(0, 1) # Cột label 1
            grid_layout.setColumnStretch(1, 2) # Cột input/display 1
            grid_layout.setColumnStretch(2, 1) # Cột label 2
            grid_layout.setColumnStretch(3, 2) # Cột input/display 2

            new_layout = grid_layout
        elif model_id == "model5":
            print(f"Creating QGridLayout for Model {model_id}")
            grid_layout = QGridLayout()
            grid_layout.setHorizontalSpacing(10)
            grid_layout.setVerticalSpacing(5)

            # Sắp xếp các key theo hàng mong muốn cho Model 5
            layout_config_m5 = [
                ('x0', 0, 0, 1), ('y0', 0, 2, 3),
                ('u',  1, 0, 1), ('v',  1, 2, 3),
                ('t₀', 2, 0, 1), ('t₁', 2, 2, 3),
            ]

            # Tạo map nhãn cho Model 5
            internal_key_to_label_m5 = {}
            if len(all_param_labels) == len(input_internal_keys):
                internal_key_to_label_m5 = dict(zip(input_internal_keys, all_param_labels))
            else:
                print(f"!!! Model 5 WARNING: Label/Key length mismatch!")

            # Thêm các trường input vào grid
            for key, row, col_lbl, col_fld in layout_config_m5:
                if key in input_internal_keys and key in internal_key_to_label_m5:
                    label_text = internal_key_to_label_m5[key]
                    line_edit = QLineEdit()
                    line_edit.setFont(QFont("Arial", 9))
                    line_edit.setPlaceholderText(self.tr("param_placeholder"))
                    param_label = QLabel(f"{label_text}:")
                    param_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    grid_layout.addWidget(param_label, row, col_lbl)
                    grid_layout.addWidget(line_edit, row, col_fld)
                    self.param_inputs[key] = line_edit
                else:
                    print(f"    !!! Key '{key}' NOT found in M5 input keys or label map!")

            # Thêm phần chọn Component (X/Y)
            self.component_button_group = QButtonGroup(self)
            self.rb_component_x = QRadioButton(self.tr("model5_component_x"))
            self.rb_component_y = QRadioButton(self.tr("model5_component_y"))
            self.rb_component_x.setFont(QFont("Arial", 9))
            self.rb_component_y.setFont(QFont("Arial", 9))

            self.component_button_group.addButton(self.rb_component_x)
            self.component_button_group.addButton(self.rb_component_y)
            self.rb_component_x.setChecked(True) # Mặc định chọn X

            component_radio_layout = QHBoxLayout()
            component_radio_layout.addWidget(self.rb_component_x)
            component_radio_layout.addWidget(self.rb_component_y)
            component_radio_layout.addStretch()

            # Thêm layout radio button vào grid ở hàng 3, cột 0, kéo dài 4 cột
            grid_layout.addLayout(component_radio_layout, 3, 0, 1, 4)

            # Điều chỉnh độ rộng cột cho Model 5
            grid_layout.setColumnStretch(0, 0) # Cột label 1 (hẹp)
            grid_layout.setColumnStretch(1, 1) # Cột input 1 (giãn)
            grid_layout.setColumnStretch(2, 0) # Cột label 2 (hẹp)
            grid_layout.setColumnStretch(3, 1) # Cột input 2 (giãn)

            new_layout = grid_layout # Gán layout mới
        else: # Các model khác dùng QFormLayout
            print(f"Creating QFormLayout for Model {model_id}")
            form_layout = QFormLayout() # Tạo layout mới
            form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
            form_layout.setHorizontalSpacing(10)
            form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
            form_layout.setSpacing(5)
            # <<< HIGHLIGHT END >>>

            if all_param_labels and len(all_param_labels) == len(input_internal_keys): # Use input_internal_keys here
                for i, label_text in enumerate(all_param_labels):
                    # Make sure we only add rows for actual inputs
                    internal_key = input_internal_keys[i]
                    line_edit = QLineEdit()
                    line_edit.setFont(QFont("Arial", 9))
                    placeholder = self.tr("param_placeholder", "Nhập giá trị số...")
                    line_edit.setPlaceholderText(placeholder)
                    param_label = QLabel(f"{label_text}:")
                    form_layout.addRow(param_label, line_edit)
                    self.param_inputs[internal_key] = line_edit

                if model_id == "model2":
                    # ... (add c widgets) ...
                    self.calculated_c_label_widget = QLabel(self.tr("model2_calculated_c_label"))
                    self.calculated_c_label_widget.setFont(QFont("Arial", 9))
                    self.calculated_c_display_widget = QLineEdit()
                    self.calculated_c_display_widget.setReadOnly(True)
                    self.calculated_c_display_widget.setFont(QFont("Arial", 9))
                    self.calculated_c_display_widget.setStyleSheet("background-color: #f0f0f0; color: #555555; border: 1px solid #cccccc;")
                    self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A", "N/A"))
                    form_layout.addRow(self.calculated_c_label_widget, self.calculated_c_display_widget)

                elif model_id == "model3":
                    # ... (add r widgets) ...
                    self.calculated_r_label_widget = QLabel(self.tr("model3_calculated_r_label"))
                    self.calculated_r_label_widget.setFont(QFont("Arial", 9))
                    self.calculated_r_display_widget = QLineEdit()
                    self.calculated_r_display_widget.setReadOnly(True)
                    self.calculated_r_display_widget.setFont(QFont("Arial", 9))
                    self.calculated_r_display_widget.setStyleSheet("background-color: #f0f0f0; color: #555555; border: 1px solid #cccccc;")
                    self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A", "N/A"))
                    form_layout.addRow(self.calculated_r_label_widget, self.calculated_r_display_widget)
            
            elif not input_internal_keys: # Check if there are no inputs needed
                no_param_label = QLabel(self.tr("no_params_text", "Model này không cần tham số đầu vào."))
                form_layout.addRow(no_param_label)
            else: # Mismatch or error
                error_label = QLabel(f"Lỗi cấu hình tham số Model {model_id}.")
                form_layout.addRow(error_label)
            new_layout = form_layout


        # --- Assign the new layout to the group box (Unchanged) ---
        if new_layout is not None:
            print(f"Setting new layout ({type(new_layout).__name__}) to params_group.")
            self.params_group.setLayout(new_layout)
            # Quan trọng: Cập nhật lại kích thước và hiển thị của params_group
            self.params_group.adjustSize()
            self.params_group.updateGeometry()
        else:
             print("Warning: No new layout was created.")

        if hasattr(self, 'method_group'): self.method_group.setVisible(True)
        if hasattr(self, 'details_group'): self.details_group.setVisible(True)
        if hasattr(self, 'canvas_solution'): self.canvas_solution.setVisible(True)
        if hasattr(self, 'canvas_abm_animation'): self.canvas_abm_animation.setVisible(False)
        # --- Reset các phần khác (Di chuyển xuống cuối) ---
        print("Resetting UI elements and data...")
        #if hasattr(self, 'show_simulation_checkbox'): # Đảm bảo checkbox tồn tại
        #    # Kiểm tra xem model hiện tại có hỗ trợ dynamic plot không
            # Nếu model không phải là model2 hoặc model3 (theo logic mới), thì không nên cho tick
        #    if model_id == "model2": # <<< CHỈ BẬT CHO MODEL 2
        #        self.show_simulation_checkbox.setEnabled(True)
        #        self.show_simulation_checkbox.setChecked(False) # Vô hiệu hóa luôn nếu không hỗ trợ
        #    else:
        #        self.show_simulation_checkbox.setEnabled(True) # Bật lại nếu hỗ trợ
        #        self.show_simulation_checkbox.setChecked(False) 
        if hasattr(self, 'rb_adams_bashforth'):
            self.rb_adams_bashforth.setChecked(True)
        self._update_method_details_options()
        self._update_select_all_checkbox_status()
        self._refresh_data() # Clear plots and inputs
        self._setup_initial_plots() # Reset đồ thị
        self.last_results_dict = {} # Xóa kết quả cũ
        self.info_text_area.setText(self.tr("screen2_info_area_init"))
        print("set_model finished.")
   
    @Slot()
    def _run_simulation_and_plot(self):
        print("--- Starting Init & Plot ---")
        self.last_results_dict = {}
        self.current_validated_input_params = {} # Reset trước mỗi lần chạy
        self.info_text_area.setText(self.tr("screen2_info_area_running"))

        # Reset hiển thị các giá trị tính toán (c, r, alpha, beta, steady_state)
        if self.calculated_c_display_widget:
            self.calculated_c_display_widget.setText("")
            self.calculated_c_display_widget.setPlaceholderText(self.tr("Calculating...", "Calculating..."))
        if self.calculated_r_display_widget:
            self.calculated_r_display_widget.setText("")
            self.calculated_r_display_widget.setPlaceholderText(self.tr("Calculating...", "Calculating..."))
        if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget:
            self.calculated_alpha_display_widget.setText("")
            self.calculated_alpha_display_widget.setPlaceholderText(self.tr("Calculating...", "Calculating..."))
        if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget: # Sửa lại điều kiện
            self.calculated_beta_display_widget.setText("")
            self.calculated_beta_display_widget.setPlaceholderText(self.tr("Calculating...", "Calculating..."))
        # if hasattr(self, 'calculated_steady_state_display_widget') and self.calculated_steady_state_display_widget: # Bỏ steady state ở đây
        #     self.calculated_steady_state_display_widget.setText("")
        #     self.calculated_steady_state_display_widget.setPlaceholderText(self.tr("Calculating...", "Calculating..."))


        all_errors = []
        selected_steps_int = []
        h_float = None
        input_params = {}
        method_short = None

        checked_method = self.method_button_group.checkedButton()
        if not checked_method:
            all_errors.append(self.tr("msg_select_method"))
        else:
            method_short = checked_method.objectName() # "Bashforth" or "Moulton"

        selected_steps_cb = [cb for k, cb in self.step_checkboxes.items() if cb.isChecked() and cb.isVisible()]
        if not selected_steps_cb:
            all_errors.append(self.tr("msg_select_step"))
        else:
            try:
                selected_steps_int = []
                for cb in selected_steps_cb:
                    cb_text = cb.text() 
                    num_str = ""
                    for char in cb_text:
                        if char.isdigit():
                            num_str += char
                        else:
                            break 
                    if num_str:
                        selected_steps_int.append(int(num_str))
                    else:
                        # Nếu không trích xuất được, để lại list rỗng để lỗi bên dưới xử lý
                        # Hoặc có thể thêm lỗi cụ thể hơn ở đây
                        print(f"Warning: Could not parse step number from checkbox text: '{cb_text}' for _run_simulation_and_plot")
                
                if not selected_steps_int and selected_steps_cb: # Nếu có checkbox được chọn nhưng không parse được số nào
                    err_steps_format = self.tr("msg_internal_error_steps", "Invalid number of steps: {}")
                    problematic_texts = [cb.text() for cb in selected_steps_cb]
                    all_errors.append(err_steps_format.format(problematic_texts))
            except (ValueError, IndexError):
                err_steps_format = self.tr("msg_internal_error_steps", "Invalid step checkbox format")
                all_errors.append(err_steps_format.format([cb.text() for cb in selected_steps_cb]))

        model_id = self.current_model_data.get("id")
        is_model2 = (model_id == "model2")
        is_abm = (model_id == "model3") and self.current_model_data.get("can_run_abm_on_screen3", False) and ABM_AVAILABLE
        is_model5 = (model_id == "model5")

        if model_id == "model5" and method_short == "Bashforth" and 5 in selected_steps_int:
            print("Model 5 with Adams-Bashforth: Removing step 5 from simulation list.")
            selected_steps_int.remove(5)
            if not selected_steps_int: # Nếu sau khi xóa không còn step nào
                 all_errors.append(self.tr("msg_select_step"))

        selected_h_rb = self.h_button_group.checkedButton()
        if not selected_h_rb:
            all_errors.append(self.tr("msg_select_h"))
        else:
            h_str = selected_h_rb.text()
            try:
                h_float_temp = float(h_str)
                if h_float_temp <= 0:
                     raise ValueError("Step size h must be positive.")
                h_float = h_float_temp
            except ValueError:
                all_errors.append(self.tr("msg_invalid_h").format(h_str))

        # Validate parameters
        params_ok, temp_input_params, param_errors = self._validate_parameters()
        all_errors.extend(param_errors)
        if params_ok:
            input_params = temp_input_params
            self.current_validated_input_params = input_params.copy()
        else: # Nếu params không ok, đảm bảo current_validated_input_params rỗng
            self.current_validated_input_params = {}


        selected_component = "x"
        if model_id == "model5":
            if hasattr(self, 'rb_component_y') and self.rb_component_y and self.rb_component_y.isChecked():
                selected_component = "y"
            print(f"Model 5 selected component: {selected_component}")

        if all_errors:
            formatted_errors = [f"{self.tr('screen2_info_area_error')}{msg}" for msg in all_errors]
            error_display_text = "\n".join(formatted_errors)
            self.info_text_area.setText(error_display_text)
            QMessageBox.critical(self, self.tr("msg_error_title", "Error"), self.tr("msg_invalid_input_text", "Check inputs."))
            print(f"Validation failed with errors:\n{error_display_text}")
            # Reset calculated displays on error
            if self.calculated_c_display_widget: self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if self.calculated_r_display_widget: self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget: self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget: self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            # if hasattr(self, 'calculated_steady_state_display_widget') and self.calculated_steady_state_display_widget: self.calculated_steady_state_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            self.current_validated_input_params = {} # Reset lại nếu có lỗi
            return

        # Chuẩn bị hàm ODE và các tham số khác
        prep_ok, prep_data = self._prepare_simulation_functions(input_params)
        if not prep_ok:
            current_text = self.info_text_area.toPlainText()
            if not current_text.startswith(self.tr("screen2_info_area_error")):
                 self.info_text_area.setText(self.tr("screen2_info_area_error") + "Model preparation failed.")
            if self.calculated_c_display_widget: self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if self.calculated_r_display_widget: self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget: self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget: self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            # if hasattr(self, 'calculated_steady_state_display_widget') and self.calculated_steady_state_display_widget: self.calculated_steady_state_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            self.current_validated_input_params = {} # Reset lại nếu có lỗi
            return

        ode_func, exact_callable, y0, t_start, t_end = prep_data

        # Cập nhật hiển thị các giá trị tính toán (c, r, alpha, beta)
        if model_id == "model2" and self.calculated_c_display_widget:
            if self._last_calculated_c is not None: self.calculated_c_display_widget.setText(f"{self._last_calculated_c:.6g}")
            else: self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
        elif model_id == "model3" and self.calculated_r_display_widget:
            if self._last_calculated_r is not None: self.calculated_r_display_widget.setText(f"{self._last_calculated_r:.8g}")
            else: self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
        elif model_id == "model4":
            if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget:
                if self._last_calculated_alpha is not None: self.calculated_alpha_display_widget.setText(f"{self._last_calculated_alpha:.6g}")
                else: self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget:
                if self._last_calculated_beta is not None: self.calculated_beta_display_widget.setText(f"{self._last_calculated_beta:.6g}")
                else: self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            # if hasattr(self, 'calculated_steady_state_display_widget') and self.calculated_steady_state_display_widget:
            #     if self._last_calculated_steady_state is not None:
            #         try: self.calculated_steady_state_display_widget.setText(f"{self._last_calculated_steady_state:.6g}")
            #         except Exception: self.calculated_steady_state_display_widget.setText(self.tr("Error", "Error"))
            #     else: self.calculated_steady_state_display_widget.setPlaceholderText(self.tr("N/A","N/A"))


        results_dict={}
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            for steps in selected_steps_int:
                print(f"  Simulating {method_short} {steps} steps...")
                res=self._perform_single_simulation(ode_func, exact_callable, y0, t_start, t_end, method_short, steps, h_float, selected_component)
                results_dict[steps]=res if res else {}
            self.last_results_dict={k:v for k,v in results_dict.items() if v}
        except Exception as e:
            err=self.tr("msg_simulation_error_text").format(e)
            QMessageBox.critical(self,self.tr("msg_simulation_error_title"),err)
            self.info_text_area.setText(self.tr("screen2_info_area_error")+err)
            import traceback
            traceback.print_exc()
            self.last_results_dict={}
            self.current_validated_input_params = {} # Reset lại nếu có lỗi
        finally:
            QApplication.restoreOverrideCursor()

        if not self.last_results_dict:
            current_text = self.info_text_area.toPlainText()
            if not current_text.startswith(self.tr("screen2_info_area_error")):
                 QMessageBox.warning(self, self.tr("msg_no_results_title"), self.tr("msg_no_results_text"))
                 self.info_text_area.setText(self.tr("screen2_info_area_no_results"))
            self._setup_initial_plots()
            if hasattr(self, 'btn_go_to_screen3'):
                self.btn_go_to_screen3.setEnabled(False)
                self.btn_go_to_screen3.setVisible(False)
            if self.calculated_c_display_widget: self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if self.calculated_r_display_widget: self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget: self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget: self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            # if hasattr(self, 'calculated_steady_state_display_widget') and self.calculated_steady_state_display_widget: self.calculated_steady_state_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
            self.current_validated_input_params = {} # Reset lại nếu không có kết quả
            return

        self._update_plots_multi_steps(self.last_results_dict, method_short, exact_callable, selected_component)

        print("Processing dynamic plot/ABM button state...")
        self.dynamic_plot_data = None
        should_enable_and_show_button = False

        if self.last_results_dict:
            if is_abm:
                should_enable_and_show_button = True
                print("ABM model detected, enabling and showing simulation button.")
            elif is_model2:
                print("Model 2 detected. Attempting to generate animation data...")
                highest_step_for_anim = -1
                result_for_animation = None
                valid_steps_with_results = [step for step in selected_steps_int if step in self.last_results_dict and self.last_results_dict[step]]
                if valid_steps_with_results:
                    highest_step_for_anim = max(valid_steps_with_results)
                    result_for_animation = self.last_results_dict.get(highest_step_for_anim)
                if result_for_animation:
                    t_anim = result_for_animation.get("t_plot")
                    y_anim = result_for_animation.get("approx_sol_plot")
                    method_label_anim = f"A{method_short[0].upper()}{highest_step_for_anim}"
                    if t_anim is not None and y_anim is not None and \
                       isinstance(t_anim, np.ndarray) and isinstance(y_anim, np.ndarray) and \
                       len(t_anim) == len(y_anim) and len(t_anim) > 0:
                        additional_plot_info = {
                            'T': t_anim.copy(),
                            'Y': y_anim.copy(),
                            'y0_anim': y0,
                            'method_label': method_label_anim,
                            't_start_anim': t_start,
                            't_end_anim': t_end,
                            'h_anim': result_for_animation.get("h_actual_plot"),
                            'c_anim': self._last_calculated_c
                        }
                        self.dynamic_plot_data = additional_plot_info
                        should_enable_and_show_button = True
                        print(f"  Successfully generated animation data for Model 2. Enabling and showing button.")
                    else:
                        print("  Failed to generate animation data for Model 2: Invalid T or Y.")
                        self.dynamic_plot_data = None
                else:
                    print("  Failed to generate animation data for Model 2: No valid result for highest step.")
                    self.dynamic_plot_data = None
            elif is_model5:
                print("Model 5 detected. Preparing data for Screen 3.")
                first_valid_step_for_anim = None
                if selected_steps_int: # selected_steps_int đã được lọc các step không hợp lệ
                    first_valid_step_for_anim = selected_steps_int[0] 
                
                # Kiểm tra xem có input params hợp lệ không
                if self.current_validated_input_params and first_valid_step_for_anim is not None:
                    self.dynamic_plot_data = {
                        'model_id': model_id,
                        'params': self.current_validated_input_params.copy(), # Các tham số x0,y0,u,v,t0,t1
                        'method_short': method_short,                 # Ví dụ "Bashforth"
                        'method_steps': first_valid_step_for_anim,    # Ví dụ 2 cho AB2
                        'h_target': h_float,                          # Bước nhảy h
                        # Screen 3 sẽ tự tính toán T, approx_x, approx_y bằng solver riêng
                    }
                    should_enable_and_show_button = True
                    print("  Successfully prepared PARAMETERS for Model 5 Sim 1 on Screen 3.")
                    print(f"  Dynamic plot data (params only) for M5S1: {self.dynamic_plot_data}")
                else:
                    print("  Failed to prepare data for Model 5: Invalid input parameters or no valid step selected for animation.")
                    self.dynamic_plot_data = None
            else:
                 print("Not enabling/showing simulation button (Not Model 2, 3 or 5).")
        else:
             print("Not enabling/showing simulation button (No simulation results).")
             self.dynamic_plot_data = None

        if hasattr(self, 'btn_go_to_screen3'):
            self.btn_go_to_screen3.setEnabled(should_enable_and_show_button)
            self.btn_go_to_screen3.setVisible(should_enable_and_show_button)

        current_text = self.info_text_area.toPlainText()
        if not current_text.startswith(self.tr("screen2_info_area_error")):
             self.info_text_area.setText(self.tr("screen2_info_area_complete"))

        print("--- Init & Plot Complete (Screen 2 updated) ---")
    
    @Slot()
    def _go_to_screen3_dynamic(self):
        """Chuyển sang Screen 3 nếu có dữ liệu plot động đã lưu."""
        model_id = self.current_model_data.get("id")
        is_abm_model_3 = (model_id == "model3") and self.current_model_data.get("can_run_abm_on_screen3", False) and ABM_AVAILABLE
        is_dynamic_model_2 = (model_id == "model2") # Giả sử Model 2 có dữ liệu động
        #can_run_ode_dynamic_animation = (model_id == "model2" or model_id == "model3")
        
        # HIGHLIGHT START
        is_model_5 = (model_id == "model5") # Add a flag for Model 5
        # HIGHLIGHT END

        if is_abm_model_3:
            print("Button clicked for ABM simulation...")
            # --- Chuẩn bị tham số cho ABM từ input ODE của Screen 2 ---
            ode_params_ok, ode_input_params, ode_param_errors = self._validate_parameters()
            if not ode_params_ok:
                QMessageBox.critical(self, self.tr("msg_error"), "Nhập đúng tham số ODE (n, t₀, t₁) trước khi chạy ABM.\n" + "\n".join(ode_param_errors))
                return
            # HIGHLIGHT END

            if not hasattr(self, '_last_calculated_r') or self._last_calculated_r is None:
                print("  ABM: _last_calculated_r not found or None. Re-preparing simulation functions...")
                # ode_input_params đã được lấy ở trên, không cần lấy lại ở đây
                prep_ok, _ = self._prepare_simulation_functions(ode_input_params) # Truyền ode_input_params đã lấy
                if not prep_ok or self._last_calculated_r is None:
                    QMessageBox.critical(self, self.tr("msg_error"), "Không thể tính toán tham số 'r' cho ABM.")
                    return

            n_initial = ode_input_params.get('n')
            t_start_ode = ode_input_params.get('t₀')
            t_end_ode = ode_input_params.get('t₁')
            r_ode = self._last_calculated_r 
            if n_initial is None or t_start_ode is None or t_end_ode is None: 
                QMessageBox.critical(self, self.tr("msg_error"), "Thiếu tham số n, t₀ hoặc t₁ cho ABM.")
                return
            if n_initial < 0:
                QMessageBox.critical(self, self.tr("msg_param_value_error_title", "Lỗi Giá trị"),
                                     self.tr("Giá trị ban đầu n (y₀) phải không âm cho mô phỏng ABM.",
                                             "Initial value n (y₀) must be non-negative for ABM simulation."))
                # Đánh dấu lỗi cho ô nhập 'n' nếu có thể
                if 'n' in self.param_inputs:
                    self.param_inputs['n'].setStyleSheet("background-color:#ffdddd; border:1px solid red;")
                return
            # Tính R_ode
            #r_ode = self._last_calculated_r
            calculated_ptrans = None
            abm_defaults = self.current_model_data.get("abm_defaults", {})
            r_factor = abm_defaults.get("r_to_ptrans_factor", ABM_R_FACTOR_DEFAULT)
            ptrans_min = abm_defaults.get("ptrans_min", ABM_PTRANS_MIN)
            ptrans_max = abm_defaults.get("ptrans_max", ABM_PTRANS_MAX)

            if r_ode is None:
                r_ode_fallback = 0.000138 # Hoặc lấy từ một nguồn khác
                calculated_ptrans = np.clip(r_ode_fallback * r_factor, ptrans_min, ptrans_max)
                print(f"Warning: r_ode failed. Using default P_trans={calculated_ptrans:.4f}")
            else:
                calculated_ptrans = np.clip(r_ode * r_factor, ptrans_min, ptrans_max)
                print(f"Calculated r_ode: {r_ode:.6e}, P_trans: {calculated_ptrans:.4f}")
            # --- Lấy các tham số điều chỉnh từ defaults ---
            abm_defaults = self.current_model_data.get("abm_defaults", {})

            base_speed = abm_defaults.get("base_agent_speed", 0.04)
            speed_scale = abm_defaults.get("speed_scaling_factor", 0.5)
            min_speed = abm_defaults.get("min_agent_speed", 0.02)
            max_speed = abm_defaults.get("max_agent_speed", 0.20)

            base_radius = abm_defaults.get("base_contact_radius", 0.5)
            radius_scale = abm_defaults.get("radius_scaling_factor", 3.0)
            min_radius = abm_defaults.get("min_contact_radius", 0.3)
            max_radius = abm_defaults.get("max_contact_radius", 1.5)

            # --- Tính toán giá trị điều chỉnh dựa trên r_ode ---
            # Đảm bảo r_ode có giá trị hợp lệ để tính toán
            r_for_scaling = r_ode if r_ode is not None and r_ode > 0 else 0.0

            # Tính tốc độ mới (ví dụ: tuyến tính)
            adjusted_speed = base_speed + speed_scale * r_for_scaling
            # Giới hạn tốc độ trong khoảng min/max
            adjusted_speed = np.clip(adjusted_speed, min_speed, max_speed)

            # Tính bán kính mới (ví dụ: tuyến tính)
            adjusted_radius = base_radius + radius_scale * r_for_scaling
            # Giới hạn bán kính trong khoảng min/max
            adjusted_radius = np.clip(adjusted_radius, min_radius, max_radius)

            print(f"--- Auto-adjusting ABM params based on r={r_for_scaling:.4g} ---")
            print(f"  Adjusted Agent Speed: {adjusted_speed:.4f} (Base:{base_speed}, Scale:{speed_scale}, Min:{min_speed}, Max:{max_speed})")
            print(f"  Adjusted Contact Radius: {adjusted_radius:.4f} (Base:{base_radius}, Scale:{radius_scale}, Min:{min_radius}, Max:{max_radius})")
            print(f"  P_trans (using fixed r_factor): {calculated_ptrans:.4f}") # P_trans vẫn tính như cũ

            # --- Tính tổng dân số ABM từ n (giữ nguyên) ---
            total_population_abm = max(1, int(n_initial + 1))
            # --- Lấy seconds_per_step từ defaults ---
            seconds_per_step = abm_defaults.get("seconds_per_step", 0.1) # Lấy giá trị hoặc dùng default 0.1
            # --- Tạo dictionary tham số cho Screen 3 với giá trị đã điều chỉnh ---
            abm_params_for_screen3 = {
                "total_population": total_population_abm,
                "initial_infected": 1,
                "room_dimension": abm_defaults.get("room_dimension", ABM_ROOM_DIMENSION_DEFAULT), # Giữ nguyên room_dimension
                # HIGHLIGHT START: Sử dụng giá trị đã điều chỉnh
                "agent_speed": adjusted_speed,
                "contact_radius": adjusted_radius,
                # HIGHLIGHT END
                "transmission_prob": calculated_ptrans, # P_trans vẫn tính từ r và r_factor cố định
                "r_to_ptrans_factor": abm_defaults.get("r_to_ptrans_factor", 5000), # Truyền cả r_factor cố định nếu cần
                "max_steps": int(abm_defaults.get("max_steps", ABM_MAX_STEPS_DEFAULT)), # Vẫn giữ max_steps phòng lỗi
                "interval_ms": int(abm_defaults.get("interval_ms", ABM_INTERVAL_DEFAULT)),
                "display_max_total": int(abm_defaults.get("display_max_total", MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY)),
                "display_sample_size": int(abm_defaults.get("display_sample_size", SAMPLE_SIZE_FOR_LARGE_POPULATION)),
                "r_parameter_ode": r_ode, # Vẫn truyền r gốc để hiển thị
                "t_start_ode": t_start_ode,
                "t_end_ode": t_end_ode,
                "seconds_per_step": seconds_per_step
            }
            # Gọi hàm chuyển màn hình mới
            self.main_window.switch_to_screen3_abm(abm_params_for_screen3)

        elif is_dynamic_model_2: # This should be just is_model_2 if you simplify
            print("Button clicked for Model 2 dynamic plot...")
            # --- Logic hiện tại của bạn để chuyển sang Screen 3 cho Model 2 ---
            # Kiểm tra xem self.dynamic_plot_data có hợp lệ không (được tạo trong _run_simulation_and_plot)
            if self.dynamic_plot_data:
                # Lấy dữ liệu cần thiết từ self.dynamic_plot_data
                time_data = self.dynamic_plot_data.get('T')
                simulation_data_list = [self.dynamic_plot_data.get('Y')] # Bọc trong list
                simulation_labels = [self.dynamic_plot_data.get('method_label')] # Bọc trong list
                additional_info = self.dynamic_plot_data # Truyền cả dict

                if time_data is not None and simulation_data_list[0] is not None:
                    # Gọi hàm chuyển màn hình CŨ (hoặc hàm mới nhưng có type)
                    self.main_window.switch_to_screen3_model2(time_data, simulation_data_list, simulation_labels, additional_info)
                else:
                    QMessageBox.warning(self, self.tr("msg_error"), "Dữ liệu mô phỏng động Model 2 không hợp lệ.")
            else:
                QMessageBox.information(self, self.tr("msg_info"), "Chạy mô phỏng Model 2 trước để tạo dữ liệu động.")
        
        # HIGHLIGHT START: Add this elif block for Model 5
        elif is_model_5:
            print("Button clicked for Model 5 visualization...")
            # Check if dynamic_plot_data is available and is for Model 5
            if self.dynamic_plot_data and self.dynamic_plot_data.get('model_id') == "model5":
                # Pass the prepared data to Screen 3 via MainWindow
                self.main_window.switch_to_screen3_model5(self.dynamic_plot_data)
            else:
                # This case should ideally not be reached if the button enabling logic is correct
                QMessageBox.warning(self, self.tr("msg_error"),
                                    self.tr("Dữ liệu mô phỏng Model 5 không hợp lệ hoặc chưa được tạo.",
                                            "Model 5 simulation data is invalid or not generated."))
        # HIGHLIGHT END
        else:
            # Trường hợp nút bị nhấn cho model khác (không nên xảy ra nếu logic set_model đúng)
            # You can make this message more generic or remove it if the button logic is robust
            QMessageBox.information(self, self.tr("msg_info"), "Chức năng này chỉ dành cho Model 2, Model 3 (ABM), hoặc Model 5.")
    
    def _validate_parameters(self):
        """Validates all input parameters and returns dict if valid."""
        input_params = {}
        valid = True
        errors = []
        needed_keys = self.current_model_data.get("internal_param_keys", [])
        model_id = self.current_model_data.get("id")
        if not needed_keys:
            return True, {} # No params needed
        current_layout = self.params_group.layout() # Lấy layout hiện tại
        if not current_layout:
             print("Validation Error: No current layout found.")
             errors.append("Internal error: Parameter layout not ready.")
             return False, {}, errors
        if not self.param_inputs:
            print("Error: param_inputs dictionary not populated correctly.")
            errors.append("Internal error: Parameter input fields not ready.")
            return False, {}, errors

        print(f"Validating params for layout type: {type(current_layout).__name__}")

        for key in needed_keys:
            line_edit = self.param_inputs.get(key)
            if line_edit is None:
                error_msg = f"Internal error: Input field for parameter key '{key}' is missing."
                print(error_msg)
                errors.append(error_msg)
                valid = False
                continue
            # Find label for error message context
            label_text = key
            label_widget = None
            if isinstance(current_layout, QFormLayout):
                # Duyệt qua các item trong layout để tìm label tương ứng với line_edit
                for i in range(current_layout.rowCount()):
                    try: # Thêm try-except phòng trường hợp item không hợp lệ
                        label_item = current_layout.itemAt(i, QFormLayout.ItemRole.LabelRole)
                        field_item = current_layout.itemAt(i, QFormLayout.ItemRole.FieldRole)
                        # Kiểm tra field_item trước khi truy cập widget
                        if field_item and field_item.widget() == line_edit:
                         if label_item and label_item.widget() and isinstance(label_item.widget(), QLabel):
                             label_widget = label_item.widget()
                             break
                    except Exception as e_find:
                         print(f"Error finding label in FormLayout (row {i}): {e_find}")
                         # Có thể tiếp tục hoặc dừng tùy logic
            elif isinstance(current_layout, QGridLayout):
                 # Tìm vị trí của line_edit trong grid
                 found_pos = False
                 for i in range(current_layout.count()):
                      item = current_layout.itemAt(i)
                      if item and item.widget() == line_edit:
                           try:
                               row, col, _, _ = current_layout.getItemPosition(i)
                               # Tìm label ở cột bên trái (col - 1)
                               label_item = current_layout.itemAtPosition(row, col - 1)
                               if label_item and label_item.widget() and isinstance(label_item.widget(), QLabel):
                                    label_widget = label_item.widget()
                                    found_pos = True
                                    break
                           except Exception as e_grid_pos:
                                print(f"Error getting grid position for item {i}: {e_grid_pos}")
                 if label_widget:
                    label_text = label_widget.text().replace(':', '').strip()

                 #if not found_pos: print(f"Warning (Validation): Could not find grid position for {key}")
            # Validate value
            val_str = line_edit.text().strip()
            line_edit.setStyleSheet("") # Reset style
            if not val_str:
                error_msg = self.tr("msg_missing_param_value").format(label_text) # <<< THAY ĐỔI
                errors.append(error_msg)
                line_edit.setStyleSheet("background-color:#ffdddd; border:1px solid red;")
                valid=False
                print(f"Validation Error: {error_msg}")
                continue
            try:
                input_params[key] = float(val_str)
    
            except ValueError as ve:
                error_msg = self.tr("msg_invalid_param_value").format(label_text, val_str)
                if str(ve):
                    error_msg += f" ({str(ve)})"
                errors.append(error_msg)
                line_edit.setStyleSheet("background-color:#ffdddd; border:1px solid red;")
                valid=False
                print(f"Validation Error: {error_msg}")
        if valid and 't₀' in input_params and 't₁' in input_params:
            if input_params['t₁'] <= input_params['t₀']:
                 errors.append(self.tr("msg_t_end_error"))
                 # Highlight both t0 and t1 fields
                 if 't₀' in self.param_inputs: self.param_inputs['t₀'].setStyleSheet("background-color:#ffdddd; border:1px solid red;")
                 if 't₁' in self.param_inputs: self.param_inputs['t₁'].setStyleSheet("background-color:#ffdddd; border:1px solid red;")
                 valid = False
                 print(f"Validation Error: {self.tr('msg_t_end_error')}")


        return valid, input_params, errors

    def _get_middle_t_value(self, t_r_pairs):
        """Lấy giá trị t từ cặp [t, r] ở giữa danh sách."""
        if not t_r_pairs: return None
        middle_index = len(t_r_pairs) // 2
        return t_r_pairs[middle_index][0]

    def _predict_r_for_model3(self, t_start, t_end, n_initial):
        """Tính toán r cho Model 3 theo logic standalone predict_t_max.
           Sử dụng tên tham số của app: t_start, t_end, n_initial (là y0).
        """
        a = t_start
        b = t_end
        n = n_initial # 'n' trong công thức standalone là giá trị ban đầu
        print(f"Calculating r (standalone logic): t_start={a}, t_end={b}, n_initial={n}")

        if n <= 0:
            print("Error: Initial value 'n' must be positive to calculate r.")
            return None
        if b <= a:
            print("Error: t_end must be greater than t_start to calculate r.")
            return None

        # ---- Logic tạo t_value từ standalone ----
        # Logic này vẫn còn nghi vấn về ý nghĩa toán học, nhưng giữ nguyên để giống standalone
        t_value_list = []
        try:
             # Standalone dùng range(1, b). Cần đảm bảo b hợp lý cho range.
             # Nếu b không nguyên, làm tròn có thể thay đổi kết quả.
             # Standalone có thể giả định b là số nguyên?
             b_int_limit = int(b) # Lấy phần nguyên để dùng làm giới hạn trên cho range
             if b_int_limit <= 1:
                print(f"Warning: int(t_end) ({b_int_limit}) <= 1. Cannot generate t_value list.")
                return None
             t_value_list = [(b - float(i)) / float(i) for i in range(1, b_int_limit)] # Dùng float để đảm bảo chia đúng
             print(f"Generated {len(t_value_list)} t_values using standalone range(1, {b_int_limit}) logic.")
        except Exception as e: print(f"Error generating t_value list with b={b}: {e}"); return None
        if not t_value_list: print("Error: t_value list is empty."); return None

        if not t_value_list:
             print("Error: t_value list is empty.")
             return None
        # ---- Hết logic tạo t_value ----

        # ---- Logic predict_t_max gốc ----
        # min_t_value = b / 2.0 if b <= 50 else 10.0 # Logic điều kiện min_t_value
        min_t_value = float(b) / 2.0 if b <= 50 else 10.0 # Đảm bảo float division
        print(f"  Using min_t_value = {min_t_value}")
        predict = []
        min_r_threshold = 1e-8 # Ngưỡng dưới rất nhỏ cho r

        for t_val in t_value_list:
            if t_val <= 1e-15: continue # Tránh chia cho 0
            # Công thức r từ standalone: r = log(n) / ((n + 1) * t_val)
            try:
                 # Cần np.log(n) chứ không phải log(n) của python math
                 current_r = (np.log(n)) / ((n + 1.0) * t_val)
            except ValueError: # Ví dụ log(số không dương)
                 print(f"Warning: Math error calculating r for t_val={t_val}. Skipping.")
                 continue
            if min_r_threshold <= current_r and b > t_val >= min_t_value:
                predict.append([t_val, current_r])
            #

        if not predict:
            print("Warning: No valid [t_value, r] pairs found meeting criteria.")
            return None

        # Sắp xếp predict theo t_value để lấy middle một cách ổn định
        # Tìm r tương ứng với giá trị t ở giữa danh sách predict đã sắp xếp
        print(f"  Predict list (unsorted, filtered) has {len(predict)} elements.")
        middle_t = self._get_middle_t_value(predict) # Lấy t ở giữa
        if middle_t is None:
            print("Error: Could not get middle t_value from sorted list.")
            return None
        print(f"  Middle t_value (based on list order) is: {middle_t:.4f}")
        calculated_r = None
        # Tìm chính xác cặp có middle_t (do đã sắp xếp, nó phải ở giữa)
        middle_index_find = len(predict) // 2
        if abs(predict[middle_index_find][0] - middle_t) < 1e-9: # Kiểm tra lại cho chắc
             calculated_r = predict[middle_index_find][1]
        else: # Dự phòng: tìm giá trị t gần nhất
            min_diff = float('inf')
            for t, r_val in predict:
                diff = abs(t - middle_t)
                if diff < min_diff:
                    min_diff = diff
                    calculated_r = r_val
            print(f"  Note: Used closest t_value match (diff={min_diff:.2e}) for r.")
        # # Cách tìm khác: lặp và so sánh (dự phòng)
        # if calculated_r is None:
        #     for t, r_val in predict:
        #         if abs(t - middle_t) < 1e-9: # So sánh số thực
        #             calculated_r = r_val
        #             break

        if calculated_r is not None:
            print(f"Standalone logic calculated r = {calculated_r:.8g} for middle t_value = {middle_t:.4g}")
        else:
            print("Error: Could not find r corresponding to the middle t_value.")

        return calculated_r
    
    def _prepare_simulation_functions(self, input_params):
        """Prepares ODE func, exact func, y0, t_start, t_end from validated params."""
        try:
            ode_gen = self.current_model_data.get("ode_func")
            exact_gen = self.current_model_data.get("exact_func")
            model_id = self.current_model_data.get("id")
            if not callable(ode_gen):
                raise ValueError(self.tr("msg_model_no_ode").format(self.tr(f"{model_id}_name", self.current_model_vi_key)))
            t_start = input_params['t₀']
            t_end = input_params['t₁']
            y0 = None # Khởi tạo y0
            if model_id == "model4":
                # Kiểm tra cả Y0 và dY0 cho Model 4
                if 'Y0' not in input_params or 'dY0' not in input_params:
                     # Có thể tạo key dịch mới hoặc dùng key cũ nhưng message sẽ hơi chung chung
                     # Ví dụ dùng key mới:
                     # raise ValueError(self.tr("msg_missing_y0_system", "Thiếu điều kiện đầu Y(t₀) hoặc Y'(t₀)."))
                     # Hoặc dùng key cũ:
                     raise ValueError(self.tr("msg_missing_y0", "Thiếu điều kiện đầu Y(t₀)/Y'(t₀).")) # Sửa text mặc định nếu cần
                # Nếu đủ, gán y0 là list [Y0, dY0]
                y0 = [input_params['Y0'], input_params['dY0']]
            elif model_id == "model5": # Model 5 là hệ, cần x0 và y0
                 if 'x0' not in input_params or 'y0' not in input_params:
                     # Sử dụng key dịch cũ, nhưng message nên rõ ràng hơn cho hệ xy
                     raise ValueError(self.tr("msg_missing_y0", "Thiếu điều kiện đầu x₀ hoặc y₀."))
                 y0 = [input_params['x0'], input_params['y0']]
            else: # Các model còn lại (1, 2, 3) là phương trình đơn
                y0_key = None
                if model_id == 'model3': y0_key = 'n'
                elif model_id == 'model1': y0_key = 'O₀'
                elif model_id == 'model2': y0_key = 'x₀'
                # Tìm key trong input_params
                actual_y0_key = next((k for k in [y0_key] if k in input_params), None)

                if actual_y0_key is None:
                    # Lấy key hiển thị đúng để báo lỗi
                    display_key = 'n' if model_id == 'model3' else ('O₀' if model_id=='model1' else 'x₀')
                    raise ValueError(self.tr("msg_missing_y0", f"Thiếu điều kiện đầu ({display_key})."))
                y0 = input_params[actual_y0_key]
            n_initial_for_model3 = y0 if model_id == 'model3' and isinstance(y0, (int, float)) else None
            self._last_calculated_c = None
            self._last_calculated_r = None
            self._last_calculated_alpha = None
            self._last_calculated_beta = None
            ode_func = None
            exact_callable = None
            if model_id == "model1":
                k=input_params['k']
                ode_func=ode_gen(k)
                exact_callable=exact_gen(y0,k,t_start) if callable(exact_gen) else None
            # elif model_id == "model2": ... # Add logic for other models
            # elif model_id == "model3": ... # Add logic for other models
            elif model_id == "model2":
                # Better handling for unimplmented models
                # Lấy các tham số cần thiết (x₀ đã có trong y0, t₀ trong t_start, t₁ trong t_end)
                x0_val = y0
                t0_val = t_start
                t1_val = t_end

                # --- Tính toán c ---
                # --- Lấy phương pháp được chọn ---
                checked_method_button = self.method_button_group.checkedButton()
                method_short_for_calc = "Bashforth" # Default nếu không có nút nào được chọn (hiếm khi xảy ra)
                if checked_method_button:
                    # objectName() của radio button đã được đặt là "Bashforth" hoặc "Moulton"
                    method_short_for_calc = checked_method_button.objectName()

                # --- Đặt number_of_double_times dựa trên phương pháp ---
                if method_short_for_calc == "Bashforth":
                    number_of_double_times = 5.0
                    print(f"Model 2 (Preparing c): Adams-Bashforth selected. number_of_double_times = {number_of_double_times}")
                elif method_short_for_calc == "Moulton":
                    number_of_double_times = 2.0
                    print(f"Model 2 (Preparing c): Adams-Moulton selected. number_of_double_times = {number_of_double_times}")
                else:
                    # Fallback nếu objectName không khớp (dù ít khả năng xảy ra với logic hiện tại)
                    number_of_double_times = 5.0 # Hoặc một giá trị mặc định an toàn khác
                    print(f"Model 2 (Preparing c): Unknown method '{method_short_for_calc}'. Defaulting number_of_double_times = {number_of_double_times}")
                
                
                # Đảm bảo x0_val không âm để tránh lỗi với căn bậc 3 số thực
                denominator_b = t1_val
                if denominator_b <= 1e-9: # Tránh chia cho 0 hoặc số quá nhỏ
                    raise ValueError("Thời gian kết thúc (t₁) phải lớn hơn 0 đáng kể để tính 'c' cho Model 2 (theo logic standalone).")
                if x0_val < 0:
                    raise ValueError("Initial mass (x₀) cannot be negative for Model 2.")
                # Tránh chia cho 0 nếu t1 = t0 (đã kiểm tra ở trên)
                x0_cbrt_safe = (x0_val + 1e-15)**(1.0/3.0)

                # Tính giới hạn dưới cho c (dựa trên N lần nhân đôi)
                doubling_factor_N_cbrt = (2.0**number_of_double_times)**(1.0/3.0)
                lower_c = 3.0 * (doubling_factor_N_cbrt - 1.0) * x0_cbrt_safe / denominator_b

                # Tính giới hạn trên cho c (dựa trên N+1 lần nhân đôi)
                doubling_factor_Nplus1_cbrt = (2.0**(number_of_double_times + 1.0))**(1.0/3.0)
                upper_c = 3.0 * (doubling_factor_Nplus1_cbrt - 1.0) * x0_cbrt_safe / denominator_b

                # Đảm bảo lower_c <= upper_c (có thể xảy ra ngược lại nếu t1 rất nhỏ)
                if lower_c > upper_c:
                    print(f"Cảnh báo: Giới hạn dưới tính toán ({lower_c}) > giới hạn trên ({upper_c}). Đảo ngược chúng cho random.uniform.")
                    lower_c, upper_c = upper_c, lower_c
                elif abs(lower_c - upper_c) < 1e-12: # Nếu giới hạn quá gần nhau, tạo một khoảng nhỏ
                     upper_c += 1e-9 # Thêm một khoảng rất nhỏ
                import random
                # Tạo giá trị c ngẫu nhiên trong khoảng đã tính toán
                calculated_c = random.uniform(lower_c, upper_c)
                self._last_calculated_c = calculated_c
                print(f"Model 2 (Logic Standalone): Tính toán c ngẫu nhiên = {self._last_calculated_c:.6g} trong khoảng [{lower_c:.6g}, {upper_c:.6g}]")
                # Tạo hàm ODE và Exact với giá trị 'c' vừa tính được
                ode_func = ode_gen(calculated_c)
                if callable(exact_gen):
                    # Truyền x0, c (vừa tính), t0
                    exact_callable = exact_gen(x0_val, calculated_c, t_start)
                else:
                    exact_callable = None
            # ================== HIGHLIGHT END: Tính toán c cho Model 2 ====================

            elif model_id == "model3":
                    # Lấy N và x0 (y0)
                    x0_val = y0 # y0 chính là x₀ cho model 3
                    t0_val = t_start
                    t1_val = t_end
                    n_initial_for_model3 = y0
                    calculated_r = self._predict_r_for_model3(t_start, t_end, n_initial_for_model3)
                    if calculated_r is None:
                        raise ValueError("Không thể tự động tính toán tham số tốc độ (r) theo logic standalone.")
                    self._last_calculated_r = calculated_r
                    # Tạo hàm ODE và Exact với r vừa tính và n_initial (y0)
                    ode_func = ode_gen(calculated_r, n_initial_for_model3)
                    if callable(exact_gen):
                        exact_callable = exact_gen(n_initial_for_model3, calculated_r, t_start)
                    else:
                        model_name_tr = self.tr(f"{model_id}_name", default_text=model_id)
                        raise NotImplementedError(f"Preparation logic for model '{model_name_tr}' is not implemented.")
            elif model_id == "model4":
                m = input_params['m']; l = input_params['l']
                a = input_params['a']; s = input_params['s']
                G = input_params['G']
                Y0_val = y0[0]; dY0_val = y0[1] # y0 đã là [Y0, dY0]

                # Tính toán alpha và beta
                try:
                    alpha_calculated = m + l*s - l*m*a
                    beta_calculated = l*m*s
                    # Kiểm tra các giá trị tính được (ví dụ: beta không quá gần 0 nếu cần thiết cho nghiệm chính xác)
                    if abs(beta_calculated) < 1e-15 and callable(exact_gen):
                         print("Warning: Calculated beta is close to zero. Exact solution might be affected.")
                         # Có thể hiển thị cảnh báo hoặc xử lý đặc biệt nếu cần
                except Exception as calc_e:
                    raise ValueError(f"Lỗi khi tính alpha/beta: {calc_e}")

                # Lưu giá trị đã tính
                self._last_calculated_alpha = alpha_calculated
                self._last_calculated_beta = beta_calculated
                print(f"Model 4: Calculated alpha = {alpha_calculated:.6g}, beta = {beta_calculated:.6g}")

                # Cập nhật ô hiển thị alpha, beta (nếu chúng tồn tại)
                if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget:
                    self.calculated_alpha_display_widget.setText(f"{alpha_calculated:.6g}")
                if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget:
                    self.calculated_beta_display_widget.setText(f"{beta_calculated:.6g}")

                # Tạo hàm ODE và Exact với alpha, beta đã tính
                ode_func = ode_gen(alpha_calculated, beta_calculated, m, G, l)
                if callable(exact_gen):
                    # Hàm _model4_exact_solution vẫn nhận alpha, beta làm tham số
                    exact_callable = exact_gen(alpha_calculated, beta_calculated, m, G, l, Y0_val, dY0_val, t_start)
            elif model_id == "model5":
                 u_param = input_params['u']
                 v_param = input_params['v']
                 ode_func = ode_gen(u_param, v_param)
                 # Model 5 không có exact_func, nên exact_callable sẽ là None (đã khởi tạo ở trên)
                 exact_callable = None # Đảm bảo là None
                 print(f"Model 5 prepared with u={u_param}, v={v_param}. No exact solution.")
            else:
                 raise NotImplementedError(f"Logic chuẩn bị cho model '{model_id}' chưa được triển khai.")
            
            if not callable(ode_func):
                 raise RuntimeError(f"Internal error: ODE function was not created for model '{model_id}'.")

            return True, (ode_func, exact_callable, y0, t_start, t_end)
        except (KeyError, ValueError, NotImplementedError, RuntimeError) as e:
             self._last_calculated_c = None; self._last_calculated_r = None
             self._last_calculated_alpha = None; self._last_calculated_beta = None
             if self.calculated_c_display_widget: self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             if self.calculated_r_display_widget: self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             # Reset cả alpha và beta display
             if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget:
                 self.calculated_alpha_display_widget.setText("")
                 self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget:
                 self.calculated_beta_display_widget.setText("")
                 self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             return False, None
        except Exception as e:
             self._last_calculated_c = None; self._last_calculated_r = None
             self._last_calculated_alpha = None; self._last_calculated_beta = None
             if self.calculated_c_display_widget: self.calculated_c_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             if self.calculated_r_display_widget: self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget:
                 self.calculated_alpha_display_widget.setText("")
                 self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget:
                 self.calculated_beta_display_widget.setText("")
                 self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
             err=self.tr("msg_unknown_error_prep").format(e)
             QMessageBox.critical(self,self.tr("msg_unknown_error_title"),err)
             self.info_text_area.setText(self.tr("screen2_info_area_error")+err)
             import traceback
             traceback.print_exc()
             return False, None

    def _perform_single_simulation(self, ode_func, exact_sol_func, y0, t_start, t_end, method_short, steps_int, h_target, selected_component='x'):
        print(f"    _perform_single_simulation (Screen2 Logic): Method={method_short}{steps_int}, h_target={h_target}, component={selected_component}")

        is_system = self.current_model_data.get("is_system", False)
        uses_rk5_reference = self.current_model_data.get("uses_rk5_reference", False)
        model_id = self.current_model_data.get("id")
        print(f"    Model ID: {model_id}, is_system: {is_system}, uses_rk5_ref: {uses_rk5_reference}")

        # --- Helper để chọn solver ---
        def get_solver_function_for_screen2():
            solver_func_to_use = None
            
            method_map_single_orig = {"Bashforth": {2: AB2, 3: AB3, 4: AB4, 5: AB5}, "Moulton": {2: AM2, 3: AM3, 4: AM4}}
            method_map_system_orig = {"Bashforth": {2: AB2_system, 3: AB3_system, 4: AB4_system, 5: AB5_system}, "Moulton": {2: AM2_system, 3: AM3_system, 4: AM4_system}}
            
            # === MAP CHO MODEL 5 TRÊN SCREEN 2 (SỬ DỤNG *_original_system_M5 VỚI BREAK ĐƠN GIẢN) ===
            # !!! BẠN CẦN ĐẢM BẢO CÁC HÀM NÀY ĐÃ ĐƯỢC ĐỊNH NGHĨA Ở GLOBAL SCOPE HOẶC IMPORT !!!
            method_map_model5_screen2_specific = {
                "Bashforth": {
                    2: AB2_original_system_M5, 3: AB3_original_system_M5, 
                    4: AB4_original_system_M5, 5: AB5_original_system_M5 
                },
                "Moulton": {
                    2: AM2_original_system_M5, 3: AM3_original_system_M5, 
                    4: AM4_original_system_M5
                }
            }
            # =======================================================================================

            if model_id == "model5":
                print(f"    Solver selection (Model 5, Screen 2): Using SPECIFIC 'original_system_M5' solvers.")
                current_map_sel = method_map_model5_screen2_specific
            elif model_id == "model4": 
                 print(f"    Solver selection (Model 4, Screen 2): Using ORIGINAL system solvers (e.g., ABx_system).")
                 current_map_sel = method_map_system_orig
            elif is_system: 
                 print(f"    Solver selection (Model {model_id}, Generic System, Screen 2): Using ORIGINAL system solvers.")
                 current_map_sel = method_map_system_orig
            else: # Model 1, 2, 3 (đơn)
                print(f"    Solver selection (Model {model_id}, Single, Screen 2): Using ORIGINAL single solvers.")
                current_map_sel = method_map_single_orig
            
            if method_short in current_map_sel and steps_int in current_map_sel[method_short]:
                solver_func_to_use = current_map_sel[method_short][steps_int]
            
            if solver_func_to_use:
                print(f"    Selected solver for Screen 2: {solver_func_to_use.__name__}")
            else:
                print(f"    Error: Solver function (for Screen 2) NOT FOUND for {method_short}{steps_int} (Model: {model_id}, System: {is_system})")
            return solver_func_to_use

        method_func_for_screen2 = get_solver_function_for_screen2()
        
        rk5_ref_for_screen2 = None
        if model_id == "model5" and uses_rk5_reference:
            # !!! BẠN CẦN ĐẢM BẢO RK5_original_system_M5 ĐÃ ĐƯỢC ĐỊNH NGHĨA !!!
            rk5_ref_for_screen2 = RK5_original_system_M5 
            if rk5_ref_for_screen2:
                 print(f"    Selected RK5 reference for Screen 2 (Model 5): {rk5_ref_for_screen2.__name__}")
            else:
                 print(f"    FATAL: RK5_original_system_M5 is not defined but needed for Model 5 reference on Screen 2.")
                 return None
        
        if method_func_for_screen2 is None:
            print("    FATAL: Could not get main solver for Screen 2. Aborting simulation.")
            return None

        interval_length = t_end - t_start
        if interval_length <= 1e-9: return None
        min_n_required = max(steps_int, 2) 
        n_plot = max(int(np.ceil(interval_length / h_target)), min_n_required if model_id != "model5" else 5)
        if uses_rk5_reference: n_plot = max(n_plot, 50) # RK5 ref cần nhiều điểm hơn
        h_actual_plot = interval_length / n_plot
        t_plot = np.linspace(t_start, t_end, n_plot + 1)

        y_approx_plot_u1, y_exact_plot_u1 = None, None
        y_approx_plot_all_components, y_exact_plot_all_components = None, None

        # --- TÍNH NGHIỆM THAM CHIẾU CHO ĐỒ THỊ CHÍNH ---
        if model_id == "model5" and uses_rk5_reference and rk5_ref_for_screen2:
            try:
                print(f"    Plot sim (Main - Model 5): Calculating RK5 reference using {rk5_ref_for_screen2.__name__}")
                # Gọi rk5_ref_for_screen2 (là RK5_original_system_M5)
                # Hàm này KHÔNG NHẬN v_t, v_n, d như các hàm _M5 phức tạp
                rk5_ref_x_plot, rk5_ref_y_plot = rk5_ref_for_screen2(ode_func, t_plot, y0[0], y0[1])
                y_exact_plot_all_components = [np.asarray(rk5_ref_x_plot), np.asarray(rk5_ref_y_plot)]
                y_exact_plot_u1 = y_exact_plot_all_components[0 if selected_component == 'x' else 1]
            except Exception as e_rk5_plot:
                print(f"    Error calculating RK5 reference for Model 5 main plot: {e_rk5_plot}")
                # import traceback; traceback.print_exc() # Bỏ comment để debug nếu cần
                return None 
        elif exact_sol_func and len(t_plot) > 0: # Các model khác có nghiệm giải tích
            if is_system: # Model 4
                exact_tuple = exact_sol_func(t_plot)
                if exact_tuple is not None and len(exact_tuple) == 2:
                    y_exact_plot_all_components = [np.asarray(exact_tuple[0]), np.asarray(exact_tuple[1])]
                    y_exact_plot_u1 = y_exact_plot_all_components[0] 
            else: # Model 1,2,3
                y_exact_plot_u1 = np.asarray(exact_sol_func(t_plot))

        # --- TÍNH NGHIỆM XẤP XỈ CHO ĐỒ THỊ CHÍNH ---
        try:
            # Sử dụng method_func_for_screen2 (là solver GỐC hoặc *_original_system_M5)
            # Hàm này KHÔNG NHẬN v_t, v_n, d như các hàm _M5 phức tạp
            if is_system: # Model 4 hoặc Model 5
                u1_plot, u2_plot = method_func_for_screen2(ode_func, t_plot, y0[0], y0[1])
                y_approx_plot_all_components = [np.asarray(u1_plot), np.asarray(u2_plot)]
                y_approx_plot_u1 = y_approx_plot_all_components[0 if selected_component == 'x' else 1]
            else: # Model 1, 2, 3
                y_plot = method_func_for_screen2(ode_func, t_plot, y0)
                y_approx_plot_u1 = np.asarray(y_plot)
            
            if y_approx_plot_u1 is not None:
                min_len_plot = len(y_approx_plot_u1)
                if y_exact_plot_u1 is not None: min_len_plot = min(min_len_plot, len(y_exact_plot_u1))
                min_len_plot = min(min_len_plot, len(t_plot))
                t_plot = t_plot[:min_len_plot]
                if y_approx_plot_all_components:
                    y_approx_plot_all_components[0] = y_approx_plot_all_components[0][:min_len_plot]
                    y_approx_plot_all_components[1] = y_approx_plot_all_components[1][:min_len_plot]
                    y_approx_plot_u1 = y_approx_plot_all_components[0 if selected_component == 'x' else 1]
                elif y_approx_plot_u1 is not None: y_approx_plot_u1 = y_approx_plot_u1[:min_len_plot]
                if y_exact_plot_all_components:
                    y_exact_plot_all_components[0] = y_exact_plot_all_components[0][:min_len_plot]
                    y_exact_plot_all_components[1] = y_exact_plot_all_components[1][:min_len_plot]
                    y_exact_plot_u1 = y_exact_plot_all_components[0 if selected_component == 'x' else 1]
                elif y_exact_plot_u1 is not None: y_exact_plot_u1 = y_exact_plot_u1[:min_len_plot]
        except Exception as e_plot_approx:
            print(f"    Error calculating APPROXIMATE solution for main plot (N={n_plot}) using {method_func_for_screen2.__name__}: {e_plot_approx}")
            # import traceback; traceback.print_exc() # Bỏ comment để debug nếu cần
            t_plot = np.array([])
            y_approx_plot_u1, y_exact_plot_u1 = None, None
            y_approx_plot_all_components, y_exact_plot_all_components = None, None

        # --- VÒNG LẶP TÍNH TOÁN LỖI/BẬC HỘI TỤ ---
        errors_convergence = []
        h_values_for_loglog_list = []
        n_values_plotted = []
        log_h_conv, log_err_conv = [], []
        slope = np.nan

        # --- LOGIC TẠO N_VALUES_FOR_CONV_LOOP ---
        # (Quan trọng: Điều chỉnh cho Model 5 để khớp Hình 2 của bạn)
        interval_n_base = max(1, int(np.ceil(interval_length)))
        n_start_conv, n_end_conv = 0, 0 
        num_points_convergence = 10 # Mặc định, có thể điều chỉnh cho Model 5
        
        if model_id == "model1": n_start_conv, n_end_conv = max(5, 2*interval_n_base), max(20, 10*interval_n_base)
        elif model_id == "model2": n_start_conv, n_end_conv = max(5,interval_n_base), max(10,interval_n_base*2)
        elif model_id == "model3": n_start_conv = interval_n_base; n_end_conv = 3 * interval_n_base
        elif model_id == "model4": n_start_conv, n_end_conv = max(10, 10*interval_n_base), max(30, 30*interval_n_base)
        elif model_id == "model5": 
            # !!! ĐIỀU CHỈNH Ở ĐÂY ĐỂ KHỚP HÌNH 2 !!!
            n_start_conv = 2000  # Ví dụ, bạn cần xem Hình 2 để xác định giá trị N bắt đầu
            n_end_conv = 10000   # Ví dụ, giá trị N kết thúc
            num_points_convergence = 8 # Số điểm N muốn có trên đồ thị log-log
        else: n_start_conv, n_end_conv = 10, 100

        n_values_for_conv_loop = np.array([], dtype=int)
        if model_id in ["model2", "model3"]: 
            if n_start_conv <= 0: n_start_conv = 1
            if n_end_conv <= n_start_conv: n_end_conv = n_start_conv + max(1, num_points_convergence -1) 
            n_values_for_conv_loop = np.arange(n_start_conv, n_end_conv +1 , 1, dtype=int) # +1 để bao gồm n_end_conv
        elif model_id == "model5": 
            if n_start_conv > n_end_conv : n_start_conv, n_end_conv = n_end_conv, n_start_conv
            if n_start_conv <= 0: n_start_conv = max(1, min_n_required)
            if n_end_conv <= n_start_conv: n_end_conv = n_start_conv + num_points_convergence 
            n_values_for_conv_loop = np.linspace(n_start_conv, n_end_conv, num_points_convergence, dtype=int)
        else: 
            if n_start_conv > n_end_conv: n_start_conv, n_end_conv = n_end_conv, n_start_conv
            if n_start_conv <= 0 and n_end_conv > 0: n_start_conv = 1 
            if n_start_conv == n_end_conv and n_start_conv <= 0: return None # Không có dải N hợp lệ
            if n_end_conv >= n_start_conv > 0:
                target_points_conv = 20 # Hoặc num_points_convergence
                range_n_conv = n_end_conv - n_start_conv
                step_n_conv = 1
                if range_n_conv > 0 and target_points_conv > 0:
                     step_n_conv = max(1, int(np.ceil(range_n_conv / target_points_conv)))
                n_values_for_conv_loop = np.arange(n_start_conv, n_end_conv + 1, step_n_conv, dtype=int) # +1 để bao gồm n_end_conv
        
        if len(n_values_for_conv_loop) == 0:
            if n_start_conv > 0: n_values_for_conv_loop = np.array([n_start_conv],dtype=int)
            else: print("Error: n_values_for_conv_loop is empty after generation."); return None
        
        n_values_filtered_conv = np.unique(n_values_for_conv_loop[n_values_for_conv_loop >= min_n_required])
        
        if len(n_values_filtered_conv) < 2:
            print(f"    Warning: Not enough N values ({len(n_values_filtered_conv)}) for convergence plot after filtering >= {min_n_required}.")
        else:
            print(f"    Convergence loop N values (original, filtered): Range [{n_values_filtered_conv[0]}, {n_values_filtered_conv[-1]}], Points: {len(n_values_filtered_conv)}")
            for n_conv_original in n_values_filtered_conv:
                n_eff_conv_sim = n_conv_original 
                h_for_logplot_conv = 0.0
                # Logic nhân N hiệu quả cho các model khác nhau (nếu có)
                if model_id == 'model2': n_eff_conv_sim = n_conv_original * 2
                elif model_id == 'model3': n_eff_conv_sim = n_conv_original * 10
                elif model_id == 'model4': n_eff_conv_sim = n_conv_original * 2
                # Model 5 và Model 1/Default sử dụng n_conv_original trực tiếp cho n_eff_conv_sim

                if n_eff_conv_sim > 0: h_for_logplot_conv = interval_length / n_eff_conv_sim
                else: continue

                n_eff_conv_sim = max(n_eff_conv_sim, min_n_required)
                t_conv_loop = np.linspace(t_start, t_end, n_eff_conv_sim + 1)
                if len(t_conv_loop) < steps_int + 1: continue

                try:
                    if is_system:
                        u1_approx_conv_loop, u2_approx_conv_loop = method_func_for_screen2(ode_func, t_conv_loop, y0[0], y0[1])
                        y_approx_conv_u1_selected_loop = u1_approx_conv_loop if selected_component == 'x' else u2_approx_conv_loop
                    else:
                        y_approx_conv_loop = method_func_for_screen2(ode_func, t_conv_loop, y0)
                        y_approx_conv_u1_selected_loop = y_approx_conv_loop
                    
                    y_exact_conv_u1_selected_loop = None
                    if model_id == "model5" and uses_rk5_reference and rk5_ref_for_screen2:
                        rk5_ref_x_conv_loop, rk5_ref_y_conv_loop = rk5_ref_for_screen2(ode_func, t_conv_loop, y0[0], y0[1])
                        y_exact_conv_u1_selected_loop = rk5_ref_x_conv_loop if selected_component == 'x' else rk5_ref_y_conv_loop
                    elif exact_sol_func and len(t_conv_loop) > 0:
                        if is_system:
                            exact_tuple_loop = exact_sol_func(t_conv_loop)
                            if exact_tuple_loop is not None and len(exact_tuple_loop) == 2:
                                y_exact_conv_u1_selected_loop = exact_tuple_loop[0] 
                        else:
                            y_exact_conv_u1_selected_loop = exact_sol_func(t_conv_loop)

                    if y_approx_conv_u1_selected_loop is None or y_exact_conv_u1_selected_loop is None : continue
                    # ... (phần khớp độ dài, tính lỗi, và thêm vào list như cũ) ...
                    y_approx_conv_u1_selected_loop = np.asarray(y_approx_conv_u1_selected_loop)
                    y_exact_conv_u1_selected_loop = np.asarray(y_exact_conv_u1_selected_loop)
                    approx_len_conv = len(y_approx_conv_u1_selected_loop)
                    exact_len_conv = len(y_exact_conv_u1_selected_loop)
                    min_len_conv_loop = min(approx_len_conv, exact_len_conv)
                    if min_len_conv_loop < 2: continue
                    approx_conv = y_approx_conv_u1_selected_loop[:min_len_conv_loop]
                    exact_conv = y_exact_conv_u1_selected_loop[:min_len_conv_loop]
                    error_conv = np.linalg.norm(exact_conv - approx_conv, np.inf)
                    if np.isfinite(error_conv) and error_conv > 1e-16 and h_for_logplot_conv > 1e-16:
                        errors_convergence.append(error_conv)
                        n_values_plotted.append(n_conv_original)
                        h_values_for_loglog_list.append(h_for_logplot_conv)
                    else:
                        print(f"    Skipping error point for N_orig={n_conv_original}: error={error_conv}, h_for_logplot={h_for_logplot_conv}")


                except Exception as e_conv_loop:
                     print(f"    Error during convergence step N_orig={n_conv_original}, N_eff={n_eff_conv_sim}: {e_conv_loop}")
                     # import traceback; traceback.print_exc() # Bỏ comment để debug

        # --- Tính toán log và bậc hội tụ ---
        valid_h_for_loglog = np.array(h_values_for_loglog_list) 
        if len(errors_convergence) >= 2 and len(valid_h_for_loglog) == len(errors_convergence):
                try:
                    h_log_array = valid_h_for_loglog
                    err_log_array = np.array(errors_convergence)
                    # Lọc bỏ các giá trị không hợp lệ cho log
                    valid_indices_log = np.where((h_log_array > 1e-16) & (err_log_array > 1e-16) & np.isfinite(h_log_array) & np.isfinite(err_log_array))[0]
                    
                    if len(valid_indices_log) >= 2:
                        log_h_conv = np.log(h_log_array[valid_indices_log])
                        log_err_conv = np.log(err_log_array[valid_indices_log])
                        
                        if len(log_h_conv) >= 2: # Cần ít nhất 2 điểm để polyfit
                            coeffs = np.polyfit(log_h_conv, log_err_conv, 1)
                            slope = coeffs[0]
                            print(f"    Convergence analysis: Found {len(log_h_conv)} valid log points. Est. order: {slope:.3f}")
                        else:
                            print(f"    Warning: Not enough finite log values for polyfit ({len(log_h_conv)} points).")
                            slope = np.nan
                    else:
                        print("    Warning: Less than 2 valid points after filtering for log calculation.")
                        slope = np.nan
                except Exception as fit_e:
                    print(f"    Error during polyfit: {fit_e}")
                    slope = np.nan
        else:
            print(f"    Warning: Not enough points for convergence analysis (errors: {len(errors_convergence)}, valid_h: {len(valid_h_for_loglog)}).")
            slope = np.nan
            
        return {
            "t_plot": np.asarray(t_plot),
            "exact_sol_plot": np.asarray(y_exact_plot_u1) if y_exact_plot_u1 is not None else None,
            "approx_sol_plot": np.asarray(y_approx_plot_u1) if y_approx_plot_u1 is not None else None,
            "exact_sol_plot_all_components": y_exact_plot_all_components,
            "approx_sol_plot_all_components": y_approx_plot_all_components,
            "h_values_for_loglog": valid_h_for_loglog, # Đã là np.array
            "errors_convergence": np.array(errors_convergence),
            "log_h_convergence": log_h_conv, # Đã là np.array
            "log_error_convergence": log_err_conv, # Đã là np.array
            "order_slope": slope,
            "n_values_convergence": np.array(n_values_plotted),
            "h_actual_plot": h_actual_plot,
            "n_plot": n_plot,
            "selected_component": selected_component
        }

    def _update_plots_multi_steps(self, results_dict, method_short, exact_callable, selected_component='x'): # Thêm selected_component
        if not results_dict:
            self._setup_initial_plots()
            return
        try:
            fs = 7; font = {'size': fs}
            n_steps = len(results_dict)
            colors = plt.cm.jet(np.linspace(0, 1, max(1, n_steps)))
            is_model5 = self.current_model_data.get("id") == "model5"
            comp_suffix = f" ({selected_component.upper()})" if is_model5 else ""
            rk5_ref_suffix = f" ({selected_component.upper()}-Ref RK5)" if is_model5 else ""

            # Chọn key dựa trên component cho các trục Y
            sol_ylabel_key = f"screen2_plot_value_axis_{selected_component}" if is_model5 else "screen2_plot_value_axis_base"
            err_ylabel_key = f"screen2_plot_error_axis_{selected_component}" if is_model5 else "screen2_plot_error_axis_base"
            ord_ylabel_key = f"screen2_plot_log_error_axis_{selected_component}" if is_model5 else "screen2_plot_log_error_axis_base"

            # <<< Lấy thông tin scale >>>
            plot_configs = [
                (self.canvas_solution, self.tr("screen2_plot_t_axis"), self.tr(sol_ylabel_key), 'linear', 'linear', False), # Dùng sol_ylabel_key đã dịch
                (self.canvas_error, self.tr("screen2_plot_n_axis"), self.tr(err_ylabel_key), 'linear', 'log', False),      # Dùng err_ylabel_key đã dịch
                (self.canvas_error_order, self.tr("screen2_plot_log_h_axis"), self.tr(ord_ylabel_key), 'linear', 'linear', False) # Dùng ord_ylabel_key đã dịch
            ]
            # Lấy scale cho từng plot
            _, sol_xlabel_text, sol_ylabel_text, sol_xscale, sol_yscale, _ = plot_configs[0]
            _, err_xlabel_text, err_ylabel_text, err_xscale, err_yscale, _ = plot_configs[1]
            _, ord_xlabel_text, ord_ylabel_text, ord_xscale, ord_yscale, _ = plot_configs[2]

            # --- 1. Solution Plot ---
            ax_sol = self.canvas_solution.axes
            ax_sol.clear(); color_idx = 0; exact_plotted = False
            for step, res in results_dict.items():
                t = res.get("t_plot"); ap = res.get("approx_sol_plot"); ex = res.get("exact_sol_plot")
                if not exact_plotted and ex is not None and t is not None and len(t) == len(ex):
                     exact_label = self.tr("screen2_plot_exact_label") + rk5_ref_suffix
                     ax_sol.plot(t, ex, color='black', lw=1, ls='--') # <<< Bỏ label ở đây
                     exact_plotted = True
                if t is not None and ap is not None and len(t) == len(ap):
                    ax_sol.plot(t, ap, color=colors[color_idx % len(colors)], lw=1, marker='.', ms=2, ls='-') # <<< Bỏ label ở đây
                    color_idx += 1
            ax_sol.set_xlabel(self.tr("screen2_plot_t_axis"), fontsize=fs)
            ax_sol.set_ylabel(sol_ylabel_text, fontsize=fs)
            ax_sol.grid(True, linestyle=':', alpha=0.7)
            ax_sol.tick_params(axis='both', which='major', labelsize=fs) # Giảm size tick label
            # if ax_sol.get_lines(): ax_sol.legend(...) # <<< BỎ DÒNG NÀY >>>
            self.canvas_solution.fig.tight_layout(pad=0.8) # Giảm padding
            self.canvas_solution.draw()

            # --- 2. Error Plot ---
            ax_err = self.canvas_error.axes
            ax_err.clear(); plotted = False; color_idx = 0; min_n, max_n = float('inf'), float('-inf')
            for step, res in results_dict.items():
                n_vals = res.get("n_values_convergence"); err = res.get("errors_convergence")
                if n_vals is not None and err is not None and len(n_vals) == len(err) > 0:
                    mask = (err > 1e-16) & np.isfinite(err) & np.isfinite(n_vals)
                    if np.any(mask):
                        valid_n, valid_err = n_vals[mask], err[mask]
                        if len(valid_n) > 0: min_n = min(min_n, np.min(valid_n)); max_n = max(max_n, np.max(valid_n))
                        ax_err.plot(valid_n, valid_err, color=colors[color_idx % len(colors)], lw=1, marker='.', ms=2, ls='-',markevery = 0.1) # <<< Bỏ label, đổi marker
                        plotted = True; color_idx += 1
            # ax_err.set_title(...) # <<< BỎ DÒNG NÀY >>>
            ax_err.set_xlabel(self.tr("screen2_plot_n_axis"), fontsize=fs)
            ax_err.set_ylabel(err_ylabel_text, fontsize=fs)
            ax_err.set_xscale(err_xscale) # <<< THÊM: Đặt xscale từ config
            ax_err.set_yscale(err_yscale) 
            ax_err.grid(True, linestyle=':', alpha=0.7, which='major')
            if err_yscale == 'log': # Chỉ thêm grid phụ nếu là log scale
                ax_err.grid(True, which='minor', linestyle=':', alpha=0.2)
            ax_err.tick_params(axis='both', which='major', labelsize=fs) # Giảm size tick label
            # if plotted: ax_err.legend(...) # <<< BỎ DÒNG NÀY >>>
            self.canvas_error.fig.tight_layout(pad=0.8) # Giảm padding
            self.canvas_error.draw()

            # --- 3. Order Plot ---
            ax_ord = self.canvas_error_order.axes
            ax_ord.clear(); plotted = False; color_idx = 0
            for step, res in results_dict.items():
                log_h = res.get("log_h_convergence"); log_err = res.get("log_error_convergence"); slope = res.get("order_slope")
                if log_h is not None and log_err is not None and len(log_h) == len(log_err) >= 2 and np.isfinite(slope):
                     mask = np.isfinite(log_h) & np.isfinite(log_err)
                     if np.any(mask):
                         log_h_valid, log_err_valid = log_h[mask], log_err[mask]
                         if len(log_h_valid) >= 2:
                            inter = np.mean(log_err_valid) - slope * np.mean(log_h_valid)
                            ax_ord.plot(log_h_valid, slope * log_h_valid + inter, color=colors[color_idx % len(colors)], marker='.',ls='-', lw=1, ms=2,markevery = 0.1) # <<< Bỏ label, đổi marker
                            plotted = True; color_idx += 1
            # ax_ord.set_title(...) # <<< BỎ DÒNG NÀY >>>
            ax_ord.set_xlabel(self.tr("screen2_plot_log_h_axis"), fontsize=fs)
            ax_ord.set_ylabel(ord_ylabel_text, fontsize=fs)
            ax_ord.set_xscale(ord_xscale) # <<< THÊM
            ax_ord.set_yscale(ord_yscale) 
            ax_ord.grid(True, linestyle=':', alpha=0.7)
            ax_ord.tick_params(axis='both', which='major', labelsize=fs) # Giảm size tick label
            # if plotted: ax_ord.legend(...) # <<< BỎ DÒNG NÀY >>>
            self.canvas_error_order.fig.tight_layout(pad=0.8) # Giảm padding
            self.canvas_error_order.draw()

            # --- Cập nhật Legend NGOÀI (Nếu vẫn muốn giữ) ---
            self._update_method_legend(results_dict, method_short, colors)
            # Hoặc nếu muốn bỏ hẳn legend ngoài:
            # if hasattr(self, 'method_legend_container'): self.method_legend_container.setVisible(False)


        except Exception as e:
            print(f"Error updating plots: {e}")
            import traceback; traceback.print_exc()
            if hasattr(self, 'method_legend_container'): self.method_legend_container.setVisible(False)

    @Slot()
    def _refresh_data(self):
        print("Refreshing UI...")
        if self.simulation_window and self.simulation_window.isVisible():
            self.simulation_window.close()
            self.simulation_window=None
        # Clear parameter inputs and reset style
        for le in self.param_inputs.values():
            le.clear()
            le.setStyleSheet("") # Reset background/border
        # Reset step checkboxes (e.g., check step 4 by default if available)
        if self.calculated_c_display_widget:
            self.calculated_c_display_widget.setText("")
            self.calculated_c_display_widget.setText(self.tr("N/A","N/A")) # Hoặc clear()
        self._last_calculated_c = None # Reset giá trị c đã lưu
        if self.calculated_r_display_widget: # Thêm cho r
            self.calculated_r_display_widget.setText("") # Clear display
            self.calculated_r_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
        self._last_calculated_r = None
        if hasattr(self, 'calculated_alpha_display_widget') and self.calculated_alpha_display_widget:
            self.calculated_alpha_display_widget.setText("")
            self.calculated_alpha_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
        self._last_calculated_alpha = None
        if hasattr(self, 'calculated_beta_display_widget') and self.calculated_beta_display_widget:
            self.calculated_beta_display_widget.setText("")
            self.calculated_beta_display_widget.setPlaceholderText(self.tr("N/A","N/A"))
        self._last_calculated_beta = None

        cb4=self.step_checkboxes.get("step4")
        step_checked = False
        if cb4 and cb4.isVisible():
             # Uncheck all first
             for cb in self.step_checkboxes.values(): cb.setChecked(False)
             cb4.setChecked(True)
             step_checked = True
        if not step_checked: # Fallback to checking the first visible checkbox
             first_visible_cb_set = False
             for i, cb in enumerate(self.step_checkboxes.values()):
                  if cb.isVisible():
                      cb.setChecked(not first_visible_cb_set) # Check only the first one found
                      first_visible_cb_set = True
                  else:
                      cb.setChecked(False) # Ensure hidden ones are unchecked

        # Reset h radio buttons (e.g., check 0.01 by default if available)
        h001=self.h_radio_buttons.get("0.01")
        if h001:
            # No need to loop, just set the specific one
            h001.setChecked(True)
        else: # Fallback to checking the first radio button
             first_rb = next(iter(self.h_radio_buttons.values()), None)
             if first_rb:
                 first_rb.setChecked(True)
        #self.show_simulation_checkbox.setChecked(False)
        # Reset simulation checkbox
        #self.show_simulation_checkbox.setChecked(False)
        # Clear plots and results
        if hasattr(self, 'btn_go_to_screen3'):
            self.btn_go_to_screen3.setVisible(False)
            self.btn_go_to_screen3.setEnabled(False)
        self.dynamic_plot_data = None
        self._update_select_all_checkbox_status()
        self._setup_initial_plots()
        self.last_results_dict={}
        # Update info area
        self.info_text_area.setText(self.tr("screen2_info_area_refreshed"))
        print("Refresh complete.")

    @Slot()
    def _show_data(self):
        print("Showing numerical data (detailed for all steps)...") # Update print message
        if not self.last_results_dict:
            self.info_text_area.setText(self.tr("screen2_info_area_no_show_data"))
            QMessageBox.information(self,self.tr("msg_info"),self.tr("msg_show_data_no_data"))
            return

        model_id = self.current_model_data.get("id")
        current_lang = self.main_window.current_language
        is_model5 = (model_id == "model5")

        model_name_tr=self.tr(f"{model_id}_name",self.current_model_vi_key)
        # ================== HIGHLIGHT START: Chỉ thêm tiêu đề model 1 lần ==================
        if model_id == "model5" and current_lang == 'vi':
            data_str=f"{model_name_tr}\n"+ "="*56+"\n"
        elif model_id == "model5" and current_lang == 'en':
            data_str=f"{model_name_tr}\n"+ "="*55+"\n"
        elif current_lang == 'vi':
            data_str=f"{model_name_tr}\n"+ "="*60+"\n"
        else:
            data_str=f"{model_name_tr}\n"+ "="*60+"\n"
        # ================== HIGHLIGHT END ==================

        # ================== HIGHLIGHT START: Lặp qua tất cả các bước ==================
        for step, res in self.last_results_dict.items(): # Lặp qua tất cả các kết quả
            header_line = "" # Reset header cho mỗi bước

            # --- Hiển thị thông tin chung cho BƯỚC HIỆN TẠI ---
            method_btn = self.method_button_group.checkedButton()
            method_name = method_btn.objectName() if method_btn else "Unknown"
            selected_component = res.get("selected_component", 'x') # Lấy component từ kết quả của bước này
            comp_suffix = f" ({selected_component.upper()}-Component)" if is_model5 else ""

            # Thêm dòng tóm tắt cho bước này
            data_str+=f"{self.tr('screen2_info_area_show_data_method')} Adam-{method_name} {step} {self.tr('screen2_info_area_show_data_textCont1')}{comp_suffix} " # Thêm dòng phân cách
            h, sl = res.get('h_actual_plot','N/A'), res.get('order_slope',np.nan)
            data_str+=f"{self.tr('screen2_info_area_show_data_textCont2')} h={h:.4g}\n" # Chỉ hiển thị h
            
            if not np.isnan(sl): data_str+=f"{self.tr('screen2_info_area_show_data_order')} {sl:.4f}\n"
            else: data_str+=f", {self.tr('screen2_info_area_show_data_order')} N/A\n"
            data_str+="\n" # Thêm dòng trống trước bảng

            # --- Tạo bảng chi tiết cho BƯỚC HIỆN TẠI ---
            t = res.get('t_plot')
            ap_selected = res.get('approx_sol_plot')
            ex_selected = res.get('exact_sol_plot')
            ap_all = res.get('approx_sol_plot_all_components')
            ex_all = res.get('exact_sol_plot_all_components')

            if t is not None and ap_selected is not None:
                max_p=15 # Số điểm tối đa hiển thị trong bảng
                num_points = len(t)
                if num_points > 0:
                    idx=np.linspace(0,num_points-1,min(max_p,num_points),dtype=int)

                    time_pos = 0
                    approx_pos = 0 # Sẽ được cập nhật sau khi có exact_pos
                    exact_ref_pos = 0 # Sẽ được cập nhật sau
                    error_pos = 0

                    # --- Tạo header động (logic giữ nguyên) ---
                    time_hdr = self.tr('screen2_info_area_show_data_time')
                    
                    # --- HIGHLIGHT START: Điều chỉnh độ rộng cột cho Model 5 ---
                    if is_model5 and current_lang == 'vi':
                        # Giảm độ rộng cột cho Model 5 để vừa vặn hơn
                        # Thử nghiệm các giá trị này:
                        header_col_time_width = 10  # Giữ nguyên hoặc giảm nếu cần
                        header_col_exact_width = 18 # Tăng nhẹ cho tên cột "Tham chiếu X (RK5)"
                        header_col_approx_width = 14 # Giảm cho "Xấp xỉ X"
                        header_col_error_width = 14  # Giảm cho "Sai số X"

                        data_col_time_width = header_col_time_width
                        data_col_exact_width = header_col_exact_width  # Dữ liệu thường ngắn hơn header
                        data_col_approx_width = header_col_approx_width 
                        data_col_error_width = header_col_error_width
                    elif is_model5 and current_lang == 'en':
                        header_col_time_width = 10  # Giữ nguyên hoặc giảm nếu cần
                        header_col_exact_width = 18 # Tăng nhẹ cho tên cột "Tham chiếu X (RK5)"
                        header_col_approx_width = 14 # Giảm cho "Xấp xỉ X"
                        header_col_error_width = 14  # Giảm cho "Sai số X"

                        data_col_time_width = header_col_time_width
                        data_col_exact_width = header_col_exact_width # Dữ liệu thường ngắn hơn header
                        data_col_approx_width = header_col_approx_width 
                        data_col_error_width = header_col_error_width
                    else:
                        # Độ rộng cho các model khác (có thể giữ nguyên hoặc điều chỉnh từ code cũ của bạn)
                        header_col_time_width = 12
                        header_col_exact_width = 18
                        header_col_approx_width = 18
                        header_col_error_width = 12

                        data_col_time_width = header_col_time_width
                        data_col_exact_width = header_col_exact_width
                        data_col_approx_width = header_col_approx_width
                        data_col_error_width = header_col_error_width
                    # --- HIGHLIGHT END ---

                    header_line = f"{time_hdr:<{header_col_time_width}}" # Sử dụng độ rộng đã định nghĩa

                    if is_model5:
                        if selected_component == 'x':
                            exact_hdr = self.tr('screen2_info_area_show_data_exact_x')
                            approx_hdr = self.tr('screen2_info_area_show_data_approx_x')
                            error_hdr = self.tr('screen2_info_area_show_data_error_x')
                        elif selected_component == 'y':
                            exact_hdr = self.tr('screen2_info_area_show_data_exact_y')
                            approx_hdr = self.tr('screen2_info_area_show_data_approx_y')
                            error_hdr = self.tr('screen2_info_area_show_data_error_y')
                        # --- HIGHLIGHT: Sử dụng độ rộng đã định nghĩa cho header Model 5 ---
                        header_line += f" {exact_hdr:<{header_col_exact_width}} {approx_hdr:<{header_col_approx_width}} {error_hdr:<{header_col_error_width}}"
                    elif ex_selected is not None: 
                        exact_hdr = self.tr('screen2_info_area_show_data_exact')
                        approx_hdr = self.tr('screen2_info_area_show_data_approx')
                        error_hdr = self.tr('screen2_info_area_show_data_error')
                        # --- HIGHLIGHT: Sử dụng độ rộng đã định nghĩa cho header model khác ---
                        header_line += f" {exact_hdr:<{header_col_exact_width}} {approx_hdr:<{header_col_approx_width}} {error_hdr:<{header_col_error_width}}"
                    else: 
                        approx_hdr = self.tr('screen2_info_area_show_data_approx')
                        header_line += f" {approx_hdr:<{header_col_approx_width}}"

                    # --- Thêm tiêu đề bảng và dòng kẻ ---
                    #table_title = f"{self.tr('screen2_info_area_show_data_points_header')}"
                    #title_padding = max(0, (len(header_line) - len(table_title)) // 2)
                    #data_str+="-"* title_padding + table_title + "-"* (len(header_line) - len(table_title) - title_padding) +"\n"
                    #data_str+=header_line+"\n"
                    #data_str+="-"*len(header_line)+"\n"

                    # --- Thêm tiêu đề bảng và dòng kẻ ---
                    if model_id == "model5" and current_lang == 'vi':
                        table_title = self.tr('screen2_info_area_show_data_points_header')
                        data_str += '-'*22 + table_title + '-'*22 + "\n"
                        data_str+=header_line+"\n"
                        data_str+='-'*55 + "\n"
                    elif model_id == "model5" and current_lang == 'en':
                        table_title = self.tr('screen2_info_area_show_data_points_header')
                        data_str += '-'*20 + table_title + '-'*21 + "\n"
                        data_str+=header_line+"\n"
                        data_str+='-'*55 + "\n"
                    elif current_lang == 'vi':
                        table_title = f"{self.tr('screen2_info_area_show_data_points_header')}"
                        data_str += '-'*25 + table_title + '-'*25 + "\n"
                        data_str+=header_line+"\n"
                        data_str+="-"*61+"\n"
                    else:
                        table_title = f"{self.tr('screen2_info_area_show_data_points_header')}"
                        data_str += '-'*24 + table_title + '-'*23 + "\n"
                        data_str+=header_line+"\n"
                        data_str+="-"*61+"\n"
                    # --- Thêm dữ liệu động (logic giữ nguyên) ---
                    for i in idx:
                        if i < len(t):
                            time_val = t[i]
                            # --- HIGHLIGHT: Sử dụng độ rộng data_col... ---
                            line = f"{time_val:<{data_col_time_width}.4f}" 

                            if is_model5 and ap_all and ex_all:
                                if selected_component == 'x' and i < len(ex_all[0]) and i < len(ap_all[0]):
                                    ex_v = ex_all[0][i]; ax_v = ap_all[0][i]
                                    err_x = abs(ax_v - ex_v)
                                    # --- HIGHLIGHT: Sử dụng độ rộng data_col... và format số phù hợp ---
                                    line += f" {ex_v:<{data_col_exact_width}.8f} {ax_v:<{data_col_approx_width}.6f} {err_x:<{data_col_error_width}.3e}"
                                elif selected_component == 'y' and i < len(ex_all[1]) and i < len(ap_all[1]):
                                    ey_v = ex_all[1][i]; ay_v = ap_all[1][i]
                                    err_y = abs(ay_v - ey_v)
                                    line += f" {ey_v:<{data_col_exact_width}.8f} {ay_v:<{data_col_approx_width}.6f} {err_y:<{data_col_error_width}.3e}"
                                else: continue
                            elif i < len(ap_selected): # Các model khác
                                approx_val = ap_selected[i]
                                if ex_selected is not None and i < len(ex_selected):
                                    exact_val = ex_selected[i]
                                    err_val = abs(approx_val - exact_val)
                                    # --- HIGHLIGHT: Sử dụng độ rộng data_col... ---
                                    line += f" {exact_val:<{data_col_exact_width}.8f} {approx_val:<{data_col_approx_width}.8f} {err_val:<{data_col_error_width}.3e}"
                                else: 
                                    line += f" {approx_val:<{data_col_approx_width}.8f}"
                            else: continue

                            data_str+=line+"\n"
                        # --- Kết thúc thêm dòng dữ liệu ---
                else: data_str+=f"  {self.tr('screen2_info_area_show_data_no_points')}\n"

                if header_line: 
                    if model_id == "model5" and current_lang == 'vi':
                        data_str+="-"*56 + "\n"
                    elif model_id == "model5" and current_lang == 'en':
                        data_str+="-"*55 + "\n"
                    else:
                        data_str+="-"*61+"\n" # Dòng kẻ cuối bảng
            else: data_str+=f"  {self.tr('screen2_info_area_show_data_no_points')}\n"

            data_str+="\n" # Thêm dòng trống ngăn cách giữa các bước

        

        self.info_text_area.setText(data_str)
        print("Numerical data displayed (detailed table for all selected steps).") # Update print message

    @Slot()
    def _save_data(self):
        # (Logic giữ nguyên, chỉ dùng self.tr)
        print("--- Starting Plot Save ---")
        has_plots=any(c.axes and (c.axes.get_lines() or c.axes.collections) for c in [self.canvas_solution,self.canvas_error,self.canvas_error_order])
        if not has_plots:
            QMessageBox.information(self,self.tr("msg_info"),self.tr("msg_save_no_plots"))
            return

        # Build filename components
        method_btn = self.method_button_group.checkedButton()
        method = method_btn.objectName() if method_btn else "UnknownMethod"
        steps=[cb.text().split()[0] for k,cb in self.step_checkboxes.items() if cb.isChecked() and cb.isVisible()]
        steps_str=f"Steps{'_'.join(steps)}" if steps else "Steps_None"
        h_str="h_unknown"
        if self.last_results_dict:
             # Try to get h from the first result, format nicely
             first_res = next(iter(self.last_results_dict.values()), {})
             h_act = first_res.get("h_actual_plot")
             if h_act is not None: # Check if h_act was found
                 h_str=f"h{h_act:.2g}".replace(".","p") # Use scientific notation for small h, replace dot
        elif self.h_button_group.checkedButton(): # Fallback to selected h radio button
             h_str=f"h{self.h_button_group.checkedButton().text()}".replace(".","p")

        model_id=self.current_model_data.get("id","UnknownModel")
        # Clean up model name for filename
        model_name_tr=self.tr(f"{model_id}_name",model_id).split(":")[0].strip().replace(" ","_").replace("(","").replace(")","")
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name=f"{model_name_tr}_{method}_{steps_str}_{h_str}_{ts}"

        # Get save directory
        save_dir=QFileDialog.getExistingDirectory(self,self.tr("msg_save_select_dir"),os.path.expanduser("~"),QFileDialog.Option.ShowDirsOnly)
        if not save_dir:
            print(self.tr("msg_save_cancelled"))
            return

        # Define plots to save
        plots_to_save=[
             (self.canvas_solution,"solution"),
             (self.canvas_error,"error_vs_h"),
             (self.canvas_error_order,"order_loglog")
        ]
        saved_count, errors = 0, [] # Initialize counters/lists

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            for canvas, suffix in plots_to_save:
                # Check if the plot actually contains data
                if canvas.axes and (canvas.axes.get_lines() or canvas.axes.collections or canvas.axes.patches): # Added patches check
                    fpath = os.path.join(save_dir, f"{base_name}_{suffix}.png")
                    try:
                        # Save with higher DPI and tight bounding box
                        canvas.fig.savefig(fpath, dpi=200, bbox_inches='tight')
                        print(f"Saved: {fpath}")
                        saved_count += 1
                    except Exception as e:
                        # Format error message using translated string
                        error_format_string = self.tr("msg_saving_plot_error")
                        formatted_error_msg = error_format_string.format(suffix, e)
                        print(formatted_error_msg)
                        errors.append(formatted_error_msg)
                else:
                    # Skip saving empty plots, inform user
                    print(self.tr("msg_skipping_save").format(suffix))
        finally:
            QApplication.restoreOverrideCursor()

        # Show summary message
        if saved_count > 0 and not errors:
            QMessageBox.information(self,self.tr("msg_save_success_title"),self.tr("msg_save_success_text").format(saved_count,save_dir))
        elif saved_count > 0 and errors:
            QMessageBox.warning(self,self.tr("msg_save_error_title"),self.tr("msg_save_error_text").format(saved_count,"\n".join(errors)))
        elif errors: # Only errors occurred
            QMessageBox.critical(self,self.tr("msg_save_fail_title"),self.tr("msg_save_fail_text").format("\n".join(errors)))
        # No message if nothing was saved and no errors occurred (e.g., all plots were skipped)

        print(f"--- Plot Saving Complete ({saved_count} saved) ---")


        self._stop_animation()
        super().closeEvent(event)

        self._stop_animation()
        super().closeEvent(event)

# ==============================================
#   NEW Cell Class for Model 2 Animation
# ==============================================
class Cell:
    def __init__(self, x, y, gen=0):
        self.x = x
        self.y = y
        self.gen = gen
        # last_division sẽ lưu frame_index của lần chia cuối
        self.last_division = -100

# ==============================================
#           Screen 3: Dynamic Simulation Plot Only
# ==============================================
class Screen3Widget(RetranslatableWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setObjectName("Screen3_DynamicPlot_Widget")
        # --- Thuộc tính chung ---
        self.current_simulation_type = None # 'model2' hoặc 'abm'
        self.ani = None
        self.is_simulation_running = False
        self.is_simulation_paused = False
        self.original_model2_data = None
        self.original_abm_params = None
        self.original_model5_data = None
        # Thêm cờ mới cho Model 5 Sim 1
        self.m5s1_animation_visually_finished = False
        # Thêm cờ tương tự cho Model 2 và ABM nếu cần
        self.model2_animation_visually_finished = False
        self.abm_simulation_visually_finished = False
        # --- Thuộc tính cho Model 2 (Cell Growth Animation) ---
        self.T_model2 = None # Đổi tên từ T_anim
        self.Y_model2 = None # Đổi tên từ Y_anim
        self.y0_model2 = None
        self.c_model2 = None
        self.method_label_model2 = ""
        
        self.t_start_model2 = 0
        self.t_end_model2 = 0
        # self.h_model2 = 0 # Không thấy sử dụng trực tiếp cho animation
        self.circles_model2 = []
        self.text_box_model2 = None
        self.model2_base_interval = 200  # Base interval for Model 2 at 1x speed
        self.model2_animation_interval = self.model2_base_interval
        self.num_animation_frames_model2 = 0
        #self.final_limit_model2 = 20
        #self.model2_anim_data = None # Store data to restart Model 2 animation
        # --- Thuộc tính MỚI hoặc ĐƯỢC SỬA ĐỔI cho Model 2 (Animation mới) ---
        self.model2_cells_list = [] # Danh sách các đối tượng Cell
        self.model2_cell_radius = 0.5 # Bán kính cố định như trong standalone
        self.model2_last_frame_processed = -1 # Theo dõi frame đã xử lý để tránh tính toán lặp lại khi pause/resume
        self.model2_min_division_interval = 10 
        # --- Thuộc tính cho Model 3 (ABM Simulation) ---
        self.last_speed_multiplier_for_abm_interval = None
        self.simulation_instance_abm = None
        self.abm_params = {}
        self.abm_scatter_susceptible = None
        self.abm_scatter_infected = None
        self.abm_base_interval = 120 # Base interval for ABM at 1x speed
        self.abm_animation_interval = self.abm_base_interval

        # HIGHLIGHT START: Model 5 specific
        self.model5_plot_data_cache = None # Cache data from Screen 2
        self.current_model5_sim_selected = 1 # 1 or 2
        # Widgets for Model 5 simulation list
        self.sim_list_group = None
        self.rb_model5_sim1 = None
        self.rb_model5_sim2 = None
        self.model5_sim_button_group = None
        # Labels for Model 5 Sim 1
        self.m5_boat_speed_label = None
        self.m5_boat_speed_value = None
        self.m5_water_speed_label = None
        self.m5_water_speed_value = None
        self.m5_crossing_time_label = None
        self.m5_crossing_time_value = None
        self.m5_start_point_boat_label = None
        self.m5_start_point_boat_value = None
        self.m5_boat_reaches_target_label = None
        self.m5_boat_reaches_target_value = None
        self.m5_boat_final_pos_label = None
        self.m5_boat_final_pos_value = None
        # HIGHLIGHT START: Attributes for Model 5, Simulation 1 (Boat Crossing)
        self.m5s1_params = {} # To store v_t, v_n, d, z0_anim, b_anim
        self.m5s1_t_array = None
        self.m5s1_z_array = None # Will store [x, y] trajectory

        self.m5s1_line_ship_path = None
        self.m5s1_point_ship = None
        self.m5s1_quiver_water = None
        self.m5s1_legend_obj = None
        self.m5s1_X_arrows_positions = None
        self.m5s1_Y_arrows_initial_positions = None
        self.m5s1_arrow_shift_per_frame = 0.005 # Default, can be adjusted
        self.m5s1_frames_for_arrows_to_drain = 0
        self.m5s1_num_frames_total_animation = 0

        # Animation state variables for m5s1
        self.m5s1_animation_fully_stopped = False
        self.m5s1_ship_has_docked = False
        self.m5s1_docking_frame_index_for_ship = -1
        self.m5s1_ship_journey_complete = False
        self.m5s1_frame_ship_interaction_ends = -1
        self.m5s1_Y_arrows_at_interaction_end = None
        self.m5s1_current_anim_frame = 0 # To track animation progress
        self.m5s1_base_interval = 50 # Animation interval for Sim 1
        self.m5s1_animation_interval = self.m5s1_base_interval
        # HIGHLIGHT END
# HIGHLIGHT START: Attributes for Model 5, Simulation 1 (Boat Crossing)
        self.m5s1_params = {} # To store v_t, v_n, d, z0_anim, b_anim
        self.m5s1_t_array = None
        self.m5s1_z_array = None # Will store [x, y] trajectory

        # Labels for Model 5 Sim 2
        self.m5_submarine_speed_value = None
        self.m5_destroyer_speed_value = None
        self.m5_submarine_trajectory_value = None
        self.m5_start_point_submarine_value = None
        self.m5_start_point_destroyer_value = None
        self.m5_destroyer_catches_submarine_value = None
        self.m5_catch_point_value = None
        self.m5_catch_time_value = None

        self.m5s1_line_ship_path = None
        self.m5s1_point_ship = None
        self.m5s1_quiver_water = None
        self.m5s1_legend_obj = None
        self.m5s1_X_arrows_positions = None
        self.m5s1_Y_arrows_initial_positions = None
        self.m5s1_arrow_shift_per_frame = 0.005 # Default, can be adjusted
        self.m5s1_frames_for_arrows_to_drain = 0
        self.m5s1_num_frames_total_animation = 0

        # Animation state variables for m5s1
        self.m5s1_animation_fully_stopped = False
        self.m5s1_ship_has_docked = False
        self.m5s1_docking_frame_index_for_ship = -1
        self.m5s1_ship_journey_complete = False
        self.m5s1_frame_ship_interaction_ends = -1
        self.m5s1_Y_arrows_at_interaction_end = None
        self.m5s1_current_anim_frame = 0 # To track animation progress
        self.m5s1_base_interval = 50 # Animation interval for Sim 1
        self.m5s1_animation_interval = self.m5s1_base_interval
        # HIGHLIGHT END

        # --- Thuộc tính cho Model 5 - Simulation 2 (Tàu khu trục - Tàu ngầm) ---
        self.m5s2_params = {} # Sẽ chứa các tham số như v_kt, z0_kt, simulation_duration
        self.m5s2_submarine_trajectory_params = { # Lưu các tham số quỹ đạo ngẫu nhiên của tàu ngầm
            "offset_x": 0.0, "offset_y": 0.0,
            "params_x": [], "params_y": []
        }
        self.m5s2_t_array_solver = None     # Mảng thời gian dùng cho solver
        self.m5s2_t_array_actual = None     # Mảng thời gian thực tế sau khi giải (có thể bị cắt ngắn nếu bắt được)
        self.m5s2_z_kt_array = None         # Quỹ đạo tàu khu trục [[x1,y1], [x2,y2], ...]
        self.m5s2_z_tn_array = None         # Quỹ đạo tàu ngầm (tính trên t_array_actual)
        self.m5s2_avoid_circle_tn_artist = None
        self.m5s2_kt_radar_circle_artist = None
        # Có thể thêm thuộc tính để lưu giá trị bán kính nếu chúng được tính động
        self.m5s2_current_avoidance_radius = 0.0
        self.m5s2_current_kt_radar_radius = 0.0

        self.m5s2_INITIAL_VIEW_LIMIT_APP = 50.0 # Giá trị mặc định, sẽ được cập nhật
        self.m5s2_current_view_span = self.m5s2_INITIAL_VIEW_LIMIT_APP
        self.m5s2_ZOOM_OUT_BOUNDARY_FACTOR_APP = 0.85 # Từ standalone
        self.m5s2_ZOOM_FACTOR_APP = 1.3    

        self.m5s2_caught_flag = False
        self.m5s2_time_of_catch = 0.0
        self.m5s2_catch_threshold = 0.05 # Ngưỡng để coi là bắt được
        self.m5s2_catch_point_coords = None # Tọa độ điểm bắt được

        # Artists cho animation Sim 2
        self.m5s2_line_tn = None
        self.m5s2_line_kt = None
        self.m5s2_point_tn = None
        self.m5s2_point_kt = None
        self.m5s2_catch_marker = None
        self.m5s2_legend_obj = None # Nếu bạn muốn legend riêng cho Sim 2

        self.m5s2_num_frames_total_animation = 0
        self.m5s2_animation_interval = 50 # ms, có thể điều chỉnh bằng slider
        self.m5s2_base_interval = 30    # Base interval for Model 5 Sim 2 at 1x speed
        self.m5s2_animation_visually_finished = False

        # --- Widgets (khai báo để _init_ui có thể truy cập) ---
        self.btn_back_to_screen2 = None
        self.btn_double_back_to_screen1 = None # Đổi tên cho rõ
        self.btn_stop = None
        self.canvas_simulation = None
        self.settings_group = None
        self.speed_slider_label = None
        self.speed_slider = None
        self.results_group = None
        self.result_time_label = None
        self.result_time_value = None
        self.result_c_label = None
        self.result_c_value = None
        self.result_mass_label = None
        self.result_mass_value = None
        self.result_r_label = None
        self.result_r_value = None
        self.result_expected_time_label = None
        self.result_expected_time_value = None
        self.result_actual_time_label = None      # Sẽ dùng chung self.result_time_label
        self.result_actual_time_value = None      # Sẽ dùng chung self.result_time_value
        self.result_total_pop_label = None
        self.result_total_pop_value = None
        self.result_infected_pop_label = None     # Sẽ dùng chung self.result_mass_label
        self.result_infected_pop_value = None     # Sẽ dùng chung self.result_mass_value
        self.result_susceptible_pop_label = None
        self.result_susceptible_pop_value = None
        self.title_label = None

        # HIGHLIGHT START: Khai báo các thuộc tính QLabel cho Model 2
        self.m2_c_value_label = None         # Label tĩnh "Hằng số tăng trưởng (c):"
        self.m2_c_value_display = None     # QLabel để hiển thị giá trị c
        self.m2_sim_time_label = None      # Label tĩnh "Thời gian mô phỏng:"
        self.m2_sim_time_display = None    # QLabel để hiển thị giá trị thời gian mô phỏng (t)
        self.m2_real_time_label = None     # Label tĩnh "Thời gian thực tế (giây):"
        self.m2_real_time_display = None   # QLabel để hiển thị giá trị thời gian thực
        self.m2_mass_label = None          # Label tĩnh "Số lượng tế bào:"
        self.m2_mass_display = None

        self._init_ui()
        self._connect_signals()
        self.retranslate_ui()

    def _init_ui(self):
        self.setStyleSheet("""
            QWidget#Screen3_DynamicPlot_Widget { /* Đổi tên objectName cho widget chính */
                background-color: #e0e7ff;
            }
            QGroupBox {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                margin-top: 1em;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 2px 8px;
                background-color: #6c757d;
                color: white;
                border-radius: 4px;
            }
            QLabel#screen3MainTitle {
                font-size: 24px;
                font-weight: bold;
                color: #343a40;
                padding: 10px;
            }
            QLabel.infoLabel {
                font-size: 11px;
                color: #212529;
            }
            QLabel#speedLabel {
                font-size: 11px;
                color: #212529;
            }
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QPushButton#screen3Button {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6c757d, stop:1 #5a6268);
                color: white;
                border: 1px solid #545b62;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton#screen3Button:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5a6268, stop:1 #495057);
            }
            QPushButton#screen3StopButton { /* Style cho nút Stop */
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dc3545, stop:1 #c82333); /* Màu đỏ */
                color: white;
                border: 1px solid #bd2130;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton#screen3StopButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c82333, stop:1 #bd2130);
            }
        """)

        main_layout_page = QVBoxLayout(self)
        main_layout_page.setContentsMargins(20, 10, 20, 20)
        main_layout_page.setSpacing(15)

        title_bar_layout = QHBoxLayout()
        self.btn_back_to_screen2 = QPushButton()
        self.btn_back_to_screen2.setObjectName("screen3Button") # Giữ style chung
        self.btn_back_to_screen2.setFont(QFont("Arial", 9))
        self.btn_back_to_screen2.setStyleSheet(""" QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ddeeff, stop:1 #3388cc); border: 2px solid #aabbcc; border-radius:10px; color:white; font-weight:bold; font-size:16px; padding:5px 10px;} QPushButton:hover{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeffff, stop:1 #4499dd); border-color:#cceeff;} QPushButton:pressed{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aaddff, stop:1 #2277bb); border-color:#88aabb; padding-top:6px; padding-bottom:4px;} """)

        title_bar_layout.addWidget(self.btn_back_to_screen2)
        self.btn_go_to_screen3 = QPushButton()
        self.btn_go_to_screen3.setVisible(False) # <<< ẨN BAN ĐẦU

        self.title_label = QLabel()
        self.title_label.setObjectName("screen3MainTitle") # Đổi objectName
        self.title_label.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #191970; padding: 4px;")
        title_bar_layout.addStretch(1)
        title_bar_layout.addWidget(self.title_label)
        title_bar_layout.addStretch(1)

        self.btn_double_back_to_screen1 = QPushButton() # Đổi tên biến
        self.btn_double_back_to_screen1.setObjectName("screen3Button") # Giữ style chung
        self.btn_double_back_to_screen1.setFont(QFont("Arial", 9))
        self.btn_double_back_to_screen1.setStyleSheet(""" QPushButton { background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ddeeff, stop:1 #3388cc); border: 2px solid #aabbcc; border-radius:10px; color:white; font-weight:bold; font-size:16px; padding:5px 10px;} QPushButton:hover{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeffff, stop:1 #4499dd); border-color:#cceeff;} QPushButton:pressed{background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #aaddff, stop:1 #2277bb); border-color:#88aabb; padding-top:6px; padding-bottom:4px;} """)

        title_bar_layout.addWidget(self.btn_double_back_to_screen1)
        main_layout_page.addLayout(title_bar_layout)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(20)
        left_column_layout = QVBoxLayout()
        left_column_layout.setSpacing(15)

        self.settings_group = QGroupBox()
        settings_content_layout = QVBoxLayout(self.settings_group)
        settings_content_layout.setContentsMargins(15, 25, 15, 15)
        settings_content_layout.setSpacing(8)

        self.speed_slider_label = QLabel()
        self.speed_slider_label.setObjectName("speedLabel")
        settings_content_layout.addWidget(self.speed_slider_label)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(5)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(10)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(10)
        settings_content_layout.addWidget(self.speed_slider)

        speed_range_layout = QHBoxLayout()
        min_speed_label = QLabel("0.5x")
        min_speed_label.setObjectName("speedLabel")
        max_speed_label = QLabel("10.0x")
        max_speed_label.setObjectName("speedLabel")

        speed_range_layout.addWidget(min_speed_label, 0, Qt.AlignmentFlag.AlignLeft)
        speed_range_layout.addStretch(1)
        speed_range_layout.addWidget(max_speed_label, 0, Qt.AlignmentFlag.AlignRight)
        settings_content_layout.addLayout(speed_range_layout)
        
        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("screen3StopButtonGray") # objectName mới cho style
        self.btn_stop.setEnabled(False)
        #left_column_layout.addWidget(self.btn_stop) # Thêm nút Stop vào cột trái
        settings_content_layout.addWidget(self.btn_stop)
        left_column_layout.addWidget(self.settings_group)
        
        #HIGHLIGHT START: Simulation List Group (for Model 5)
        self.sim_list_group = QGroupBox()
        self.sim_list_group.setObjectName("simulationListGroup") # For potential styling
        sim_list_layout = QVBoxLayout(self.sim_list_group)
        sim_list_layout.setContentsMargins(10, 20, 10, 10)
        sim_list_layout.setSpacing(5)

        self.model5_sim_button_group = QButtonGroup(self) # Ensure exclusive selection
        self.rb_model5_sim1 = QRadioButton()
        self.model5_sim_button_group.addButton(self.rb_model5_sim1)
        sim_list_layout.addWidget(self.rb_model5_sim1)

        self.rb_model5_sim2 = QRadioButton()
        self.model5_sim_button_group.addButton(self.rb_model5_sim2)
        sim_list_layout.addWidget(self.rb_model5_sim2)
        self.sim_list_group.setVisible(False) # Hidden by default
        left_column_layout.addWidget(self.sim_list_group)
        # HIGHLIGHT END

        # --- Results Group (will contain QFormLayout) ---
        self.results_group = QGroupBox()
        self.results_form_layout = QFormLayout() # Create the QFormLayout
        self.results_form_layout.setContentsMargins(10, 20, 10, 10)
        self.results_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.results_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.results_form_layout.setVerticalSpacing(6) # Adjusted spacing
        self.results_group.setLayout(self.results_form_layout) # Set it to the group
        left_column_layout.addWidget(self.results_group)

        left_column_layout.addStretch(1)
        body_layout.addLayout(left_column_layout, 1) # Left column takes 1 part

        self.canvas_simulation = MplCanvas(self, width=7, height=6, dpi=100)
        self.canvas_simulation.setStyleSheet("border: 1px solid #ced4da; background-color: white;")
        body_layout.addWidget(self.canvas_simulation, 3)
        main_layout_page.addLayout(body_layout, 1)
        self._setup_initial_plot()

    def _clear_results_form_layout(self):
        """Clears all widgets from the self.results_form_layout."""
        if self.results_form_layout is not None:
            while self.results_form_layout.count():
                item = self.results_form_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout(): # Should not happen often with QFormLayout rows
                    self._clear_layout(item.layout()) # Recursive clear for sub-layouts

    def _add_info_row(self, label_text_key, value_text="..."):
        """Helper to add a row to the results_form_layout."""
        if self.results_form_layout is None:
            return None, None # Should not happen if _init_ui is correct
        label_widget = QLabel(self.tr(label_text_key))
        # HIGHLIGHT START: Đổi objectName để CSS có thể áp dụng
        label_widget.setObjectName("infoLabelScreen3")
        value_widget = QLabel(value_text)
        value_widget.setObjectName("infoLabelScreen3")
        value_widget.setWordWrap(True)
        self.results_form_layout.addRow(label_widget, value_widget)
        return label_widget, value_widget # Return them if they need to be stored

    def _update_simulation_info_display(self):
        """Clears and repopulates the results_group based on current_simulation_type."""
        print(f"DEBUG: _update_simulation_info_display called. Current type: {self.current_simulation_type}")
        self._clear_results_form_layout()
        is_model2 = (self.current_simulation_type == 'model2')
        is_abm = (self.current_simulation_type == 'abm')
        is_model5_sim1 = (self.current_simulation_type == 'model5_sim1')
        is_model5_sim2 = (self.current_simulation_type == 'model5_sim2')
        print(f"DEBUG: Flags - is_model2:{is_model2}, is_abm:{is_abm}, is_model5_sim1:{is_model5_sim1}, is_model5_sim2:{is_model5_sim2}")
        self.results_group.setVisible(is_model2 or is_abm or is_model5_sim1 or is_model5_sim2)
        if not (is_model2 or is_abm or is_model5_sim1 or is_model5_sim2):
            print("DEBUG: No specific simulation type matched. Setting default results title.")
            self.results_group.setTitle(self.tr("screen3_results_group_title")) # Default
            return

        if is_model2:
            print("DEBUG: Setting up for Model 2.")
            self.results_group.setTitle(self.tr("screen3_results_group_title")) # Or a specific title
            self.m2_c_value_label, self.m2_c_value_display = self._add_info_row("screen3_result_c")
            self.m2_sim_time_label, self.m2_sim_time_display = self._add_info_row("screen3_result_time") # Thời gian mô phỏng (t)
            #self.m2_real_time_label, self.m2_real_time_display = self._add_info_row("screen3_actual_time") # Thời gian thực tế
            self.m2_mass_label, self.m2_mass_display = self._add_info_row("screen3_result_mass")
        elif is_abm:
            print("DEBUG: Setting up for ABM.")
            self.results_group.setTitle(self.tr("screen3_results_group_title")) # Or specific ABM title
            _, self.result_r_value = self._add_info_row("screen3_result_r_param")
            #self.abm_sim_time_label, self.abm_sim_time_value = self._add_info_row("screen3_model3_simulation_time_label")
            _, self.result_actual_time_value = self._add_info_row("screen3_actual_time")
            _, self.result_total_pop_value = self._add_info_row("screen3_total_pop")
            _, self.result_infected_pop_value = self._add_info_row("screen3_infected_pop")
            _, self.result_susceptible_pop_value = self._add_info_row("screen3_susceptible_pop")
        elif is_model5_sim1:
            print("DEBUG: Setting up for Model 5 - Sim 1.")
            self.results_group.setTitle(self.tr("screen3_info_m5_sim1_title"))
            self.m5_boat_speed_label, self.m5_boat_speed_value = self._add_info_row("screen3_m5_boat_speed")
            self.m5_water_speed_label, self.m5_water_speed_value = self._add_info_row("screen3_m5_water_speed")
            self.m5_crossing_time_label, self.m5_crossing_time_value = self._add_info_row("screen3_m5_crossing_time")
            if self.m5_crossing_time_value: self.m5_crossing_time_value.setText("0.00 s")
            self.m5_start_point_boat_label, self.m5_start_point_boat_value = self._add_info_row("screen3_m5_start_point_boat")
            self.m5_boat_reaches_target_label, self.m5_boat_reaches_target_value = self._add_info_row("screen3_m5_boat_reaches_target")
            # Khởi tạo trạng thái "Đang xác định..."
            if self.m5_boat_reaches_target_value: self.m5_boat_reaches_target_value.setText(self.tr("screen3_m5_determining_status"))
            self.m5_boat_final_pos_label, self.m5_boat_final_pos_value = self._add_info_row("screen3_m5_boat_final_pos")
            if self.m5_boat_final_pos_value: self.m5_boat_final_pos_value.setText(self.tr("screen3_m5_determining_status"))
        elif is_model5_sim2:
            print("DEBUG: Setting up for Model 5 - Sim 2.")
            # ================== HIGHLIGHT: Gán đúng thuộc tính ==================
            # Các _label chỉ là để nhận giá trị trả về đầu tiên (QLabel tĩnh) nếu không cần dùng
            self.results_group.setTitle(self.tr("screen3_info_m5_sim2_title"))
            _label_sub_speed, self.m5_submarine_speed_value = self._add_info_row("screen3_m5_submarine_speed", "...")
            _label_dest_speed, self.m5_destroyer_speed_value = self._add_info_row("screen3_m5_destroyer_speed", "...")
           # _label_sub_traj, self.m5_submarine_trajectory_value = self._add_info_row("screen3_m5_submarine_trajectory", "...")
            _label_sub_start, self.m5_start_point_submarine_value = self._add_info_row("screen3_m5_start_point_submarine", "...")
            _label_dest_start, self.m5_start_point_destroyer_value = self._add_info_row("screen3_m5_start_point_destroyer", "...")
            _label_catch_time, self.m5_catch_time_value = self._add_info_row("screen3_m5_catch_time", "0.00 s")
            if self.m5_catch_time_value:
                self.m5_catch_time_value.setText(self.tr("screen3_m5_catch_time"))
            _label_dest_catches, self.m5_destroyer_catches_submarine_value = self._add_info_row("screen3_m5_destroyer_catches_submarine", self.tr("screen3_m5_determining_status"))
            _label_catch_point, self.m5_catch_point_value = self._add_info_row("screen3_m5_catch_point", self.tr("screen3_m5_determining_status"))

        self.results_group.updateGeometry() # Ensure layout recalculates
    
    @Slot(bool)
    def _on_model5_sim_selected(self, checked):
        if not checked:
            return

        sender = self.sender()
        print(f"DEBUG Screen3 _on_model5_sim_selected: RadioButton '{sender.text()}' was CHECKED.")

        self._fully_stop_and_cleanup_animation() # Gọi ở đây để dọn dẹp animation CŨ
        print(f"DEBUG Screen3 _on_model5_sim_selected: Called _fully_stop_and_cleanup_animation() for sender '{sender.text()}'.")

        if sender == self.rb_model5_sim1:
            # ... (code cho Sim 1 như cũ) ...
            print("Screen3 _on_model5_sim_selected: Activating Model 5 - Simulation 1 (Boat).")
            self.current_model5_sim_selected = 1
            self.current_simulation_type = "model5_sim1"
            self._update_simulation_info_display()
            self._populate_model5_sim1_data()
            if self.model5_plot_data_cache and \
               hasattr(self, 'm5s1_z_array') and self.m5s1_z_array is not None and \
               len(self.m5s1_z_array) > 0:
                print("  M5S1: Data is valid, proceeding to start boat animation.")
                self._start_boat_animation_m5s1()
            else:
                # ... (hiển thị chờ/lỗi cho Sim 1)
                print("  M5S1: No valid data for boat animation. Displaying waiting/error.")
                ax = self.canvas_simulation.axes
                if ax:
                    ax.clear()
                    ax.text(0.5, 0.5, self.tr("screen3_waiting_for_data"),
                            ha='center', va='center', transform=ax.transAxes, fontsize=12, color='gray')
                    ax.set_xticks([]); ax.set_yticks([])
                    ax.set_facecolor('white')
                    self.canvas_simulation.draw_idle()
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)


        elif sender == self.rb_model5_sim2:
            print("Screen3 _on_model5_sim_selected: Activating Model 5 - Simulation 2 (Destroyer).") # Log 1
            self.current_model5_sim_selected = 2
            self.current_simulation_type = "model5_sim2"

            self._update_simulation_info_display() # Log 2 (bên trong hàm này)
            
            # Log ngay trước khi gọi hàm chính của Sim 2
            print("  M5S2: >>>>>>>>>>>> ABOUT TO CALL _prepare_and_start_model5_sim2_animation() <<<<<<<<<<<<")
            self._prepare_and_start_model5_sim2_animation() # GỌI HÀM CHO SIM 2
        
        else:
            print(f"Screen3 _on_model5_sim_selected: Warning - Unknown sender: {sender}")

    def _setup_initial_plot(self):
        ax = self.canvas_simulation.axes
        ax.clear()
        # Chỉ hiển thị text chờ, không gọi retranslate_ui từ đây
        ax.text(0.5, 0.5, self.tr("screen3_waiting_for_data"),
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, color='gray')
        ax.set_facecolor('white')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('auto') # Hoặc 'equal' tùy theo loại plot
        try:
            self.canvas_simulation.fig.tight_layout(pad=1.0) # Sửa lỗi subplots_adjust
        except Exception:
            pass
        # Không gọi self.retranslate_ui() ở đây nữa.
        self.canvas_simulation.draw_idle()

    def _connect_signals(self):
        if self.btn_back_to_screen2: # Kiểm tra widget tồn tại
            self.btn_back_to_screen2.clicked.connect(self._go_back_to_screen2)
        if self.btn_double_back_to_screen1:
            self.btn_double_back_to_screen1.clicked.connect(self._go_back_to_screen1)
        if self.speed_slider:
            self.speed_slider.valueChanged.connect(self._on_speed_changed)
        if self.btn_stop:
            self.btn_stop.clicked.connect(self._toggle_pause_resume_animation)
        if self.rb_model5_sim1:
            self.rb_model5_sim1.toggled.connect(self._on_model5_sim_selected)
        if self.rb_model5_sim2: # <<< THIS CONNECTION IS CRUCIAL
            self.rb_model5_sim2.toggled.connect(self._on_model5_sim_selected)
    
    @Slot(int)
    def _on_speed_changed(self, value):
        if self.speed_slider.signalsBlocked(): # Nếu slider đang bị block, không xử lý
            print(f"Slider value changed to {value} but signals are blocked. Ignoring.")
            return

        speed_multiplier = value / 10.0 if value > 0 else 0.05
        print(f"Slider value: {value}, Speed multiplier: {speed_multiplier:.1f}x - Current Sim Type: {self.current_simulation_type}")

        # Lưu lại giá trị interval mới dựa trên speed_multiplier
        # Việc restart animation sẽ được xử lý bởi các hàm setup_and_start...
        # hoặc hàm _toggle_pause_resume_animation nếu animation đang pause
        # Mục tiêu chính ở đây là cập nhật self.xxx_animation_interval

        if self.current_simulation_type == 'model2':
            new_interval = int(self.model2_base_interval / speed_multiplier) if speed_multiplier > 0 else self.model2_base_interval * 20
            self.model2_animation_interval = max(5, min(new_interval, 1000))
            print(f"  Model 2 target interval updated to: {self.model2_animation_interval} ms")
            if self.ani and (self.is_simulation_running or self.is_simulation_paused): # Nếu animation đã tồn tại và đang chạy/pause
                print("  Model 2: Animation active/paused. Restarting with new speed.")
                if self.original_model2_data: self.setup_and_start_model2_animation(**self.original_model2_data)
                else: print("  Model 2: Cannot restart, no original data.")
            elif not self.ani and self.original_model2_data : # Nếu chưa có animation nhưng có data (ví dụ sau khi chọn model)
                 print("  Model 2: Animation not yet started but data exists. Will use new interval on start.")


        elif self.current_simulation_type == 'abm':
            new_interval = int(self.abm_base_interval / speed_multiplier) if speed_multiplier > 0 else self.abm_base_interval * 20
            self.abm_animation_interval = max(5, min(new_interval, 1000))
            print(f"  ABM target interval updated to: {self.abm_animation_interval} ms")
            if self.ani and (self.is_simulation_running or self.is_simulation_paused):
                print("  ABM: Animation active/paused. Restarting with new speed.")
                if self.original_abm_params: self.setup_and_start_abm(self.original_abm_params.copy())
                else: print("  ABM: Cannot restart, no original params.")
            elif not self.ani and self.original_abm_params:
                 print("  ABM: Animation not yet started but data exists. Will use new interval on start.")


        elif self.current_simulation_type == 'model5_sim1':
            new_interval = int(self.m5s1_base_interval / speed_multiplier) if speed_multiplier > 0 else self.m5s1_base_interval * 20
            self.m5s1_animation_interval = max(10, min(new_interval, 1000))
            print(f"  Model 5 Sim 1 target interval updated to: {self.m5s1_animation_interval} ms")
            if self.ani and (self.is_simulation_running or self.is_simulation_paused):
                print("  Model 5 Sim 1: Animation active/paused. Restarting with new speed.")
                if self.original_model5_data: self._start_boat_animation_m5s1() # _start_boat_animation_m5s1 sẽ dùng self.m5s1_animation_interval
                else: print("  Model 5 Sim 1: Cannot restart, no original data.")
            elif not self.ani and self.original_model5_data:
                 print("  Model 5 Sim 1: Animation not yet started but data exists. Will use new interval on start.")


        elif self.current_simulation_type == 'model5_sim2':
            new_interval = int(self.m5s2_base_interval / speed_multiplier) if speed_multiplier > 0 else self.m5s2_base_interval * 20
            self.m5s2_animation_interval = max(20, min(new_interval, 1000))
            print(f"  Model 5 Sim 2 target interval updated to: {self.m5s2_animation_interval} ms")
            
            if self.ani and (self.is_simulation_running or self.is_simulation_paused):
                print("  Model 5 Sim 2: Animation active/paused. Restarting with new speed.")
                if self.original_model5_data: # original_model5_data chứa dữ liệu từ Screen 2
                    self._prepare_and_start_model5_sim2_animation() # Hàm này sẽ dùng self.m5s2_animation_interval
                else: print("  Model 5 Sim 2: Cannot restart, no original data.")
            elif not self.ani and self.original_model5_data: # Chưa có animation nhưng đã có data từ Screen 2
                 print("  Model 5 Sim 2: Animation not yet started but data exists. Will use new interval on start.")
                 # Không cần làm gì thêm ở đây, vì _prepare_and_start_model5_sim2_animation()
                 # sẽ được gọi bởi _on_model5_sim_selected và nó sẽ đọc self.m5s2_animation_interval mới nhất.
            else:
                # Trường hợp này có thể xảy ra nếu slider được chạm vào ngay khi Sim 2 được chọn
                # nhưng _prepare_and_start_model5_sim2_animation chưa kịp chạy để tạo self.ani
                print(f"  Model 5 Sim 2: Speed change, self.ani is None. New interval {self.m5s2_animation_interval} will be used when animation starts.")
        
        else:
            print(f"  _on_speed_changed: No specific logic for current_simulation_type ('{current_anim_type}') or animation not ready.")
    
    def retranslate_ui(self):
        if self.title_label:
            self.title_label.setText(self.tr("screen3_dyn_only_title"))
        if self.btn_back_to_screen2:
            self.btn_back_to_screen2.setText(self.tr("screen3_back_button"))
            self.btn_back_to_screen2.setToolTip(self.tr("screen3_dyn_back_tooltip"))
        if self.btn_double_back_to_screen1:
            self.btn_double_back_to_screen1.setText(self.tr("screen3_double_back_button"))
        if self.btn_stop:
            self.btn_stop.setText(self.tr("screen3_stop_button"))

        if self.settings_group:
            self.settings_group.setTitle(self.tr("screen3_settings_group_title"))
        if self.speed_slider_label:
            self.speed_slider_label.setText(self.tr("screen3_speed_label"))

        if self.sim_list_group:
            self.sim_list_group.setTitle(self.tr("screen3_sim_list_group_title"))
        if self.rb_model5_sim1:
            self.rb_model5_sim1.setText(self.tr("screen3_sim1_name_m5"))
        if self.rb_model5_sim2:
            self.rb_model5_sim2.setText(self.tr("screen3_sim2_name_m5"))
        # HIGHLIGHT END

        self._update_simulation_info_display() 
        if self.canvas_simulation and self.canvas_simulation.axes:
            # If a specific simulation is active, its update frame will handle titles.
            # Otherwise, for a blank canvas or "Not Implemented" message:
            if self.current_simulation_type == "model5_sim2" and self.current_model5_sim_selected == 2:
                 ax = self.canvas_simulation.axes
                 ax.clear()
                 ax.text(0.5, 0.5, self.tr("screen3_model5_not_implemented_msg"),
                         horizontalalignment='center', verticalalignment='center',
                         transform=ax.transAxes, fontsize=12, color='gray')
                 ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor('white')

            self.canvas_simulation.draw_idle()
        super().retranslate_ui()

    def _fully_stop_and_cleanup_animation(self):
        print("Screen3: _fully_stop_and_cleanup_animation called.")
        if self.ani:
            if hasattr(self.ani, 'event_source') and self.ani.event_source is not None:
                try:
                    self.ani.event_source.stop()
                    print("  Internal stop: Animation source stopped.")
                except Exception as e_stop:
                    print(f"  Error stopping animation (internal): {e_stop}")
            if hasattr(self.ani, '_stop'): # For older Matplotlib versions
                try: self.ani._stop()
                except Exception: pass
            # self.ani.pause() # Thử thêm dòng này nếu event_source.stop() không đủ
            self.canvas_simulation.draw_idle() # Đảm bảo canvas được vẽ lại sau khi dừng
        self.ani = None
        self.is_simulation_running = False
        self.is_simulation_paused = False

        self.model2_animation_visually_finished = False
        self.abm_simulation_visually_finished = False
        self.m5s1_animation_visually_finished = False
        self.m5s2_animation_visually_finished = False

        # Dọn dẹp Model 2
        for circle in self.circles_model2:
            try: circle.remove()
            except Exception: pass
        self.circles_model2.clear()
        self.model2_cells_list.clear()
        self.model2_last_frame_processed = -1
        if self.text_box_model2:
            try: self.text_box_model2.remove()
            except Exception: pass
            self.text_box_model2 = None
        self.original_model2_data = None
        self.T_model2 = None

        # Dọn dẹp ABM
        if self.abm_scatter_susceptible:
            try: self.abm_scatter_susceptible.remove()
            except Exception: pass
            self.abm_scatter_susceptible = None
        if self.abm_scatter_infected:
            try: self.abm_scatter_infected.remove()
            except Exception: pass
            self.abm_scatter_infected = None
        if self.simulation_instance_abm and hasattr(self.simulation_instance_abm, 'contact_radius_patches'):
            for patch in self.simulation_instance_abm.contact_radius_patches:
                try: patch.remove()
                except Exception: pass
            self.simulation_instance_abm.contact_radius_patches.clear()
        self.simulation_instance_abm = None
        self.abm_params = {}

        # Dọn dẹp Model 5 Sim 1
        artists_to_clear_m5s1 = [
            'm5s1_line_ship_path', 'm5s1_point_ship',
            'm5s1_quiver_water', 'm5s1_legend_obj'
        ]
        for attr_name in artists_to_clear_m5s1:
            artist = getattr(self, attr_name, None)
            if artist and hasattr(artist, 'axes') and artist.axes: # Kiểm tra artist có tồn tại và có axes không
                try: artist.remove()
                except Exception: pass
            setattr(self, attr_name, None) # Luôn reset thuộc tính

        self.m5s1_params = {}
        self.m5s1_t_array = None; self.m5s1_z_array = None
        self.m5s1_X_arrows_positions = None; self.m5s1_Y_arrows_initial_positions = None
        self.m5s1_Y_arrows_at_interaction_end = None
        self.m5s1_ship_has_docked = False; self.m5s1_docking_frame_index_for_ship = -1
        self.m5s1_ship_journey_complete = False; self.m5s1_frame_ship_interaction_ends = -1
        self.m5s1_current_anim_frame = 0

        # Dọn dẹp Model 5 Sim 2
        artists_to_clear_m5s2 = [
            'm5s2_line_tn', 'm5s2_line_kt', 'm5s2_point_tn', 'm5s2_point_kt',
            'm5s2_catch_marker', 'm5s2_legend_obj',
            'm5s2_avoid_circle_tn_artist', 'm5s2_kt_radar_circle_artist' # Thêm vòng tròn
        ]
        for attr_name in artists_to_clear_m5s2:
            artist = getattr(self, attr_name, None)
            if artist and hasattr(artist, 'axes') and artist.axes:
                try: artist.remove()
                except Exception: pass
            setattr(self, attr_name, None)

        self.m5s2_params = {}
        self.m5s2_submarine_trajectory_params = {"offset_x": 0.0, "offset_y": 0.0, "params_x": [], "params_y": []}
        self.m5s2_t_array_solver = None; self.m5s2_t_array_actual = None
        self.m5s2_z_kt_array = None; self.m5s2_z_tn_array = None
        self.m5s2_caught_flag = False; self.m5s2_catch_point_coords = None

        # Dọn dẹp legend của figure (nếu có)
        if hasattr(self, 'current_fig_legend') and self.current_fig_legend:
            try:
                self.current_fig_legend.remove()
            except Exception: pass
            self.current_fig_legend = None
        # Hoặc cách tổng quát hơn (nếu bạn không chắc tên biến legend của figure)
        if self.canvas_simulation and self.canvas_simulation.fig and self.canvas_simulation.fig.legends:
            for fig_leg in list(self.canvas_simulation.fig.legends):
                try: fig_leg.remove()
                except Exception: pass
        
        if self.canvas_simulation and self.canvas_simulation.axes:
            ax = self.canvas_simulation.axes
            ax.clear()
            # Xóa legend của axes nếu có (thường dùng cho plot tĩnh, không phải fig.legend)
            if ax.get_legend():
                try: ax.get_legend().remove()
                except Exception: pass
            ax.text(0.5, 0.5, self.tr("screen3_waiting_for_data"),
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12, color='gray')
            ax.set_facecolor('white')
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_aspect('auto') # Hoặc 'equal'
            try: self.canvas_simulation.fig.tight_layout(pad=1.0)
            except Exception: pass
            self.canvas_simulation.draw_idle()

        # Kích hoạt lại các nút điều hướng
        if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
        if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
        if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False) # Nút Dừng/Tiếp bị vô hiệu hóa
        print("Screen3: Animation fully stopped and all model resources reset.")

    @Slot()
    def _toggle_pause_resume_animation(self):
        """Xử lý việc dừng tạm thời hoặc tiếp tục animation."""
        if not self.ani: # Không có animation để dừng/tiếp
            print("Toggle Pause/Resume: No animation object exists.")
            return
        # ================== HIGHLIGHT START: Kiểm tra cờ visually_finished ==================
        is_visually_finished = False
        if self.current_simulation_type == 'model5_sim1':
            is_visually_finished = self.m5s1_animation_visually_finished
        elif self.current_simulation_type == 'model2':
            is_visually_finished = self.model2_animation_visually_finished
        elif self.current_simulation_type == 'abm':
            is_visually_finished = self.abm_simulation_visually_finished

        if is_visually_finished:
            print("Toggle Pause/Resume: Animation has visually finished. No action.")
            # Có thể bạn muốn nút này làm hành động khác, ví dụ "Chạy lại từ đầu"
            # hoặc chỉ đơn giản là không làm gì và giữ nút Dừng/Tiếp bị vô hiệu hóa.
            # Hiện tại, nút btn_stop đã được setEnabled(False) khi visually_finished.
            return
        # ================== HIGHLIGHT END ==================

        if self.is_simulation_running:
            # ---- Đang chạy -> Dừng tạm thời ----
            try:
                if hasattr(self.ani, 'pause'): # Matplotlib versions >= 3.4
                    self.ani.pause()
                elif hasattr(self.ani, 'event_source') and self.ani.event_source is not None:
                     # Fallback cho phiên bản cũ hơn
                     self.ani.event_source.stop()
                self.is_simulation_running = False
                self.is_simulation_paused = True # Đánh dấu là đang pause
                print("Animation Paused.")
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                # Nút Dừng/Tiếp vẫn được bật để có thể Resume
                # Nút Back vẫn bị vô hiệu hóa
            except Exception as e_pause:
                print(f"Error pausing animation: {e_pause}")
        elif self.is_simulation_paused:
            # ---- Đang dừng tạm thời -> Tiếp tục ----
            try:
                if hasattr(self.ani, 'resume'): # Matplotlib versions >= 3.4
                    self.ani.resume()
                elif hasattr(self.ani, 'event_source') and self.ani.event_source is not None:
                     # Fallback cho phiên bản cũ hơn
                     self.ani.event_source.start()
                self.is_simulation_running = True
                self.is_simulation_paused = False # Hủy đánh dấu pause
                print("Animation Resumed.")
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(False)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(False)
                # Nút Dừng/Tiếp vẫn được bật
                # Nút Back vẫn bị vô hiệu hóa
            except Exception as e_resume:
                print(f"Error resuming animation: {e_resume}")
        else:
            # Trường hợp is_simulation_running=False và is_simulation_paused=False
            # Điều này xảy ra khi animation đã kết thúc tự nhiên hoặc bị dừng hẳn
            print("Toggle Pause/Resume: Animation is not active or paused.")

    @Slot()
    def _go_back_to_screen2(self):
        self._fully_stop_and_cleanup_animation()
        print("Going back to Screen 2 from Screen 3")
        self.main_window.switch_to_specific_screen(self.main_window.screen2)

    @Slot()
    def _go_back_to_screen1(self):
        self._fully_stop_and_cleanup_animation() # Dừng animation trước khi quay lại
        print("Going back to Screen 1 from Screen 3")
        self.main_window.switch_to_specific_screen(self.main_window.screen1)

    def _reset_buttons_on_finish(self):
        """Reset nút khi simulation tự kết thúc."""
        print("Animation finished naturally.")
        # is_simulation_running sẽ được đặt lại trong _stop_animation
        self._fully_stop_and_cleanup_animation() # Gọi hàm public để xử lý đúng cách

    def setup_and_start_model2_animation(self, t_data, y_data_list, labels, additional_info):
        print("Screen 3: Setting up Model 2 (Cell Growth) animation - NEW LOGIC...")
        self._fully_stop_and_cleanup_animation()
        if hasattr(self, 'sim_list_group') and self.sim_list_group:
            self.sim_list_group.setVisible(False)
        self.original_model2_data = { # Lưu lại để có thể restart
            't_data': t_data, 'y_data_list': y_data_list,
            'labels': labels, 'additional_info': additional_info
        }
        self.current_simulation_type = 'model2'
        self.model2_animation_visually_finished = False
        self.is_simulation_paused = False
        self.model2_last_frame_processed = -1 # Reset cho lần chạy mới
        self.retranslate_ui()

        self.T_model2 = np.asarray(t_data) if t_data is not None else None
        # self.Y_model2 không còn dùng trực tiếp cho logic animation mới,
        # số lượng tế bào mục tiêu sẽ được tính từ t_current
        if additional_info:
            self.t_start_model2 = additional_info.get('t_start_anim', 0)
            self.t_end_model2 = additional_info.get('t_end_anim', 0)
            self.y0_model2 = additional_info.get('y0_anim') # Đây là x0 ban đầu
            self.c_model2 = additional_info.get('c_anim')   # Đây là hằng số c
            if self.m2_c_value_display: self.m2_c_value_display.setText(f"{self.c_model2:.6g}" if self.c_model2 is not None else "N/A")
            if self.m2_sim_time_display: self.m2_sim_time_display.setText(f"{self.t_start_model2:.3f} s - {self.t_end_model2:.3f} s") # Ban đầu là khoảng thời gian
            if self.m2_real_time_display: self.m2_real_time_display.setText("0.00 s") # Bắt đầu từ 0
            if self.m2_mass_display: self.m2_mass_display.setText(str(int(round(self.y0_model2))) if self.y0_model2 is not None else "1") # Số lượng ban đầu

        if self.T_model2 is None or len(self.T_model2) == 0 or \
           self.y0_model2 is None or self.c_model2 is None:
            QMessageBox.critical(self, self.tr("Lỗi Dữ liệu Model 2", "Model 2 Data Error"),
                                 self.tr("Thiếu dữ liệu (T, y0, c) để chạy animation Model 2.", "Missing data (T, y0, c) for Model 2 animation."))
            return

        # Khởi tạo danh sách tế bào với một tế bào gốc
        self.model2_cells_list = [Cell(0, 0, gen=0)] # Một tế bào ở gốc tọa độ
        self.model2_cell_radius = 0.5 # Bán kính cố định

        # Cài đặt animation interval (giữ nguyên)
        if self.T_model2 is not None and len(self.T_model2) > 0:
            self.num_animation_frames_model2 = len(self.T_model2)
        else: self.model2_base_interval = 200 # Fallback
        current_slider_value = self.speed_slider.value()
        current_speed_multiplier = current_slider_value / 10.0 if current_slider_value > 0 else 0.05
        new_interval = int(self.model2_base_interval / current_speed_multiplier) if current_speed_multiplier > 0 else self.model2_base_interval * 20
        self.model2_animation_interval = max(5, min(new_interval, 1000))
        # self._calculate_model2_anim_params() không còn cần thiết để set final_limit

        ax = self.canvas_simulation.axes
        ax.clear()
        # Không set xlim, ylim cố định ở đây, sẽ được đặt động trong _update_model2_frame
        ax.set_aspect('equal')
        ax.set_facecolor('white')
        #ax.set_xticks([])
        #ax.set_yticks([])
        ax.axis('off') # Ẩn hoàn toàn trục và viền
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        ##ax.spines['bottom'].set_visible(False)
        #ax.spines['left'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        # Tạo một Line2D với marker hình tròn, không có đường kẻ
        proxy_cell_legend = Line2D([0], [0], # Tọa độ không quan trọng, sẽ không được vẽ
                                marker='o', # 'o' là marker hình tròn đặc
                                color='w', # Màu của đường kẻ (đặt là trắng hoặc transparent để ẩn đi)
                                markerfacecolor='#8B0000', # Màu của hình tròn
                                markersize=10, # Kích thước của hình tròn trong legend (điều chỉnh nếu cần)
                                linestyle='None', # Không vẽ đường kẻ
                                label=self.tr("screen3_legend_model2_cell"))

        # HIGHLIGHT START: Sử dụng fig.legend()
        fig = self.canvas_simulation.fig

        # Xóa legend cũ của figure nếu có (quan trọng khi setup lại)
        if hasattr(self, 'current_fig_legend') and self.current_fig_legend:
            try:
                self.current_fig_legend.remove()
            except Exception:
                pass
            self.current_fig_legend = None
        
        legend_loc_fig = 'upper left'
        bbox_anchor_fig = (0.05, 0.95) # 5% từ lề trái Figure, 95% từ lề dưới Figure (tức 5% từ lề trên)

        fig_legend_instance = fig.legend(
            handles=[proxy_cell_legend],
            loc=legend_loc_fig,
            bbox_to_anchor=bbox_anchor_fig, # Quan trọng khi muốn tinh chỉnh
            # bbox_transform=fig.transFigure, # Mặc định là transFigure rồi
            fontsize='medium', # Hoặc giá trị số
            markerscale=1.8,
            borderpad=0.7,
            labelspacing=0.8,
            handletextpad=1.0, # Đảm bảo biến này được định nghĩa đúng
            frameon=True,
            facecolor='lightyellow',
            edgecolor='gray'
        )
        if fig_legend_instance:
            fig_legend_instance.set_zorder(100)
        self.circles_model2.clear() # Dọn dẹp các patch cũ
        if self.text_box_model2 and self.text_box_model2.axes:
            try: self.text_box_model2.remove()
            except: pass
        self.text_box_model2 = ax.text(0.02, 0.98, '', fontsize=9, transform=ax.transAxes, va='top',
                                       bbox={'facecolor': 'lightblue', 'alpha': 0.8, 'pad': 5})

        num_frames_to_run = len(self.T_model2)
        if num_frames_to_run == 0: return

        self.is_simulation_running = True
        self.is_simulation_paused = False # Đảm bảo reset
        self.ani = animation.FuncAnimation(self.canvas_simulation.fig,
                                           self._update_model2_frame,
                                           frames=num_frames_to_run, fargs=(ax,),
                                           interval=self.model2_animation_interval,
                                           blit=False, repeat=False)
        self.canvas_simulation.draw_idle()
        if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(True)
        if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(False)
        if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(False)
        print("Screen 3: Model 2 animation (NEW LOGIC) started.")

    def _update_model2_frame(self, frame_index, ax):
        if self.model2_animation_visually_finished:
            return []

        # ==============================================================
        # START PORTED LOGIC FROM STANDALONE (Modified for app context)
        # ==============================================================
        ax.clear() # Xóa toàn bộ nội dung của trục ở mỗi frame
        fig = self.canvas_simulation.fig
        if hasattr(self, 'current_fig_legend') and self.current_fig_legend:
            try:
                self.current_fig_legend.remove()
            except Exception: # Có thể nó đã bị xóa hoặc không tồn tại
                pass
            self.current_fig_legend = None

        proxy_cell_legend = MplCircle((0,0), 0.1, color='#8B0000', label=self.tr("screen3_legend_model2_cell"))
        legend_loc_fig = 'upper left'
        bbox_anchor_fig = (0.05, 0.95)
        handletextpad_value = 1.0 # Đảm bảo biến này được định nghĩa

        # Lưu trữ instance legend mới vào self.current_fig_legend
        self.current_fig_legend = fig.legend(
            handles=[proxy_cell_legend],
            loc=legend_loc_fig,
            bbox_to_anchor=bbox_anchor_fig,
            fontsize='medium',
            markerscale=1.8,
            borderpad=0.7,
            labelspacing=0.8,
            handletextpad=handletextpad_value, # Sử dụng biến đã định nghĩa
            frameon=True,
            facecolor='lightyellow',
            edgecolor='gray'
        )
    
        if not self.model2_cells_list:
            max_abs_coord = self.model2_cell_radius * 2
        else:
            all_x = [cell.x for cell in self.model2_cells_list]
            all_y = [cell.y for cell in self.model2_cells_list]
            max_x_val = max(abs(x) for x in all_x) if all_x else self.model2_cell_radius
            max_y_val = max(abs(y) for y in all_y) if all_y else self.model2_cell_radius
            max_abs_coord = max(max_x_val, max_y_val, self.model2_cell_radius)

        margin = self.model2_cell_radius * 2
        ax.set_xlim(-max_abs_coord - margin, max_abs_coord + margin)
        ax.set_ylim(-max_abs_coord - margin, max_abs_coord + margin)
        #ax.set_xticks([])
        #ax.set_yticks([])
        ax.set_aspect('equal')
        ax.set_facecolor('white')
        ax.axis('off')
        #proxy_cell_legend = MplCircle((0,0), 0.1, color='#8B0000', label=self.tr("screen3_legend_model2_cell"))
        ax.set_xticks([])
        ax.set_yticks([])

        if frame_index > self.model2_last_frame_processed:
            t_current = self.T_model2[frame_index]
            target_n_float = (self.y0_model2**(1/3) + self.c_model2 * t_current / 3)**3
            target_n = int(round(target_n_float))
            current_n_actual = len(self.model2_cells_list)
            to_add = target_n - current_n_actual

            if to_add > 0:
                positions = [(cell.x, cell.y) for cell in self.model2_cells_list]
                candidates = [cell for cell in self.model2_cells_list
                              if frame_index - cell.last_division > self.model2_min_division_interval]
                random.shuffle(candidates)
                added_count_this_frame = 0
                for parent_cell in candidates:
                    if added_count_this_frame >= to_add:
                        break
                    num_daughters_to_try = min(2, to_add - added_count_this_frame)
                    daughters_created_for_parent = 0
                    for _ in range(num_daughters_to_try):
                        angle = random.uniform(0, 2 * np.pi)
                        dist = random.uniform(self.model2_cell_radius * 1.1, self.model2_cell_radius * 1.3)
                        dx, dy = dist * np.cos(angle), dist * np.sin(angle)
                        new_x, new_y = parent_cell.x + dx, parent_cell.y + dy
                        too_close = False
                        for (px, py) in positions:
                            if np.hypot(new_x - px, new_y - py) < self.model2_cell_radius * 1.05:
                                too_close = True
                                break
                        if not too_close:
                            new_cell = Cell(new_x, new_y, parent_cell.gen + 1)
                            new_cell.last_division = frame_index
                            self.model2_cells_list.append(new_cell)
                            positions.append((new_x, new_y))
                            added_count_this_frame += 1
                            daughters_created_for_parent +=1
                            if added_count_this_frame >= to_add: break
                    if daughters_created_for_parent > 0:
                         parent_cell.last_division = frame_index
            self.model2_last_frame_processed = frame_index

        # --- Vẽ tất cả các tế bào hiện có ---
        # ax.clear() đã xóa các patch cũ khỏi trục.
        # Bây giờ chúng ta chỉ cần xóa danh sách tham chiếu self.circles_model2.
        self.circles_model2.clear() # <--- THAY ĐỔI Ở ĐÂY: Xóa list, không remove từng patch

        for cell_obj in self.model2_cells_list:
            circle_patch = plt.Circle((cell_obj.x, cell_obj.y), self.model2_cell_radius,
                                      color='#8B0000', ec='black', lw=0.3, alpha=0.9)
            ax.add_patch(circle_patch)
            self.circles_model2.append(circle_patch) # Lưu lại patch mới
        # ============================================================
        # END PORTED LOGIC
        # ============================================================

        # --- Cập nhật thông tin hiển thị (giữ nguyên) ---
        num_cells_display = len(self.model2_cells_list)
        time_val_display = self.T_model2[frame_index]
        real_time_elapsed_seconds = frame_index * (self.model2_animation_interval / 1000.0)
        if self.text_box_model2:
             self.text_box_model2.set_text(
                 f'{self.tr("screen3_result_mass")} {num_cells_display}\n'
                 f'{self.tr("screen3_result_time")} {time_val_display:.3f} s\n' # Thời gian mô phỏng t
                 f'{self.tr("screen3_actual_time")} {real_time_elapsed_seconds:.2f} s' # Thời gian thực
                 )
        if self.m2_mass_display: self.m2_mass_display.setText(str(num_cells_display))
        if self.m2_sim_time_display: self.m2_sim_time_display.setText(f"{time_val_display:.3f} s")
        if self.m2_real_time_display: self.m2_real_time_display.setText(f"{real_time_elapsed_seconds:.2f} s")
        # --- Logic kết thúc animation (giữ nguyên) ---
        if frame_index >= len(self.T_model2) - 1:
            if not self.model2_animation_visually_finished:
                print(f"Model 2 Animation (NEW LOGIC) visually finished at frame {frame_index}.")
                self.model2_animation_visually_finished = True
                self.is_simulation_running = False
                self.is_simulation_paused = False
                if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source:
                    self.ani.event_source.stop()
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            artists_to_return = self.circles_model2[:] # Các tế bào vẽ trên ax
            if self.text_box_model2:
                artists_to_return.append(self.text_box_model2)
            return artists_to_return

    def setup_and_start_abm(self, abm_params):
        if not ABM_AVAILABLE:
            QMessageBox.warning(self, "ABM Error", "ABM components are not available.")
            return
        print("Screen 3: Setting up ABM...")
        self._fully_stop_and_cleanup_animation()
        if hasattr(self, 'current_fig_legend') and self.current_fig_legend:
            try:
                self.current_fig_legend.remove()
                print("  Fig legend explicitly removed at start of ABM setup.")
            except Exception:
                pass
            self.current_fig_legend = None
        if hasattr(self, 'sim_list_group') and self.sim_list_group:
            self.sim_list_group.setVisible(False)
        # ================== HIGHLIGHT START: Sửa lại tên biến cho khớp ==================
        if abm_params and isinstance(abm_params, dict): # Sử dụng abm_params ở đây
            self.original_abm_params = abm_params.copy()
            current_abm_params_for_this_run = abm_params # Gán vào một biến mới nếu muốn rõ ràng
                                                        # hoặc dùng trực tiếp abm_params
            print(f"  ABM: Stored original_abm_params: {self.original_abm_params}")
        else:
            print("  ABM ERROR: Input abm_params is None or not a dict. Cannot setup ABM.")
            # _fully_stop_and_cleanup_animation đã vẽ lại canvas chờ rồi
            return
        # ================== HIGHLIGHT END ==================
        self.current_simulation_type = 'abm'
        self.abm_simulation_visually_finished = False # Reset cờ
        self.is_simulation_paused = False
        self.abm_params = abm_params # Lưu params mới
        self.retranslate_ui()
        # ... (cập nhật UI labels cho ABM như cũ) ...
        r_ode = self.abm_params.get("r_parameter_ode"); 
        #t_start_ode = self.abm_params.get("t_start_ode")
        #t_end_ode = self.abm_params.get("t_end_ode"); total_pop_abm = int(self.abm_params.get('total_population', 0))
        total_pop_abm = int(self.abm_params.get('total_population', 0))
        initial_infected_abm = int(self.abm_params.get('initial_infected',0))
        initial_infected_abm = int(self.abm_params.get('initial_infected',0)); initial_susceptible_abm = total_pop_abm - initial_infected_abm
        if self.result_r_value: self.result_r_value.setText(f"{r_ode:.6g}" if r_ode is not None else "N/A")
        #if hasattr(self, 'abm_sim_time_value') and self.abm_sim_time_value: # Kiểm tra widget tồn tại
        #    self.abm_sim_time_value.setText("0")
        if self.result_actual_time_value: self.result_actual_time_value.setText("0.00")
        if self.result_total_pop_value: self.result_total_pop_value.setText(str(total_pop_abm))
        if self.result_infected_pop_value: self.result_infected_pop_value.setText(str(initial_infected_abm))
        if self.result_susceptible_pop_value: self.result_susceptible_pop_value.setText(str(initial_susceptible_abm))

        try:
            self.simulation_instance_abm = DiseaseSimulationABM(
                total_population=total_pop_abm, #Sửa ở đây
                initial_infected_count_for_abm=initial_infected_abm, #Sửa ở đây
                room_dimension=self.abm_params['room_dimension'],
                contact_radius=self.abm_params['contact_radius'],
                transmission_prob=self.abm_params['transmission_prob'],
                agent_speed=self.abm_params['agent_speed']
            )
        except Exception as e:
             QMessageBox.critical(self, self.tr("ABM Init Error", "ABM Init Error"), f"{e}")
             # _fully_stop_and_cleanup_animation đã vẽ lại canvas chờ rồi
             return

        ax = self.canvas_simulation.axes
        ax.clear(); room_dim = self.abm_params.get('room_dimension', ABM_ROOM_DIMENSION_DEFAULT)
        ax.set_facecolor('lightgray'); 
        ax.set_xticks([]); 
        ax.set_yticks([])
        ax.set_xlim(0, room_dim); 
        ax.set_ylim(0, room_dim); 
        ax.set_aspect('equal')
        self.abm_scatter_susceptible = ax.scatter([],[],c='blue', marker='o', s=30)
        self.abm_scatter_infected = ax.scatter([],[],c='yellow', marker='*', s=70, edgecolors='red')
        #ax.legend(loc='upper right', fontsize='x-small')
        # === TẠO FIG.LEGEND CHO ABM ===
        fig = self.canvas_simulation.fig
        
        # Proxy artist cho "Chưa nhiễm" (Susceptible)
        proxy_susceptible = Line2D([0], [0], linestyle='None', marker='o', 
                                   color='blue', markersize=8, 
                                   label=self.tr("screen3_legend_abm_susceptible"))
        
        # Proxy artist cho "Bị nhiễm" (Infected)
        proxy_infected = Line2D([0], [0], linestyle='None', marker='*', 
                                markerfacecolor='yellow', markeredgecolor='red', 
                                markersize=10, label=self.tr("screen3_legend_abm_infected"))

        legend_handles_abm = [proxy_susceptible, proxy_infected]
        
        # Vị trí và style cho fig.legend (tương tự Model 2)
        legend_loc_fig_abm = 'upper left' 
        bbox_anchor_fig_abm = (0.02, 0.98) # Gần góc trên bên trái của Figure, có chút padding

        # Lưu trữ instance legend mới vào self.current_fig_legend
        self.current_fig_legend = fig.legend(
            handles=legend_handles_abm,
            loc=legend_loc_fig_abm,
            bbox_to_anchor=bbox_anchor_fig_abm,
            bbox_transform=fig.transFigure, # Quan trọng: tọa độ theo Figure
            fontsize='medium',
            markerscale=1.2, # Điều chỉnh kích thước marker trong legend
            borderpad=0.5,   # Padding bên trong viền legend
            labelspacing=0.5, # Khoảng cách giữa các mục
            handletextpad=0.5, # Khoảng cách giữa marker và text
            frameon=True,
            facecolor='#f0f0f0', # Màu nền cho legend
            edgecolor='gray'
        )
        if self.current_fig_legend:
            self.current_fig_legend.set_zorder(100)
        # ... (cập nhật abm_animation_interval) ...
        current_slider_value = self.speed_slider.value()
        current_speed_multiplier = current_slider_value / 10.0 if current_slider_value > 0 else 0.05
        new_interval = int(self.abm_base_interval / current_speed_multiplier) if current_speed_multiplier > 0 else self.abm_base_interval * 20
        self.abm_animation_interval = max(5, min(new_interval, 1000))

        self.is_simulation_running = True
        self.ani = animation.FuncAnimation(self.canvas_simulation.fig,
                                 self._update_abm_frame,
                                 init_func=self._init_abm_frame, # init_func quan trọng
                                 frames=100000, # Chạy "vô hạn" hoặc đến khi logic ABM dừng
                                 interval=self.abm_animation_interval,
                                 blit=False, repeat=False)
        self.canvas_simulation.draw_idle()
        if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(True)
        if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(False)
        if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(False)

    def _init_abm_frame(self):
        if not self.simulation_instance_abm: return []
        ax = self.canvas_simulation.axes
        s_disp, i_disp = get_display_coords_mixed(
            self.simulation_instance_abm.susceptible_coords,
            self.simulation_instance_abm.infected_coords,
            self.abm_params.get('display_max_total', MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY), # Sử dụng hằng số đúng
            self.abm_params.get('display_sample_size', SAMPLE_SIZE_FOR_LARGE_POPULATION) # Sử dụng hằng số đúng
        )
        self.abm_scatter_susceptible.set_offsets(s_disp if s_disp.shape[0] > 0 else np.zeros((0,2)))
        self.abm_scatter_infected.set_offsets(i_disp if i_disp.shape[0] > 0 else np.zeros((0,2)))
        # Xóa các vòng tròn cũ trước khi vẽ mới
        for patch in self.simulation_instance_abm.contact_radius_patches: patch.remove()
        self.simulation_instance_abm.contact_radius_patches.clear()
        self.simulation_instance_abm.update_contact_circles(ax, i_disp)

        #stats = self.simulation_instance_abm.get_current_stats()
        #title = (f"S: {stats['susceptible_count']} - I: {stats['infected_count']} (t={stats['time_step']}) "
        #         f"[N={stats['total_population']}, Display: {s_disp.shape[0]+i_disp.shape[0]}]")
        #ax.set_title(title, fontsize=9)
        return [self.abm_scatter_susceptible, self.abm_scatter_infected] + self.simulation_instance_abm.contact_radius_patches

    def _update_abm_frame(self, frame):
        if self.abm_simulation_visually_finished:
            return [self.abm_scatter_susceptible, self.abm_scatter_infected] + self.simulation_instance_abm.contact_radius_patches if self.simulation_instance_abm and self.abm_scatter_susceptible and self.abm_scatter_infected else []


        if not self.simulation_instance_abm:
            if not self.abm_simulation_visually_finished:
                self.abm_simulation_visually_finished = True
                self.is_simulation_running = False; self.is_simulation_paused = False
                if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source: self.ani.event_source.stop()
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            return []

        simulation_ended_by_logic = self.simulation_instance_abm.step()
        # ... (code vẽ frame của ABM như cũ) ...
        ax = self.canvas_simulation.axes # Lấy lại ax nếu cần, hoặc truyền vào
        s_disp, i_disp = get_display_coords_mixed(
            self.simulation_instance_abm.susceptible_coords, self.simulation_instance_abm.infected_coords,
            self.abm_params.get('display_max_total', MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY),
            self.abm_params.get('display_sample_size', SAMPLE_SIZE_FOR_LARGE_POPULATION)
        )
        if self.abm_scatter_susceptible: self.abm_scatter_susceptible.set_offsets(s_disp if s_disp.shape[0] > 0 else np.zeros((0,2)))
        if self.abm_scatter_infected: self.abm_scatter_infected.set_offsets(i_disp if i_disp.shape[0] > 0 else np.zeros((0,2)))
        for patch in self.simulation_instance_abm.contact_radius_patches: patch.remove()
        self.simulation_instance_abm.contact_radius_patches.clear()
        self.simulation_instance_abm.update_contact_circles(ax, i_disp)

        stats = self.simulation_instance_abm.get_current_stats()
        # ... (cập nhật UI labels) ...
        #if hasattr(self, 'abm_sim_time_value') and self.abm_sim_time_value: # Kiểm tra widget tồn tại
        #    self.abm_sim_time_value.setText(str(stats['time_step']))
        seconds_per_step = self.abm_params.get("seconds_per_step", 0.1)
        actual_time_seconds = stats['time_step'] * seconds_per_step
        if self.result_actual_time_value: self.result_actual_time_value.setText(f"{actual_time_seconds:.2f}")
        if self.result_infected_pop_value: self.result_infected_pop_value.setText(str(stats['infected_count']))
        if self.result_susceptible_pop_value: self.result_susceptible_pop_value.setText(str(stats['susceptible_count']))

        if simulation_ended_by_logic:
            if not self.abm_simulation_visually_finished:
                print(f"Screen 3: ABM Simulation ended by logic. Step {stats['time_step']}, Frame {frame}.")
                self.abm_simulation_visually_finished = True
                self.is_simulation_running = False; self.is_simulation_paused = False
                if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source: self.ani.event_source.stop()
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
        
        return [self.abm_scatter_susceptible, self.abm_scatter_infected] + self.simulation_instance_abm.contact_radius_patches

    def _populate_model5_sim1_data(self):
        print("DEBUG Screen3 _populate: Populating Model 5 Sim 1 data.")
        # ================== HIGHLIGHT START: Reset các biến thuộc tính trước khi gán ==================
        self.m5s1_params = {}
        self.m5s1_t_array = None
        self.m5s1_z_array = None
        # ================== HIGHLIGHT END ==================

        if not self.model5_plot_data_cache or self.current_simulation_type != "model5_sim1":
            print("DEBUG Screen3 _populate: No cache or wrong sim type. Clearing animation params and UI.")
            self.m5s1_params = {}
            # Clear UI labels nếu chúng đã được tạo
            if self.m5_boat_speed_value: self.m5_boat_speed_value.setText("N/A")
            if self.m5_water_speed_value: self.m5_water_speed_value.setText("N/A")
            if self.m5_crossing_time_value: self.m5_crossing_time_value.setText("N/A")
            if self.m5_start_point_boat_value: self.m5_start_point_boat_value.setText("N/A")
            if self.m5_boat_reaches_target_value: self.m5_boat_reaches_target_value.setText(self.tr("Chưa xác định", "Undetermined"))
            if self.m5_boat_final_pos_value: self.m5_boat_final_pos_value.setText("N/A")
            return

        # Lấy thông tin cần thiết từ cache (được truyền từ Screen 2)
        data_cache_s3 = self.model5_plot_data_cache 
        params_from_s2_s3 = data_cache_s3.get('params', {})
        method_short_s3 = data_cache_s3.get('method_short')
        method_steps_s3 = data_cache_s3.get('method_steps')
        h_target_s3 = data_cache_s3.get('h_target')

        print(f"DEBUG M5S1 Populate: Params from S2: {params_from_s2_s3}, Method: {method_short_s3}{method_steps_s3}, h: {h_target_s3}")

        if not all([params_from_s2_s3, method_short_s3, method_steps_s3, h_target_s3 is not None]):
            print("DEBUG M5S1 Populate: Missing critical data from Screen 2 for recalculation.")
            # Hiển thị thông báo lỗi trên canvas nếu cần
            ax = self.canvas_simulation.axes
            if ax:
                ax.clear()
                ax.text(0.5, 0.5, self.tr("Lỗi: Thiếu dữ liệu để chạy lại mô phỏng Sim 1."),
                        color='red', ha='center', va='center', transform=ax.transAxes, fontsize=10)
                self.canvas_simulation.draw_idle()
            return

        # Lấy các giá trị tham số
        u_param_input_s3 = params_from_s2_s3.get('u', 0.0)
        v_param_input_s3 = params_from_s2_s3.get('v', 0.0)
        x0_input_s3 = params_from_s2_s3.get('x0', 10.0)
        y0_input_s3 = params_from_s2_s3.get('y0', 0.0)
        t0_input_s3 = params_from_s2_s3.get('t₀', 0.0)
        t1_input_s3 = params_from_s2_s3.get('t₁', 10.0) # Đây là t_end tối đa từ input

        # Cập nhật UI labels (giữ nguyên logic cũ của bạn)
        # ... (cập nhật self.m5_boat_speed_value.setText(...), etc.) ...
        if self.m5_boat_speed_value: self.m5_boat_speed_value.setText(f"{v_param_input_s3:.2f}")
        if self.m5_water_speed_value: self.m5_water_speed_value.setText(f"{u_param_input_s3:.2f}")
        if self.m5_crossing_time_value: self.m5_crossing_time_value.setText("0.00 s") 
        if self.m5_start_point_boat_value: self.m5_start_point_boat_value.setText(f"({x0_input_s3:.2f}, {y0_input_s3:.2f})")
        if self.m5_boat_reaches_target_value: self.m5_boat_reaches_target_value.setText(self.tr("screen3_m5_determining_status"))
        if self.m5_boat_final_pos_value: self.m5_boat_final_pos_value.setText(self.tr("screen3_m5_determining_status"))

        # --- Chuẩn bị self.m5s1_params cho animation ---
        # 1. Tạo hàm ODE cho Model 5
        # Hàm _model5_ode_system đã có sẵn ở global scope
        ode_func_m5s1 = lambda t, x, y: _model5_ode_system(t, x, y, u_param_input_s3, v_param_input_s3)

        # 2. Chọn solver ABx_system_M5 hoặc AMx_system_M5 (phiên bản cho Sim 1, có v_t, v_n, d)
        solver_sim1_map = {
            "Bashforth": {
                2: AB2_system_M5, 3: AB3_system_M5, 
                4: AB4_system_M5, 5: AB5_system_M5 
            },
            "Moulton": {
                2: AM2_system_M5, 3: AM3_system_M5, 
                4: AM4_system_M5
            }
        }
        solver_for_sim1 = None
        if method_short_s3 in solver_sim1_map and method_steps_s3 in solver_sim1_map[method_short_s3]:
            solver_for_sim1 = solver_sim1_map[method_short_s3][method_steps_s3]
        
        if not solver_for_sim1:
            print(f"ERROR M5S1 Populate: Could not find solver {method_short_s3}{method_steps_s3} for Sim 1.")
            # Hiển thị lỗi trên canvas
            return

        print(f"DEBUG M5S1 Populate: Recalculating with solver {solver_for_sim1.__name__}")

        # 3. Chuẩn bị mảng thời gian và các tham số cho solver
        # Tham số d cho Sim 1 là x0_input_s3
        d_param_sim1 = x0_input_s3 
        # v_t_param cho Sim 1 là v_param_input_s3 (vận tốc thuyền)
        v_t_param_sim1 = v_param_input_s3
        # v_n_param cho Sim 1 là u_param_input_s3 (vận tốc dòng nước)
        v_n_param_sim1 = u_param_input_s3

        # Tạo mảng thời gian dựa trên h_target và khoảng t0, t1
        # Số điểm N cần tính toán lại cho phù hợp với h_target
        interval_length_s3 = t1_input_s3 - t0_input_s3
        if interval_length_s3 <= 0:
            print("ERROR M5S1 Populate: Invalid time interval.")
            return
        
        # Giữ N lớn một chút để quỹ đạo mượt hơn cho animation
        # Có thể bạn muốn số điểm cố định hoặc dựa trên h_target
        num_points_for_anim = max(200, int(np.ceil(interval_length_s3 / h_target_s3))) 
        
        t_recalc_s3 = np.linspace(t0_input_s3, t1_input_s3, num_points_for_anim + 1)

        # 4. Gọi solver
        try:
            # Các hàm ABx_system_M5 và AMx_system_M5 (phiên bản Sim 1) nhận (F, t_array, u10, u20, v_t_param, v_n_param, d_param)
            # Ở đây F là ode_func_m5s1
            # (u10, u20) là (x0_input_s3, y0_input_s3)
            recalc_x, recalc_y = solver_for_sim1(
                ode_func_m5s1, 
                t_recalc_s3, 
                x0_input_s3, 
                y0_input_s3,
                v_t_param_sim1, # v_t
                v_n_param_sim1, # v_n
                d_param_sim1    # d
            )
            self.m5s1_t_array = recalc_x # Thực ra đây là t_array trả về từ solver (có thể bị cắt ngắn)
                                          # Cần đảm bảo solver_for_sim1 trả về (t_actual, x_actual, y_actual)
                                          # Hoặc nếu nó trả về (x, y) thì dùng t_recalc_s3 tương ứng đã cắt.
                                          # GIẢ SỬ: Các hàm ABx_system_M5 đã được sửa để trả về t_actual, x_actual, y_actual
                                          # NẾU KHÔNG, bạn cần điều chỉnh lại phần này.
                                          # TẠM THỜI, nếu solver chỉ trả về x, y:
            
            # Điều chỉnh độ dài của t_recalc_s3 cho khớp với recalc_x, recalc_y (nếu solver cắt ngắn)
            min_len_recalc = min(len(recalc_x), len(recalc_y))
            self.m5s1_t_array = t_recalc_s3[:min_len_recalc]
            self.m5s1_z_array = np.array(list(zip(recalc_x[:min_len_recalc], recalc_y[:min_len_recalc])))
            
            print(f"DEBUG M5S1 Populate: Recalculated trajectory. t_array len: {len(self.m5s1_t_array)}, z_array shape: {self.m5s1_z_array.shape if self.m5s1_z_array is not None else 'None'}")

        except Exception as e_recalc:
            print(f"ERROR M5S1 Populate: Recalculation failed: {e_recalc}")
            import traceback
            traceback.print_exc()
            self.m5s1_t_array = None
            self.m5s1_z_array = None
            # Hiển thị lỗi trên canvas
            ax = self.canvas_simulation.axes
            if ax:
                ax.clear()
                ax.text(0.5, 0.5, self.tr("Lỗi khi tính toán lại quỹ đạo Sim 1."),
                        color='red', ha='center', va='center', transform=ax.transAxes, fontsize=10)
                self.canvas_simulation.draw_idle()
            return
        # Cập nhật self.m5s1_params cho animation (giữ nguyên logic cũ)
        self.m5s1_params = {
            'v_t': v_param_input_s3,
            'v_n': u_param_input_s3,
            'd': x0_input_s3,
            'z0_anim': np.array([x0_input_s3, y0_input_s3]),
            'b_anim': t1_input_s3 # Thời gian kết thúc tối đa
        }
        
        print(f"DEBUG _populate END: self.m5s1_z_array SHAPE: {self.m5s1_z_array.shape if self.m5s1_z_array is not None else 'None'}")
        print(f"DEBUG _populate END: self.m5s1_t_array LEN: {len(self.m5s1_t_array) if self.m5s1_t_array is not None else 'None'}")

    def setup_and_start_model5_pursuit_curve(self, model5_plot_data):
        print("Screen 3: Setting up Model 5 (Pursuit Curve) visualization...")
        self._fully_stop_and_cleanup_animation() # Đã bao gồm reset visually_finished
        if hasattr(self, 'current_fig_legend') and self.current_fig_legend:
            try:
                self.current_fig_legend.remove()
                print("  Fig legend explicitly removed at start of ABM setup.")
            except Exception:
                pass
            self.current_fig_legend = None
        if model5_plot_data is None or not isinstance(model5_plot_data, dict):
            print("ERROR Screen3 setup_model5: model5_plot_data is invalid!")
            self.model5_plot_data_cache = None
            # _fully_stop_and_cleanup_animation đã vẽ lại canvas chờ rồi
            return
        # ================== HIGHLIGHT START: Sửa lại tên biến cho khớp ==================
        if model5_plot_data and isinstance(model5_plot_data, dict): # Sử dụng model5_plot_data ở đây
            self.original_model5_data = model5_plot_data.copy() # Lưu bản sao của dữ liệu gốc
            current_model5_data = model5_plot_data # Dùng model5_plot_data cho lần setup này
            # Gán vào cache để _populate có thể dùng nếu bạn vẫn muốn giữ cache
            self.model5_plot_data_cache = current_model5_data
            print(f"  Model 5: Stored original_model5_data. Params: {self.original_model5_data.get('params', {})}")
        else:
            print("  MODEL5 ERROR: Input model5_plot_data is None or not a dict. Cannot setup Model 5.")
            self.original_model5_data = None # Đảm bảo original data cũng là None
            self.model5_plot_data_cache = None # Và cache cũng vậy
            # _fully_stop_and_cleanup_animation đã vẽ lại canvas chờ rồi
            return
        # ================== HIGHLIGHT END ==================
        print(f"DEBUG Screen3 setup_model5: New model5_plot_data received. Params: {model5_plot_data.get('params', {})}")
        self.model5_plot_data_cache = model5_plot_data

        self.current_simulation_type = "model5_sim1" # Mặc định
        self.current_model5_sim_selected = 1
        self.m5s1_animation_visually_finished = False # Reset cờ cho lần chạy mới

        if hasattr(self, 'sim_list_group') and self.sim_list_group: # Kiểm tra thêm
            self.sim_list_group.setVisible(True)
        self._update_simulation_info_display() # Cập nhật UI tĩnh trước

        if not self.rb_model5_sim1.isChecked():
            # Việc setChecked(True) sẽ trigger _on_model5_sim_selected,
            # hàm này sẽ gọi _populate và _start_boat_animation
            self.rb_model5_sim1.setChecked(True)
        else:
            # Nếu đã check, tự gọi các hàm xử lý
            print("DEBUG Screen3 setup_model5: rb_model5_sim1 was already checked. Manually processing Sim 1.")
            self._populate_model5_sim1_data() # Populate dữ liệu mới
            if self.m5s1_z_array is not None and len(self.m5s1_z_array) > 0:
                self._start_boat_animation_m5s1() # Bắt đầu animation với dữ liệu mới
            else:
                print("DEBUG Screen3 setup_model5 (manual): m5s1_z_array is None or empty after populate. Not starting animation.")
                # Hiển thị lỗi/chờ trên canvas (đã có trong _start_boat_animation_m5s1)
                self._start_boat_animation_m5s1() # Gọi để nó hiển thị "No trajectory data"

        self.btn_stop.setEnabled(False) # Sẽ được bật nếu animation bắt đầu thành công
        self.btn_back_to_screen2.setEnabled(True)
        self.btn_double_back_to_screen1.setEnabled(True)
        print("DEBUG Screen3: setup_and_start_model5_pursuit_curve finished.")

    def _start_boat_animation_m5s1(self):
        try:
            #self._fully_stop_and_cleanup_animation()
            print("DEBUG M5S1: _start_boat_animation_m5s1 called.")

            if self.m5s1_z_array is None or self.m5s1_t_array is None or len(self.m5s1_z_array) == 0:
                print("DEBUG M5S1: No trajectory data for boat animation. Cannot start.")
                ax = self.canvas_simulation.axes
                if ax:
                    ax.clear()
                    ax.text(0.5, 0.5, self.tr("Không có dữ liệu quỹ đạo", "No trajectory data"),
                            color='red', ha='center', va='center', transform=ax.transAxes, fontsize=10)
                    ax.set_facecolor('white')
                    self.canvas_simulation.draw_idle()
                return

            print(f"DEBUG M5S1: Trajectory shape: {self.m5s1_z_array.shape}, Time array shape: {self.m5s1_t_array.shape if self.m5s1_t_array is not None else 'None'}")

            # Reset animation state variables
            self.m5s1_animation_fully_stopped = False
            self.m5s1_ship_has_docked = False
            self.m5s1_docking_frame_index_for_ship = -1
            self.m5s1_ship_journey_complete = False
            self.m5s1_frame_ship_interaction_ends = -1
            self.m5s1_Y_arrows_at_interaction_end = None # Reset vị trí mũi tên khi dừng
            self.m5s1_current_anim_frame = 0

            ax = self.canvas_simulation.axes
            if ax is None:
                print("CRITICAL ERROR M5S1: self.canvas_simulation.axes is None. Cannot proceed.")
                return
            ax.clear()
            print("DEBUG M5S1: Axes cleared in _start_boat_animation_m5s1.")

            # Setup plot limits and background based on standalone logic
            d_val = self.m5s1_params.get('d', 10.0)
            z0_val = self.m5s1_params.get('z0_anim', np.array([d_val, 0.0]))

            x_traj_min, x_traj_max = np.min(self.m5s1_z_array[:, 0]), np.max(self.m5s1_z_array[:, 0])
            y_traj_min, y_traj_max = np.min(self.m5s1_z_array[:, 1]), np.max(self.m5s1_z_array[:, 1])

            padding_x_standalone = 0.1 * d_val
            y_range_for_padding_standalone = max(abs(y_traj_max - y_traj_min), 0.5 * d_val)
            padding_y_abs_standalone = 0.2 * y_range_for_padding_standalone

            xlim_min_standalone = min(x_traj_min - padding_x_standalone, -padding_x_standalone)
            xlim_max_standalone = max(x_traj_max + padding_x_standalone, d_val + padding_x_standalone)

            ylim_min_calc = min(y_traj_min - padding_y_abs_standalone, z0_val[1] - padding_y_abs_standalone)
            ylim_max_calc = max(y_traj_max + padding_y_abs_standalone, z0_val[1] + padding_y_abs_standalone)

            if ylim_min_calc >= -1.0 :
                ylim_min_standalone = min(ylim_min_calc, -max(2.0, padding_y_abs_standalone))
            else:
                ylim_min_standalone = ylim_min_calc

            if ylim_max_calc <= 1.0:
                ylim_max_standalone = max(ylim_max_calc, max(2.0, padding_y_abs_standalone))
            else:
                ylim_max_standalone = ylim_max_calc

            ax.set_xlim(xlim_min_standalone, xlim_max_standalone)
            ax.set_ylim(ylim_min_standalone, ylim_max_standalone)

            y_min_plot, y_max_plot = ax.get_ylim()
            x_min_plot, x_max_plot = ax.get_xlim()
            print(f"DEBUG M5S1: Final Axes Limits -> Xlim: ({x_min_plot:.2f}, {x_max_plot:.2f}), Ylim: ({y_min_plot:.2f}, {y_max_plot:.2f})")

            ax.fill_betweenx([y_min_plot, y_max_plot], x_min_plot, 0, color='#A0522D', alpha=0.8, zorder=0)
            ax.fill_betweenx([y_min_plot, y_max_plot], 0, d_val, color='#87CEEB', alpha=0.7, zorder=0)
            ax.fill_betweenx([y_min_plot, y_max_plot], d_val, x_max_plot, color='#A0522D', alpha=0.8, zorder=0)

            # Create plot artists
            try:
                self.m5s1_line_ship_path, = ax.plot([], [], '--', lw=2.5, color='darkslategray', label=self.tr("Quỹ đạo di chuyển", "Path"), zorder=2)
                self.m5s1_point_ship, = ax.plot([], [], marker='$\u2605$', markersize=15, color='gold',
                                               markeredgecolor='red', markeredgewidth=0.5, label=self.tr("Con tàu", "Boat"), zorder=3)

                v_n_val = self.m5s1_params.get('v_n', 0.0)
                self.m5s1_quiver_water = None
                # self.m5s1_frames_for_arrows_to_drain = 0 # Không dùng nữa
                if v_n_val != 0:
                    num_arrows_x = 8; num_arrows_y = 6
                    x_coords_arr = np.linspace(0 + d_val/(2*num_arrows_x), d_val - d_val/(2*num_arrows_x), num_arrows_x)
                    y_coords_template_arr = np.linspace(y_min_plot + (y_max_plot-y_min_plot)/(2*num_arrows_y),
                                                        y_max_plot - (y_max_plot-y_min_plot)/(2*num_arrows_y),
                                                        num_arrows_y)
                    self.m5s1_X_arrows_positions, self.m5s1_Y_arrows_initial_positions = np.meshgrid(x_coords_arr, y_coords_template_arr)
                    U_arrows_vec_arr = np.zeros_like(self.m5s1_X_arrows_positions)
                    V_arrows_vec_arr = -np.sign(v_n_val) * np.ones_like(self.m5s1_Y_arrows_initial_positions)

                    self.m5s1_quiver_water = ax.quiver(self.m5s1_X_arrows_positions.ravel(),
                                                     self.m5s1_Y_arrows_initial_positions.ravel(),
                                                     U_arrows_vec_arr.ravel(), V_arrows_vec_arr.ravel(),
                                                     color='blue', scale=25, width=0.004,
                                                     headwidth=5, headlength=7, zorder=1, alpha=1.0)
                    print("DEBUG M5S1: Water quiver created.")

                    self.m5s1_arrow_shift_per_frame = abs(v_n_val) * ( (self.m5s1_t_array[1] - self.m5s1_t_array[0]) if len(self.m5s1_t_array) > 1 else 0.02 ) * 0.5
                else:
                    self.m5s1_arrow_shift_per_frame = 0

                # Legend
                proxy_ship_legend = Line2D([0], [0], linestyle='None', marker='$\u2605$', markersize=10, color='gold', markeredgecolor='red', markeredgewidth=0.15, label=self.tr("Con tàu", "Boat"))
                legend_handles = [self.m5s1_line_ship_path, proxy_ship_legend]
                legend_labels = [self.tr("screen3_legend_m5s1_path"),self.tr("screen3_legend_m5s1_boat"),]
                if self.m5s1_quiver_water:
                    arrow_marker_char = r'$\downarrow$' if v_n_val > 0 else (r'$\uparrow$' if v_n_val < 0 else '')
                    if arrow_marker_char:
                        proxy_arrow = Line2D([0], [0], linestyle='None', marker=arrow_marker_char, markersize=10, markerfacecolor='blue', markeredgecolor='blue')
                        legend_handles.append(proxy_arrow)
                        legend_labels.append(self.tr("screen3_legend_m5s1_water_current"))

                legend_bbox_x_val = 0.99
                if (x_max_plot - x_min_plot) != 0:
                     legend_bbox_x_val = (d_val - x_min_plot) / (x_max_plot - x_min_plot) - 0.005
                     legend_bbox_x_val = min(0.99, max(0.7, legend_bbox_x_val))
                legend_bbox_y_val = 0.98
                self.m5s1_legend_obj = ax.legend(legend_handles, legend_labels, loc="upper right",
                                                 bbox_to_anchor=(legend_bbox_x_val, legend_bbox_y_val),
                                                 facecolor='lightgray', edgecolor='black', labelcolor='black', framealpha=0.9, fontsize='small')
                if self.m5s1_legend_obj: self.m5s1_legend_obj.set_zorder(20)
                print("DEBUG M5S1: Legend created.")

            except Exception as e_create_artist:
                print(f"ERROR M5S1 creating artists: {e_create_artist}")
                import traceback
                traceback.print_exc()
                return

            if self.m5s1_line_ship_path is None or self.m5s1_point_ship is None:
                print("CRITICAL ERROR M5S1: A primary artist (line or point) is None AFTER supposed creation block!")
                return

            ax.axhline(0, color='slategray', linestyle=':', linewidth=1.2, zorder=0.5)
            ax.axvline(0, color='gray', linestyle=':', linewidth=0.8, zorder=0.5)
            ax.axvline(d_val, color='gray', linestyle=':', linewidth=0.8, zorder=0.5)

            #ax.set_xlabel(self.tr("Vị trí X (m)", "X Position (m)"), fontsize=9)
            #ax.set_ylabel(self.tr("Vị trí Y (m)", "Y Position (m)"), fontsize=9)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.grid(True, linestyle=':', alpha=0.6, zorder=-1)

            # ----- START: THÊM XTICKS VÀ YTICKS -----
            # Sử dụng MaxNLocator để Matplotlib tự động chọn số lượng ticks hợp lý
            # Đảm bảo đã import: from matplotlib.ticker import MaxNLocator
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5, prune='both')) # nbins có thể là 'auto' hoặc một số nguyên
            ax.yaxis.set_major_locator(MaxNLocator(nbins=5, prune='both')) # prune='both' để tránh tick ở đầu/cuối nếu không đẹp
            ax.tick_params(axis='both', which='major', labelsize=8)
            
            try:
                self.canvas_simulation.fig.tight_layout(pad=1.0)
                # Điều chỉnh lề để có thêm không gian cho nhãn trục
                # Các giá trị này là tỷ lệ phần trăm của chiều rộng/cao của figure
                # Bạn có thể cần thử nghiệm các giá trị khác nhau
                #self.canvas_simulation.fig.subplots_adjust(left=0.5, bottom=0.5, right=0.5, top=1.66)
            except Exception as e_adjust:
                print(f"Error adjusting subplots: {e_adjust}")

            # Total frames for animation: length of trajectory plus a small buffer
            self.m5s1_num_frames_total_animation = len(self.m5s1_z_array) + 5 # Buffer of 5 frames

            current_slider_value = self.speed_slider.value()
            current_speed_multiplier = current_slider_value / 10.0 if current_slider_value > 0 else 0.05
            new_interval = int(self.m5s1_base_interval / current_speed_multiplier) if current_speed_multiplier > 0 else self.m5s1_base_interval * 20
            self.m5s1_animation_interval = max(20, min(new_interval, 500))

            print(f"DEBUG M5S1: Total animation frames: {self.m5s1_num_frames_total_animation}, Interval: {self.m5s1_animation_interval} ms")

            self.is_simulation_running = True
            self.is_simulation_paused = False

            self.ani = animation.FuncAnimation(
                self.canvas_simulation.fig,
                self._update_model5_sim1_frame,
                frames=self.m5s1_num_frames_total_animation,
                init_func=self._init_model5_sim1_animation,
                blit=False,
                interval=self.m5s1_animation_interval,
                repeat=False
            )
            print("DEBUG M5S1: FuncAnimation created.")
            self.canvas_simulation.draw_idle()
            print("DEBUG M5S1: canvas_simulation.draw_idle() called after FuncAnimation.")

            self.btn_stop.setEnabled(True)
            self.btn_back_to_screen2.setEnabled(False)
            self.btn_double_back_to_screen1.setEnabled(False)
            print("DEBUG M5S1: _start_boat_animation_m5s1 finished successfully.")

        except Exception as e_start_anim_outer:
            print(f"ERROR in _start_boat_animation_m5s1 (outer try-except): {e_start_anim_outer}")
            import traceback
            traceback.print_exc()
            ax = self.canvas_simulation.axes
            if ax:
                ax.clear()
                ax.text(0.5, 0.5, self.tr("Lỗi khi bắt đầu mô phỏng", "Error starting simulation"),
                        color='red', ha='center', va='center', transform=ax.transAxes)
                #ax.set_xticks([]); ax.set_yticks([])
                self.canvas_simulation.draw_idle()
            self.btn_stop.setEnabled(False)
            self.btn_back_to_screen2.setEnabled(True)
            self.btn_double_back_to_screen1.setEnabled(True)

    def _init_model5_sim1_animation(self):
        try:
            print("DEBUG M5S1: _init_model5_sim1_animation called.")
            self.m5s1_line_ship_path.set_data([], [])
            self.m5s1_point_ship.set_data([], [])
            if self.m5s1_quiver_water and self.m5s1_X_arrows_positions is not None and self.m5s1_Y_arrows_initial_positions is not None:
                self.m5s1_quiver_water.set_offsets(np.c_[self.m5s1_X_arrows_positions.ravel(), self.m5s1_Y_arrows_initial_positions.ravel()])
                self.m5s1_quiver_water.set_visible(True)

            # Reset state vars
            self.m5s1_animation_fully_stopped = False
            self.m5s1_ship_has_docked = False
            self.m5s1_docking_frame_index_for_ship = -1
            self.m5s1_ship_journey_complete = False
            self.m5s1_frame_ship_interaction_ends = -1
            self.m5s1_Y_arrows_at_interaction_end = None # Reset vị trí mũi tên
            self.m5s1_current_anim_frame = 0

            artists = [self.m5s1_line_ship_path, self.m5s1_point_ship]
            if self.m5s1_legend_obj: artists.append(self.m5s1_legend_obj)
            if self.m5s1_quiver_water: artists.append(self.m5s1_quiver_water)
            print(f"DEBUG M5S1: Init returning {len(artists)} artists.")
            return artists
        except Exception as e:
            print(f"ERROR in _init_model5_sim1_animation: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _update_model5_sim1_frame(self, frame):
        try:
            self.m5s1_current_anim_frame = frame
            current_time_in_animation = 0.0
            # ================== HIGHLIGHT START: Logic mới khi hết frame ==================
            if self.m5s1_animation_visually_finished: # Nếu đã đánh dấu là xong về mặt hình ảnh
                return [] # Không làm gì thêm, giữ nguyên frame cuối
            # Xác định thời gian hiện tại của thuyền trong animation
            if self.m5s1_t_array is not None and frame < len(self.m5s1_t_array):
                current_time_in_animation = self.m5s1_t_array[frame]
            elif self.m5s1_t_array is not None and len(self.m5s1_t_array) > 0: # Nếu frame vượt quá, dùng thời gian cuối
                current_time_in_animation = self.m5s1_t_array[-1]
            
            # Cập nhật label thời gian mô phỏng
            if self.m5_crossing_time_value:
                max_sim_time_from_s2 = self.m5s1_params.get('b_anim', 0.0) # Thời gian tối đa của quỹ đạo
                # self.m5_crossing_time_value.setText(f"{current_time_in_animation:.2f} s / {max_sim_time_from_s2:.2f} s")
                self.m5_crossing_time_value.setText(f"{current_time_in_animation:.2f} s")
            # Kiểm tra nếu animation đã chạy hết logic (docked hoặc hết quỹ đạo)
            # hoặc đã chạy đủ số frame của quỹ đạo
            is_logical_end = (self.m5s1_ship_has_docked or self.m5s1_ship_journey_complete or \
                              frame >= len(self.m5s1_z_array) -1 )

            if is_logical_end and not self.m5s1_animation_visually_finished:
                print(f"DEBUG M5S1 Update: Logical end of animation reached at frame {frame}.")
                self.m5s1_animation_visually_finished = True # Đánh dấu là đã xong về hiển thị
                self.is_simulation_running = False # Không còn "đang chạy" theo nghĩa tự động nữa
                self.is_simulation_paused = False  # Cũng không phải là "paused"
                
                if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source is not None:
                    try:
                        self.ani.event_source.stop() # Dừng timer để không gọi frame tiếp theo
                        print("  M5S1: Animation timer stopped (visually finished).")
                    except Exception as e:
                        print(f"  M5S1: Error stopping timer on visual finish: {e}")
                
                # Vẫn bật nút "Dừng/Tiếp" nhưng nó sẽ không có tác dụng Resume nữa (xem _toggle_pause_resume_animation)
                # Các nút Back sẽ được enable
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False) # Có thể vô hiệu hóa nút Stop luôn
            # ================== HIGHLIGHT END ==================
                # Cập nhật "Thuyền có đến đích không?" và "Vị trí cuối"
                final_x_pos = self.m5s1_z_array[-1, 0] if self.m5s1_z_array is not None and len(self.m5s1_z_array) > 0 else 0.0
                final_y_pos = self.m5s1_z_array[-1, 1] if self.m5s1_z_array is not None and len(self.m5s1_z_array) > 0 else 0.0
                
                if self.m5_boat_final_pos_value:
                    self.m5_boat_final_pos_value.setText(f"({final_x_pos:.2f}, {final_y_pos:.2f})")

                if self.m5_boat_reaches_target_value:
                    # Điều kiện đến đích: x cuối cùng rất gần 0
                    # self.m5s1_params.get('d', 10.0) là chiều rộng sông ban đầu (x0)
                    if abs(final_x_pos) < 0.01 * self.m5s1_params.get('d', 10.0):
                        self.m5_boat_reaches_target_value.setText(self.tr("answer_yes"))
                    else:
                        self.m5_boat_reaches_target_value.setText(self.tr("answer_no"))
            # Điều kiện dừng cũ hơn (nếu vượt quá tổng số frame dự kiến)
            if frame >= self.m5s1_num_frames_total_animation - 1 and not self.m5s1_animation_visually_finished:
                print(f"DEBUG M5S1 Update: Reached total animation frames ({frame}). Forcing visual finish.")
                self.m5s1_animation_visually_finished = True
                self.is_simulation_running = False
                self.is_simulation_paused = False
                if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source:
                    self.ani.event_source.stop()
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            
            # Nếu animation đang chạy bình thường (chưa đến điểm kết thúc logic)
            if self.is_simulation_running and not self.m5s1_animation_visually_finished:
                 # ... (code vẽ thuyền, mũi tên như cũ) ...
                current_ship_path_idx = min(frame, len(self.m5s1_z_array) - 1)
                ship_event_this_frame = False # Reset cho mỗi frame
                # --- Ship movement and docking/completion check ---
                if not self.m5s1_ship_has_docked and not self.m5s1_ship_journey_complete:
                    ship_x_pos = self.m5s1_z_array[current_ship_path_idx, 0]
                    self.m5s1_line_ship_path.set_data(self.m5s1_z_array[:current_ship_path_idx+1, 0],
                                                    self.m5s1_z_array[:current_ship_path_idx+1, 1])
                    self.m5s1_point_ship.set_data([ship_x_pos], [self.m5s1_z_array[current_ship_path_idx, 1]])

                    if ship_x_pos <= 1e-4 and frame > 0: # Docked
                        self.m5s1_ship_has_docked = True
                        self.m5s1_docking_frame_index_for_ship = current_ship_path_idx
                        self.m5s1_frame_ship_interaction_ends = frame # Lưu frame tương tác kết thúc
                        ship_event_this_frame = True
                        print(f"DEBUG M5S1: Ship docked at frame {frame}, index {current_ship_path_idx}")
                    elif frame >= len(self.m5s1_z_array) - 1: # Reached end of trajectory
                        if not self.m5s1_ship_has_docked:
                            self.m5s1_ship_journey_complete = True
                            self.m5s1_frame_ship_interaction_ends = frame
                            ship_event_this_frame = True
                            print(f"DEBUG M5S1: Ship journey complete (all points) at frame {frame}")
                
                # --- Water current arrows update (logic như cũ, nhưng có thể tối ưu) ---
                # ... (logic vẽ mũi tên)
                v_n_val = self.m5s1_params.get('v_n', 0.0)
                ship_interaction_has_ended_anim = self.m5s1_ship_has_docked or self.m5s1_ship_journey_complete

                if self.m5s1_quiver_water and self.m5s1_Y_arrows_initial_positions is not None and self.m5s1_X_arrows_positions is not None and v_n_val != 0:
                    current_Y_for_arrows_np = None
                    y_min_plot_val, y_max_plot_val = self.canvas_simulation.axes.get_ylim()
                    direction_multiplier = -np.sign(v_n_val)

                    if not ship_interaction_has_ended_anim:
                        total_y_shift_magnitude = frame * self.m5s1_arrow_shift_per_frame
                        Y_raw_shifted_from_start_val = self.m5s1_Y_arrows_initial_positions + direction_multiplier * total_y_shift_magnitude
                        if direction_multiplier < 0: 
                            current_Y_for_arrows_np = y_max_plot_val - ((y_max_plot_val - Y_raw_shifted_from_start_val) % (y_max_plot_val - y_min_plot_val))
                        else: 
                            current_Y_for_arrows_np = y_min_plot_val + ((Y_raw_shifted_from_start_val - y_min_plot_val) % (y_max_plot_val - y_min_plot_val))
                        if ship_event_this_frame and self.m5s1_Y_arrows_at_interaction_end is None:
                            self.m5s1_Y_arrows_at_interaction_end = current_Y_for_arrows_np.copy()
                    else: # Ship has stopped, use saved arrow positions
                        if self.m5s1_Y_arrows_at_interaction_end is not None:
                            current_Y_for_arrows_np = self.m5s1_Y_arrows_at_interaction_end
                        # Fallback if somehow m5s1_Y_arrows_at_interaction_end was not set
                        elif self.m5s1_frame_ship_interaction_ends != -1:
                            total_y_shift_magnitude_at_stop = self.m5s1_frame_ship_interaction_ends * self.m5s1_arrow_shift_per_frame
                            Y_raw_at_stop = self.m5s1_Y_arrows_initial_positions + direction_multiplier * total_y_shift_magnitude_at_stop
                            if direction_multiplier < 0: self.m5s1_Y_arrows_at_interaction_end = y_max_plot_val - ((y_max_plot_val - Y_raw_at_stop) % (y_max_plot_val - y_min_plot_val))
                            else: self.m5s1_Y_arrows_at_interaction_end = y_min_plot_val + ((Y_raw_at_stop - y_min_plot_val) % (y_max_plot_val - y_min_plot_val))
                            current_Y_for_arrows_np = self.m5s1_Y_arrows_at_interaction_end

                    if current_Y_for_arrows_np is not None:
                        self.m5s1_quiver_water.set_offsets(np.c_[self.m5s1_X_arrows_positions.ravel(), current_Y_for_arrows_np.ravel()])


            # Return artists (danh sách này nên cố định nếu dùng blit=True,
            # nhưng với blit=False, Matplotlib sẽ tự xử lý việc vẽ lại)
            artists_to_return = []
            if hasattr(self, 'm5s1_line_ship_path') and self.m5s1_line_ship_path: artists_to_return.append(self.m5s1_line_ship_path)
            if hasattr(self, 'm5s1_point_ship') and self.m5s1_point_ship: artists_to_return.append(self.m5s1_point_ship)
            if hasattr(self, 'm5s1_legend_obj') and self.m5s1_legend_obj: artists_to_return.append(self.m5s1_legend_obj)
            if hasattr(self, 'm5s1_quiver_water') and self.m5s1_quiver_water: artists_to_return.append(self.m5s1_quiver_water)
            return artists_to_return

        except Exception as e:
            # ... (xử lý lỗi như cũ, nhưng không gọi _fully_stop_and_cleanup_animation ngay)
            print(f"ERROR in _update_model5_sim1_frame (frame {frame}): {e}")
            import traceback
            traceback.print_exc()
            # Có thể dừng timer ở đây nếu lỗi nghiêm trọng
            if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source:
                self.ani.event_source.stop()
            self.is_simulation_running = False
            self.btn_stop.setEnabled(False) # Vô hiệu hóa nút stop/resume
            self.btn_back_to_screen2.setEnabled(True)
            self.btn_double_back_to_screen1.setEnabled(True)
            return []

    def _prepare_and_start_model5_sim2_animation(self):
        self._fully_stop_and_cleanup_animation() # Dọn dẹp animation/trạng thái cũ
        self.current_simulation_type = "model5_sim2"
        self.m5s2_animation_visually_finished = False
        self.is_simulation_paused = False
        print("DEBUG M5S2: Preparing Model 5 - Simulation 2 (Destroyer vs Submarine)")

        ax = self.canvas_simulation.axes
        if ax is None:
            print("CRITICAL ERROR M5S2: Canvas axes not available.")
            if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            return
        ax.clear()
        ax.set_facecolor('#AFDDFF')

        if not self.model5_plot_data_cache or not isinstance(self.model5_plot_data_cache, dict):
            ax.text(0.5, 0.5, self.tr("Lỗi: Thiếu dữ liệu đầu vào từ Screen 2."),
                    color='red', ha='center', va='center', transform=ax.transAxes, fontsize=10)
            self.canvas_simulation.draw_idle()
            if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            return

        cached_s2_data = self.model5_plot_data_cache
        params_from_s2 = cached_s2_data.get('params', {})

        # --- 1. Khởi tạo Tham Số Mô Phỏng ---
        V_TN_MAX_SIM = params_from_s2.get('u', 3.0)
        R_TN_PARAM_SIM = 2.0
        V_KT_SIM = params_from_s2.get('v', 6.0)
        # Ưu tiên INITIAL_DISTANCE_D_SIM từ thuộc tính nếu đã được set (ví dụ từ code standalone)
        INITIAL_DISTANCE_D_SIM = getattr(self, 'm5s2_INITIAL_DISTANCE_D_SIM_standalone_value', 30.0)
        if INITIAL_DISTANCE_D_SIM is None : INITIAL_DISTANCE_D_SIM = 30.0 # Fallback nếu thuộc tính không tồn tại

        OMEGA_TN_PARAM_SIM = V_TN_MAX_SIM / R_TN_PARAM_SIM if R_TN_PARAM_SIM > 1e-6 else 0.1
        
        T_START_SIM = params_from_s2.get('t₀', 0.0)
        t1_value_from_screen2_for_comparison = params_from_s2.get('t₁', T_START_SIM + 150.0) # Dòng cũ
        SOLVER_MAX_DURATION_GUESS = 70.0
        if t1_value_from_screen2_for_comparison <= 70.0:
            SOLVER_MAX_DURATION_GUESS = 70.0
        else:
            SOLVER_MAX_DURATION_GUESS = T_END_SIM_S2
        T_END_SIM_S2 = T_START_SIM + SOLVER_MAX_DURATION_GUESS
        SIMULATION_DURATION_B_SIM = SOLVER_MAX_DURATION_GUESS
        print(f"DEBUG M5S2: Initial SOLVER_MAX_DURATION_GUESS: {SOLVER_MAX_DURATION_GUESS}s. Calculated T_END_SIM_S2: {T_END_SIM_S2}")

        # Các tham số hành vi và hằng số
        self.m5s2_current_avoidance_radius = INITIAL_DISTANCE_D_SIM * 0.40
        AVOIDANCE_STRENGTH_FACTOR_SIM = 1.1
        self.m5s2_catch_threshold = 0.75 # Ngưỡng bắt
        FIELD_OF_VIEW_TN_DEGREES_SIM = 120.0
        self.m5s2_current_kt_radar_radius = self.m5s2_current_avoidance_radius * 2.8
        MIN_TIME_BETWEEN_FREE_TURNS_TN_SIM = SOLVER_MAX_DURATION_GUESS / 10.0
        FREE_TURN_ANGLE_MAX_RAD_TN_SIM = np.deg2rad(50)
        
        # Tính toán INITIAL_VIEW_LIMIT_APP dựa trên các tham số đã có
        self.m5s2_INITIAL_VIEW_LIMIT_APP = max(45.0, INITIAL_DISTANCE_D_SIM * 1.6, self.m5s2_current_kt_radar_radius * 1.2)
        self.m5s2_current_view_span = self.m5s2_INITIAL_VIEW_LIMIT_APP # Reset khi bắt đầu sim mới
        print(f"DEBUG M5S2: Initial View Limit App: {self.m5s2_INITIAL_VIEW_LIMIT_APP:.2f}, Current View Span: {self.m5s2_current_view_span:.2f}")


        # Lưu các tham số vào self.m5s2_params
        self.m5s2_params = {
            'v_kt': V_KT_SIM, 'z0_kt': np.array([params_from_s2.get('x0', 0.0), params_from_s2.get('y0', 0.0)]),
            'v_tn_max': V_TN_MAX_SIM,
            't_start': T_START_SIM,
            't_end': T_END_SIM_S2, # t_end cho solver
            'simulation_duration': SOLVER_MAX_DURATION_GUESS,
            'method_short': cached_s2_data.get('method_short', 'Bashforth'),
            'method_steps': cached_s2_data.get('method_steps', 4),
            'avoidance_radius': self.m5s2_current_avoidance_radius,
            'avoidance_strength': AVOIDANCE_STRENGTH_FACTOR_SIM,
            'fov_tn_degrees': FIELD_OF_VIEW_TN_DEGREES_SIM,
            'kt_radar_radius': self.m5s2_current_kt_radar_radius,
            'min_time_free_turn': MIN_TIME_BETWEEN_FREE_TURNS_TN_SIM,
            'max_angle_free_turn_rad': FREE_TURN_ANGLE_MAX_RAD_TN_SIM,
            'catch_threshold': self.m5s2_catch_threshold,
            'R_TN_PARAM': R_TN_PARAM_SIM, # Thêm R_TN_PARAM vào đây
            'OMEGA_TN_PARAM': OMEGA_TN_PARAM_SIM # Thêm OMEGA_TN_PARAM
        }
        z0_kt_sim = self.m5s2_params['z0_kt'] # Lấy từ params đã lưu

        # Sinh quỹ đạo cơ sở TN và offset
        random_angle_init = random.uniform(0, 2 * np.pi)
        tn_offset_x_from_kt_init = INITIAL_DISTANCE_D_SIM * np.cos(random_angle_init)
        tn_offset_y_from_kt_init = INITIAL_DISTANCE_D_SIM * np.sin(random_angle_init)
        num_terms_x_sim = 1; num_terms_y_sim = 1
        params_x_tn_sim = []
        sum_sin_cos_x_at_t0_sim = 0
        for _ in range(num_terms_x_sim):
            p_temp_sim = {"amp": random.uniform(self.m5s2_params['R_TN_PARAM'] * 6.0, self.m5s2_params['R_TN_PARAM'] * 12.0),
                          "freq": random.uniform(self.m5s2_params['OMEGA_TN_PARAM'] * 0.015, self.m5s2_params['OMEGA_TN_PARAM'] * 0.07) if self.m5s2_params['OMEGA_TN_PARAM'] > 0 else random.uniform(0.001, 0.01),
                          "phase": random.uniform(0, 2 * np.pi), "type": random.choice(['sin', 'cos'])}
            params_x_tn_sim.append(p_temp_sim)
            val_at_t0 = p_temp_sim["amp"] * (np.sin(p_temp_sim["freq"] * T_START_SIM + p_temp_sim["phase"]) if p_temp_sim["type"] == 'sin' else np.cos(p_temp_sim["freq"] * T_START_SIM + p_temp_sim["phase"]))
            sum_sin_cos_x_at_t0_sim += val_at_t0
        params_y_tn_sim = []
        sum_sin_cos_y_at_t0_sim = 0
        for _ in range(num_terms_y_sim):
            p_temp_sim = {"amp": random.uniform(self.m5s2_params['R_TN_PARAM'] * 5.0, self.m5s2_params['R_TN_PARAM'] * 10.0),
                          "freq": random.uniform(self.m5s2_params['OMEGA_TN_PARAM'] * 0.02, self.m5s2_params['OMEGA_TN_PARAM'] * 0.08) if self.m5s2_params['OMEGA_TN_PARAM'] > 0 else random.uniform(0.001, 0.01),
                          "phase": random.uniform(0, 2 * np.pi), "type": random.choice(['sin', 'cos'])}
            params_y_tn_sim.append(p_temp_sim)
            val_at_t0 = p_temp_sim["amp"] * (np.sin(p_temp_sim["freq"] * T_START_SIM + p_temp_sim["phase"]) if p_temp_sim["type"] == 'sin' else np.cos(p_temp_sim["freq"] * T_START_SIM + p_temp_sim["phase"]))
            sum_sin_cos_y_at_t0_sim += val_at_t0
        offset_x_tn_sim = z0_kt_sim[0] + tn_offset_x_from_kt_init - sum_sin_cos_x_at_t0_sim
        offset_y_tn_sim = z0_kt_sim[1] + tn_offset_y_from_kt_init - sum_sin_cos_y_at_t0_sim
        self.m5s2_submarine_trajectory_params = {
            "offset_x": offset_x_tn_sim, "offset_y": offset_y_tn_sim,
            "params_x": params_x_tn_sim, "params_y": params_y_tn_sim
        }

        # Cập nhật UI ban đầu
        z_tn_actual_start_sim = self._z_tn_m5s2(T_START_SIM)
        if self.m5_destroyer_speed_value: self.m5_destroyer_speed_value.setText(f"{V_KT_SIM:.2f}")
        if self.m5_submarine_speed_value: self.m5_submarine_speed_value.setText(f"{V_TN_MAX_SIM:.2f}")
        if self.m5_start_point_destroyer_value: self.m5_start_point_destroyer_value.setText(f"({z0_kt_sim[0]:.2f}, {z0_kt_sim[1]:.2f})")
        if self.m5_start_point_submarine_value: self.m5_start_point_submarine_value.setText(f"({z_tn_actual_start_sim[0]:.2f}, {z_tn_actual_start_sim[1]:.2f})")
        if self.m5_destroyer_catches_submarine_value : self.m5_destroyer_catches_submarine_value.setText(self.tr("screen3_m5_determining_status"))
        if self.m5_catch_point_value: self.m5_catch_point_value.setText(self.tr("screen3_m5_determining_status"))
        if self.m5_catch_time_value: self.m5_catch_time_value.setText("0.00 s")
        
        self.m5s2_last_kt_pursuit_direction = np.array([random.uniform(-1,1), random.uniform(-1,1)])
        norm_dir_kt_init = np.linalg.norm(self.m5s2_last_kt_pursuit_direction)
        if norm_dir_kt_init > 1e-9: self.m5s2_last_kt_pursuit_direction /= norm_dir_kt_init
        else: self.m5s2_last_kt_pursuit_direction = np.array([1.0, 0.0])
        self.m5s2_last_non_avoid_turn_time_tn = T_START_SIM - self.m5s2_params['min_time_free_turn'] * 2.0 # Cho phép rẽ ngay

        # --- 2. Định nghĩa f_combined_for_solver ---
        def f_combined_for_solver(t_ode, current_state_ode_local):
            z_kt_curr_ode = current_state_ode_local[0:2]
            z_tn_curr_ode = current_state_ode_local[2:4]
            dx_kt_ode, dy_kt_ode = 0.0, 0.0
            distance_kt_to_tn_ode = np.linalg.norm(z_tn_curr_ode - z_kt_curr_ode)

            if 0 < distance_kt_to_tn_ode < self.m5s2_params['kt_radar_radius']:
                if distance_kt_to_tn_ode > self.m5s2_params['catch_threshold'] / 2.0:
                    direction_to_tn_unit_ode = (z_tn_curr_ode - z_kt_curr_ode) / distance_kt_to_tn_ode
                    dx_kt_ode = self.m5s2_params['v_kt'] * direction_to_tn_unit_ode[0]
                    dy_kt_ode = self.m5s2_params['v_kt'] * direction_to_tn_unit_ode[1]
                    self.m5s2_last_kt_pursuit_direction = direction_to_tn_unit_ode
            elif distance_kt_to_tn_ode > self.m5s2_params['catch_threshold'] / 2.0:
                dx_kt_ode = (self.m5s2_params['v_kt'] * 0.5) * self.m5s2_last_kt_pursuit_direction[0]
                dy_kt_ode = (self.m5s2_params['v_kt'] * 0.5) * self.m5s2_last_kt_pursuit_direction[1]

            v_base_tn_scaled_ode = self._get_base_submarine_velocity_m5s2(
                t_ode,
                self.m5s2_submarine_trajectory_params["params_x"],
                self.m5s2_submarine_trajectory_params["params_y"],
                self.m5s2_params['v_tn_max']
            )
            norm_v_base_ode = np.linalg.norm(v_base_tn_scaled_ode)
            v_base_tn_normalized_direction_ode = v_base_tn_scaled_ode / norm_v_base_ode if norm_v_base_ode > 1e-6 else np.array([0.0,0.0])
            
            v_avoid_actual_ode, currently_avoiding_ode = self._get_smarter_avoidance_info_m5s2(
                z_tn_curr_ode, z_kt_curr_ode, v_base_tn_normalized_direction_ode,
                self.m5s2_params['avoidance_radius'], self.m5s2_params['v_tn_max'],
                self.m5s2_params['avoidance_strength'], self.m5s2_params['fov_tn_degrees']
            )
            
            v_total_tn_desired_ode = np.array([0.0,0.0])
            if currently_avoiding_ode:
                avoid_weight = 0.8 # Trọng số cho việc né
                base_weight = 0.2  # Trọng số cho quỹ đạo cơ sở
                v_total_tn_desired_ode = base_weight * v_base_tn_scaled_ode + avoid_weight * v_avoid_actual_ode
                #v_total_tn_desired_ode = v_avoid_actual_ode #v_base_tn_scaled_ode +
                print(f"T={t_ode:.2f} AVOIDING: BaseV=({v_base_tn_scaled_ode[0]:.1f},{v_base_tn_scaled_ode[1]:.1f}), AvoidV=({v_avoid_actual_ode[0]:.1f},{v_avoid_actual_ode[1]:.1f}), TotalV=({v_total_tn_desired_ode[0]:.1f},{v_total_tn_desired_ode[1]:.1f})")
            else:
                v_final_base_ode = v_base_tn_scaled_ode
                if (t_ode - self.m5s2_last_non_avoid_turn_time_tn) >= self.m5s2_params['min_time_free_turn'] and norm_v_base_ode > 1e-6:
                    random_turn_angle_ode = random.uniform(-self.m5s2_params['max_angle_free_turn_rad'], self.m5s2_params['max_angle_free_turn_rad'])
                    cos_a_ode, sin_a_ode = np.cos(random_turn_angle_ode), np.sin(random_turn_angle_ode)
                    rotation_matrix_ode = np.array([[cos_a_ode, -sin_a_ode], [sin_a_ode,  cos_a_ode]])
                    v_final_base_ode = np.dot(rotation_matrix_ode, v_base_tn_scaled_ode)
                    self.m5s2_last_non_avoid_turn_time_tn = t_ode
                v_total_tn_desired_ode = v_final_base_ode
            norm_total_tn_ode = np.linalg.norm(v_total_tn_desired_ode)
            if norm_total_tn_ode < 1e-9: # Nếu vector mong muốn gần như bằng 0
                # ================== HIGHLIGHT START: Xử lý khi không có hướng rõ ràng ==================
                # Có thể cho tàu ngầm giữ hướng cũ hoặc đi theo hướng base nếu không né
                if currently_avoiding_ode:
                    # Nếu đang né mà không có hướng né, đây là một vấn đề. Tạm thời giữ hướng cũ của tàu ngầm.
                    # Cần một cách để lấy hướng hiện tại của tàu ngầm. Điều này hơi phức tạp vì f_combined chỉ nhận state.
                    # Giải pháp đơn giản: giữ nguyên vận tốc trước đó hoặc cho đi thẳng theo hướng base_normalized nếu có.
                    if norm_v_base_ode > 1e-6:
                        dx_tn_ode = v_base_tn_normalized_direction_ode[0] * self.m5s2_params['v_tn_max']
                        dy_tn_ode = v_base_tn_normalized_direction_ode[1] * self.m5s2_params['v_tn_max']
                    else:
                        dx_tn_ode, dy_tn_ode = 0.0, 0.0 # Đứng yên nếu không có hướng nào
                else: # Không né và không có hướng mong muốn (ví dụ v_base là 0)
                    dx_tn_ode, dy_tn_ode = 0.0, 0.0
                # ================== HIGHLIGHT END ==================
            else:
                dx_tn_ode = (v_total_tn_desired_ode[0] / norm_total_tn_ode) * self.m5s2_params['v_tn_max']
                dy_tn_ode = (v_total_tn_desired_ode[1] / norm_total_tn_ode) * self.m5s2_params['v_tn_max']
                
            return np.array([dx_kt_ode, dy_kt_ode, dx_tn_ode, dy_tn_ode])

        # --- 3. Chọn Solver và Giải ---
        solver_func_app = None
        method_short_s2 = self.m5s2_params['method_short']
        method_steps_s2 = self.m5s2_params['method_steps']
        map_solver_sim2_app = {
            "Bashforth": {2: AB2_system_M5_Sim2_CombinedLogic, 3: AB3_system_M5_Sim2_CombinedLogic, 4: AB4_system_M5_Sim2_CombinedLogic, 5: AB5_system_M5_Sim2_CombinedLogic},
            "Moulton":   {2: AM2_system_M5_Sim2_CombinedLogic, 3: AM3_system_M5_Sim2_CombinedLogic, 4: AM4_system_M5_Sim2_CombinedLogic}
        }
        if method_short_s2 in map_solver_sim2_app and method_steps_s2 in map_solver_sim2_app[method_short_s2]:
            solver_func_app = map_solver_sim2_app[method_short_s2][method_steps_s2]
        else:
            print(f"Warning M5S2: Solver from Screen 2 ({method_short_s2}{method_steps_s2}) not found. Defaulting to AB4.")
            solver_func_app = AB4_system_M5_Sim2_CombinedLogic

        num_solver_steps = int(np.ceil(100 * self.m5s2_params['simulation_duration']))
        num_solver_steps = max(200, num_solver_steps)
        self.m5s2_t_array_solver = np.linspace(self.m5s2_params['t_start'], self.m5s2_params['t_end'], num_solver_steps + 1)
        if len(self.m5s2_t_array_solver) <= 1: print("ERROR M5S2: t_array_solver has insufficient points."); return

        initial_combined_state_app = np.array([z0_kt_sim[0], z0_kt_sim[1], z_tn_actual_start_sim[0], z_tn_actual_start_sim[1]])
        print(f"DEBUG M5S2: Using App Solver: {solver_func_app.__name__}. N_solver_steps={num_solver_steps}")

        try:
            time_result_solver, state_history_solver, caught_solver, time_catch_solver = solver_func_app(
                f_combined_for_solver, self.m5s2_t_array_solver,
                initial_combined_state_app, self.m5s2_params['catch_threshold']
            )
            self.m5s2_caught_flag = caught_solver
            self.m5s2_time_of_catch = time_catch_solver

            MAX_ANIMATION_TIME_IF_NOT_CAUGHT = 50.0 # Thời gian tối đa cho animation nếu không bắt được

            if self.m5s2_caught_flag:
                # Nếu bắt được, cắt dữ liệu đến thời điểm bắt được
                end_index_anim = np.searchsorted(time_result_solver, self.m5s2_time_of_catch, side='right')
                self.m5s2_t_array_actual = time_result_solver[:end_index_anim]
                self.m5s2_z_kt_array = state_history_solver[:end_index_anim, 0:2]
                self.m5s2_z_tn_array = state_history_solver[:end_index_anim, 2:4]
                print(f"DEBUG M5S2: Caught! Animation data truncated to catch time: {self.m5s2_time_of_catch:.2f}s. Num points: {len(self.m5s2_t_array_actual)}")
            else:
                # Nếu không bắt được, cắt dữ liệu đến MAX_ANIMATION_TIME_IF_NOT_CAUGHT (50s)
                time_limit_anim = self.m5s2_params['t_start'] + MAX_ANIMATION_TIME_IF_NOT_CAUGHT
                end_index_anim = np.searchsorted(time_result_solver, time_limit_anim, side='right')
                self.m5s2_t_array_actual = time_result_solver[:end_index_anim]
                self.m5s2_z_kt_array = state_history_solver[:end_index_anim, 0:2]
                self.m5s2_z_tn_array = state_history_solver[:end_index_anim, 2:4]
                print(f"DEBUG M5S2: Not caught. Animation data truncated to {MAX_ANIMATION_TIME_IF_NOT_CAUGHT:.2f}s. Num points: {len(self.m5s2_t_array_actual)}")

            if self.m5s2_caught_flag and len(self.m5s2_z_kt_array) > 0:
                 self.m5s2_catch_point_coords = self.m5s2_z_kt_array[-1].copy()
            else:
                self.m5s2_catch_point_coords = None
        except Exception as e_solve_app:
            print(f"ERROR M5S2: App Solver execution failed: {e_solve_app}"); import traceback; traceback.print_exc()
            ax.text(0.5, 0.5, self.tr("Lỗi khi giải PTVP."), color='red', ha='center', va='center', transform=ax.transAxes); self.canvas_simulation.draw_idle()
            self.btn_stop.setEnabled(False); return
        self._update_final_sim2_info_labels()

        if hasattr(self,'m5_destroyer_catches_submarine_value') and self.m5_destroyer_catches_submarine_value :
            self.m5_destroyer_catches_submarine_value.setText(self.tr("screen3_m5_determining_status"))
        if hasattr(self,'m5_catch_point_value') and self.m5_catch_point_value :
            self.m5_catch_point_value.setText(self.tr("screen3_m5_determining_status"))
        
        # Đảm bảo label tĩnh hiển thị "Thời gian mô phỏng:" ban đầu
        if hasattr(self, 'm5_catch_time_value') and self.m5_catch_time_value:
             self.m5_catch_time_value.setText(self.tr("screen3_m5_catch_time")) # Dùng key bạn muốn
        if hasattr(self,'m5_catch_time_value') and self.m5_catch_time_value :
            self.m5_catch_time_value.setText("0.00 s")

        # --- 4. Setup Artists và Animation ---
        if len(self.m5s2_t_array_actual) == 0 or \
           (self.m5s2_z_kt_array is not None and len(self.m5s2_z_kt_array) == 0) or \
           (self.m5s2_z_tn_array is not None and len(self.m5s2_z_tn_array) == 0):
            ax.text(0.5, 0.5, self.tr("Lỗi: Không có dữ liệu để vẽ."), color='red', ha='center', va='center', transform=ax.transAxes)
            self.canvas_simulation.draw_idle(); self.btn_stop.setEnabled(False); return

        # Set plot limits (sử dụng self.m5s2_current_view_span đã được reset bởi _init)
        ax.set_xlim(-self.m5s2_current_view_span, self.m5s2_current_view_span)
        ax.set_ylim(-self.m5s2_current_view_span, self.m5s2_current_view_span)
        #ax.set_xlabel(""); ax.set_ylabel(""); ax.set_title("")
        ax.grid(True, linestyle=':', alpha=0.7, zorder=-1) # zorder để grid nằm dưới
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7, steps=[1, 2, 2.5, 5, 10], integer=False, prune='both'))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=7, steps=[1, 2, 2.5, 5, 10], integer=False, prune='both'))
        #ax.tick_params(axis='both', which='major', labelsize=8, color='gray', labelcolor='dimgray') # Thêm màu cho tick
        ax.set_aspect('equal', adjustable='box')

        # Tạo/cập nhật artists
        sub_path_lbl = self.tr("screen3_legend_m5s2_path_submarine"); dest_path_lbl = self.tr("screen3_legend_m5s2_path_destroyer")
        sub_lbl = self.tr("screen3_legend_m5s2_submarine"); dest_lbl = self.tr("screen3_legend_m5s2_destroyer")
        catch_lbl = self.tr("screen3_legend_m5s2_catch_point")
        avoid_tn_lbl = self.tr("screen3_legend_m5s2_tn_avoid_radius", "TN Avoid (R={:.1f})").format(self.m5s2_current_avoidance_radius)
        radar_kt_lbl = self.tr("screen3_legend_m5s2_kt_radar_radius", "KT Radar (R={:.1f})").format(self.m5s2_current_kt_radar_radius)

        self.m5s2_line_tn, = ax.plot([], [], lw=1.5, color="darkorange", linestyle='--', label=sub_path_lbl, zorder=2)
        self.m5s2_line_kt, = ax.plot([], [], lw=1.5, color="red", linestyle='-', label=dest_path_lbl, zorder=2)
        self.m5s2_point_tn, = ax.plot([], [], '*', color="darkorange", markeredgecolor='black', markersize=10, label=sub_lbl, zorder=4)
        self.m5s2_point_kt, = ax.plot([], [], '*', color="red", markeredgecolor='black', markersize=10, label=dest_lbl, zorder=4)
        #self.m5s2_catch_marker, = ax.plot([], [], 'X', color='purple', markersize=12, label=catch_lbl, visible=False, zorder=5)
        
        # Xóa artist cũ nếu tồn tại trước khi tạo mới
        if self.m5s2_avoid_circle_tn_artist and self.m5s2_avoid_circle_tn_artist.axes: self.m5s2_avoid_circle_tn_artist.remove()
        self.m5s2_avoid_circle_tn_artist = MplCircle((0, 0), self.m5s2_current_avoidance_radius, color='darkorange', fill=False, linestyle=':', alpha=0.6, zorder=3)
        ax.add_artist(self.m5s2_avoid_circle_tn_artist)

        if self.m5s2_kt_radar_circle_artist and self.m5s2_kt_radar_circle_artist.axes: self.m5s2_kt_radar_circle_artist.remove()
        self.m5s2_kt_radar_circle_artist = MplCircle((0, 0), self.m5s2_current_kt_radar_radius, color='red', fill=False, linestyle=':', alpha=0.5, zorder=3)
        ax.add_artist(self.m5s2_kt_radar_circle_artist)

        fig = self.canvas_simulation.fig
        # Xóa legend cũ của Figure nếu có
        if hasattr(self, 'current_fig_legend') and self.current_fig_legend:
            try: self.current_fig_legend.remove()
            except Exception: pass
        self.current_fig_legend = None

        legend_handles_m5s2 = [self.m5s2_line_tn, self.m5s2_line_kt, self.m5s2_point_tn, self.m5s2_point_kt]
        legend_labels_m5s2 = [sub_path_lbl, dest_path_lbl, sub_lbl, dest_lbl]
        if self.m5s2_caught_flag:
            legend_handles_m5s2.append(self.m5s2_catch_marker)
            legend_labels_m5s2.append(catch_lbl)

        proxy_avoid_tn_fig = Line2D([0], [0], linestyle=':', color='darkorange', marker=None, label=avoid_tn_lbl) # Dùng Line2D cho legend fig
        proxy_radar_kt_fig = Line2D([0], [0], linestyle=':', color='red', marker=None, label=radar_kt_lbl)
        legend_handles_m5s2.extend([proxy_avoid_tn_fig, proxy_radar_kt_fig])
        legend_labels_m5s2.extend([avoid_tn_lbl, radar_kt_lbl])

        self.current_fig_legend = fig.legend(
            legend_handles_m5s2, legend_labels_m5s2,
            loc='upper left', # Vị trí góc trên bên trái của Figure
            bbox_to_anchor=(0.01, 0.95), # Tọa độ (x,y) của góc trên bên trái legend, tính theo Figure
            fontsize='small',
            facecolor='lightyellow', # Nền trắng cho legend
            edgecolor='black',
            framealpha=0.9,
            borderpad=0.5,      # Padding bên trong viền
            labelspacing=0.4,   # Khoảng cách giữa các mục
            handletextpad=0.5   # Khoảng cách giữa marker và text
        )
        if self.current_fig_legend:
            self.current_fig_legend.set_zorder(150) # Đảm bảo legend nổi lên trên

        try:
            # self.canvas_simulation.fig.tight_layout(pad=1.2) # Có thể không cần nếu legend nằm ngoài
            # Thay vào đó, dùng subplots_adjust để tạo không gian cho legend và ticks
            fig.subplots_adjust(left=0.35, right=0.95, top=0.95, bottom=0.08)
        except Exception as e_tight: print(f"Warning M5S2: subplots_adjust/tight_layout error: {e_tight}")

        self.m5s2_num_frames_total_animation = len(self.m5s2_t_array_actual)
        if self.m5s2_num_frames_total_animation == 0: self.btn_stop.setEnabled(False); return

        current_slider_value = self.speed_slider.value()
        current_speed_multiplier = current_slider_value / 10.0 if current_slider_value > 0 else 0.05
        self.m5s2_animation_interval = max(20, int(self.m5s2_base_interval / current_speed_multiplier))

        self.is_simulation_running = True; self.is_simulation_paused = False
        self.ani = animation.FuncAnimation(
            self.canvas_simulation.fig, self._update_model5_sim2_frame,
            frames=self.m5s2_num_frames_total_animation,
            init_func=self._init_model5_sim2_animation,
            blit=False, interval=self.m5s2_animation_interval, repeat=False
        )
        self.canvas_simulation.draw_idle()
        self.btn_stop.setEnabled(True)
        self.btn_back_to_screen2.setEnabled(False); self.btn_double_back_to_screen1.setEnabled(False)
        print(f"DEBUG M5S2: Animation for Sim 2 (App Solvers) started. Frames: {self.m5s2_num_frames_total_animation}, Interval: {self.m5s2_animation_interval}ms.")
    
    # --- Hàm helper cho quỹ đạo tàu ngầm Sim 2 ---
    def _z_tn_m5s2(self, t): # Hàm này bạn đã có
        if not self.m5s2_submarine_trajectory_params or \
           not self.m5s2_submarine_trajectory_params.get("params_x") or \
           not self.m5s2_submarine_trajectory_params.get("params_y"):
            return np.array([0.0, 0.0])
        x_val = self.m5s2_submarine_trajectory_params["offset_x"]
        for p_item in self.m5s2_submarine_trajectory_params["params_x"]:
            x_val += p_item["amp"] * (np.sin(p_item["freq"] * t + p_item["phase"]) if p_item["type"] == 'sin' else np.cos(p_item["freq"] * t + p_item["phase"]))
        y_val = self.m5s2_submarine_trajectory_params["offset_y"]
        for p_item in self.m5s2_submarine_trajectory_params["params_y"]:
            y_val += p_item["amp"] * (np.sin(p_item["freq"] * t + p_item["phase"]) if p_item["type"] == 'sin' else np.cos(p_item["freq"] * t + p_item["phase"]))
        return np.array([x_val, y_val])

    def _get_base_submarine_velocity_m5s2(self, t, p_x_data, p_y_data, v_tn_max_local):
        # (Copy y hệt từ hàm get_base_submarine_velocity trong standalone)
        vx_base = 0; vy_base = 0
        for p in p_x_data: vx_base += p["amp"] * p["freq"] * (np.cos(p["freq"] * t + p["phase"]) if p["type"] == 'sin' else -np.sin(p["freq"] * t + p["phase"]))
        for p in p_y_data: vy_base += p["amp"] * p["freq"] * (np.cos(p["freq"] * t + p["phase"]) if p["type"] == 'sin' else -np.sin(p["freq"] * t + p["phase"]))
        v_base_tn_vector = np.array([vx_base, vy_base])
        norm_v_base = np.linalg.norm(v_base_tn_vector)
        if norm_v_base < 1e-9: return np.array([0.0, 0.0])
        return (v_base_tn_vector / norm_v_base) * v_tn_max_local

    def _get_smarter_avoidance_info_m5s2(self, z_tn_curr, z_kt_curr, v_base_tn_normalized_dir,
                                        radius_avoid, v_tn_max_local, strength_avoid,
                                        field_of_view_deg):
        # (Copy y hệt từ hàm get_smarter_avoidance_info trong standalone)
        vector_tn_to_kt = z_kt_curr - z_tn_curr; distance_tn_to_kt = np.linalg.norm(vector_tn_to_kt)
        is_avoiding = False; v_avoid_tn_vector = np.array([0.0, 0.0])
        if 0 < distance_tn_to_kt < radius_avoid:
            direction_tn_to_kt = vector_tn_to_kt / distance_tn_to_kt
            if np.linalg.norm(v_base_tn_normalized_dir) < 1e-6: # Nếu vận tốc cơ sở quá nhỏ, chỉ đẩy ra
                avoid_direction_simple = (z_tn_curr - z_kt_curr) / distance_tn_to_kt
                v_avoid_tn_vector = avoid_direction_simple * v_tn_max_local * strength_avoid; is_avoiding = True
            else:
                dot_product = np.dot(v_base_tn_normalized_dir, direction_tn_to_kt) # KT có nằm trong FOV không?
                if dot_product > np.cos(np.deg2rad(field_of_view_deg / 2.0)): # Sử dụng field_of_view_deg
                    is_avoiding = True; avoid_push_away = (z_tn_curr - z_kt_curr) / distance_tn_to_kt
                    # Tính toán hướng rẽ (vuông góc với hướng hiện tại của TN)
                    cross_prod_val = v_base_tn_normalized_dir[0] * direction_tn_to_kt[1] - v_base_tn_normalized_dir[1] * direction_tn_to_kt[0]
                    turn_direction = np.array([0.0,0.0])
                    if cross_prod_val > 0.05: # KT ở bên trái hướng đi của TN -> rẽ phải
                        turn_direction = np.array([v_base_tn_normalized_dir[1], -v_base_tn_normalized_dir[0]])
                    elif cross_prod_val < -0.05: # KT ở bên phải -> rẽ trái
                        turn_direction = np.array([-v_base_tn_normalized_dir[1], v_base_tn_normalized_dir[0]])
                    # Kết hợp hướng đẩy ra và hướng rẽ
                    chosen_avoid_direction = 0.6 * turn_direction + 0.6 * avoid_push_away # Trọng số có thể điều chỉnh
                    if np.linalg.norm(turn_direction) < 1e-6: # Nếu không có hướng rẽ rõ ràng (KT gần như đối đầu)
                        chosen_avoid_direction = avoid_push_away
                    norm_chosen_avoid = np.linalg.norm(chosen_avoid_direction)
                    if norm_chosen_avoid > 1e-6:
                        v_avoid_tn_vector = (chosen_avoid_direction / norm_chosen_avoid) * v_tn_max_local * strength_avoid
        return v_avoid_tn_vector, is_avoiding

    def _build_submarine_equation_string_m5s2(self, var_name, offset, params_list):
        """Xây dựng chuỗi phương trình cho một tọa độ (x hoặc y) của tàu ngầm Model 5, Sim 2."""
        parts = []
        # Thêm offset nếu nó đáng kể hoặc nếu không có term nào khác
        if abs(offset) > 1e-4 or not params_list:
            parts.append(f"{offset:.2f}")

        for p in params_list:
            term_str = f"{p['amp']:.2f}*{p['type']}({p['freq']:.2f}*t + {p['phase']:.2f})"
            # Kiểm tra dấu cho các term sau
            # Dấu '+' đã được xử lý bằng cách thêm vào trước mỗi term sau term đầu tiên
            parts.append(term_str)

        if not parts: # Trường hợp offset rất gần 0 và không có params
            return f"{var_name}(t) = 0.00"

        # Xây dựng chuỗi cuối cùng
        equation_str = f"{var_name}(t) = {parts[0]}"
        for i in range(1, len(parts)):
            # Các biên độ amp luôn dương, nên các term sau offset hoặc term đầu tiên sẽ là cộng
            equation_str += f" + {parts[i]}"
        return equation_str
    
    def _init_model5_sim2_animation(self):
        print("DEBUG M5S2: Initializing animation frame for Sim 2.")
        if self.m5s2_line_tn: self.m5s2_line_tn.set_data([], [])
        if self.m5s2_line_kt: self.m5s2_line_kt.set_data([], [])
        if self.m5s2_point_tn: self.m5s2_point_tn.set_data([], [])
        if self.m5s2_point_kt: self.m5s2_point_kt.set_data([], [])
        if self.m5s2_catch_marker:
            self.m5s2_catch_marker.set_data([],[])
            self.m5s2_catch_marker.set_visible(False)

        # Reset current_view_span và đặt lại giới hạn trục
        ax = self.canvas_simulation.axes
        self.m5s2_current_view_span = self.m5s2_INITIAL_VIEW_LIMIT_APP # Sử dụng giá trị đã tính toán
        ax.set_xlim(-self.m5s2_current_view_span, self.m5s2_current_view_span)
        ax.set_ylim(-self.m5s2_current_view_span, self.m5s2_current_view_span)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7, steps=[1, 2, 2.5, 5, 10], integer=False, prune='both'))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=7, steps=[1, 2, 2.5, 5, 10], integer=False, prune='both'))
        ax.tick_params(axis='both', which='major', labelsize=8, color='gray', labelcolor='dimgray')

        # Đặt vị trí ban đầu cho vòng tròn radar và né tránh
        if self.m5s2_z_tn_array is not None and len(self.m5s2_z_tn_array) > 0 and \
           self.m5s2_z_kt_array is not None and len(self.m5s2_z_kt_array) > 0:
            if self.m5s2_avoid_circle_tn_artist:
                self.m5s2_avoid_circle_tn_artist.center = (self.m5s2_z_tn_array[0, 0], self.m5s2_z_tn_array[0, 1])
                self.m5s2_avoid_circle_tn_artist.set_radius(self.m5s2_current_avoidance_radius)
                self.m5s2_avoid_circle_tn_artist.set_visible(True)
            if self.m5s2_kt_radar_circle_artist:
                self.m5s2_kt_radar_circle_artist.center = (self.m5s2_z_kt_array[0, 0], self.m5s2_z_kt_array[0, 1])
                self.m5s2_kt_radar_circle_artist.set_radius(self.m5s2_current_kt_radar_radius)
                self.m5s2_kt_radar_circle_artist.set_visible(True)
        else:
            if self.m5s2_avoid_circle_tn_artist: self.m5s2_avoid_circle_tn_artist.set_visible(False)
            if self.m5s2_kt_radar_circle_artist: self.m5s2_kt_radar_circle_artist.set_visible(False)
        
        self.m5s2_animation_visually_finished = False
        
        artists_to_return = []
        if self.m5s2_line_tn: artists_to_return.append(self.m5s2_line_tn)
        if self.m5s2_line_kt: artists_to_return.append(self.m5s2_line_kt)
        if self.m5s2_point_tn: artists_to_return.append(self.m5s2_point_tn)
        if self.m5s2_point_kt: artists_to_return.append(self.m5s2_point_kt)
        if self.m5s2_catch_marker: artists_to_return.append(self.m5s2_catch_marker)
        if self.m5s2_avoid_circle_tn_artist: artists_to_return.append(self.m5s2_avoid_circle_tn_artist)
        if self.m5s2_kt_radar_circle_artist: artists_to_return.append(self.m5s2_kt_radar_circle_artist)
        # Legend không cần trả về nếu blit=False
        # if self.m5s2_legend_obj: artists_to_return.append(self.m5s2_legend_obj)
        return artists_to_return
    
    def _update_final_sim2_info_labels(self):
        """Cập nhật các label thông tin cuối cùng cho Sim 2."""
        print("DEBUG M5S2: Updating final UI labels for Sim 2 results.")
        if self.m5s2_caught_flag:
            # ================== HIGHLIGHT START: Đổi label tĩnh và cập nhật giá trị khi bắt được ==================
            if hasattr(self, 'm5_catch_time_value') and self.m5_catch_time_value:
                self.m5_catch_time_value.setText(self.tr("screen3_m5_time_when_caught_label")) # "Thời gian bắt được tàu ngầm:"
            # ================== HIGHLIGHT END ==================
            catch_duration = self.m5s2_time_of_catch - self.m5s2_params.get('t_start', 0.0)
            if hasattr(self,'m5_catch_time_value') and self.m5_catch_time_value :
                self.m5_catch_time_value.setText(f"{catch_duration:.2f} s")

            if hasattr(self,'m5_destroyer_catches_submarine_value') and self.m5_destroyer_catches_submarine_value :
                self.m5_destroyer_catches_submarine_value.setText(self.tr("answer_yes"))
            if hasattr(self,'m5_catch_point_value') and self.m5_catch_point_value and self.m5s2_catch_point_coords is not None:
                self.m5_catch_point_value.setText(f"({self.m5s2_catch_point_coords[0]:.2f}, {self.m5s2_catch_point_coords[1]:.2f})")
            else:
                 if hasattr(self,'m5_catch_point_value') and self.m5_catch_point_value :
                     self.m5_catch_point_value.setText(self.tr("N/A"))
        else: # Không bắt được
            # ================== HIGHLIGHT START: Giữ label là "Thời gian mô phỏng" khi không bắt được ==================
            if hasattr(self, 'm5_catch_time_value') and self.m5_catch_time_value:
                self.m5_catch_time_value.setText(self.tr("screen3_m5_catch_time")) # "Thời gian mô phỏng:"
            # ================== HIGHLIGHT END ==================
            sim_duration_to_display = 0.0
            if self.m5s2_t_array_actual is not None and len(self.m5s2_t_array_actual) > 0:
                actual_run_time = self.m5s2_t_array_actual[-1] - self.m5s2_params.get('t_start', 0.0)
                sim_duration_to_display = actual_run_time
            else:
                sim_duration_to_display = self.m5s2_params.get('simulation_duration', 0.0)

            if hasattr(self,'m5_catch_time_value') and self.m5_catch_time_value :
                self.m5_catch_time_value.setText(f"{sim_duration_to_display:.2f} s")

            if hasattr(self,'m5_destroyer_catches_submarine_value') and self.m5_destroyer_catches_submarine_value :
                self.m5_destroyer_catches_submarine_value.setText(self.tr("answer_no"))
            if hasattr(self,'m5_catch_point_value') and self.m5_catch_point_value :
                self.m5_catch_point_value.setText(self.tr("N/A"))

    def _update_model5_sim2_frame(self, frame):
        if self.m5s2_animation_visually_finished: return []

        if self.m5s2_z_tn_array is None or self.m5s2_z_kt_array is None or \
           frame >= len(self.m5s2_z_tn_array) or frame >= len(self.m5s2_z_kt_array):
            if not self.m5s2_animation_visually_finished: self._update_final_sim2_info_labels()
            if self.is_simulation_running or self.is_simulation_paused:
                if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source: self.ani.event_source.stop()
                self.is_simulation_running = False; self.is_simulation_paused = False
                if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
                if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
                if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            self.m5s2_animation_visually_finished = True
            return []

        if self.m5_catch_time_value and self.m5s2_t_array_actual is not None and frame < len(self.m5s2_t_array_actual):
            if not self.m5s2_caught_flag or (self.m5s2_caught_flag and self.m5s2_t_array_actual[frame] <= self.m5s2_time_of_catch):
                current_elapsed_time = self.m5s2_t_array_actual[frame] - self.m5s2_params.get('t_start', 0.0)
                self.m5_catch_time_value.setText(f"{current_elapsed_time:.2f} s")
            elif self.m5s2_caught_flag:
                catch_duration = self.m5s2_time_of_catch - self.m5s2_params.get('t_start', 0.0)
                self.m5_catch_time_value.setText(f"{catch_duration:.2f} s")

        if hasattr(self,'m5_catch_time_value') and self.m5_catch_time_value and \
           self.m5s2_t_array_actual is not None and frame < len(self.m5s2_t_array_actual):
            
            # Chỉ cập nhật nếu animation đang thực sự chạy và CHƯA hiển thị kết quả cuối cùng
            if not self.m5s2_animation_visually_finished:
                # Đảm bảo label tĩnh vẫn là "Thời gian mô phỏng:" trong khi chạy
                if hasattr(self, 'm5_catch_time_value') and self.m5_catch_time_value.text() != self.tr("screen3_m5_catch_time"):
                    self.m5_catch_time_value.setText(self.tr("screen3_m5_catch_time"))

                current_elapsed_time = self.m5s2_t_array_actual[frame] - self.m5s2_params.get('t_start', 0.0)
                self.m5_catch_time_value.setText(f"{current_elapsed_time:.2f} s")

        tn_x, tn_y = self.m5s2_z_tn_array[frame, 0], self.m5s2_z_tn_array[frame, 1]
        kt_x, kt_y = self.m5s2_z_kt_array[frame, 0], self.m5s2_z_kt_array[frame, 1]

        if self.m5s2_line_tn: self.m5s2_line_tn.set_data(self.m5s2_z_tn_array[:frame+1, 0], self.m5s2_z_tn_array[:frame+1, 1])
        if self.m5s2_line_kt: self.m5s2_line_kt.set_data(self.m5s2_z_kt_array[:frame+1, 0], self.m5s2_z_kt_array[:frame+1, 1])
        if self.m5s2_point_tn: self.m5s2_point_tn.set_data([tn_x], [tn_y])
        if self.m5s2_point_kt: self.m5s2_point_kt.set_data([kt_x], [kt_y])

        if self.m5s2_avoid_circle_tn_artist:
            self.m5s2_avoid_circle_tn_artist.center = (tn_x, tn_y)
            if not self.m5s2_avoid_circle_tn_artist.get_visible(): self.m5s2_avoid_circle_tn_artist.set_visible(True)
        if self.m5s2_kt_radar_circle_artist:
            self.m5s2_kt_radar_circle_artist.center = (kt_x, kt_y)
            if not self.m5s2_kt_radar_circle_artist.get_visible(): self.m5s2_kt_radar_circle_artist.set_visible(True)
        
        # Logic Zoom Out động
        ax = self.canvas_simulation.axes
        needs_zoom_out = False
        boundary_check = self.m5s2_current_view_span * self.m5s2_ZOOM_OUT_BOUNDARY_FACTOR_APP
        for p_x_coord, p_y_coord in [(tn_x, tn_y), (kt_x, kt_y)]:
            if abs(p_x_coord) > boundary_check or abs(p_y_coord) > boundary_check:
                needs_zoom_out = True; break
        if needs_zoom_out:
            self.m5s2_current_view_span *= self.m5s2_ZOOM_FACTOR_APP
            ax.set_xlim(-self.m5s2_current_view_span, self.m5s2_current_view_span)
            ax.set_ylim(-self.m5s2_current_view_span, self.m5s2_current_view_span)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=7, steps=[1, 2, 2.5, 5, 10], integer=False, prune='both'))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=7, steps=[1, 2, 2.5, 5, 10], integer=False, prune='both'))
            ax.tick_params(axis='both', which='major', labelsize=8, color='gray', labelcolor='dimgray')

        is_last_logical_frame = (frame >= len(self.m5s2_t_array_actual) - 1)
        if self.m5s2_caught_flag and self.m5s2_catch_marker and self.m5s2_catch_point_coords is not None:
            if is_last_logical_frame:
                if not self.m5s2_catch_marker.get_visible():
                    self.m5s2_catch_marker.set_data([self.m5s2_catch_point_coords[0]], [self.m5s2_catch_point_coords[1]])
                    self.m5s2_catch_marker.set_visible(True)
            else:
                 if self.m5s2_catch_marker.get_visible(): self.m5s2_catch_marker.set_visible(False)
        elif self.m5s2_catch_marker and self.m5s2_catch_marker.get_visible():
            self.m5s2_catch_marker.set_visible(False)

        if is_last_logical_frame and not self.m5s2_animation_visually_finished :
            print(f"DEBUG M5S2 Update: Animation visually finished at frame {frame} (end of data).")
            self.m5s2_animation_visually_finished = True
            self.is_simulation_running = False; self.is_simulation_paused = False
            if self.ani and hasattr(self.ani, 'event_source') and self.ani.event_source: self.ani.event_source.stop()
            if hasattr(self, 'btn_back_to_screen2'): self.btn_back_to_screen2.setEnabled(True)
            if hasattr(self, 'btn_double_back_to_screen1'): self.btn_double_back_to_screen1.setEnabled(True)
            if hasattr(self, 'btn_stop'): self.btn_stop.setEnabled(False)
            self._update_final_sim2_info_labels()

        artists = [self.m5s2_line_tn, self.m5s2_line_kt, self.m5s2_point_tn, self.m5s2_point_kt]
        if self.m5s2_catch_marker: artists.append(self.m5s2_catch_marker)
        if self.m5s2_avoid_circle_tn_artist: artists.append(self.m5s2_avoid_circle_tn_artist)
        if self.m5s2_kt_radar_circle_artist: artists.append(self.m5s2_kt_radar_circle_artist)
        return artists

    def closeEvent(self, event):
        self._fully_stop_and_cleanup_animation()
        super().closeEvent(event)

# ==============================================
#           Main Window
# ==============================================
class MainWindow(QMainWindow):
    languageChanged = Signal()
    def __init__(self):
        super().__init__()
        self.current_language = "vi"
        self.translations = LANG_VI
        self.screen2 = None
        self.screen3_dyn_only = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(self.translations.get("app_title", "Simulation App"))
        self.setGeometry(50, 50, 1300, 800)
        self.setMinimumSize(950, 650) # Điều chỉnh kích thước
        icon_filename = "icon-app.ico" # Tên file icon của bạn
        final_icon_path = icon_filename # Mặc định, thử load trực tiếp (hoạt động khi chạy .py)

        # Kiểm tra xem có đang chạy từ file .exe được đóng gói bởi PyInstaller không
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Nếu có, xây dựng đường dẫn tuyệt đối đến file icon trong thư mục tạm _MEIPASS
            final_icon_path = os.path.join(sys._MEIPASS, icon_filename)
        
        # Trường hợp bạn không dùng --onefile, mà là một thư mục, 
        # file icon có thể nằm cùng cấp với file .exe chính.
        # Đoạn code trên với sys._MEIPASS vẫn là cách tổng quát nhất.

        try:
            app_icon = QIcon(final_icon_path)
            if not app_icon.isNull():
                self.setWindowIcon(app_icon)
                print(f"Window icon set from: {final_icon_path}")
            else:
                # Nếu không load được, có thể thử load từ thư mục làm việc hiện tại như một fallback
                # (nhưng với --onefile, thư mục làm việc hiện tại không phải là _MEIPASS)
                print(f"Warning: Could not load window icon from {final_icon_path}. QIcon isNull.")
                # Thử load trực tiếp tên file (nếu file icon được copy vào cùng thư mục với .exe khi không dùng --onefile)
                # fallback_icon = QIcon(icon_filename)
                # if not fallback_icon.isNull():
                #     self.setWindowIcon(fallback_icon)
                #     print(f"Window icon set from fallback (current dir): {icon_filename}")
                # else:
                #     print(f"Warning: Fallback icon load also failed for: {icon_filename}")
        except Exception as e:
            print(f"Error setting window icon: {e}")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)
        self.welcome_screen = WelcomeScreenWidget(self)
        self.screen1 = Screen1Widget(self)
        self.screen2 = Screen2Widget(self)
        self.screen3_dyn_only = Screen3Widget(self)
        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.screen1)
        self.stacked_widget.addWidget(self.screen2)
        self.stacked_widget.addWidget(self.screen3_dyn_only)
        self.stacked_widget.setCurrentWidget(self.welcome_screen)

    def set_language(self, lang_code):
        if lang_code == self.current_language:
            return
        print(f"Changing language to: {lang_code}")
        # Ensure lang_code is either 'en' or 'vi'
        self.current_language = "en" if lang_code == "en" else "vi"
        self.translations = LANG_EN if self.current_language == "en" else LANG_VI
        self.setWindowTitle(self.translations.get("app_title", "Simulation App"))
        self.languageChanged.emit()

    def switch_to_screen1(self):
        print("Switching to Screen 1")
        self.stacked_widget.setCurrentWidget(self.screen1)

    def switch_to_screen2(self, selected_model_vi_key):
        print(f"Switching to Screen 2 with key: {selected_model_vi_key}")
        self.screen2.set_model(selected_model_vi_key)
        self.stacked_widget.setCurrentWidget(self.screen2)

    def switch_to_screen3_abm(self, abm_params):
        """Chuyển sang Screen 3 và yêu cầu chạy ABM."""
        print(f"Switching to Screen 3 for ABM...")
        if not hasattr(self, 'screen3_dyn_only') or self.screen3_dyn_only is None:
            # Nếu Screen 3 chưa được tạo, tạo nó
            self.screen3_dyn_only = Screen3Widget(self)
            self.stacked_widget.addWidget(self.screen3_dyn_only)
            print("Screen 3 widget created and added.")
        # Gọi hàm setup và start trên Screen 3
        self.screen3_dyn_only.setup_and_start_abm(abm_params) # Hàm này sẽ xử lý việc bắt đầu animation ABM
        self.stacked_widget.setCurrentWidget(self.screen3_dyn_only)

    def switch_to_screen3_model5(self, model5_plot_data):
        print(f"Switching to Screen 3 for Model 5 visualization...")
        if not hasattr(self, 'screen3_dyn_only') or self.screen3_dyn_only is None:
            self.screen3_dyn_only = Screen3Widget(self)
            self.stacked_widget.addWidget(self.screen3_dyn_only)
            print("Screen 3 widget created and added.")
        
        # ================== HIGHLIGHT START: Đảm bảo dữ liệu mới được truyền ==================
        # In ra để kiểm tra dữ liệu được truyền vào
        if isinstance(model5_plot_data, dict) and 'params' in model5_plot_data:
            print(f"DEBUG MainWindow: Passing new data to Screen3. Params from Screen2: {model5_plot_data['params']}")
            if 'T' in model5_plot_data and model5_plot_data['T'] is not None:
                 print(f"DEBUG MainWindow: New T data length: {len(model5_plot_data['T'])}")
        else:
            print(f"DEBUG MainWindow: model5_plot_data being passed to Screen3 might be problematic: {type(model5_plot_data)}")

        self.screen3_dyn_only.setup_and_start_model5_pursuit_curve(model5_plot_data) # Dữ liệu mới được truyền ở đây
        # ================== HIGHLIGHT END ==================
        self.stacked_widget.setCurrentWidget(self.screen3_dyn_only)
   
    def switch_to_screen3_model2(self, t_data, y_data_list, labels, additional_info):
        """Chuyển sang Screen 3 và yêu cầu chạy animation Model 2."""
        print(f"Switching to Screen 3 for Model 2 animation...")
        if not hasattr(self, 'screen3_dyn_only') or self.screen3_dyn_only is None:
            self.screen3_dyn_only = Screen3Widget(self)
            self.stacked_widget.addWidget(self.screen3_dyn_only)
            print("Screen 3 widget created and added.")
        # Gọi hàm setup và start mới cho Model 2
        self.screen3_dyn_only.setup_and_start_model2_animation(t_data, y_data_list, labels, additional_info)
        self.stacked_widget.setCurrentWidget(self.screen3_dyn_only)
    
    def switch_to_specific_screen(self, screen_widget):
        if screen_widget and screen_widget in [self.stacked_widget.widget(i) for i in range(self.stacked_widget.count())]:
            self.stacked_widget.setCurrentWidget(screen_widget)
        else:
            print(f"Error: Cannot switch to non-existent or invalid screen widget.")
            self.stacked_widget.setCurrentWidget(self.welcome_screen)

# ==============================================
#           Application Entry Point
# ==============================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    

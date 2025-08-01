# ==============================================
#           TRANSLATION DICTIONARIES
# ==============================================
LANG_VI = {
	"app_title": "Ứng dụng mô phỏng phương pháp đa bước - FMS TDTU", 
	# Welcome Screen
	"welcome_uni": "TRƯỜNG ĐẠI HỌC TÔN ĐỨC THẮNG",
	"welcome_faculty": "KHOA TOÁN - THỐNG KÊ", 
	"welcome_project_title": "Phương pháp đa bước và ứng dụng\ntrong mô phỏng một số mô hình thực tế", 
	"welcome_authors_title": "Tác giả",
	"welcome_authors_names": "   Khưu Tấn Đạt – Huỳnh Nhựt Trường – Đào Nhật Gia Ân", 
	"welcome_advisors_title": "Giảng viên hướng dẫn",
	"welcome_advisor1": "PGS. TS. Trần Minh Phương", 
	"welcome_advisor2": "TS. Nguyễn Hữu Cần", 
	"lang_vi": "Tiếng Việt",
	"lang_en": "English", 
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
	"model3_desc": ("Mô hình mô phỏng sự thay đổi về số lượng cá thể chưa bị nhiễm bệnh trong một cộng đồng theo thời gian.<br>" 
	"x(t): Số lượng cá thể chưa bị nhiễm tại thời điểm t.<br>"
	"n: Số lượng cá thể dễ bị nhiễm ban đầu.<br>" 
	"r: Hằng số dương đo lường tốc độ lây nhiễm.<br>"
	"dx/dt: Tốc độ giảm của số người chưa nhiễm (tốc độ lây nhiễm).<br>" 
	"t<sub>0</sub>: Thời điểm ban đầu."),
	"model3_param2": "Số lượng cá thể dễ bị nhiễm ban đầu (n)",
	"model3_param4": "Thời điểm ban đầu (t₀)",
	"model3_param5": "Thời điểm kết thúc (t₁)",
	"model3_calculated_r_label": "Hằng số tốc độ lây nhiễm (r):",
	# ================== MODEL 4: National Economy ==================
	"model4_name": "Mô hình 4: Nền kinh tế quốc gia",
	"model4_eq": "Y''(t) + αY'(t) + βY(t) = mlG", 
	"model4_desc": ("Mô hình mô phỏng sự thay đổi của nền kinh tế theo thời gian dựa trên các biến số của kinh tế vĩ mô.<br>"
	"Y(t): Thu nhập quốc dân.<br>"
	"Y'(t): Tốc độ thay đổi thu nhập.<br>"
	"α: Hệ số liên quan đến khuynh hướng tiêu dùng/đầu tư (α = m + ls - lma).<br>"
	"β: Hệ số phản ứng đầu tư theo thay đổi thu nhập (β = lms).<br>" 
	"m: Số nhân chi tiêu chính phủ.<br>"
	"l: Tham số liên quan đến cầu tiền.<br>"
	"a: Tham số độ nhạy đầu tư theo lãi suất.<br>"
	"s: Tham số độ nhạy cầu tiền theo lãi suất.<br>"
	"G: Chi tiêu chính phủ (hằng số)."),
	"model4_param_alpha": "Hệ số α", 
	"model4_param_beta": "Hệ số β", 
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
	"screen2_back_button": "Quay lại chọn mô hình", 
	"screen2_goto_screen3_button": "Xem mô phỏng động", 
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
	"screen2_actions_group": "4. Thực thi và lưu trữ", 
	"screen2_init_button": "🚀 Khởi tạo và vẽ đồ thị", 
	"screen2_refresh_button": "🔄 Làm mới thông số",
	"screen2_show_data_button": "📊 Xem dữ liệu số",
	"screen2_save_button": "💾 Lưu hình ảnh đồ thị",
	"screen2_plot_solution_title": "Đồ thị nghiệm",
	"screen2_plot_error_title": "Đồ thị sai số $L_\\infty$",
	"screen2_plot_order_title": "Đồ thị bậc hội tụ",
	"screen2_plot_t_axis": "Thời gian (t)",
	"screen2_plot_value_axis": "Giá trị nghiệm",
	"screen2_plot_n_axis": "Số khoảng con (N)",
	"screen2_plot_h_axis": "Bước nhảy (h)",
	"screen2_plot_error_axis": "Sai số L∞",
	"screen2_plot_log_h_axis": "log(h)",
	"screen2_plot_log_error_axis_base": "log(Sai số $L_\\infty$)",
	"screen2_plot_exact_label": "Nghiệm chính xác / Tham chiếu",
	"screen2_plot_error_label_prefix": "Sai số ",
	"screen2_plot_order_data_label_suffix": " (dữ liệu)",
	"screen2_plot_order_fit_label_suffix": " Fit: O(h<sup>{:.2f}</sup>)",
	"screen2_info_area_init": "Nhấn 'Khởi tạo và vẽ đồ thị' để bắt đầu mô phỏng.", 
	"screen2_info_area_running": "Đang xử lý, vui lòng chờ...",
	"screen2_info_area_error": "Lỗi: ",
	"screen2_info_area_no_results": "Không có kết quả mô phỏng để hiển thị.",
	"screen2_info_area_no_show_data": "Chưa có dữ liệu. Vui lòng chạy mô phỏng trước.",
	"screen2_info_area_show_data_method": "Phương pháp:",
	"screen2_info_area_show_data_textCont1": "bước",
	"screen2_info_area_show_data_textCont2": "với",
	"screen2_info_area_show_data_order": "Bậc hội tụ ước tính:",
	"screen2_info_area_show_data_points_header": "Bảng sai số",
	"screen2_info_area_show_data_time": "t",
	"screen2_info_area_show_data_approx": "Xấp xỉ", 
	"screen2_info_area_show_data_exact": "Chính xác", 
	"screen2_info_area_show_data_error": "Sai số",
	"screen2_info_area_show_data_more": "(và các điểm khác...)",
	"screen2_info_area_show_data_no_points": "(Không có dữ liệu điểm)",
	"screen2_info_area_refreshed": "Đã làm mới. Sẵn sàng cho mô phỏng mới.",
	"screen2_info_area_complete": "Hoàn thành!",
	"screen2_legend_title": "Chú thích",
	"screen2_legend_order_title": "Bậc hội tụ:",
	"screen2_plot_value_axis_base": "Giá trị",
	"screen2_plot_value_axis_x": "Giá trị (thành phần X)", 
	"screen2_plot_value_axis_y": "Giá trị (thành phần Y)", 
	"screen2_plot_error_axis_base": "Sai số $L_\\infty$",
	"screen2_plot_error_axis_x": "Sai số $L_\\infty$ (thành phần X)", 
	"screen2_plot_error_axis_y": "Sai số $L_\\infty$ (thành phần Y)", 
	"screen2_plot_log_error_axis_base": "log(Sai số $L_\\infty$)",
	"screen2_plot_log_error_axis_x": "log(Sai số $L_\\infty$ X)",
	"screen2_plot_log_error_axis_y": "log(Sai số $L_\\infty$ Y)",
	"screen2_info_area_show_data_approx_x": "Xấp xỉ",    
	"screen2_info_area_show_data_approx_y": "Xấp xỉ",    
	"screen2_info_area_show_data_exact_x": "Tham chiếu", 
	"screen2_info_area_show_data_exact_y": "Tham chiếu", 
	"screen2_info_area_show_data_error_x": "Sai số",     
	"screen2_info_area_show_data_error_y": "Sai số",     	
	# Simulation Plot Window
	"sim_window_title": "Cửa sổ đồ thị mô phỏng động", 
	"sim_window_plot_title": "Mô phỏng nghiệm theo thời gian", 
	"sim_window_t_axis": "Thời gian (t)",
	"sim_window_value_axis": "Giá trị nghiệm", 
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
	"msg_model_error_title": "Lỗi mô hình", 
	"msg_model_no_ode": "Mô hình '{}' chưa được định nghĩa hàm PTVP.",
	"msg_param_error_title": "Lỗi tham số", 
	"msg_missing_keys": "Thiếu các tham số bắt buộc: {}",
	"msg_missing_y0": "Thiếu điều kiện ban đầu (ví dụ: O₀, x₀, Y(t₀)).",
	"msg_param_value_error_title": "Lỗi giá trị tham số", 
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
	"screen3_back_button": "Quay lại nhập tham số", 
	"screen3_double_back_button": "Quay lại chọn mô hình", 
	"screen3_dyn_only_title": "Mô phỏng động của mô hình",
	"screen3_dyn_back_tooltip": "Quay lại màn hình nhập liệu và các đồ thị kết quả tĩnh",
	"screen3_settings_group_title": "Cài đặt mô phỏng động",
	"screen3_speed_label": "Tốc độ phát lại:",
	"screen3_results_group_title": "Thông tin mô phỏng động",
	"screen3_unified_results_title": "Thông tin mô phỏng",
	"screen3_stop_button": "⏹ Dừng/Tiếp tục mô phỏng", 
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
	
	"screen3_info_m5_sim1_title": "Thông tin mô phỏng 1 (con thuyền)", 
	"screen3_m5_boat_speed": "Vận tốc thuyền (v):",
	"screen3_m5_water_speed": "Vận tốc dòng nước (u):",
	"screen3_m5_crossing_time": "Thời gian mô phỏng (t):",
	"screen3_m5_start_point_boat": "Điểm bắt đầu của thuyền:",
	"screen3_m5_boat_reaches_target": "Thuyền có đến được đích không?",
	"screen3_m5_boat_final_pos": "Vị trí cuối cùng của thuyền:",
	"screen3_m5_determining_status": "Đang xác định...",
	"answer_yes": "Có",
	"answer_no": "Không",
	
	"screen3_info_m5_sim2_title": "Thông tin mô phỏng 2 (tàu khu trục vs tàu ngầm)", 
	"screen3_m5_submarine_speed": "Vận tốc tàu ngầm (v<sub>target</sub>):",
	"screen3_m5_destroyer_speed": "Vận tốc tàu khu trục (v<sub>pursuer</sub>):",
	"screen3_legend_m5s2_tn_avoid_radius": "Radar của tàu ngầm",
	"screen3_legend_m5s2_kt_radar_radius": "Radar của tàu khu trục",
	"screen3_m5_submarine_trajectory": "Phương trình quỹ đạo cơ sở của tàu ngầm:",
	"screen3_m5_start_point_submarine": "Điểm bắt đầu của tàu ngầm:",
	"screen3_m5_start_point_destroyer": "Điểm bắt đầu của tàu khu trục:",
	"screen3_m5_destroyer_catches_submarine": "Tàu khu trục có bắt được tàu ngầm không?",
	"screen3_m5_catch_point": "Điểm bắt được (tọa độ):",
	"screen3_m5_catch_time": "Thời gian mô phỏng:", 
	"screen3_model5_not_implemented_msg": "Mô phỏng cho kịch bản này chưa được triển khai.",
	
	"screen3_model2_anim_plot_title": "Mô phỏng động: Sự tăng trưởng tế bào", 
	"screen3_abm_anim_plot_title": "Mô phỏng động: Sự lây lan dịch bệnh (ABM)", 
	
	"screen3_model5_plot_title_sim1": "Mô phỏng động: Con thuyền qua sông", 
	"screen3_model5_plot_title_sim2": "Mô phỏng động: Tàu khu trục - Tàu ngầm", 
	
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
	"screen3_m5_time_when_caught_label": "Thời gian bắt được tàu ngầm:",
}

# ========================================================================================================

LANG_EN = {
	"app_title": "Multi-step methods simulation application - FMS TDTU", 
	# Welcome Screen
	"welcome_uni": "TON DUC THANG UNIVERSITY",
	"welcome_faculty": "FACULTY OF MATHEMATICS - STATISTICS",
	"welcome_project_title": "Multi-step methods and applications\n in simulating some real-life models", 
	"welcome_authors_title": "Authors",
	"welcome_authors_names": "Tan Dat Khuu – Nhut Truong Huynh – Nhat Gia An Dao",
	"welcome_advisors_title": "Advisors",
	"welcome_advisor1": "Assoc. Prof. Minh Phuong Tran",
	"welcome_advisor2": "PhD. Huu Can Nguyen",
	"lang_vi": "Tiếng Việt", 
	"lang_en": "English",
	"start_button": "Start",
	# Screen 1
	"screen1_title": "Select a real-life model", 
	"screen1_model_info_group_title": "Model information", 
	"screen1_model_application_group_title": "Model application", 
	"screen1_equation_label": "Differential equation / Analytical solution:", 
	"screen1_description_label": "Description and parameters:", 
	"screen1_continue_button": "Continue with this model", 
	# ================== MODEL 1: Energy Demand ==================
	"model1_name": "Model 1: Energy demand", 
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
	"model2_name": "Model 2: Cell growth", 
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
	"model3_name": "Model 3: Spread of epidemic", 
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
	"model4_name": "Model 4: National economy", 
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
	"model4_param_alpha": "Coefficient α", 
	"model4_param_beta": "Coefficient β", 
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
	"model5_name": "Model 5: Pursuit curve", 
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
	"screen2_back_button": "Back to model selection", 
	"screen2_goto_screen3_button": "View dynamic simulation", 
	"screen2_goto_screen3_tooltip": "Switch to the dynamic simulation screen (if available)",
	"screen2_method_group": "1. Select main method",
	"screen2_method_ab": "Adams-Bashforth (AB)",
	"screen2_method_am": "Adams-Moulton (AM)",
	"screen2_details_group_ab": "2. Adams-Bashforth details", 
	"screen2_details_group_am": "2. Adams-Moulton details", 
	"screen2_steps_label": "Number of steps:",
	"screen2_select_all_steps_cb": "All",
	"screen2_step2": "2-step",
	"screen2_step3": "3-step",
	"screen2_step4": "4-step",
	"screen2_step5": "5-step",
	"param_placeholder": "Enter numeric value...",
	"screen2_h_label": "Step size (h):",
	"screen2_sim_toggle": "Show separate dynamic simulation window",
	"screen2_params_group": "3. Model input parameters", 
	"screen2_actions_group": "4. Execute and save", 
	"screen2_init_button": "🚀 Initialize and plot graphs", 
	"screen2_refresh_button": "🔄 Refresh parameters", 
	"screen2_show_data_button": "📊 View numerical data", 
	"screen2_save_button": "💾 Save plot images", 
	"screen2_plot_solution_title": "Solution plot", 
	"screen2_plot_error_title": "$L_\\infty$ error plot", 
	"screen2_plot_order_title": "Convergence order plot", 
	"screen2_plot_t_axis": "Time (t)",
	"screen2_plot_value_axis": "Solution value",
	"screen2_plot_n_axis": "Number of subintervals (N)",
	"screen2_plot_h_axis": "Step size (h)",
	"screen2_plot_error_axis": "L∞ Error",
	"screen2_plot_log_h_axis": "log(h)",
	"screen2_plot_log_error_axis": "log($L_\\infty$ Error)",
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
	"screen2_info_area_show_data_time": "t", 
	"screen2_info_area_show_data_approx": "Approximate", 
	"screen2_info_area_show_data_exact": "Exact",
	"screen2_info_area_show_data_error": "Error",
	"screen2_info_area_show_data_more": "(and other points...)",
	"screen2_info_area_show_data_no_points": "(No point data)",
	"screen2_info_area_refreshed": "Fields refreshed. Ready for new simulation.",
	"screen2_info_area_complete": "Completed!",
	"screen2_legend_title": "Legend",
	"screen2_legend_order_title": "Convergence order:", 
	"screen2_plot_value_axis_base": "Value",
	"screen2_plot_value_axis_x": "Value (X-component)", 
	"screen2_plot_value_axis_y": "Value (Y-component)", 
	"screen2_plot_error_axis_base": "$L_\\infty$ Error",
	"screen2_plot_error_axis_x": "$L_\\infty$ Error (X-component)", 
	"screen2_plot_error_axis_y": "$L_\\infty$ Error (Y-component)", 
	"screen2_plot_log_error_axis_base": "log($L_\\infty$ Error)",
	"screen2_plot_log_error_axis_x": "log($L_\\infty$ Error X)",
	"screen2_plot_log_error_axis_y": "log($L_\\infty$ Error Y)",
	"screen2_info_area_show_data_approx_x": "Approximate",
	"screen2_info_area_show_data_approx_y": "Approximate",
	"screen2_info_area_show_data_exact_x": "Reference",
	"screen2_info_area_show_data_exact_y": "Reference",
	"screen2_info_area_show_data_error_x": "Error",
	"screen2_info_area_show_data_error_y": "Error",
	
	# Simulation Plot Window
	"sim_window_title": "Dynamic simulation plot window", 
	"sim_window_plot_title": "Solution simulation over time", 
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
	"msg_invalid_input_title": "Input error", 
	"msg_invalid_input_text": "Please check the parameters highlighted in red.",
	"msg_invalid_param_value": "Parameter '{}' is not a valid number (received value: '{}').",
	"msg_missing_param_value": "Parameter '{}' cannot be empty.",
	"msg_model_error_title": "Model error", 
	"msg_model_no_ode": "Model '{}' does not have an ODE function defined.",
	"msg_param_error_title": "Parameter error", 
	"msg_missing_keys": "Missing required parameters: {}",
	"msg_missing_y0": "Missing initial condition (e.g., O₀, x₀, Y(t₀)).",
	"msg_param_value_error_title": "Parameter value error", 
	"msg_param_value_error_text": "Value error in parameter: {}",
	"msg_t_end_error": "End time t₁ must be greater than start time t₀.",
	"msg_unknown_error_title": "Unknown error", 
	"msg_unknown_error_prep": "An error occurred while preparing for the simulation: {}",
	"msg_internal_error_title": "Internal error", 
	"msg_internal_error_steps": "Invalid number of steps: {}",
	"msg_simulation_error_title": "Simulation error", 
	"msg_simulation_error_text": "An error occurred during the simulation process: {}",
	"msg_no_results_title": "No results", 
	"msg_no_results_text": "No valid simulation results were generated.",
	"msg_sim_window_no_data": "No data available to display in the dynamic simulation window.",
	"msg_show_data_no_data": "No simulation data has been generated yet.",
	"msg_save_no_plots": "No plots have been generated to save.",
	"msg_save_select_dir": "Please select a directory to save images",
	"msg_save_cancelled": "Directory selection was cancelled.",
	"msg_save_success_title": "Save successful", 
	"msg_save_success_text": "Saved {} image(s) to the directory:\n{}",
	"msg_save_error_title": "Save error", 
	"msg_save_error_text": "Saved {} image(s) but encountered some errors:\n{}",
	"msg_save_fail_title": "Save failed", 
	"msg_save_fail_text": "Could not save images due to an error:\n{}",
	"msg_saving_plot_error": "Error saving plot '{}': {}",
	"msg_skipping_save": "Skipping save for plot '{}' (no data).",
	
	#Screen 3
	"screen3_back_button": "Back to parameters", 
	"screen3_double_back_button": "Back to model selection", 
	"screen3_dyn_only_title": "Dynamic model simulation", 
	"screen3_dyn_back_tooltip": "Back to the input and static results screen",
	"screen3_settings_group_title": "Dynamic simulation settings", 
	"screen3_speed_label": "Playback speed:",
	"screen3_results_group_title": "Dynamic simulation information", 
	"screen3_unified_results_title": "Simulation information", 
	"screen3_stop_button": "⏹ Pause/Resume simulation", 
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
	
	"screen3_info_m5_sim1_title": "Simulation 1 information (boat crossing)", 
	"screen3_m5_boat_speed": "Boat velocity (v):",
	"screen3_m5_water_speed": "Current velocity (u):",
	"screen3_m5_crossing_time": "Simulation time (t):",
	"screen3_m5_start_point_boat": "Boat's starting point:",
	"screen3_m5_boat_reaches_target": "Does the boat reach the target?",
	"screen3_m5_boat_final_pos": "Boat's final position:",
	"screen3_m5_determining_status": "Determining...",
	"answer_yes": "Yes",
	"answer_no": "No",
	
	"screen3_info_m5_sim2_title": "Simulation 2 information (destroyer vs. submarine)", 
	"screen3_m5_submarine_speed": "Submarine velocity (v<sub>target</sub>):",
	"screen3_m5_destroyer_speed": "Destroyer velocity (v<sub>pursuer</sub>):",
	"screen3_legend_m5s2_tn_avoid_radius": "Submarine radar zone", 
	"screen3_legend_m5s2_kt_radar_radius": "Destroyer radar zone", 
	"screen3_m5_submarine_trajectory": "Submarine base trajectory equation:",
	"screen3_m5_start_point_submarine": "Submarine's starting point:",
	"screen3_m5_start_point_destroyer": "Destroyer's starting point:",
	"screen3_m5_destroyer_catches_submarine": "Does the destroyer catch the submarine?",
	"screen3_m5_catch_point": "Catch point (coordinates):",
	"screen3_m5_catch_time": "Simulation time:", 
	"screen3_model5_not_implemented_msg": "Simulation for this scenario is not yet implemented.",
	
	"screen3_model2_anim_plot_title": "Dynamic simulation: Cell growth", 
	"screen3_abm_anim_plot_title": "Dynamic simulation: Epidemic spread (ABM)", 
	
	"screen3_model5_plot_title_sim1": "Dynamic simulation: Boat crossing river", 
	"screen3_model5_plot_title_sim2": "Dynamic simulation: Destroyer - Submarine", 
	
	"screen3_model5_plot_xlabel_sim1": "X Position (m)",
	"screen3_model5_plot_ylabel_sim1": "Y Position (m)",
	"screen3_legend_m5s1_path": "Boat trajectory", 
	"screen3_legend_m5s1_boat": "Boat",
	"screen3_legend_m5s1_water_current": "Water current direction", 
	
	"screen3_model5_plot_xlabel_sim2": "X Position (m)",
	"screen3_model5_plot_ylabel_sim2": "Y Position (m)",
	"screen3_legend_m5s2_submarine": "Submarine",
	"screen3_legend_m5s2_destroyer": "Destroyer",
	"screen3_legend_m5s2_path_submarine": "Submarine trajectory", 
	"screen3_legend_m5s2_path_destroyer": "Destroyer trajectory", 
	"screen3_legend_m5s2_catch_point": "Catch point",
	"screen3_m5_time_when_caught_label": "Time to catch submarine:",
}

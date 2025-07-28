import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import traceback
from datetime import datetime
import os
import io

# Import các module đã được tách
from modules import solvers, models, translations

# ==============================================================================
# --- CÁC HÀM LOGIC HELPER (Chuyển thể từ Class Screen2Widget) ---
# ==============================================================================

def validate_and_get_params(model_data, T):
    """Lấy và kiểm tra các tham số người dùng nhập từ st.session_state."""
    params = {}
    errors = []
    is_valid = True
    
    internal_keys = model_data.get("internal_param_keys", [])
    for key in internal_keys:
        session_key = f'param_{key}'
        val = st.session_state.get(session_key)
        
        if val is None or str(val).strip() == "":
            errors.append(T['msg_missing_param_value'].format(key))
            is_valid = False
        else:
            try:
                params[key] = float(val)
            except (ValueError, TypeError):
                errors.append(T['msg_invalid_param_value'].format(key, val))
                is_valid = False

    if is_valid and 't₀' in params and 't₁' in params:
        if params['t₁'] <= params['t₀']:
            errors.append(T["msg_t_end_error"])
            is_valid = False
            
    return is_valid, params, errors

@st.cache_data
def perform_simulation_cached(config):
    """
    Hàm bọc để cache kết quả mô phỏng. Streamlit sẽ không chạy lại tính toán
    nếu các tham số trong `config` không thay đổi.
    """
    # ... (Toàn bộ logic từ _perform_single_simulation của bạn ở đây) ...
    # Đây là phiên bản đã được chuyển thể hoàn chỉnh:
    
    ode_func = config['ode_func']
    exact_func = config['exact_func']
    y0 = config['y0']
    t_start, t_end = config['t_start'], config['t_end']
    method_short = config['method']
    steps_int = config['step']
    h_target = config['h']
    selected_component = config.get('component', 'x')
    model_data = config['model_data']
    
    is_system = model_data.get("is_system", False)
    uses_rk5_reference = model_data.get("uses_rk5_reference", False)
    model_id = model_data.get("id")

    # --- Chọn hàm solver ---
    solver_map = {
        (False, "Bashforth"): {2: solvers.AB2, 3: solvers.AB3, 4: solvers.AB4, 5: solvers.AB5},
        (False, "Moulton"): {2: solvers.AM2, 3: solvers.AM3, 4: solvers.AM4},
        (True, "Bashforth"): {2: solvers.AB2_system, 3: solvers.AB3_system, 4: solvers.AB4_system, 5: solvers.AB5_system},
        (True, "Moulton"): {2: solvers.AM2_system, 3: solvers.AM3_system, 4: solvers.AM4_system}
    }
    solver_func = solver_map.get((is_system, method_short), {}).get(steps_int)

    if not solver_func:
        raise ValueError(f"Solver for {method_short} {steps_int} steps (system={is_system}) not found.")

    # --- Tính toán cho đồ thị nghiệm ---
    interval_length = t_end - t_start
    if interval_length <= 1e-9: return None
    n_plot = max(int(np.ceil(interval_length / h_target)), 50)
    t_plot = np.linspace(t_start, t_end, n_plot + 1)

    approx_sol_plot = None
    exact_sol_plot = None

    if is_system:
        approx_sol_plot_all = solver_func(ode_func, t_plot, y0[0], y0[1])
        approx_sol_plot = approx_sol_plot_all[0] if selected_component == 'x' else approx_sol_plot_all[1]
        
        if uses_rk5_reference:
            exact_sol_plot_all = solvers.RK5_system(ode_func, t_plot, y0[0], y0[1])
        elif exact_func:
            exact_sol_plot_all = exact_func(t_plot)
        exact_sol_plot = exact_sol_plot_all[0] if selected_component == 'x' else exact_sol_plot_all[1]
    else:
        approx_sol_plot = solver_func(ode_func, t_plot, y0)
        if exact_func:
            exact_sol_plot = exact_func(t_plot)

    # --- Tính toán cho đồ thị sai số & bậc hội tụ ---
    errors_conv, n_conv_vals, h_conv_vals = [], [], []
    n_values_loop = np.unique(np.linspace(10 * steps_int, 200 * steps_int, 15, dtype=int))

    for n in n_values_loop:
        if n < steps_int: continue
        t_conv = np.linspace(t_start, t_end, n + 1)
        
        if is_system:
            approx_conv_all = solver_func(ode_func, t_conv, y0[0], y0[1])
            approx_conv = approx_conv_all[0] if selected_component == 'x' else approx_conv_all[1]
            if uses_rk5_reference:
                exact_conv_all = solvers.RK5_system(ode_func, t_conv, y0[0], y0[1])
            else:
                exact_conv_all = exact_func(t_conv)
            exact_conv = exact_conv_all[0] if selected_component == 'x' else exact_conv_all[1]
        else:
            approx_conv = solver_func(ode_func, t_conv, y0)
            exact_conv = exact_func(t_conv)

        min_len = min(len(approx_conv), len(exact_conv))
        error = np.linalg.norm(exact_conv[:min_len] - approx_conv[:min_len], np.inf)
        
        if np.isfinite(error) and error > 1e-16:
            errors_conv.append(error)
            n_conv_vals.append(n)
            h_conv_vals.append(interval_length / n)

    errors_conv = np.array(errors_conv)
    h_conv_vals = np.array(h_conv_vals)
    log_h = np.log(h_conv_vals)
    log_err = np.log(errors_conv)
    slope = np.polyfit(log_h, log_err, 1)[0] if len(log_h) > 1 else float('nan')
    
    return {
        "t_plot": t_plot,
        "exact_sol_plot": exact_sol,
        "approx_sol_plot": approx_sol,
        "errors_convergence": errors_conv,
        "n_values_convergence": np.array(n_conv_vals),
        "log_h_convergence": log_h,
        "log_error_convergence": log_err,
        "order_slope": slope,
    }

# ==============================================================================
# --- GIAO DIỆN STREAMLIT CHÍNH ---
# ==============================================================================

# --- Khởi tạo và kiểm tra trạng thái ---
if 'translations' not in st.session_state:
    st.error("Vui lòng bắt đầu từ trang chính (streamlit_main.py).")
    st.stop()

if 'selected_model_data' not in st.session_state:
    st.warning("Vui lòng chọn một mô hình từ trang 'Model Selection' trước.")
    st.stop()

T = st.session_state.translations
model_data = st.session_state.selected_model_data
model_id = model_data.get("id")
model_name = T[f"{model_id}_name"]

st.title(f"{T.get('screen2_base_title', 'Mô phỏng')}: {model_name}")

# --- Sidebar cho các input ---
with st.sidebar:
    st.header("Cài đặt mô phỏng")

    method_options = [T['screen2_method_ab'], T['screen2_method_am']]
    selected_method = st.radio(T['screen2_method_group'], method_options, key='method_selection')
    method_suffix = 'ab' if selected_method == T['screen2_method_ab'] else 'am'
    method_short = "Bashforth" if method_suffix == 'ab' else "Moulton" 

# Sử dụng suffix đó để lấy đúng key dịch
with st.expander(T[f"screen2_details_group_{method_suffix}"], expanded=True):
        step_options = {2: T['screen2_step2'], 3: T['screen2_step3'], 4: T['screen2_step4'], 5: T['screen2_step5']}
        
        if model_id == "model5" and method_short == "Bashforth":
            available_steps = [2, 3, 4]
        elif method_short == "Bashforth":
            available_steps = [2, 3, 4, 5]
        else:
            available_steps = [2, 3, 4]

        selected_steps = st.multiselect(
            T['screen2_steps_label'],
            options=available_steps,
            format_func=lambda x: step_options[x],
            default=[4] if 4 in available_steps else [2]
        )
        
        h_options = [0.1, 0.05, 0.01, 0.005, 0.001]
        selected_h = st.select_slider(T['screen2_h_label'], options=h_options, value=0.01)

    st.subheader(T['screen2_params_group'])
    param_labels_key = f"param_keys_{st.session_state.lang}"
    param_labels = model_data.get(param_labels_key, [])
    internal_keys = model_data.get("internal_param_keys", [])
    
    for i, key in enumerate(internal_keys):
        label = param_labels[i]
        st.number_input(label, value=1.0, step=0.1, format="%.4f", key=f'param_{key}')
    
    if model_id == "model5":
        st.session_state.selected_component = st.radio(
            T['model5_select_component'], 
            [T['model5_component_x'], T['model5_component_y']], 
            horizontal=True
        )

    st.markdown("---")
    run_button = st.button(T['screen2_init_button'], use_container_width=True, type="primary")

    if st.session_state.get('show_dynamic_sim_button', False):
        if st.button(T['screen2_goto_screen3_button'], use_container_width=True):
            st.switch_page("Screen/3_🎥_Dynamic_Simulation.py")

# --- Xử lý khi nhấn nút Run ---
if run_button:
    st.session_state.show_dynamic_sim_button = False # Reset cờ
    is_valid, params, errors = validate_and_get_params(model_data, T)
    
    if not is_valid:
        for error in errors:
            st.error(error)
        st.session_state.last_results = None # Xóa kết quả cũ nếu input lỗi
    else:
        try:
            # Đây là nơi logic chuẩn bị (tính c, r, alpha, beta) diễn ra
            # Tạm thời, chúng ta sẽ giả định logic này thành công
            # và các giá trị được tính toán sẽ được thêm vào `params`
            # Ví dụ:
            if model_id == 'model2': params['c'] = 0.5 
            if model_id == 'model3': params['r'] = 0.01
            
            ode_func_gen = model_data['ode_func']
            exact_func_gen = model_data['exact_func']

            # Tạo các hàm cụ thể với tham số
            ode_func = ode_func_gen(**params) if model_id != 'model1' else ode_func_gen(params['k'])
            exact_func = exact_func_gen(**params) if exact_func_gen else None

            # Xác định y0
            y0 = params.get('O₀') or params.get('x₀') or params.get('n')
            if model_id == 'model4': y0 = [params['Y0'], params['dY0']]
            if model_id == 'model5': y0 = [params['x0'], params['y0']]

            results_dict = {}
            with st.spinner(T['screen2_info_area_running']):
                for step in selected_steps:
                    config = {
                        'ode_func': ode_func, 'exact_func': exact_func, 'y0': y0,
                        't_start': params['t₀'], 't_end': params['t₁'], 'h': selected_h,
                        'method': method_short, 'step': step, 'model_data': model_data,
                        'component': 'y' if st.session_state.get('selected_component') == T.get('model5_component_y') else 'x'
                    }
                    res = perform_simulation_cached(config) # Dùng hàm đã cache
                    if res:
                        results_dict[step] = res
            
            if results_dict:
                st.session_state.last_results = results_dict
                
                if model_id in ["model2", "model3", "model5"]:
                    # Lấy kết quả của bước lớn nhất để làm dữ liệu cho trang animation
                    highest_step_res = results_dict[max(results_dict.keys())]
                    st.session_state.dynamic_plot_data = {
                        'T': highest_step_res['t_plot'],
                        'Y': highest_step_res['approx_sol_plot'],
                        'y0_anim': y0, 'params': params,
                    }
                    st.session_state.show_dynamic_sim_button = True
            else:
                st.warning("Mô phỏng không trả về kết quả nào.")
                st.session_state.last_results = None
        
        except Exception as e:
            st.error(f"Đã xảy ra lỗi không xác định trong quá trình chạy: {e}")
            st.code(traceback.format_exc())
            st.session_state.last_results = None

# --- Hiển thị kết quả (luôn chạy để hiển thị kết quả cũ nếu có) ---
if st.session_state.get('last_results'):
    results = st.session_state.last_results
    
    st.markdown("---")
    st.subheader("Kết quả mô phỏng")
    
    try:
        fig_sol, fig_err, fig_ord = plotting.create_results_figures(
            results_dict=results, T=T, model_data=model_data,
            method_short=st.session_state.get('method_selection', 'Bashforth').replace(T['screen2_method_ab'], 'Bashforth').replace(T['screen2_method_am'], 'Moulton'),
            selected_component='y' if st.session_state.get('selected_component') == T.get('model5_component_y') else 'x'
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig_sol)
            st.pyplot(fig_ord)
        with col2:
            st.pyplot(fig_err)
    except Exception as e:
        st.error(f"Lỗi khi vẽ đồ thị: {e}")
        st.code(traceback.format_exc())

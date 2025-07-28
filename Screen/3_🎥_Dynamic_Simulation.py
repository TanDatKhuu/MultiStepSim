# Screen/3_🎥_Dynamic_Simulation.py
import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import traceback
from modules.animations import Cell, DiseaseSimulationABM, get_display_coords_mixed
from modules import solvers # Import solvers cho Model 5

# --- Cấu hình trang ---
st.set_page_config(page_title="Dynamic Simulation", layout="wide")

# --- Kiểm tra trạng thái và lấy dữ liệu cần thiết ---
if 'translations' not in st.session_state:
    st.error("Vui lòng bắt đầu từ trang chính (streamlit_main.py).")
    st.stop()

if 'selected_model_data' not in st.session_state:
    st.warning("Vui lòng chọn một mô hình từ trang 'Model Selection' trước.")
    st.stop()

# Lấy dữ liệu từ st.session_state
T = st.session_state.translations
model_data = st.session_state.selected_model_data
model_id = model_data.get("id")
model_name = T[f"{model_id}_name"]

st.title(f"{T['screen3_dyn_only_title']}: {model_name}")

# Kiểm tra xem model này có hỗ trợ animation không
can_animate = model_id in ["model2", "model3", "model5"]
if not can_animate:
    st.warning(f"Mô hình '{model_name}' không hỗ trợ mô phỏng động.")
    st.stop()

# --- Giao diện điều khiển trong Sidebar ---
with st.sidebar:
    st.header(T['screen3_settings_group_title'])
    
    # Slider tốc độ
    speed_multiplier = st.slider(
        T['screen3_speed_label'], 
        min_value=0.5, max_value=5.0, value=1.0, step=0.5
    )
    
    # Nút Bắt đầu/Chạy lại
    if st.button("Bắt đầu / Chạy lại Mô phỏng", use_container_width=True, type="primary"):
        st.session_state.anim_running = True
        # Xóa trạng thái cũ để bắt đầu lại từ đầu
        if 'abm_instance' in st.session_state:
            del st.session_state.abm_instance
        if 'm5_trajectory' in st.session_state:
            del st.session_state.m5_trajectory

    # Nút Dừng
    if st.button("Dừng Mô phỏng", use_container_width=True):
        st.session_state.anim_running = False

# --- Placeholder cho animation và thông tin ---
# st.empty() tạo ra một "khung" rỗng mà ta có thể cập nhật nội dung liên tục
plot_placeholder = st.empty()
info_placeholder = st.empty()


# --- Vòng lặp Animation Chính ---
if st.session_state.get('anim_running', False):
    try:
        # ===================================================================
        # LOGIC CHO MODEL 2: SỰ TĂNG TRƯỞNG TẾ BÀO
        # ===================================================================
        if model_id == "model2":
            # Lấy các tham số cần thiết từ trang trước (được lưu trong dynamic_plot_data)
            sim_data = st.session_state.get('dynamic_plot_data', {})
            t_data = sim_data.get('T')
            y0 = sim_data.get('y0_anim', 1)
            c_const = sim_data.get('c_anim', 0.1)

            if t_data is None:
                st.error("Thiếu dữ liệu thời gian để chạy mô phỏng động. Vui lòng chạy lại ở trang Simulation.")
                st.session_state.anim_running = False
            else:
                fig, ax = plt.subplots(figsize=(8, 8))
                cells = [Cell(0, 0)] # Bắt đầu với 1 cell
                
                for frame_idx, t_current in enumerate(t_data):
                    if not st.session_state.get('anim_running', False): break

                    # 1. Cập nhật trạng thái
                    target_n = int(round((y0**(1/3) + c_const * t_current / 3)**3))
                    while len(cells) < target_n:
                        parent = random.choice(cells)
                        angle = random.uniform(0, 2 * np.pi)
                        dist = random.uniform(0.6, 0.8)
                        new_cell = Cell(parent.x + dist * np.cos(angle), parent.y + dist * np.sin(angle))
                        cells.append(new_cell)

                    # 2. Vẽ lại frame
                    ax.clear()
                    ax.set_aspect('equal')
                    ax.axis('off')
                    
                    for cell in cells:
                        circle = plt.Circle((cell.x, cell.y), 0.5, color='darkred', ec='black', lw=0.5)
                        ax.add_patch(circle)

                    max_coord = max(max(abs(c.x), abs(c.y)) for c in cells) if cells else 1
                    ax.set_xlim(-max_coord - 2, max_coord + 2)
                    ax.set_ylim(-max_coord - 2, max_coord + 2)
                    
                    # 3. Hiển thị frame và thông tin
                    with plot_placeholder:
                        st.pyplot(fig)
                    with info_placeholder:
                        cols = st.columns(3)
                        cols[0].metric(label=T['screen3_result_mass'], value=f"{len(cells)}")
                        cols[1].metric(label=T['screen3_result_time'], value=f"{t_current:.2f} s")
                        cols[2].metric(label=T['screen3_result_c'], value=f"{c_const:.4f}")

                    plt.close(fig)
                    time.sleep(0.1 / speed_multiplier)
                
                st.success("Mô phỏng Model 2 hoàn tất!")
                st.session_state.anim_running = False

        # ===================================================================
        # LOGIC CHO MODEL 3: DỊCH BỆNH (ABM)
        # ===================================================================
        elif model_id == "model3":
            if 'abm_instance' not in st.session_state:
                # Khởi tạo mô phỏng lần đầu
                abm_params = st.session_state.get('dynamic_plot_data', {})
                if not abm_params:
                    st.error("Thiếu tham số để khởi tạo mô phỏng ABM.")
                    st.session_state.anim_running = False
                else:
                    st.session_state.abm_instance = DiseaseSimulationABM(**abm_params)

            sim = st.session_state.abm_instance
            if sim:
                fig, ax = plt.subplots(figsize=(8, 8))
                
                for step in range(sim.abm_params.get('max_steps', 400)):
                    if not st.session_state.get('anim_running', False): break
                    
                    sim_ended = sim.step() # Cập nhật trạng thái
                    stats = sim.get_current_stats()

                    # Vẽ frame
                    ax.clear()
                    ax.set_facecolor('lightgray')
                    ax.set_xlim(0, sim.room_dimension)
                    ax.set_ylim(0, sim.room_dimension)
                    ax.set_xticks([]); ax.set_yticks([])
                    ax.set_aspect('equal')
                    
                    # Lấy mẫu để vẽ nếu dân số quá đông
                    s_coords, i_coords = get_display_coords_mixed(
                        sim.susceptible_coords, sim.infected_coords, 150, 100
                    )
                    ax.scatter(s_coords[:, 0], s_coords[:, 1], c='blue', label=T['screen3_legend_abm_susceptible'])
                    ax.scatter(i_coords[:, 0], i_coords[:, 1], c='red', marker='*', s=60, label=T['screen3_legend_abm_infected'])
                    
                    # Hiển thị
                    with plot_placeholder:
                        st.pyplot(fig)
                    with info_placeholder:
                        cols = st.columns(4)
                        cols[0].metric(T['screen3_total_pop'], stats['total_population'])
                        cols[1].metric(T['screen3_susceptible_pop'], stats['susceptible_count'])
                        cols[2].metric(T['screen3_infected_pop'], stats['infected_count'])
                        cols[3].metric("Time Step", stats['time_step'])

                    plt.close(fig)
                    time.sleep(0.12 / speed_multiplier)
                    
                    if sim_ended:
                        st.success("Mô phỏng ABM hoàn tất (tất cả đã bị nhiễm).")
                        st.session_state.anim_running = False
                        break
                
                if st.session_state.get('anim_running', False):
                    st.warning("Mô phỏng ABM đạt giới hạn số bước.")
                    st.session_state.anim_running = False

        # ===================================================================
        # LOGIC CHO MODEL 5: ĐƯỜNG CONG TRUY ĐUỔI
        # ===================================================================
        elif model_id == "model5":
            if 'm5_trajectory' not in st.session_state:
                sim_data = st.session_state.get('dynamic_plot_data', {})
                if not sim_data:
                    st.error("Thiếu tham số để tính toán quỹ đạo. Vui lòng chạy lại ở trang Simulation.")
                    st.session_state.anim_running = False
                else:
                    with st.spinner("Đang tính toán quỹ đạo..."):
                        params = sim_data['params']
                        method = solvers.AB4_system_M5 if sim_data['method_short'] == 'Bashforth' else solvers.AM4_system_M5
                        
                        ode_func = models._model5_ode_system
                        F = lambda t, x, y: ode_func(t, x, y, params['u'], params['v'])
                        
                        t_array = np.linspace(params['t₀'], params['t₁'], 1000)
                        x_coords, y_coords = method(F, t_array, params['x0'], params['y0'])
                        
                        # Cắt ngắn mảng thời gian cho khớp với kết quả
                        t_actual = t_array[:len(x_coords)]
                        
                        st.session_state.m5_trajectory = {
                            "t": t_actual,
                            "x": x_coords,
                            "y": y_coords,
                            "params": params
                        }

            traj = st.session_state.get('m5_trajectory')
            if traj:
                fig, ax = plt.subplots(figsize=(8, 8))
                
                for frame_idx in range(len(traj['t'])):
                    if not st.session_state.get('anim_running', False): break

                    ax.clear()
                    ax.set_aspect('equal')
                    ax.grid(True, linestyle=':')
                    
                    # Vẽ toàn bộ quỹ đạo
                    ax.plot(traj['x'], traj['y'], '--', color='gray', label="Quỹ đạo")
                    # Vẽ vị trí hiện tại
                    ax.plot(traj['x'][frame_idx], traj['y'][frame_idx], 'o', color='red', markersize=10, label="Thuyền")
                    # Vẽ đích
                    ax.plot(0, 0, 'X', color='green', markersize=15, label="Đích")
                    
                    ax.set_title(T['screen3_model5_plot_title_sim1'])
                    ax.legend()

                    with plot_placeholder:
                        st.pyplot(fig)
                    with info_placeholder:
                        cols = st.columns(3)
                        cols[0].metric("Thời gian (t)", f"{traj['t'][frame_idx]:.2f} s")
                        cols[1].metric("Vị trí X", f"{traj['x'][frame_idx]:.2f} m")
                        cols[2].metric("Vị trí Y", f"{traj['y'][frame_idx]:.2f} m")
                    
                    plt.close(fig)
                    time.sleep(0.05 / speed_multiplier)
                
                st.success("Mô phỏng Model 5 hoàn tất!")
                st.session_state.anim_running = False

    except Exception as e:
        st.error(f"Đã xảy ra lỗi trong quá trình mô phỏng: {e}")
        st.code(traceback.format_exc())
        st.session_state.anim_running = False

else:
    # Hiển thị thông báo chờ khi chưa chạy
    with plot_placeholder.container():
        st.info("Nhấn 'Bắt đầu / Chạy lại Mô phỏng' ở thanh bên để xem mô phỏng động.")

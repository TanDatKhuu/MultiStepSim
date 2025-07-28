# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import traceback
from modules.animations import Cell, DiseaseSimulationABM, get_display_coords_mixed
from modules import solvers, models

# --- Cấu hình trang ---
st.set_page_config(page_title="Dynamic Simulation", layout="wide")

# --- Kiểm tra trạng thái ---
if 'translations' not in st.session_state or 'selected_model_data' not in st.session_state:
    st.warning("Vui lòng bắt đầu từ trang chính và chọn một mô hình.")
    st.stop()

# --- Lấy dữ liệu cần thiết ---
T = st.session_state.translations
model_data = st.session_state.selected_model_data
model_id = model_data.get("id")
model_name = T[f"{model_id}_name"]

st.title(f"{T['screen3_dyn_only_title']}: {model_name}")

can_animate = model_id in ["model2", "model3", "model5"]
if not can_animate:
    st.warning(f"Mô hình '{model_name}' không hỗ trợ mô phỏng động.")
    st.stop()

# --- Giao diện điều khiển Sidebar ---
with st.sidebar:
    st.header(T['screen3_settings_group_title'])
    speed_multiplier = st.slider(T['screen3_speed_label'], 0.5, 5.0, 1.0, 0.5)
    
    if st.button("Bắt đầu / Chạy lại", use_container_width=True, type="primary"):
        st.session_state.anim_running = True
        # Xóa state cũ để đảm bảo chạy lại từ đầu
        if 'abm_instance' in st.session_state: del st.session_state.abm_instance
        if 'm5_trajectory' in st.session_state: del st.session_state.m5_trajectory

    if st.button("Dừng", use_container_width=True):
        st.session_state.anim_running = False

# --- Placeholder ---
plot_placeholder = st.empty()
info_placeholder = st.empty()

# --- Vòng lặp Animation Chính ---
if st.session_state.get('anim_running', False):
    try:
        sim_data = st.session_state.get('dynamic_plot_data')
        if not sim_data:
            st.error("Không có dữ liệu để chạy mô phỏng. Vui lòng chạy mô phỏng ở trang 'Simulation' trước.")
            st.session_state.anim_running = False
            st.stop()

        # ==================== LOGIC CHO MODEL 2: CELL GROWTH ====================
        if model_id == "model2":
            t_data, y0, c = sim_data['T'], sim_data['y0_anim'], sim_data['params']['c']
            fig, ax = plt.subplots(figsize=(8, 8))
            cells = [Cell(0, 0)]
            
            for t_current in t_data:
                if not st.session_state.get('anim_running'): break
                target_n = int(round((y0**(1/3) + c * t_current / 3)**3))
                while len(cells) < target_n:
                    parent = random.choice(cells)
                    angle = random.uniform(0, 2 * np.pi)
                    cells.append(Cell(parent.x + np.cos(angle), parent.y + np.sin(angle)))
                
                ax.clear(); ax.set_aspect('equal'); ax.axis('off')
                for cell in cells: ax.add_patch(plt.Circle((cell.x, cell.y), 0.5, color='darkred'))
                max_coord = max(max(abs(c.x), abs(c.y)) for c in cells) if cells else 1
                ax.set_xlim(-max_coord-2, max_coord+2); ax.set_ylim(-max_coord-2, max_coord+2)
                
                with plot_placeholder: st.pyplot(fig)
                with info_placeholder:
                    cols = st.columns(2)
                    cols[0].metric(T['screen3_result_mass'], f"{len(cells)}")
                    cols[1].metric(T['screen3_result_time'], f"{t_current:.2f} s")
                plt.close(fig)
                time.sleep(0.05 / speed_multiplier)

        # ==================== LOGIC CHO MODEL 3: EPIDEMIC (ABM) ====================
        elif model_id == "model3":
            if 'abm_instance' not in st.session_state:
                abm_params = model_data.get('abm_defaults', {})
                params = sim_data['params']
                abm_params['total_population'] = int(params['n'] + 1)
                st.session_state.abm_instance = DiseaseSimulationABM(**abm_params)

            sim = st.session_state.abm_instance
            fig, ax = plt.subplots(figsize=(8, 8))
            for _ in range(sim.abm_params.get('max_steps', 400)):
                if not st.session_state.get('anim_running'): break
                sim_ended = sim.step()
                stats = sim.get_current_stats()
                
                ax.clear(); ax.set_facecolor('lightgray')
                ax.set_xlim(0, sim.room_dimension); ax.set_ylim(0, sim.room_dimension)
                ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
                s_coords, i_coords = get_display_coords_mixed(sim.susceptible_coords, sim.infected_coords, 150, 100)
                ax.scatter(s_coords[:, 0], s_coords[:, 1], c='blue', label=T['screen3_legend_abm_susceptible'])
                ax.scatter(i_coords[:, 0], i_coords[:, 1], c='red', marker='*', s=60, label=T['screen3_legend_abm_infected'])
                
                with plot_placeholder: st.pyplot(fig)
                with info_placeholder:
                    cols = st.columns(4)
                    cols[0].metric(T['screen3_total_pop'], stats['total_population'])
                    cols[1].metric(T['screen3_susceptible_pop'], stats['susceptible_count'])
                    cols[2].metric(T['screen3_infected_pop'], stats['infected_count'])
                    cols[3].metric("Time Step", stats['time_step'])
                plt.close(fig)
                time.sleep(0.1 / speed_multiplier)
                if sim_ended: break
        
        # ==================== LOGIC CHO MODEL 5: PURSUIT CURVE ====================
        elif model_id == "model5":
            traj = sim_data # Cho Model 5, dynamic_plot_data chính là quỹ đạo
            fig, ax = plt.subplots(figsize=(8, 8))
            for frame in range(len(traj['t'])):
                if not st.session_state.get('anim_running'): break
                ax.clear(); ax.set_aspect('equal'); ax.grid(True, linestyle=':')
                ax.plot(traj['x'], traj['y'], '--', color='gray', label="Quỹ đạo")
                ax.plot(traj['x'][frame], traj['y'][frame], 'o', color='red', markersize=10, label="Thuyền")
                ax.plot(0, 0, 'X', color='green', markersize=15, label="Đích")
                ax.set_title(T['screen3_model5_plot_title_sim1']); ax.legend()
                
                with plot_placeholder: st.pyplot(fig)
                with info_placeholder:
                    cols = st.columns(3)
                    cols[0].metric("Thời gian (t)", f"{traj['t'][frame]:.2f} s")
                    cols[1].metric("Vị trí X", f"{traj['x'][frame]:.2f} m")
                    cols[2].metric("Vị trí Y", f"{traj['y'][frame]:.2f} m")
                plt.close(fig)
                time.sleep(0.02 / speed_multiplier)

        # --- Kết thúc vòng lặp ---
        if st.session_state.get('anim_running', False):
            st.success("Mô phỏng hoàn tất!")
        st.session_state.anim_running = False

    except Exception as e:
        st.error(f"Đã xảy ra lỗi trong quá trình mô phỏng động: {e}")
        st.code(traceback.format_exc())
        st.session_state.anim_running = False

else:
    # Hiển thị thông báo chờ ban đầu
    with plot_placeholder.container():
        st.info("Nhấn 'Bắt đầu / Chạy lại' ở thanh bên để xem mô phỏng.")

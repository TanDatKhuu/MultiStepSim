import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker # <<< THÊM IMPORT NÀY

def create_results_figures(results_dict, T, model_data, method_short, selected_component='x'):
    """
    Tạo và trả về 3 đối tượng Figure của Matplotlib dựa trên kết quả mô phỏng.
    """
    # --- Khởi tạo ---
    fs = 8
    n_steps = len(results_dict)
    colors = plt.cm.viridis(np.linspace(0, 0.9, max(1, n_steps)))
    
    is_model5 = model_data.get("id") == "model5"
    
    # --- Tạo 3 Figure và Axes ---
    fig_sol, ax_sol = plt.subplots(figsize=(6, 4), dpi=100)
    fig_err, ax_err = plt.subplots(figsize=(6, 4), dpi=100)
    fig_ord, ax_ord = plt.subplots(figsize=(6, 4), dpi=100)

    # --- 1. Vẽ Đồ thị Nghiệm (Solution Plot) ---
    exact_plotted = False
    color_idx = 0
    sorted_steps = sorted(results_dict.keys())

    for step in sorted_steps:
        res = results_dict.get(step, {})
        t = res.get("t_plot")
        approx_sol = res.get("approx_sol_plot")
        exact_sol = res.get("exact_sol_plot")
        
        if not exact_plotted and exact_sol is not None and t is not None and len(t) == len(exact_sol):
            label = T['screen2_plot_exact_label']
            if is_model5: label += f" (RK5-{selected_component.upper()})"
            ax_sol.plot(t, exact_sol, color='black', lw=1.5, ls='--', label=label)
            exact_plotted = True
        
        if t is not None and approx_sol is not None and len(t) == len(approx_sol):
            label = f"A{method_short[0]}{step}"
            ax_sol.plot(t, approx_sol, color=colors[color_idx], lw=1.2, marker='.', ms=3, ls='-', label=label, markevery=int(len(t)/20) or 1)
            color_idx += 1

    sol_ylabel_key = f"screen2_plot_value_axis_{selected_component}" if is_model5 else "screen2_plot_value_axis_base"
    ax_sol.set_xlabel(T.get("screen2_plot_t_axis", "Thời gian (t)"), fontsize=fs)
    ax_sol.set_ylabel(T.get(sol_ylabel_key, "Giá trị"), fontsize=fs)
    ax_sol.set_title(T.get("screen2_plot_solution_title", "Đồ thị nghiệm"), fontsize=fs + 2, weight='bold')
    ax_sol.grid(True, linestyle=':', alpha=0.7)
    ax_sol.tick_params(axis='both', which='major', labelsize=fs - 1)
    if ax_sol.get_lines():
        ax_sol.legend(fontsize='small')
    fig_sol.tight_layout()

    # --- 2. Vẽ Đồ thị Sai số (Error Plot) ---
    color_idx = 0
    for step in sorted_steps:
        res = results_dict.get(step, {})
        n_vals = res.get("n_values_convergence")
        errors = res.get("errors_convergence")
        if n_vals is not None and errors is not None and len(n_vals) == len(errors) > 0:
            label = f"{T.get('screen2_plot_error_label_prefix', 'Sai số ')}A{method_short[0]}{step}"
            ax_err.plot(n_vals, errors, color=colors[color_idx], lw=1.2, marker='.', ms=4, ls='-', label=label)
            color_idx += 1
            
    err_ylabel_key = f"screen2_plot_error_axis_{selected_component}" if is_model5 else "screen2_plot_error_axis_base"
    ax_err.set_xlabel(T.get("screen2_plot_n_axis", "Số khoảng con (N)"), fontsize=fs)
    ax_err.set_ylabel(T.get(err_ylabel_key, "Sai số L∞"), fontsize=fs)
    ax_err.set_title(T.get("screen2_plot_error_title", "Đồ thị sai số L∞"), fontsize=fs + 2, weight='bold')
    
    # <<< SỬA LỖI PARSEEXCEPTION Ở ĐÂY >>>
    ax_err.set_yscale('log')
    ax_err.yaxis.set_major_formatter(mticker.ScalarFormatter()) # Tắt định dạng toán học của số
    
    ax_err.grid(True, linestyle=':', alpha=0.7, which='both')
    ax_err.tick_params(axis='both', which='major', labelsize=fs - 1)
    if ax_err.get_lines():
        ax_err.legend(fontsize='small')
    fig_err.tight_layout()

    # --- 3. Vẽ Đồ thị Bậc hội tụ (Order Plot) ---
    color_idx = 0
    for step in sorted_steps:
        res = results_dict.get(step, {})
        log_h = res.get("log_h_convergence")
        log_err = res.get("log_error_convergence")
        slope = res.get("order_slope")

        if log_h is not None and log_err is not None and len(log_h) >= 2 and np.isfinite(slope):
            data_label = f"A{method_short[0]}{step}{T.get('screen2_plot_order_data_label_suffix', ' (dữ liệu)')}"
            ax_ord.plot(log_h, log_err, color=colors[color_idx], marker='o', ms=4, linestyle='none', label=data_label)
            
            fit_label = T.get('screen2_plot_order_fit_label_suffix', 'Fit: O(h^{:.2f})').format(slope)
            fit_line = np.poly1d(np.polyfit(log_h, log_err, 1))
            ax_ord.plot(log_h, fit_line(log_h), color=colors[color_idx], linestyle='--', lw=1.5, label=fit_label)
            
            color_idx += 1
            
    ord_ylabel_key = f"screen2_plot_log_error_axis_{selected_component}" if is_model5 else "screen2_plot_log_error_axis_base"
    ax_ord.set_xlabel(T.get("screen2_plot_log_h_axis", "log(h)"), fontsize=fs)
    ax_ord.set_ylabel(T.get(ord_ylabel_key, "log(Sai số L∞)"), fontsize=fs)
    ax_ord.set_title(T.get("screen2_plot_order_title", "Đồ thị bậc hội tụ"), fontsize=fs + 2, weight='bold')
    ax_ord.grid(True, linestyle=':', alpha=0.7)
    ax_ord.tick_params(axis='both', which='major', labelsize=fs - 1)
    if ax_ord.get_lines():
        ax_ord.legend(fontsize='small')
    fig_ord.tight_layout()
    
    return fig_sol, fig_err, fig_ord

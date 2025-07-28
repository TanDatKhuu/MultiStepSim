# modules/models.py
# -*- coding: utf-8 -*-
import numpy as np
from modules.translations import LANG_VI, LANG_EN
from modules.animations import (ABM_ROOM_DIMENSION_DEFAULT, ABM_PTRANS_MIN, ABM_PTRANS_MAX,
                         ABM_MAX_STEPS_DEFAULT, ABM_INTERVAL_DEFAULT,
                         MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY, SAMPLE_SIZE_FOR_LARGE_POPULATION)

# ==============================================
#           Models Data (RESTRUCTURED)
# ==============================================
MODELS_DATA = {
    "model1": {
        "id": "model1",
        "name_key": "model1_name", # Key để tra cứu tên đã dịch
        "equation_key": "model1_eq", "description_key": "model1_desc",
        "internal_param_keys": ["O₀", "k", "t₀", "t₁"],
        "ode_params": ["k"],
        "exact_params": ["O₀", "k", "t₀"],
        "ode_func": lambda k: (lambda t, y: k * y),
        "exact_func": lambda O₀, k, t₀: (lambda t: O₀ * np.exp(k * (np.asarray(t) - t₀))),
    },
    "model2": {
        "id": "model2",
        "name_key": "model2_name",
        "equation_key": "model2_eq", "description_key": "model2_desc",
        "internal_param_keys": ["x₀", "t₀", "t₁"],
        "ode_params": ["c"],
        "exact_params": ["x₀", "c", "t₀"],
        "ode_func": lambda c: (lambda t, y: c * (y**(2.0/3.0) + 1e-15)),
        "exact_func": lambda x₀, c, t₀: (lambda t: (x₀**(1.0/3.0) + c * (np.asarray(t) - t₀) / 3.0)**3),
    },
    "model3": {
        "id": "model3", "can_run_abm_on_screen3": True,
        "name_key": "model3_name",
        "equation_key": "model3_eq", "description_key": "model3_desc",
        "internal_param_keys": ["n", "t₀", "t₁"],
        "ode_params": ["r", "n"],
        "exact_params": ["n", "r", "t₀"],
        "ode_func": lambda r, n: (lambda t, y: -r * y * (n + 1.0 - y)),
        "exact_func": lambda n, r, t₀: (
            lambda t: (n * (n + 1.0) * np.exp(-r * (n + 1.0) * (np.asarray(t) - t₀))) /
                      (1.0 + n * np.exp(-r * (n + 1.0) * (np.asarray(t) - t₀))) if n > 0 else
            (lambda t: np.zeros_like(np.asarray(t)))
        ),
        "abm_defaults": { # Giữ nguyên
            "initial_infected": 1, "room_dimension": ABM_ROOM_DIMENSION_DEFAULT,
            "r_to_ptrans_factor": 5000, "ptrans_min": ABM_PTRANS_MIN, "ptrans_max": ABM_PTRANS_MAX,
            "base_agent_speed": 0.04, "speed_scaling_factor": 0.5, "min_agent_speed": 0.02, "max_agent_speed": 0.20,
            "base_contact_radius": 0.5, "radius_scaling_factor": 3.0, "min_contact_radius": 0.3, "max_contact_radius": 1.5,
            "seconds_per_step": 0.1, "max_steps": ABM_MAX_STEPS_DEFAULT, "interval_ms": ABM_INTERVAL_DEFAULT,
            "display_max_total": MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY, "display_sample_size": SAMPLE_SIZE_FOR_LARGE_POPULATION
        }
    },
    "model4": {
        "id": "model4", "is_system": True,
        "name_key": "model4_name",
        "equation_key": "model4_eq", "description_key": "model4_desc",
        "internal_param_keys": ["m", "l", "a", "s", "G", "Y0", "dY0", "t₀", "t₁"],
        "ode_params": ["alpha", "beta", "m", "G", "l"],
        "exact_params": ["alpha", "beta", "m", "G", "l", "Y0", "dY0", "t₀"],
        "ode_func": lambda alpha, beta, m, G, l: (lambda t, u1, u2: np.array([u2, m * l * G - alpha * u2 - beta * u1])),
        "exact_func": lambda alpha, beta, m, G, l, Y0, dY0, t₀: (lambda t_arr: _model4_exact_solution(alpha, beta, m, G, l, Y0, dY0, t₀, t_arr)),
    },
    "model5": {
        "id": "model5", "is_system": True, "uses_rk5_reference": True,
        "name_key": "model5_name",
        "equation_key": "model5_eq", "description_key": "model5_desc",
        "internal_param_keys": ["x0", "y0", "u", "v", "t₀", "t₁"],
        "ode_params": ["u", "v"],
        "exact_params": [],
        "ode_func": lambda u, v: (lambda t, x, y: _model5_ode_system(t, x, y, u, v)),
        "exact_func": None,
    },
}
#Solve model 4
def _model4_exact_solution(alpha, beta, m, G, l, Y0, dY0, t₀, t_arr):
    """
    Calculates the exact solution Y(t) and Y'(t) for Model 4.
    Y0 = Y(t₀), dY0 = Y'(t₀)
    Returns a tuple: (Y_exact_values, dY_exact_values)
    """
    t_rel = np.asarray(t_arr) - t₀  # Sửa t0 thành t₀
    Y_vals = np.zeros_like(t_rel)
    dY_vals = np.zeros_like(t_rel)

    # Handle beta = 0 case separately to avoid division by zero later
    if abs(beta) < 1e-15:
        if abs(alpha) < 1e-15:  # Should not happen with alpha > 0 constraint
            # If alpha is also zero, it's just Y'' = m*l*G
            c = m * l * G
            Y_vals = Y0 + dY0 * t_rel + 0.5 * c * t_rel**2 # Sửa n thành Y0, k thành dY0
            dY_vals = dY0 + c * t_rel                   # Sửa k thành dY0
            return Y_vals, dY_vals
        else:
            # Y'' + alpha*Y' = m*l*G
            c = m * l * G
            # General solution: A + B*exp(-alpha*t) + (c/alpha)*t
            # Apply ICs: Y(0_rel)=Y0, Y'(0_rel)=dY0
            B = (c / alpha - dY0) / alpha               # Sửa k thành dY0
            A = Y0 - B                                  # Sửa n thành Y0
            Y_vals = A + B * np.exp(-alpha * t_rel) + (c / alpha) * t_rel
            dY_vals = -alpha * B * np.exp(-alpha * t_rel) + (c / alpha)
            return Y_vals, dY_vals

    # Case beta != 0
    steady_state = (m * l * G) / beta
    delta = alpha**2 - 4 * beta

    if delta > 1e-15:  # Overdamped
        r1 = (-alpha + np.sqrt(delta)) / 2.0
        r2 = (-alpha - np.sqrt(delta)) / 2.0
        # Y(t) = C1*exp(r1*t_rel) + C2*exp(r2*t_rel) + steady_state
        # Y(0_rel) = Y0 => C1 + C2 = Y0 - steady_state
        # Y'(0_rel) = dY0 => C1*r1 + C2*r2 = dY0
        if abs(r1 - r2) > 1e-15:
            C2 = (dY0 - r1 * (Y0 - steady_state)) / (r2 - r1) # Sửa k thành dY0, n thành Y0
            C1 = (Y0 - steady_state) - C2                    # Sửa n thành Y0
        else:
            C1, C2 = 0, 0
        Y_vals = C1 * np.exp(r1 * t_rel) + C2 * np.exp(r2 * t_rel) + steady_state
        dY_vals = C1 * r1 * np.exp(r1 * t_rel) + C2 * r2 * np.exp(r2 * t_rel)

    elif delta < -1e-15:  # Underdamped
        omega = np.sqrt(-delta) / 2.0
        zeta = -alpha / 2.0
        # Y(t) = exp(zeta*t_rel)*(C1*cos(omega*t_rel) + C2*sin(omega*t_rel)) + steady_state
        # Y(0_rel) = Y0 => C1 = Y0 - steady_state
        # Y'(0_rel) = dY0 => zeta*C1 + omega*C2 = dY0
        C1 = Y0 - steady_state                          # Sửa n thành Y0
        if abs(omega) > 1e-15:
            C2 = (dY0 - zeta * C1) / omega              # Sửa k thành dY0
        else:
            C2 = 0
        exp_term = np.exp(zeta * t_rel)
        cos_term = np.cos(omega * t_rel)
        sin_term = np.sin(omega * t_rel)
        Y_vals = exp_term * (C1 * cos_term + C2 * sin_term) + steady_state
        dY_vals = zeta * exp_term * (C1 * cos_term + C2 * sin_term) + \
                  exp_term * (-C1 * omega * sin_term + C2 * omega * cos_term)
    else:  # Critically damped
        r = -alpha / 2.0
        # Y(t) = (C1 + C2*t_rel)*exp(r*t_rel) + steady_state
        # Y(0_rel) = Y0 => C1 = Y0 - steady_state
        # Y'(0_rel) = dY0 => C2 + r*C1 = dY0
        C1 = Y0 - steady_state                          # Sửa n thành Y0
        C2 = dY0 - r * C1                               # Sửa k thành dY0
        Y_vals = (C1 + C2 * t_rel) * np.exp(r * t_rel) + steady_state
        dY_vals = C2 * np.exp(r * t_rel) + (C1 + C2 * t_rel) * r * np.exp(r * t_rel)

    return Y_vals, dY_vals
#Solve model 5
def _model5_ode_system(t, x, y, u, v):
    r = np.sqrt(x**2 + y**2) + 1e-15
    dxdt = -v * x / r
    dydt = -v * y / r - u
    return np.array([dxdt, dydt])

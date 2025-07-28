import numpy as np
from .translations import LANG_VI, LANG_EN
from .animations import (
    ABM_ROOM_DIMENSION_DEFAULT,
    ABM_PTRANS_MIN,
    ABM_PTRANS_MAX,
    ABM_MAX_STEPS_DEFAULT,
    ABM_INTERVAL_DEFAULT,
    MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY,
    SAMPLE_SIZE_FOR_LARGE_POPULATION
)
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
    #Model 2: Cell growth
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
        "id": "model3", 
        "can_run_abm_on_screen3": True,
        "equation_key": "model3_eq",
        "description_key": "model3_desc",
        "param_keys_vi": [LANG_VI["model3_param2"], LANG_VI["model3_param4"], LANG_VI["model3_param5"]],
        "param_keys_en": [LANG_EN["model3_param2"], LANG_EN["model3_param4"], LANG_EN["model3_param5"]],
        "internal_param_keys": ["n", "t₀", "t₁"], 
        "ode_func": lambda r, n_initial: (lambda t, y: -r * y * (n_initial + 1.0 - y)),
        "exact_func": lambda n_initial, r, t0: (
            lambda t: (n_initial * (n_initial + 1.0) * np.exp(-r * (n_initial + 1.0) * (np.asarray(t) - t0))) / \
                      (1.0 + n_initial * np.exp(-r * (n_initial + 1.0) * (np.asarray(t) - t0))) if n_initial > 0 else
            (lambda t: np.zeros_like(np.asarray(t))) 
        ),
        "abm_defaults": {
            "initial_infected": 1,
            "room_dimension": ABM_ROOM_DIMENSION_DEFAULT, 
            "r_to_ptrans_factor": 5000,
            "ptrans_min": ABM_PTRANS_MIN, 
            "ptrans_max": ABM_PTRANS_MAX, 
            "base_agent_speed": 0.04,
            "speed_scaling_factor": 0.5,
            "min_agent_speed": 0.02,
            "max_agent_speed": 0.20,

            "base_contact_radius": 0.5,
            "radius_scaling_factor": 3.0,
            "min_contact_radius": 0.3,
            "max_contact_radius": 1.5,
            "seconds_per_step": 0.1,

            "max_steps": ABM_MAX_STEPS_DEFAULT, 
            "interval_ms": ABM_INTERVAL_DEFAULT, 
            "display_max_total": MAX_TOTAL_AGENTS_FOR_FULL_DISPLAY, 
            "display_sample_size": SAMPLE_SIZE_FOR_LARGE_POPULATION 
        }
    },
    #Model 4: National economy
    LANG_VI["model4_name"]: {
        "id": "model4",
        "is_system": True,
        "equation_key": "model4_eq",
        "description_key": "model4_desc",
        "param_keys_vi": [
            LANG_VI["model4_param_m"], LANG_VI["model4_param_l"],
            LANG_VI["model4_param_a"], LANG_VI["model4_param_s"], 
            LANG_VI["model4_param_G"],
            LANG_VI["model4_param_alpha"], LANG_VI["model4_param_beta"], 
            LANG_VI["model4_param_dY0"], LANG_VI["model4_param_Y0"], 
            LANG_VI["model4_param_t0"], LANG_VI["model4_param_t1"]
        ],
        "param_keys_en": [
            LANG_EN["model4_param_m"], LANG_EN["model4_param_l"],
            LANG_EN["model4_param_a"], LANG_EN["model4_param_s"], 
            LANG_EN["model4_param_G"],
            LANG_EN["model4_param_alpha"], LANG_EN["model4_param_beta"], 
            LANG_EN["model4_param_dY0"], LANG_EN["model4_param_Y0"],
            LANG_EN["model4_param_t0"], LANG_EN["model4_param_t1"]
        ],
        "internal_param_keys": ["m", "l", "a", "s", "G", "Y0", "dY0", "t₀", "t₁"], 
        "ode_func": lambda alpha, beta, m, G, l: (
            lambda t, u1, u2: np.array([u2, m * l * G - alpha * u2 - beta * u1])
        ),
        "exact_func": lambda alpha, beta, m, G, l, n, k, t0: (
            lambda t_arr: _model4_exact_solution(alpha, beta, m, G, l, n, k, t0, t_arr)
        ),
    },
    #Model 5: Pursuit curve
    LANG_VI["model5_name"]: {
        "id": "model5",
        "is_system": True,                 
        "uses_rk5_reference": True,      
        "equation_key": "model5_eq",
        "description_key": "model5_desc",
        "param_keys_vi": [
            LANG_VI["model5_param_x0"], LANG_VI["model5_param_y0"],
            LANG_VI["model5_param_u"], LANG_VI["model5_param_v"] ,
            LANG_VI["model5_param_t0"], LANG_VI["model5_param_t1"],
        ],
        "param_keys_en": [
            LANG_EN["model5_param_x0"], LANG_EN["model5_param_y0"],
             LANG_EN["model5_param_u"], LANG_EN["model5_param_v"],
            LANG_EN["model5_param_t0"], LANG_EN["model5_param_t1"],
        ],
        "internal_param_keys": ["x0", "y0", "u", "v", "t₀", "t₁"], 
        "ode_func": lambda u_param, v_param: (
            lambda t, x, y: _model5_ode_system(t, x, y, u_param, v_param)
        ),
        "exact_func": None,
    },
}
#Solve model 4
def _model4_exact_solution(alpha, beta, m, G, l, n, k, t0, t_arr):
    t_rel = np.asarray(t_arr) - t0 
    Y_vals = np.zeros_like(t_rel)
    dY_vals = np.zeros_like(t_rel)
    if abs(beta) < 1e-15:
        if abs(alpha) < 1e-15: 
             c = m * l * G
             Y_vals = n + k * t_rel + 0.5 * c * t_rel**2
             dY_vals = k + c * t_rel
             return Y_vals, dY_vals
        else:
             c = m * l * G
             B = (c / alpha - k) / alpha
             A = n - B
             Y_vals = A + B * np.exp(-alpha * t_rel) + (c / alpha) * t_rel
             dY_vals = -alpha * B * np.exp(-alpha * t_rel) + (c / alpha)
             return Y_vals, dY_vals
    # Case beta != 0
    steady_state = (m * l * G) / beta
    delta = alpha**2 - 4 * beta
    if delta > 1e-15: 
        r1 = (-alpha + np.sqrt(delta)) / 2.0
        r2 = (-alpha - np.sqrt(delta)) / 2.0
        if abs(r1 - r2) > 1e-15:
            C2 = (k - r1 * (n - steady_state)) / (r2 - r1)
            C1 = (n - steady_state) - C2
        else:
             C1, C2 = 0, 0 
        Y_vals = C1 * np.exp(r1 * t_rel) + C2 * np.exp(r2 * t_rel) + steady_state
        dY_vals = C1 * r1 * np.exp(r1 * t_rel) + C2 * r2 * np.exp(r2 * t_rel)
    elif delta < -1e-15: # Underdamped
        omega = np.sqrt(-delta) / 2.0
        zeta = -alpha / 2.0
        C1 = n - steady_state
        if abs(omega)>1e-15:
            C2 = (k - zeta * C1) / omega
        else:
            C2 = 0 
        exp_term = np.exp(zeta * t_rel)
        cos_term = np.cos(omega * t_rel)
        sin_term = np.sin(omega * t_rel)
        Y_vals = exp_term * (C1 * cos_term + C2 * sin_term) + steady_state
        dY_vals = zeta * exp_term * (C1 * cos_term + C2 * sin_term) + \
                  exp_term * (-C1 * omega * sin_term + C2 * omega * cos_term)
    else: 
        r = -alpha / 2.0
        C1 = n - steady_state
        C2 = k - r * C1
        Y_vals = (C1 + C2 * t_rel) * np.exp(r * t_rel) + steady_state
        dY_vals = C2 * np.exp(r * t_rel) + (C1 + C2 * t_rel) * r * np.exp(r * t_rel)
    return Y_vals, dY_vals
#Solve model 5
def _model5_ode_system(t, x, y, u, v):
    r = np.sqrt(x**2 + y**2) + 1e-15
    dxdt = -v * x / r
    dydt = -v * y / r - u
    return np.array([dxdt, dydt])

import numpy as np
# ==============================================
#           ODE Solver Methods
# ==============================================
#RK,AB,AM bậc 1
# Runge-Kutta 2nd order method 
def RK2(f, t, y0):
    h = t[1] - t[0]
    y = [y0]
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2_std = h * f(t[i] + h, y[i] + k1)
        y_new = y[i] + (k1 + k2_std) / 2.0
        y.append(y_new)
    return np.array(y) 

# Runge-Kutta 3rd order method
def RK3(f, t, y0):
    h = t[1] - t[0]
    y = [y0]
    for i in range(len(t) - 1):
        k1 = h * f(t[i], y[i])
        k2 = h * f(t[i] + h / 2.0, y[i] + k1 / 2.0)
        k3 = h * f(t[i] + h, y[i] - k1 + 2.0 * k2)
        y_new = y[i] + (k1 + 4.0 * k2 + k3) / 6.0
        y.append(y_new)
    return np.array(y) 

# Runge-Kutta 4th order method
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
    return np.array(y) 

# Runge-Kutta 5th order method
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
    return np.array(y)

# --- Các hàm ABx, AMx giữ nguyên cách gọi RKx đã sửa ở trên ---
def AB2(f, t, y0):
    h = t[1]-t[0]
    y_start = RK2(f,t[:2],y0) if len(t)>=2 else np.array([y0])
    y = list(y_start)
    for i in range(1, len(t) - 1):
         if i < len(y) and i-1 < len(y):
             y_new = y[i] + h / 2.0 * (3.0 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
             y.append(y_new)
         else:
             print(f"Warning (AB2): Index out of bounds at i={i}, len(y)={len(y)}")
             break 
    return np.array(y)

def AB3(f, t, y0):
    h = t[1]-t[0]
    y_start = RK3(f, t[:3], y0) if len(t) >= 3 else AB2(f, t, y0) 
    y = list(y_start)
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
    y_start = RK4(f, t[:4], y0) if len(t) >= 4 else AB3(f, t, y0)
    y = list(y_start)
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
    y_start = RK5(f, t[:5], y0) if len(t) >= 5 else AB4(f, t, y0)
    y = list(y_start)
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
    y_start = RK2(f, t[:2], y0) if len(t) >= 2 else np.array([y0])
    y = list(y_start)
    for i in range(1, len(t) - 1):
         if i < len(y) and i-1 < len(y):
             y_pred = y[i] + h / 2.0 * (3.0 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
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
    y_start = RK3(f, t[:3], y0) if len(t) >= 3 else AM2(f, t, y0)
    y = list(y_start)
    for i in range(2, len(t) - 1):
         if i < len(y) and i-1 < len(y) and i-2 < len(y):
             y_pred = y[i] + h / 12.0 * (23.0 * f(t[i], y[i]) - 16.0 * f(t[i-1], y[i-1]) + 5.0 * f(t[i-2], y[i-2]))
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
    y_start = RK4(f, t[:4], y0) if len(t) >= 4 else AM3(f, t, y0)
    y = list(y_start)
    for i in range(3, len(t) - 1):
         if i < len(y) and i-1 < len(y) and i-2 < len(y) and i-3 < len(y):
             y_pred = y[i] + h / 24.0 * (55.0 * f(t[i], y[i]) - 59.0 * f(t[i-1], y[i-1]) + 37.0 * f(t[i-2], y[i-2]) - 9.0 * f(t[i-3], y[i-3]))
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

#RK,AB,AM bậc 2
# Runge-Kutta 2nd order method for SYSTEMS
def RK2_system(F, t_array, u10, u20): 
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(1, len(t_array)):
        t = t_array[i-1]
        k1_vec = F(t, u1[i-1], u2[i-1]) 
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
        u1[i + 1] = u1_i + h / 90.0 * (7.0 * k1_u1 + 32.0 * k3_u1 + 12.0 * k4_u1 + 32.0 * k5_u1 + 7.0 * k6_u1)
        u2[i + 1] = u2_i + h / 90.0 * (7.0 * k1_u2 + 32.0 * k3_u2 + 12.0 * k4_u2 + 32.0 * k5_u2 + 7.0 * k6_u2)
    return u1, u2

# Adams-Bashforth 2nd order method for SYSTEMS
def AB2_system(F, t_array, u10, u20):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1_start, u2_start = RK2_system(F, t_array[:2], u10, u20)
    u1[:2] = u1_start
    u2[:2] = u2_start
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
    u1_start, u2_start = RK5_system(F, t_array[:5], u10, u20)
    if len(u1_start) < 5: 
         print(f"Warning (AB5_system): RK5 initializer returned fewer than 5 points ({len(u1_start)}). Cannot proceed.")
         return u1_start, u2_start 
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
    u1_start, u2_start = RK2_system(F, t_array[:2], u10, u20)
    u1[:2] = u1_start
    u2[:2] = u2_start
    for i in range(2, len(t_array)):
        t_curr = t_array[i]
        t_prev1 = t_array[i-1]
        t_prev2 = t_array[i-2]
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        u1_pred = u1[i-1] + h/2.0 * (3.0*F_prev1[0] - F_prev2[0])
        u2_pred = u2[i-1] + h/2.0 * (3.0*F_prev1[1] - F_prev2[1])
        F_pred = F(t_curr, u1_pred, u2_pred) 
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
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])
        u1_pred = u1[i-1] + h/12.0 * (23.0*F_prev1[0] - 16.0*F_prev2[0] + 5.0*F_prev3[0])
        u2_pred = u2[i-1] + h/12.0 * (23.0*F_prev1[1] - 16.0*F_prev2[1] + 5.0*F_prev3[1])
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
        F_prev1 = F(t_prev1, u1[i-1], u2[i-1])
        F_prev2 = F(t_prev2, u1[i-2], u2[i-2])
        F_prev3 = F(t_prev3, u1[i-3], u2[i-3])
        F_prev4 = F(t_prev4, u1[i-4], u2[i-4])
        u1_pred = u1[i-1] + h/24.0 * (55.0*F_prev1[0] - 59.0*F_prev2[0] + 37.0*F_prev3[0] - 9.0*F_prev4[0])
        u2_pred = u2[i-1] + h/24.0 * (55.0*F_prev1[1] - 59.0*F_prev2[1] + 37.0*F_prev3[1] - 9.0*F_prev4[1])
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
        if u1[i] <= 0.5:
            return u1[:i+1], u2[:i+1]
    return u1, u2

def RK3_original_system_M5(F, t_array, u10, u20): 
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

def RK4_original_system_M5(F, t_array, u10, u20): 
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

def RK5_original_system_M5(F, t_array, u10, u20): 
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
        if u1[i+1] <= 0.5: return u1[:i+2], u2[:i+2] 
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
    for i in range(2, len(t_array)): 
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

def AB3_original_system_M5(F, t_array, u10, u20): 
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

def AB4_original_system_M5(F, t_array, u10, u20): 
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

def AB5_original_system_M5(F, t_array, u10, u20): 
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
def AM2_original_system_M5(F, t_array, u10, u20): 
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array)); u2 = np.zeros(len(t_array)); u1[0],u2[0] = u10,u20
    try:
        u1_start, u2_start = RK2_system_M5(F, t_array[:2], u10, u20); start_len=len(u1_start)
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
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AM3_original_system_M5(F, t_array, u10, u20): 
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
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

def AM4_original_system_M5(F, t_array, u10, u20): 
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
        if u1[i] <= 0.5: actual_len = i + 1; break
    return u1[:actual_len], u2[:actual_len]

# ==============================================
#   NEW Solver Methods for Model 5 - SIMULATION 1
# ==============================================

# --- RK Methods with Break (Simplified Break for RK initializers) ---
def RK2_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None): 
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
        if u1[i] <= 0.01: 
            return u1[:i+1], u2[:i+1]
    return u1, u2

def RK3_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None): 
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
        if u1[i] <= 0.01: return u1[:i+1], u2[:i+1]
    return u1, u2

def RK4_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None): 
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
        if u1[i] <= 0.01: return u1[:i+1], u2[:i+1]
    return u1, u2

def RK5_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0] = u10
    u2[0] = u20
    for i in range(len(t_array) - 1): 
        t = t_array[i]
        u1_i, u2_i = u1[i], u2[i]
        if not np.isfinite(u1_i) or not np.isfinite(u2_i):
            print(f"RK5_M5 stopping at step i={i} due to non-finite input u1_i, u2_i.")
            return u1[:i], u2[:i] 
        try:
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
        u1_new_rk5 = u1_i + h / 90.0 * (7.0 * k1_u1 + 32.0 * k3_u1 + 12.0 * k4_u1 + 32.0 * k5_u1 + 7.0 * k6_u1)
        u2_new_rk5 = u2_i + h / 90.0 * (7.0 * k1_u2 + 32.0 * k3_u2 + 12.0 * k4_u2 + 32.0 * k5_u2 + 7.0 * k6_u2)
        if not np.isfinite(u1_new_rk5) or not np.isfinite(u2_new_rk5):
            print(f"RK5_M5 stopping at step i={i}: Non-finite result u1_new, u2_new.")
            return u1[:i], u2[:i] 
        u1[i+1] = u1_new_rk5
        u2[i+1] = u2_new_rk5
        new_z_vec_for_break_rk5 = np.array([u1[i+1], u2[i+1]])
        break_occurred_rk5 = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_rk5[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_rk5) < 0.5:
                    break_occurred_rk5 = True
            else:
                if np.linalg.norm(new_z_vec_for_break_rk5) < 0.001:
                    return u1[:i+1], u2[:i+1] 
            if break_occurred_rk5:
                return u1[:i+2], u2[:i+2] 
        else:
            if u1[i+1] <= 0.01: 
                return u1[:i+2], u2[:i+2] 
    return u1, u2

def AB2_system_M5(F, t_array, u10, u20, v_t_param=None, v_n_param=None, d_param=None):
    h = t_array[1] - t_array[0]
    u1 = np.zeros(len(t_array))
    u2 = np.zeros(len(t_array))
    u1[0], u2[0] = u10, u20
    try:
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
        new_z_vec_for_break_ab = np.array([u1[i], u2[i]])
        break_occurred_ab = False
        if v_t_param is not None and v_n_param is not None and d_param is not None:
            if v_n_param == 2 * v_t_param or v_t_param == 2 * v_n_param:
                if new_z_vec_for_break_ab[0] < -0.1 * d_param or np.linalg.norm(new_z_vec_for_break_ab) < 0.5:
                    actual_len = i + 1 
                    break_occurred_ab = True
            else:
                if np.linalg.norm(new_z_vec_for_break_ab) < 0.001:
                    actual_len = i 
                    break_occurred_ab = True
            if break_occurred_ab: break
        else: 
            if u1[i] <= 0.01: actual_len = i + 1; break
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
    return u1[:actual_len], u2[:actual_len]

# =================================================================
#  NEW SOLVERS for Model 5, Simulation 2 (Combined Logic)
# =================================================================
# --- RK Methods (Initializer for AB/AM) ---
def RK2_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]
    t_curr, current_st = t_array_initial_segment[0], initial_state_combined
    try:
        k1 = f_combined_ode_func(t_curr, current_st)
        k2 = f_combined_ode_func(t_curr + h_step / 2.0, current_st + h_step / 2.0 * k1)
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
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def RK3_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]
    current_st_loop = initial_state_combined
    for i in range(len(t_array_initial_segment) - 1): 
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
        current_st_loop = new_st 
        if np.linalg.norm(new_st[2:4] - new_st[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_initial_segment[i+1]
            break 
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def RK4_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]
    current_st_loop = initial_state_combined
    for i in range(len(t_array_initial_segment) - 1): 
        t_curr = t_array_initial_segment[i]
        try:
            k1 = f_combined_ode_func(t_curr, current_st_loop)
            k2 = f_combined_ode_func(t_curr + h_step / 2.0, current_st_loop + h_step / 2.0 * k1)
            k3 = f_combined_ode_func(t_curr + h_step / 2.0, current_st_loop + h_step / 2.0 * k2)
            k4 = f_combined_ode_func(t_curr + h_step, current_st_loop + h_step * k3)
            new_st = current_st_loop + h_step / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        except Exception as e:
            print(f"RK4_Sim2_Combined: Error in f_combined_ode_func call at t={t_curr:.2f}: {e}")
            return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_mai
        time_points_list.append(t_array_initial_segment[i+1])
        state_history_list.append(new_st)
        current_st_loop = new_st
        if np.linalg.norm(new_st[2:4] - new_st[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_initial_segment[i+1]
            break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def RK5_system_M5_Sim2_CombinedLogic(f_combined_ode_func, t_array_initial_segment, initial_state_combined, catch_dist_threshold):
    h_step = t_array_initial_segment[1] - t_array_initial_segment[0]
    time_points_list = [t_array_initial_segment[0]]
    state_history_list = [initial_state_combined]
    caught_flag_main = False
    time_of_catch_main = t_array_initial_segment[-1]
    current_st_loop = initial_state_combined
    for i in range(len(t_array_initial_segment) - 1):
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
    num_initial_points = 2 
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK2_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points:
        return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list)
    state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]
    caught_flag_main = False
    time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)]
    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1):
        try:
            y_i = state_history_list[i]
            f_i = f_values_history[i]
            f_im1 = f_values_history[i-1]
            y_ip1 = y_i + (h_step / 2.0) * (3.0 * f_i - 1.0 * f_im1)
        except Exception as e:
            print(f"AB2_Sim2_Combined: Error calculating y_ip1 at t={time_points_list[i]:.2f}: {e}")
            break 
        state_history_list.append(y_ip1)
        time_points_list.append(t_array_full_potential[i+1])
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold:
            caught_flag_main = True
            time_of_catch_main = t_array_full_potential[i+1]
            break 
        try:
            f_ip1 = f_combined_like(t_array_full_potential[i+1], y_ip1)
            f_values_history.append(f_ip1)
        except Exception as e:
            print(f"AB2_Sim2_Combined: Error calculating f_ip1 at t={t_array_full_potential[i+1]:.2f}: {e}")
            break

    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AB3_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 3 
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
    num_initial_points = 4 
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
    num_initial_points = 5 
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
    num_initial_points = 2 
    t_init_segment = t_array_full_potential[:num_initial_points]
    time_points_list, states_init, caught_init, time_catch_init = RK2_system_M5_Sim2_CombinedLogic(f_combined_like, t_init_segment, initial_state_combined, catch_dist_threshold)
    if caught_init or len(states_init) < num_initial_points: return time_points_list, states_init, caught_init, time_catch_init
    time_points_list = list(time_points_list); state_history_list = list(states_init)
    h_step = t_array_full_potential[1] - t_array_full_potential[0]; caught_flag_main = False; time_of_catch_main = t_array_full_potential[-1]
    f_values_history = [f_combined_like(time_points_list[j], state_history_list[j]) for j in range(num_initial_points)] 
    for i in range(num_initial_points - 1, len(t_array_full_potential) - 1): 
        try:
            y_i = state_history_list[i]; t_i = time_points_list[i]
            f_i = f_values_history[i]
            f_im1 = f_values_history[i-1] 
            y_pred_ip1 = y_i + (h_step / 2.0) * (3.0 * f_i - 1.0 * f_im1)
            t_ip1 = t_array_full_potential[i+1]
            f_pred_ip1 = f_combined_like(t_ip1, y_pred_ip1) 
            y_ip1 = y_i + (h_step / 12.0) * (5.0 * f_pred_ip1 + 8.0 * f_i - 1.0 * f_im1)
        except Exception as e: print(f"AM2_Sim2_Combined: Error y_ip1 t={t_i:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_ip1)
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_ip1; break
        try: f_ip1_corrected = f_combined_like(t_ip1, y_ip1); f_values_history.append(f_ip1_corrected)
        except Exception as e: print(f"AM2_Sim2_Combined: Error f_ip1_corr t={t_ip1:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AM3_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 3 
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
            y_pred_ip1 = y_i + (h_step / 12.0) * (23.0 * f_i - 16.0 * f_im1 + 5.0 * f_im2)
            t_ip1 = t_array_full_potential[i+1]
            f_pred_ip1 = f_combined_like(t_ip1, y_pred_ip1)
            y_ip1 = y_i + (h_step / 24.0) * (9.0 * f_pred_ip1 + 19.0 * f_i - 5.0 * f_im1 + 1.0 * f_im2)
        except Exception as e: print(f"AM3_Sim2_Combined: Error y_ip1 t={t_i:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_ip1)
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_ip1; break
        try: f_ip1_corrected = f_combined_like(t_ip1, y_ip1); f_values_history.append(f_ip1_corrected)
        except Exception as e: print(f"AM3_Sim2_Combined: Error f_ip1_corr t={t_ip1:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

def AM4_system_M5_Sim2_CombinedLogic(f_combined_like, t_array_full_potential, initial_state_combined, catch_dist_threshold):
    num_initial_points = 4 
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
            y_pred_ip1 = y_i + (h_step / 24.0) * (55.0 * f_i - 59.0 * f_im1 + 37.0 * f_im2 - 9.0 * f_im3)
            t_ip1 = t_array_full_potential[i+1]
            f_pred_ip1 = f_combined_like(t_ip1, y_pred_ip1)
            y_ip1 = y_i + (h_step / 720.0) * (251.0 * f_pred_ip1 + 646.0 * f_i - 264.0 * f_im1 + 106.0 * f_im2 - 19.0 * f_im3)
        except Exception as e: print(f"AM4_Sim2_Combined: Error y_ip1 t={t_i:.2f}: {e}"); break
        state_history_list.append(y_ip1); time_points_list.append(t_ip1)
        if np.linalg.norm(y_ip1[2:4] - y_ip1[0:2]) <= catch_dist_threshold: caught_flag_main = True; time_of_catch_main = t_ip1; break
        try: f_ip1_corrected = f_combined_like(t_ip1, y_ip1); f_values_history.append(f_ip1_corrected)
        except Exception as e: print(f"AM4_Sim2_Combined: Error f_ip1_corr t={t_ip1:.2f}: {e}"); break
    return np.array(time_points_list), np.array(state_history_list), caught_flag_main, time_of_catch_main

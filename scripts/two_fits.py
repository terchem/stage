import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# RAW xTB
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15], dtype=float)
y_xtb = np.array([14.188904447868, 11.921677178032, 10.997390604466,
                  10.476157893797, 10.136931024835,  9.899000590125,
                   9.725113872395,  9.595133639275,  9.498277095008,
                   9.429389363896, 9.382628158495, 9.347312494256,
                   9.315677380441, 9.265934002720], dtype=float)

# DFT REFERENCE
x_majdi = np.array([1, 2, 3, 4])
y_majdi = np.array([9.211, 7.393, 6.572, 6.082])

#DFT MODEL FUNCTION
def majdi_model(n):
    return 4.359 + 4.8743 * n**(-0.72057)

# SHIFT xTB
delta_shift = np.mean(y_xtb[:4] - y_majdi)
y_shifted = y_xtb - delta_shift

# FITTING FUNCTION
def model_func(n, a, b, c):
    return a + b * n**(-c)


popt_all, _ = curve_fit(model_func, x, y_shifted, p0=(2, 5, 1))
a_all, b_all, c_all = popt_all

# Fit only for n ≥ 5
mask_n_ge_5 = x >= 5
x_fit_gt5 = x[mask_n_ge_5]
y_fit_gt5 = y_shifted[mask_n_ge_5]
popt_gt5, _ = curve_fit(model_func, x_fit_gt5, y_fit_gt5, p0=(2, 5, 1))
a_gt5, b_gt5, c_gt5 = popt_gt5

#
x_fit = np.linspace(1, 100, 2000)
y_fit_all = model_func(x_fit, a_all, b_all, c_all)
y_fit_gt5 = model_func(x_fit, a_gt5, b_gt5, c_gt5)
y_dft_model = majdi_model(x_fit)


plt.figure(figsize=(8.5, 4.7))

# Fitted curves
plt.plot(x_fit, y_fit_all, label='xTB fit (all n)', linestyle='-', color='tab:blue')
plt.plot(x_fit, y_fit_gt5, label='xTB fit (n ≥ 5)', linestyle='-', color='tab:green')

# DFT model
plt.plot(x_fit, y_dft_model, '--', color='tab:red', label='DFT model')

# Shifted xTB data
plt.scatter(x, y_shifted, marker='x', color='tab:blue', label='xTB shifted data')

# DFT reference points
plt.scatter(x_majdi, y_majdi, marker='o', edgecolors='black', color='tab:red', label='DFT reference points')


plt.plot([], [], ' ', label=f'Vertical shift = {delta_shift:.3f} eV')
plt.xlabel('n')
plt.ylabel('IE (eV)')
plt.title('xTB vs DFT: Shifted and Fitted Models')
plt.xlim(1, 100)
plt.ylim(4, max(y_shifted.max(), y_fit_all.max()) + 1)
plt.legend()
plt.tight_layout()
plt.show()

# ───────── OUTPUT ─────────
print(f"Vertical shift applied: {delta_shift:.6f} eV")
print(f"Fit (all n):     a = {a_all:.6f}, b = {b_all:.6f}, c = {c_all:.6f}")
print(f"Fit (n ≥ 5):     a = {a_gt5:.6f}, b = {b_gt5:.6f}, c = {c_gt5:.6f}")

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---- Input: C–C axis ----
A = np.array([-12.07,  1.229756,  0.0])  # Central carbon (e.g., in CH3)
B = np.array([-11.36,  2.459512,  0.0])  # Defines direction (C–C axis)

# ---- Parameters ----
bond_length = 1      # C–H bond length (Å)
bond_angle = 109.5        # H–C–H angle (degrees)
theta_deg = bond_angle / 2
theta_rad = np.radians(theta_deg)

# ---- Unit vector along A→B ----
direction = B - A
unit_dir = direction / np.linalg.norm(direction)

# ---- Base point at bond_length along axis ----
P_base = A + bond_length * unit_dir

# ---- Perpendicular direction for symmetry ----
if not np.allclose(unit_dir, [0, 0, 1]):
    arbitrary = np.array([0, 1, 0])
else:
    arbitrary = np.array([1, 0, 0])

perp_vec = np.cross(unit_dir, arbitrary)
perp_unit = perp_vec / np.linalg.norm(perp_vec)

# ---- Offset for angled hydrogens ----
offset = bond_length * np.tan(theta_rad)

# ---- Hydrogen positions ----
H1 = P_base + offset * perp_unit  # angled up
H2 = P_base - offset * perp_unit  # angled down
H3 = P_base                       # on-axis

# ---- Print coordinates ----
print("Hydrogen 1 (angled +θ):", H1)
print("Hydrogen 2 (angled -θ):", H2)
print("Hydrogen 3 (on axis):   ", H3)

# ---- Plotting ----
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot atoms
ax.scatter(*A, color='blue', label='Carbon to put hydrogens on')
ax.scatter(*B, color='green', label='Deleted Carbon')
# ax.scatter(*H1, color='red', label='Hydrogen 1 (angled)')
# ax.scatter(*H2, color='orange', label='Hydrogen 2 (angled)')
ax.scatter(*H3, color='purple', label='Hydrogen 3 (on axis)')

# Plot bonds
ax.plot(*np.column_stack((A, B)), '--', color='gray', label='C–C Axis')
# ax.plot(*np.column_stack((A, H1)), '-', color='red')
# ax.plot(*np.column_stack((A, H2)), '-', color='orange')
ax.plot(*np.column_stack((A, H3)), '-', color='purple')

# Labels and styling
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('CH')
ax.legend()
ax.set_box_aspect([1, 1, 1])
plt.show()

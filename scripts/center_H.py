import numpy as np
def add_h(center,adj):
    A = adj
    B = center

    bond_length = 1
    bond_angle = 60
    theta_deg = bond_angle / 2
    theta_rad = np.radians(theta_deg)

    # Unit vector
    direction = B - A
    unit_dir = direction / np.linalg.norm(direction)

    #Base point
    P_base = A + bond_length * unit_dir

    # Perpendicular direction
    if not np.allclose(unit_dir, [0, 0, 1]):
        arbitrary = np.array([0, 1, 0])
    else:
        arbitrary = np.array([1, 0, 0])

    perp_vec = np.cross(unit_dir, arbitrary)
    perp_unit = perp_vec / np.linalg.norm(perp_vec)

    #angled hydrogens
    offset = bond_length * np.tan(theta_rad)

    # Hydrogen positions
    H1 = P_base + offset * perp_unit  # angled up
    H2 = P_base - offset * perp_unit  # angled down
    H3 = P_base                       # on-axis
    return H1,H2,H3

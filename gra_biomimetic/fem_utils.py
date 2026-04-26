import numpy as np
from typing import List, Tuple

Pore = Tuple[float, float, float, float]

def compute_mass_properties(R: float, H: float, pores: List[Pore], material_density: float = 1000.0):
    """Return (mass, porosity, I_min) for given column parameters."""
    V_cylinder = np.pi * R**2 * H
    V_pores = sum((4/3) * np.pi * r**3 for (_, _, _, r) in pores if r > 0)
    V_material = V_cylinder - V_pores
    porosity = V_pores / V_cylinder if V_cylinder > 0 else 0
    mass = V_material * material_density
    I_min = min_moment_of_inertia(R, H, pores)
    return mass, porosity, I_min

def min_moment_of_inertia(R: float, H: float, pores: List[Pore], n_slices: int = 50) -> float:
    """Compute minimum area moment of inertia along column height."""
    y_vals = np.linspace(0, H, n_slices)
    I_full = np.pi / 4 * R**4
    I_min = I_full
    for y in y_vals:
        I_y = I_full
        for (cx, cy, cz, r) in pores:
            if r <= 0:
                continue
            dy = y - cy
            if abs(dy) >= r:
                continue
            # radius of intersection circle at this y
            r_cut = np.sqrt(r**2 - dy**2)
            # area of intersection circle
            A_cut = np.pi * r_cut**2
            # distance from column axis (x=0,z=0) to center of intersection
            d_sq = cx**2 + cz**2
            # moment of inertia of removed circular segment about its own centroid is I_cut = pi/4 * r_cut^4
            I_removed = np.pi / 4 * r_cut**4 + A_cut * d_sq
            I_y -= I_removed
        if I_y < I_min:
            I_min = I_y
    return max(I_min, 1e-10)  # avoid zero

def critical_buckling_load(I_min: float, H: float, E_modulus: float, K: float = 1.0) -> float:
    """Euler critical load for column (pinned-pinned K=1)."""
    return np.pi**2 * E_modulus * I_min / (K * H)**2

import numpy as np
from .fem_utils import compute_mass_properties, critical_buckling_load

class BioFoam:
    def __init__(self, F_target, m_target, p_target, w=(0.5, 0.3, 0.2), E_modulus=30e9):
        self.F_target = F_target
        self.m_target = m_target
        self.p_target = p_target
        self.w = w
        self.E = E_modulus

    def __call__(self, R, H, pores, material_density=2400.0):
        mass, porosity, I_min = compute_mass_properties(R, H, pores, material_density)
        F_cr = critical_buckling_load(I_min, H, self.E)
        f_str = (1.0 - F_cr / self.F_target) ** 2
        f_mass = (mass / self.m_target - 1.0) ** 2
        f_por = (porosity / self.p_target - 1.0) ** 2
        return self.w[0] * f_str + self.w[1] * f_mass + self.w[2] * f_por

class ArchFoam:
    def __init__(self, F_req, t_min, target_ratio=1.618, v=(0.5, 0.3, 0.2), E_modulus=30e9):
        self.F_req = F_req
        self.t_min = t_min
        self.target_ratio = target_ratio
        self.v = v
        self.E = E_modulus

    def __call__(self, R, H, pores, material_density=2400.0):
        mass, porosity, I_min = compute_mass_properties(R, H, pores, material_density)
        F_cr = critical_buckling_load(I_min, H, self.E)
        f_stability = (1.0 - F_cr / self.F_req) ** 2
        # technology: min wall thickness
        actual_t_min = min_wall_thickness_full(R, H, pores)
        if actual_t_min >= self.t_min:
            f_tech = 0.0
        else:
            f_tech = ((self.t_min - actual_t_min) / self.t_min) ** 2
        # aesthetics: height to diameter ratio
        ratio = H / (2 * R)
        f_aesthetics = ((ratio - self.target_ratio) / self.target_ratio) ** 2
        return self.v[0] * f_stability + self.v[1] * f_tech + self.v[2] * f_aesthetics

def min_wall_thickness(R: float, pores) -> float:
    """Simple estimate: distance from each pore to closest surface or other pore."""
    if not pores:
        return R
    min_dist = float('inf')
    for (cx, cy, cz, r) in pores:
        # distance to outer cylinder
        dist_cyl = R - np.sqrt(cx**2 + cz**2) - r
        # distance to top/bottom
        dist_top = H = ??? (we need H, pass or define)
        # We'll simplify: get global H from somewhere; but function doesn't have H. We'll compute min only from radial direction, later we can add.
        # For now, we'll assume H is large enough; we can pass H if needed.
        pass
    # Since H is not passed, we'll implement a function that takes H.
    return min_dist

def min_wall_thickness_full(R, H, pores):
    """Distance to outer surface & top/bottom for each pore."""
    if not pores:
        return R
    min_d = float('inf')
    for (cx, cy, cz, r) in pores:
        d_cyl = R - np.sqrt(cx**2 + cz**2) - r
        d_top = H - cy - r
        d_bottom = cy - r
        min_pore = min(d_cyl, d_top, d_bottom)
        if min_pore < min_d:
            min_d = min_pore
    return max(min_d, 0.0)

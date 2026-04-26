import numpy as np
import trimesh
from typing import List, Tuple

Pore = Tuple[float, float, float, float]  # (cx, cy, cz, r)

def params_to_mesh(R: float, H: float, pores: List[Pore], resolution: int = 64) -> trimesh.Trimesh:
    """Generate a column with spherical pores."""
    cylinder = trimesh.creation.cylinder(radius=R, height=H, sections=resolution)
    for (cx, cy, cz, r) in pores:
        if r <= 0:
            continue
        sphere = trimesh.creation.icosphere(radius=r, subdivisions=2)
        sphere.apply_translation([cx, cy, cz])
        cylinder = cylinder.difference(sphere)
    return cylinder

def random_genome(R_range=(0.2, 1.0), H_range=(1.0, 5.0), max_pores=10) -> np.ndarray:
    """Generate random genome: [R, H, active1, cx1, cy1, cz1, r1, ...]"""
    R = np.random.uniform(*R_range)
    H = np.random.uniform(*H_range)
    genome = [R, H]
    n_active = np.random.randint(0, max_pores + 1)
    for i in range(max_pores):
        if i < n_active:
            active = 1
            r = np.random.uniform(0.05 * R, 0.4 * R)
            cx = np.random.uniform(-R + r, R - r)
            cy = np.random.uniform(r, H - r)
            cz = np.random.uniform(-R + r, R - r)
            genome.extend([active, cx, cy, cz, r])
        else:
            genome.extend([0, 0.0, 0.0, 0.0, 0.0])
    return np.array(genome)

def decode_genome(genome: np.ndarray) -> Tuple[float, float, List[Pore]]:
    """Decode a genome into R, H, and list of active pores."""
    R, H = genome[0], genome[1]
    pores = []
    idx = 2
    while idx < len(genome):
        active = int(genome[idx])
        cx, cy, cz, r = genome[idx+1:idx+5]
        if active and r > 0:
            pores.append((cx, cy, cz, r))
        idx += 5
    return R, H, pores

def genome_length(max_pores: int) -> int:
    return 2 + 5 * max_pores

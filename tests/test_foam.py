import unittest
from gra_biomimetic.fem_utils import compute_mass_properties, critical_buckling_load
from gra_biomimetic.foam_calculators import BioFoam, ArchFoam
import math

class TestFoam(unittest.TestCase):
    def test_solid_cylinder(self):
        R, H = 0.3, 3.0
        pores = []
        mass, porosity, I_min = compute_mass_properties(R, H, pores)
        V_cyl = math.pi * R**2 * H
        self.assertAlmostEqual(mass, V_cyl * 2400, places=1)
        self.assertEqual(porosity, 0.0)

    def test_biofoam_solid(self):
        bf = BioFoam(F_target=500e3, m_target=500, p_target=0.0, E_modulus=30e9)
        val = bf(0.3, 3.0, [], material_density=2400)
        self.assertTrue(val > 0)

    def test_archfoam_proportion(self):
        af = ArchFoam(F_req=400e3, t_min=0.01, target_ratio=1.618, E_modulus=30e9)
        val = af(0.3, 3.0, [])
        # For R=0.3, H=3.0, ratio=5.0 which is far from 1.618, penalty should be >0
        self.assertTrue(val > 0)

if __name__ == '__main__':
    unittest.main()

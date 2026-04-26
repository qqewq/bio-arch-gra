from gra_biomimetic.optimizer import optimize
from gra_biomimetic.visualizer import save_mesh, show_mesh

if __name__ == "__main__":
    # Target values for a concrete column (example)
    R_range = (0.1, 0.5)  # meters
    H_range = (2.0, 5.0)
    max_pores = 8
    lambda_bio = 0.5
    F_target = 500e3  # N
    m_target = 100.0  # kg
    p_target = 0.5
    F_req = 400e3
    t_min = 0.02  # m
    target_ratio = 1.618

    R_best, H_best, pores_best, fitness = optimize(
        R_range, H_range, max_pores, lambda_bio, F_target, m_target, p_target,
        F_req, t_min, target_ratio, pop_size=30, ngen=50
    )
    print(f"Best genome: R={R_best:.3f}, H={H_best:.3f}, fitness={fitness:.4f}")
    print(f"Pores: {pores_best}")

    save_mesh(R_best, H_best, pores_best, "bio_column.obj")
    show_mesh(R_best, H_best, pores_best)

import numpy as np
from deap import base, creator, tools, algorithms
from .geometry_generator import random_genome, decode_genome, genome_length
from .foam_calculators import BioFoam, ArchFoam
from .fem_utils import critical_buckling_load
import random

def optimize(R_range, H_range, max_pores, lambda_bio, F_target, m_target, p_target,
             F_req, t_min, target_ratio, material_density=2400.0, E_modulus=30e9,
             pop_size=50, ngen=100, cxpb=0.5, mutpb=0.2):

    bio_foam = BioFoam(F_target, m_target, p_target, E_modulus=E_modulus)
    arch_foam = ArchFoam(F_req, t_min, target_ratio, E_modulus=E_modulus)

    def evaluate(individual):
        R, H, pores = decode_genome(individual)
        if R <= 0 or H <= 0:
            return (1e6,)
        # check that pores are inside
        for (cx, cy, cz, r) in pores:
            if r <= 0: continue
            if np.sqrt(cx**2+cz**2)+r > R or cy-r < 0 or cy+r > H:
                return (1e6,)
        bio = bio_foam(R, H, pores, material_density)
        arch = arch_foam(R, H, pores, material_density)
        total = lambda_bio * bio + (1 - lambda_bio) * arch
        return (total,)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    n_genes = genome_length(max_pores)
    toolbox.register("attr_float", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=n_genes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(5)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen,
                        stats=stats, halloffame=hof, verbose=True)
    best = hof[0]
    R_best, H_best, pores_best = decode_genome(best)
    return R_best, H_best, pores_best, best.fitness.values[0]

https://orcid.org/my-orcid?orcid=0009-0004-1872-1153
https://doi.org/10.5281/zenodo.19780996
# Bio-Arch GRA: Synthesis of Biological and Architectural Forms

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository implements a multilevel GRA (Geometric Recursive Analytics) nullification experiment that generates 3D forms combining biological efficiency (lightweight, high porosity) with architectural functionality (column stability, aesthetics).

## Installation

```bash
git clone https://github.com/yourname/bio-arch-gra.git
cd bio-arch-gra
pip install -r requirements.txt
```

## Quick Start

Run the example optimization:

```bash
python examples/run_bio_column.py
```

This will evolve a bio-inspired column and save the resulting mesh as `bio_column.obj`. You can also explore interactively with the Jupyter notebook:

```bash
jupyter notebook notebooks/exploration.ipynb
```

## Repository Structure

- `gra_biomimetic/` – Core modules (foam calculators, geometry generation, optimizer, FEM utilities, visualization)
- `examples/` – Runnable scripts
- `notebooks/` – Interactive demonstration
- `tests/` – Unit tests
- `paper/` – LaTeX paper describing the experiment

## How It Works

We define a two-level GRA foam:

- **Level 0 (Biology)**: $\Phi_{bio}$ penalizes deviation from optimal specific strength, mass, and porosity.
- **Level 1 (Architecture)**: $\Phi_{arch}$ penalizes insufficient stability, unmanufacturable thin walls, and non-harmonic proportions.

A genetic algorithm evolves a column with external dimensions and internal spherical pores, minimizing $J = \lambda \Phi_{bio} + (1-\lambda) \Phi_{arch}$.

## Citation

If you use this work, please cite:

```bibtex
@software{bioarchgra2026,
  author = {Bitsoev, Oleg},
  title = {Bio-Arch GRA: Biomimetic Architecture via GRA Nullification},
  year = {2026},
  url = {https://github.com/qqewq/bio-arch-gra}
}
```

## License

MIT

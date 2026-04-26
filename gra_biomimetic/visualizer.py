import trimesh
from .geometry_generator import params_to_mesh

def save_mesh(R, H, pores, filename="column.obj"):
    mesh = params_to_mesh(R, H, pores)
    mesh.export(filename)
    print(f"Saved to {filename}")

def show_mesh(R, H, pores):
    mesh = params_to_mesh(R, H, pores)
    mesh.show()

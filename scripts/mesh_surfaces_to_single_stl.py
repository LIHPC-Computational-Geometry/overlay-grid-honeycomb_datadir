import gmsh
import sys
import struct
import numpy as np

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

if len(sys.argv) < 3:
    print("Usage: python mesh_surfaces_to_single_stl.py model.step output.stl")
    gmsh.finalize()
    exit()

step_file = sys.argv[1]
stl_output = sys.argv[2]

gmsh.open(step_file)
gmsh.model.occ.synchronize()

# Mesh size
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 1)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 5)

surfaces = gmsh.model.getEntities(2)
print(f"Found {len(surfaces)} surfaces.")

all_triangles = []


def extract_triangles():
    """Extract triangles from the *current* mesh (only one surface)."""
    
    triangles = []

    # Get all nodes in this mesh
    nodeTags, coords, _ = gmsh.model.mesh.getNodes()
    coords = np.array(coords).reshape(-1, 3)

    # Build lookup: nodeTag -> coordinate index
    node_index = {tag: i for i, tag in enumerate(nodeTags)}

    # Get elements of dimension 2
    elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(2)

    for etype, _, nodeTagsElem in zip(elemTypes, elemTags, elemNodeTags):
        if etype != 2:  # 2 = triangle
            continue

        nodeTagsElem = np.array(nodeTagsElem).reshape(-1, 3)

        for triNodeTags in nodeTagsElem:
            tri_xyz = np.array([coords[node_index[tag]] for tag in triNodeTags])
            triangles.append(tri_xyz)

    return triangles


# ---- Mesh each surface independently ----
for dim, tag in surfaces:
    print(f"Meshing surface {tag}...")

    gmsh.model.removePhysicalGroups()
    gmsh.model.addPhysicalGroup(2, [tag])

    gmsh.model.mesh.generate(2)

    tris = extract_triangles()
    all_triangles.extend(tris)

    gmsh.model.mesh.clear()


# ---- Write a single combined ASCII STL ----
print(f"Writing ASCII STL: {stl_output}")

with open(stl_output, "w") as f:
    f.write("solid gmsh_export\n")

    for tri in all_triangles:
        # Dummy normal (0,0,0) — most tools recompute normals anyway
        f.write("  facet normal 0.0 0.0 0.0\n")
        f.write("    outer loop\n")

        # Write 3 vertices (ALWAYS duplicated per triangle)
        for v in tri:
            f.write(f"      vertex {v[0]} {v[1]} {v[2]}\n")

        f.write("    endloop\n")
        f.write("  endfacet\n")

    f.write("endsolid gmsh_export\n")


print("Done.")
gmsh.finalize()


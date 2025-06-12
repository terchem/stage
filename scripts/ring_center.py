#MODULE RING
def ring(input_xyz):
    import numpy as np
    import networkx as nx


    covalent_radii = {"H": 0.31, "C": 0.76,}

    def read_xyz(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()[2:]
        atoms = [line.split()[0] for line in lines]
        coords = np.array([[float(x) for x in line.split()[1:4]] for line in lines])
        return atoms, coords


    def infer_bonds(atoms, coords, scale=1.3):
        bonds = []
        for i in range(len(coords)):
            for j in range(i + 1, len(coords)):
                if atoms[i] not in covalent_radii or atoms[j] not in covalent_radii:
                    continue
                thr = scale * (covalent_radii[atoms[i]] + covalent_radii[atoms[j]])
                if np.linalg.norm(coords[i] - coords[j]) <= thr:
                    bonds.append((i, j))
        return bonds


    def build_graph(n_atoms, bonds):
        G = nx.Graph()
        G.add_nodes_from(range(n_atoms))
        G.add_edges_from(bonds)
        return G


    def compute_ring_centers(rings, coords):
        return [coords[ring].mean(axis=0) for ring in rings]


    def all_cycles_len_k(G, k):
        cycles = set()
        for start in G.nodes:
            stack = [(start, [start])]
            while stack:
                v, path = stack.pop()
                if len(path) == k:
                    if start in G[v]:
                        cycles.add(tuple(sorted(path)))
                    continue
                for nb in G[v]:
                    if nb > start and nb not in path:
                        stack.append((nb, path + [nb]))
        return [list(c) for c in cycles]


    def carbon_subgraph(atoms, G):
        carbons = [i for i, a in enumerate(atoms) if a == "C"]
        return G.subgraph(carbons)



    atoms, coords = read_xyz(input_xyz)
    bonds         = infer_bonds(atoms, coords)
    Gfull         = build_graph(len(atoms), bonds)

    Gcarbon       = carbon_subgraph(atoms, Gfull)      # optional
    rings         = all_cycles_len_k(Gcarbon, 6)       # enumerate ALL 6-rings
    centres       = compute_ring_centers(rings, coords)
    return centres

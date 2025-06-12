

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import cKDTree          # fast neighbour search


from bare_flake import bare
from hyd_flake  import hyd
from new_sym_logics import sym


m = 15          # full flake radius
n = 13          # radius used to define the symmetry-unique sites
bond_len  = 1.42   # C–C bond length
bond_tol  = 0.05
# ─────────────────────────────────────────────────────────────────────────────



def xyz_to_coords(raw_xyz, element="C"):
    """Return a list of (x, y, z) floats for the chosen element."""
    return [tuple(map(float, line.split()[1:4]))
            for line in raw_xyz if line.startswith(element)]



#graph construction
def build_graph(coords, bond=bond_len, thr=bond_tol):
    """O(N log N) neighbour detection with a KD-tree."""
    xy   = np.array([(x, y) for x, y, _ in coords])
    tree = cKDTree(xy)
    pairs = tree.query_pairs(r=bond + thr)

    G = nx.Graph()
    for i, (x, y, _) in enumerate(coords):
        G.add_node(i, pos=(x, y))
    G.add_edges_from(pairs)
    return G




if __name__ == "__main__":

    # 1) full lattice to draw --------------------------------------------------
    full_coords = xyz_to_coords(bare(m))
    G           = build_graph(full_coords)
    pos         = nx.get_node_attributes(G, "pos")

    # 2) symmetry-unique sites from the *smaller* flake ------------------------
    uniques_df  = sym(bare(n))                   # DataFrame ['x','y','z']
    perim_sites = uniques_df.to_numpy()          # → array of (x, y, z) rows

    # 3) plot ------------------------------------------------------------------
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos, width=1, alpha=.6, edge_color="grey")
    nx.draw_networkx_nodes(G, pos, node_size=40, node_color="lightgrey")

    for x, y, z in perim_sites:
        plt.scatter(x, y, s=110, c="red", zorder=5)

    plt.title(f"Graphene flake m={m}  |  perimeter holes n={n}")
    plt.axis("equal"); plt.axis("off"); plt.tight_layout(); plt.show()

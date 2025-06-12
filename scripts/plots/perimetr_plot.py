
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import cKDTree, ConvexHull

from bare_flake import bare


m = 13     # full flake radius
n = 11    # highlighted inner radius
bond_len  = 1.42
bond_tol  = 0.05



def xyz_to_coords(raw_xyz, element="C"):

    return [tuple(map(float, line.split()[1:4]))
            for line in raw_xyz if line.startswith(element)]

def build_graph(coords, bond=bond_len, tol=bond_tol):
    xy = np.array([(x, y) for x, y, _ in coords])
    tree = cKDTree(xy)
    pairs = tree.query_pairs(r=bond + tol)

    G = nx.Graph()
    for i, (x, y, _) in enumerate(coords):
        G.add_node(i, pos=(x, y))
    G.add_edges_from(pairs)
    return G



if __name__ == "__main__":
    full_coords  = xyz_to_coords(bare(m))
    small_coords = xyz_to_coords(bare(n))

    G   = build_graph(full_coords)
    pos = nx.get_node_attributes(G, "pos")

    small_xy = np.array([(x, y) for x, y, _ in small_coords])
    small_set = set(map(tuple, small_xy))


    plt.figure(figsize=(8, 8))

    # full lattice: grey nodes + grey bonds
    nx.draw_networkx_edges(G, pos, width=1, alpha=.6, edge_color="grey")
    nx.draw_networkx_nodes(
        G, pos,
        node_size=40,
        node_color="lightgrey"
    )

    if len(small_xy) >= 3:
        hull = ConvexHull(small_xy)
        hull_pts = small_xy[hull.vertices]  # coordinates in hull order
        hull_pts = np.vstack([hull_pts, hull_pts[0]])

        plt.plot(
            hull_pts[:, 0], hull_pts[:, 1],
            color="green", linewidth=2
        )

    plt.title(f"Graphene flake m={m} | perimeter n={n}")
    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

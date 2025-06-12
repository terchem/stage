#OLD sym check. WRONG
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from scripts.bare_flake import bare
from scripts.hyd_flake  import hyd
from scripts.sym_check  import sym
from scripts.center_H   import add_h

#parameters
m = 15  # total flake radius
n = 13     # perimeter
bond = 1.42
tol  = 0.05


def xyz_to_coords(raw, element='C'):
    return [tuple(map(float, l.split()[1:4]))
            for l in raw if l.startswith(element)]

def build_graph(coords, bond_len=bond, thr=tol):
    G = nx.Graph()
    for i, (x1,y1,_) in enumerate(coords):
        G.add_node(i, pos=(x1,y1))
        for j, (x2,y2,_) in enumerate(coords[:i]):
            if abs(np.hypot(x1-x2, y1-y2) - bond_len) < thr:
                G.add_edge(i,j)
    return G

# Full lattice
full_coords = xyz_to_coords(bare(m))     # pristine graphene
G           = build_graph(full_coords)
pos         = nx.get_node_attributes(G, 'pos')

# Symmetry-defined hole positions
perim_sites = [tuple(row[:3]) for row in sym(bare(n)).to_numpy()]

# Centre of gravity
cx, cy = np.mean([p for p,_ in pos.values()]), np.mean([q for _,q in pos.values()])

# Plot
plt.figure(figsize=(8,8))
nx.draw_networkx_edges(G, pos, width=1, alpha=.6, edge_color='grey')
nx.draw_networkx_nodes(G, pos, node_size=40, node_color='lightgrey')

for (x,y,z) in perim_sites:
    plt.scatter(x, y, s=110, c='red', zorder=5)
    plt.plot([cx, x], [cy, y], 'k--', lw=.8)

    neigh = min(full_coords,
                key=lambda c: np.linalg.norm(np.subtract(c, (x,y,z))) if c!=(x,y,z) else 1e6)
    _ = add_h(np.array([x,y,z]), np.array(neigh))


_ = hyd(m)

plt.title(f"Graphene flake m={m}  |  perimeter holes n={n}")
plt.axis('equal'); plt.axis('off'); plt.tight_layout(); plt.show()

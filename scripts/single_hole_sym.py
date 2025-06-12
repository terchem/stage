import re
import pandas as pd
import numpy as np
from bare_flake import bare
from hyd_flake import hyd
from center_H import add_h
from new_sym_logics import sym

print('ONlY 111 ARE READY for the further optimization etc')
multiplicity = int(input(('Define a pattern 111 or 121 = ')))
n = int(input("Define a peremiter n="))
m = int(input("Define a complete mol m="))

nC = 6*m**2
nH = 6*m

count = 0

sym = sym(bare(n))
for idx, carbon in sym.iterrows():
    count += 1
    carbon = carbon.to_frame().T
    coordinates = bare(m)
    coord = {
        'x':[],
        'y':[],
        'z':[]
    }
    for elem in coordinates:
        numb = re.findall("[-+]?(?:\d*\.*\d+)",elem)
        coord['x'].append(numb[0])
        coord['y'].append((numb[1]))
        coord['z'].append((numb[2]))

    df = pd.DataFrame.from_dict(coord)
    df = df.astype(float)

    #Find two sym carbons

    for i in range (len(df['x'])):
        print(carbon)
        #Find three closest atoms to syms + ADD checker if the 3 deistances are equal>not then skip
        distances = np.linalg.norm(df[['x', 'y', 'z']].values - carbon[['x', 'y', 'z']].values, axis=1)
        df['distance'] = distances
        closest = df[df['distance'] > 0].nsmallest(3, 'distance')
        #print(closest)
        if np.allclose(closest['distance'], closest['distance'].iloc[0], atol=1e-3):
            break

    closest = closest.drop(['distance'], axis = 1)

    #print(closest)

    coordinates = hyd(m)

    if 'distance' in carbon.columns:
        carbon = carbon.drop(['distance'], axis = 1)
    #print(carbon)
    target = carbon.iloc[0]
    #print(target)

    def parse(line):
        parts = line.split()
        return tuple(map(float, parts[1:]))  # skip the first column (like '21')

    def match(c1, c2, tol=1e-6):
        return all(abs(a - b) < tol for a, b in zip(c1, c2))
    filtered_coords = [line for line in coordinates if not match(parse(line), target)]



    if multiplicity ==111:
        natom = nH + nC - 1 + 3
        for index, row in closest.iterrows():
            adj_atom = np.array([row['x'], row['y'], row['z']])
            #print(adj_atom)
            H1, H2, H3 = add_h(target, adj_atom)
            H3.values[2] = 0.3
            filtered_coords.append(("H    " + "    ".join(f"{v:.6f}" for v in H3.values)))
    elif multiplicity == 121:
        natom = nH + nC - 1 + 4
        for index, row in closest.iloc[:2].iterrows():
            adj_atom = np.array([row['x'], row['y'], row['z']])
            H1, H2, H3 = add_h(target, adj_atom)
            filtered_coords.append(("H    " + "    ".join(f"{v:.6f}" for v in H3.values)))
        row = closest.iloc[2]
        adj_atom = np.array([row['x'], row['y'], row['z']])
        H1, H2, H3 = add_h(target, adj_atom)
        filtered_coords.append(("H    " + "    ".join(f"{v:.6f}" for v in H1.values)))
        filtered_coords.append(("H    " + "    ".join(f"{v:.6f}" for v in H2.values)))



    outFile = open("graphene-C" + str(nC) + "H" + str(nH) + str(count)  + ".xyz", 'w')
    outFile.write(str(natom) + "\n")
    outFile.write("Graphene C" + str(nC) + "H" + str(nH) + " in xyz format\n")
    for point in filtered_coords:
        outFile.write(point + "\n")

    outFile.close()
    sym = sym.iloc[1:].reset_index(drop=True)

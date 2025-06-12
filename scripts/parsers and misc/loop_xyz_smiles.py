import os
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, Draw


input_folder = "/Users/anton/PycharmProjects/CUSTODI/data/coordinates"
output_folder = "/Users/anton/PycharmProjects/CUSTODI/data/topo"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".xyz"):
        xyz_path = os.path.join(input_folder, filename)
        try:
            raw_mol = Chem.MolFromXYZFile(xyz_path)
            if raw_mol is None:
                print(f"Failed to parse XYZ file: {filename}")
                continue

            mol = Chem.RWMol(raw_mol)
            rdDetermineBonds.DetermineBonds(mol, charge=0)

            mol_final = mol.GetMol()
            Chem.SanitizeMol(mol_final)
            smiles = Chem.MolToSmiles(mol_final)
            mol2d = Chem.MolFromSmiles(smiles)

            if mol2d is not None:
                img = Draw.MolToImage(mol2d)
                output_img_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
                img.save(output_img_path)
                print(f"Image saved: {output_img_path}")
                print(smiles)
            else:
                print(f"Invalid SMILES for {filename}")
            print(smiles)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

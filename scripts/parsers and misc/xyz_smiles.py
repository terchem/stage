from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
from rdkit.Chem import Draw


raw_mol = Chem.MolFromXYZFile("/Users/anton/Desktop/stage2025/xtb/coord/3/neut_opt.xyz")


mol = Chem.RWMol(raw_mol)


rdDetermineBonds.DetermineBonds(mol, charge=0)


mol_final = mol.GetMol()
Chem.SanitizeMol(mol_final)
smiles = Chem.MolToSmiles(mol_final)
mol = Chem.MolFromSmiles(smiles)
# Check
if mol:

    img = Draw.MolToImage(mol)
    img.show()  # Opens the image in the default viewer
else:
    print("Invalid SMILES string")

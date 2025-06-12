import os
import re


with open("/data/c24h12.cml", "r", encoding="ISO-8859-1") as f:
    content = f.read()


molecules = re.findall(r'(<\?xml.*?<!DOCTYPE molecule SYSTEM "cml.dtd" \[\]>\s*<molecule.*?</molecule>)', content, re.DOTALL)

os.makedirs("/data/split_cml_files", exist_ok=True)


for i, mol in enumerate(molecules, 1):
    with open(f"/Users/anton/PycharmProjects/CUSTODI/data/split_cml_files/molecule_{i}.cml", "w", encoding="ISO-8859-1") as out_file:
        out_file.write(mol)

print(f"Done! {len(molecules)} CML files created in the 'split_cml_files' folder.")

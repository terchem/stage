import xml.etree.ElementTree as ET

def parse_custom_cml_to_xyz(cml_path, xyz_path):
    tree = ET.parse(cml_path)
    root = tree.getroot()

    ns = {'cml': root.tag.split('}')[0].strip('{')}

    element_types = []
    x_coords = []
    y_coords = []
    z_coords = []

    for array in root.findall(".//stringArray[@builtin='elementType']"):
        element_types = array.text.strip().split()

    for array in root.findall(".//floatArray[@builtin='x3']"):
        x_coords = list(map(float, array.text.strip().split()))

    for array in root.findall(".//floatArray[@builtin='y3']"):
        y_coords = list(map(float, array.text.strip().split()))

    for array in root.findall(".//floatArray[@builtin='z3']"):
        z_coords = list(map(float, array.text.strip().split()))
    if not (len(element_types) == len(x_coords) == len(y_coords) == len(z_coords)):
        raise ValueError("Mismatched array lengths")

    with open(xyz_path, "w") as f:
        f.write(f"{len(element_types)}\n")
        f.write("Converted from custom CML\n")
        for symbol, x, y, z in zip(element_types, x_coords, y_coords, z_coords):
            f.write(f"{symbol} {x:.6f} {y:.6f} {z:.6f}\n")


parse_custom_cml_to_xyz("/Users/anton/PycharmProjects/CUSTODI/scripts/hole.cml", "/Users/anton/PycharmProjects/CUSTODI/scripts/c96h48.xyz")

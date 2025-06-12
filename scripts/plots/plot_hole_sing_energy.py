import matplotlib.pyplot as plt
import re

data = []

with open("/scripts/enrgies_holes/c468.txt", "r") as file:
    for line in file:
        # Match “graphene-C294H42”
        match = re.search(r"graphene-C486H54(\d+)\s+AIE:\s+([\d.]+)", line.strip())
        if match:
            index = int(match.group(1))
            energy = float(match.group(2))  # the AIE value in eV
            data.append((index, energy))

if not data:
    raise ValueError("No valid data found.")

# Sort by the integer index
data.sort(key=lambda x: x[0])


# Separate into x and y arrays
indices, energies = zip(*data)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(indices, energies, marker="o", linestyle="-")
plt.xticks(indices)
plt.xlabel("distance from center, without scale")
plt.ylabel("AIE Energy (eV)")
plt.title("AIE Energies by distance")
plt.grid(True)
plt.tight_layout()
plt.show()

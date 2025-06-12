

import matplotlib.pyplot as plt
import numpy as np
x_vals = np.array([2,3, 4, 5, 6, 7,8,9,10,11, 12, 13, 15], dtype=float)
y_vals = np.array([11.482394617213,11.221339243968,10.332103829847,10.204171591537,9.847713667236,9.746735043441,9.578408502612,9.502994186490,9.426787099509,9.380745824240,9.348526420388,9.313750164302,9.265770219290],dtype=float)
y2= np.array([11.921677178032,10.997390604466,
              10.476157893797, 10.136931024835,  9.899000590125,
               9.725113872395,  9.595133639275,  9.498277095008,
               9.429389363896,9.382628158495,9.347312494256,9.315677380441,  9.265934002720], dtype=float)


plt.figure()
plt.xlabel('n')
plt.ylabel('IE (eV)')
plt.plot(x_vals,y_vals,'o',color='tab:red',label='6 membered ring hole  ')
plt.plot(x_vals,y2,'o', label= 'complete flake')
plt.legend()
plt.show()


plt.figure()
plt.plot(x_vals, y_vals - y2, 'o-', label='Difference (No hole - Hole)')
plt.xlabel('n')
plt.ylabel('Δ IE (eV)')
plt.title('Ionization Energy Difference')
plt.legend()
plt.show()


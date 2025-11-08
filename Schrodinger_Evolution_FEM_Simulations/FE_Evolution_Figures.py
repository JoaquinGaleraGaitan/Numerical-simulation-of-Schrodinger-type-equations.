import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.tri as tri
import glob
import re

# --- Cargar el potencial una sola vez ---
Vdata = np.loadtxt("/Users/joaquingaleragaitan/Desktop/Códigos/SchrodingerEvolucionEF/potencial.txt", skiprows=1)
xv, yv, V = Vdata[:, 0], Vdata[:, 1], Vdata[:, 2]
triangV = tri.Triangulation(xv, yv)

# --- Buscar archivos psi2_t.txt ---
files = sorted(glob.glob("/Users/joaquingaleragaitan/Desktop/Códigos/SchrodingerEvolucionEF/psi2_t1.05.txt"), key=lambda f: float(re.findall(r"[\d.]+", f)[0]))
print(f"Archivos encontrados: {files}\n")

# --- Recorremos cada instante de tiempo ---
for fname in files:
    # Extraer el valor de t del nombre 
    t_val = float(re.findall(r"[\d.]+", fname)[0])

    # Cargar los datos de la función de onda
    data = np.loadtxt(fname, skiprows=1)
    x, y, psi2 = data[:, 0], data[:, 1], data[:, 2]
    triangPsi = tri.Triangulation(x, y)

    # --- Crear figura ---
    plt.figure(figsize=(6, 5))

    # Densidad de probabilidad
    plt.tricontourf(triangPsi, psi2, levels=100, cmap='inferno')
    plt.colorbar(label=r'$|\psi(x,y,t)|^2$')

    # Barrera de potencial 
    plt.tricontour(triangV, V, levels=[10, 50, 90], colors='cyan', linewidths=1.0)

    # --- Ajustes del gráfico ---
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()



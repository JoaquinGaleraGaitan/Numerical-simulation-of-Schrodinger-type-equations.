import numpy as np
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','notebook'])

#Cargamos los datos .dat
psi_data = np.loadtxt("/Users/joaquingaleragaitan/Desktop/Códigos/SchrodingerIndependienteTiempoEF/psi.dat")      # columnas: idx  x  y  psi
evals = np.loadtxt("/Users/joaquingaleragaitan/Desktop/Códigos/SchrodingerIndependienteTiempoEF/autovalores.dat") # columnas: idx  E

idx = psi_data[:,0].astype(int)
x   = psi_data[:,1]
y   = psi_data[:,2]
psi = psi_data[:,3]

#Estados analíticos no degenerados
estados = [(1,1),(2,2),(3,3),(4,4)]
L = 1

def psi_analitica(nx, ny, x, y):
    return (2/L)*np.sin(nx*np.pi*x/L) * np.sin(ny*np.pi*y/L)

#Cálculo del error L2
errors = []

for n,(nx,ny) in enumerate(estados):

    # energía analítica equivalente
    i = n  # suponiendo que evals está ordenado (lo está en FreeFEM)
    
    # seleccionar los puntos FEM correspondientes al modo i
    mask = (idx == i)
    psi_num = psi[mask]
    xx = x[mask]
    yy = y[mask]

    # normalizar numérica
    psi_num = psi_num / np.sqrt(np.sum(psi_num**2))

    # analítica en los mismos puntos FEM
    psi_ana = psi_analitica(nx, ny, xx, yy)
    psi_ana = psi_ana / np.sqrt(np.sum(psi_ana**2))

    # densidades
    rho_num = psi_num**2
    rho_ana = psi_ana**2

    # error L2 (promedio sobre la malla FEM)
    error = np.sqrt(np.mean((rho_num - rho_ana)**2))
    errors.append(error)

    print(f"Error ({nx},{ny}) = {error:.6e}")


labels = [f"({nx},{ny})" for nx,ny in estados]

plt.figure(figsize=(6,4))
plt.plot(range(1,len(errors)+1), errors, "o-", lw=2)
plt.xticks(range(1,len(errors)+1), labels)
plt.xlabel("Estado (nₓ,nᵧ)")
plt.ylabel("Error $L^2$")
plt.grid()
plt.tight_layout()
plt.show()

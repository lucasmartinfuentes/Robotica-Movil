import pandas as pd
import matplotlib.pyplot as plt

# Asegúrate de haber renombrado tus archivos real_pose de cada corrida a estos nombres:
archivo_p = 'trayectoria_P.csv'
archivo_pi = 'trayectoria_PI.csv'
archivo_dead_reckoning = 'trayectoria_DR.csv' 

plt.figure(figsize=(8, 8))

# 1. Trayectoria Controlador P (Leemos sin cabecera y le asignamos 'x' e 'y')
try:
    df_p = pd.read_csv(archivo_p, header=None, names=['x', 'y'])
    plt.plot(df_p['x'], df_p['y'], label='Controlador P', color='blue', linewidth=2)
except FileNotFoundError:
    print(f"Aviso: No se encontró '{archivo_p}'.")

# 2. Trayectoria Controlador PI
try:
    df_pi = pd.read_csv(archivo_pi, header=None, names=['x', 'y'])
    plt.plot(df_pi['x'], df_pi['y'], label='Controlador PI', color='red', linestyle='--', linewidth=2)
except FileNotFoundError:
    print(f"Aviso: No se encontró '{archivo_pi}'.")

# 3. Trayectoria Dead Reckoning (Lab 1)
try:
    df_dr = pd.read_csv(archivo_dead_reckoning, header=None, names=['x', 'y'])
    plt.plot(df_dr['x'], df_dr['y'], label='Lazo Abierto (Dead Reckoning Lab 1)', color='green', linestyle=':', linewidth=2)
except FileNotFoundError:
    print(f"Aviso: No se encontró '{archivo_dead_reckoning}'.")

# Configuración visual
plt.title('Comparación de Trayectorias 2D (Plano XY)')
plt.xlabel('Posición X [m]')
plt.ylabel('Posición Y [m]')
plt.legend()
plt.grid(True)
plt.axis('equal') # Mantiene la proporción real del espacio 2D

plt.tight_layout()
plt.show()
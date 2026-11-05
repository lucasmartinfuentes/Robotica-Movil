import pandas as pd
import matplotlib.pyplot as plt

# Definir los nombres de los archivos
archivo_p = 'datos_control_P.csv'
archivo_pi = 'datos_control_PI.csv'

def procesar_datos(df):
    """Filtra el dataframe para obtener solo el primer movimiento lineal y angular."""
    df_lineal = df[df['tipo'] == 'lineal']
    df_angular = df[df['tipo'] == 'angular']

    # Cortar en el punto donde el tiempo vuelve a caer a 0 (solo el primer movimiento)
    corte_lin = df_lineal[df_lineal['tiempo'].diff() < 0].index.min()
    if pd.notna(corte_lin):
        df_lineal = df_lineal.loc[:corte_lin-1]

    corte_ang = df_angular[df_angular['tiempo'].diff() < 0].index.min()
    if pd.notna(corte_ang):
        df_angular = df_angular.loc[:corte_ang-1]
        
    return df_lineal, df_angular

try:
    # Leer los CSV
    df_p = pd.read_csv(archivo_p)
    df_pi = pd.read_csv(archivo_pi)

    # Procesar ambos datasets
    p_lin, p_ang = procesar_datos(df_p)
    pi_lin, pi_ang = procesar_datos(df_pi)

    # Crear la figura con 4 sub-gráficos (2 filas x 2 columnas)
    plt.figure(figsize=(16, 10))

    # ==========================================
    # FILA 1: CONTROLADOR P
    # ==========================================
    
    # --- Gráfico 1: Controlador P (Lineal) ---
    plt.subplot(2, 2, 1)
    plt.plot(p_lin['tiempo'], p_lin['referencia'], label='Pref (Referencia)', linestyle='--', color='red')
    plt.plot(p_lin['tiempo'], p_lin['salida_real'], label='Preal (Salida)', linewidth=2, color='blue')
    plt.plot(p_lin['tiempo'], p_lin['actuacion'], label='Vs (Actuación)', alpha=0.6, color='green')
    plt.title('Controlador P - Movimiento Lineal')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Distancia [m] / Velocidad [m/s]')
    plt.ylim(-0.05, p_lin['referencia'].max() * 1.15) # Ajuste de escala para ver el error estacionario
    plt.legend()
    plt.grid(True)

    # --- Gráfico 2: Controlador P (Angular) ---
    plt.subplot(2, 2, 2)
    plt.plot(p_ang['tiempo'], p_ang['referencia'], label='Pref (Referencia)', linestyle='--', color='red')
    plt.plot(p_ang['tiempo'], p_ang['salida_real'], label='Preal (Salida)', linewidth=2, color='blue')
    plt.plot(p_ang['tiempo'], p_ang['actuacion'], label='Vs (Actuación)', alpha=0.6, color='green')
    plt.title('Controlador P - Movimiento Angular')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Ángulo [rad] / Velocidad [rad/s]')
    plt.ylim(-0.05, p_ang['referencia'].max() * 1.15)
    plt.legend()
    plt.grid(True)

    # ==========================================
    # FILA 2: CONTROLADOR PI
    # ==========================================

    # --- Gráfico 3: Controlador PI (Lineal) ---
    plt.subplot(2, 2, 3)
    plt.plot(pi_lin['tiempo'], pi_lin['referencia'], label='Pref (Referencia)', linestyle='--', color='red')
    plt.plot(pi_lin['tiempo'], pi_lin['salida_real'], label='Preal (Salida)', linewidth=2, color='blue')
    plt.plot(pi_lin['tiempo'], pi_lin['actuacion'], label='Vs (Actuación)', alpha=0.6, color='green')
    plt.title('Controlador PI - Movimiento Lineal')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Distancia [m] / Velocidad [m/s]')
    plt.ylim(-0.05, pi_lin['referencia'].max() * 1.15)
    plt.legend()
    plt.grid(True)

    # --- Gráfico 4: Controlador PI (Angular) ---
    plt.subplot(2, 2, 4)
    plt.plot(pi_ang['tiempo'], pi_ang['referencia'], label='Pref (Referencia)', linestyle='--', color='red')
    plt.plot(pi_ang['tiempo'], pi_ang['salida_real'], label='Preal (Salida)', linewidth=2, color='blue')
    plt.plot(pi_ang['tiempo'], pi_ang['actuacion'], label='Vs (Actuación)', alpha=0.6, color='green')
    plt.title('Controlador PI - Movimiento Angular')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Ángulo [rad] / Velocidad [rad/s]')
    plt.ylim(-0.05, pi_ang['referencia'].max() * 1.15)
    plt.legend()
    plt.grid(True)

    # Ajustar layout para que no se superpongan los títulos
    plt.tight_layout()
    plt.show()

except FileNotFoundError as e:
    print(f"Error: {e}. Asegúrate de tener 'datos_P.csv' y 'datos_PI.csv' en esta carpeta.")
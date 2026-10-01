# Robotica-Movil

Laboratorio 1 - IIC2685 Robotica Movil

## Requisitos previos

- ROS2 Humble instalado.
- Dependencias del sistema (instalar una sola vez):
```bash
  sudo apt install -y ros-humble-image-transport ros-humble-tf-transformations ros-humble-cv-bridge libcv-bridge-dev python3-pil.imagetk python3-opencv xterm
```
- Clonar el simulador del curso (rama `master`) y este repo dentro de la carpeta `src/` de un workspace de ROS2:
```bash
  cd ~/tu_workspace/src
  git clone -b master https://github.com/gasevi/very_simple_robot_simulator.git
  git clone https://github.com/lucasmartinfuentes/Robotica-Movil.git
```
- Compilar:
```bash
  cd ~/tu_workspace
  colcon build --symlink-install
  source install/setup.bash
```

## Parte 1: Programando movimientos de TurtleBot

Nodos: `dead_reckoning_nav`, `pose_loader`, `pose_recorder`.

### Ejecucion (todo junto, recomendado)

```bash
ros2 launch lab1 avanzar_y_rotar.xml
```

Esto levanta el simulador y los 3 nodos. El robot deberia empezar a
moverse automaticamente siguiendo las poses definidas en
`lab1/config/poses.txt` (actualmente configurado para trazar un
cuadrado de 1m, 3 vueltas).

Antes de volver a ejecutar el launch, asegurate de haber detenido
la ejecucion anterior con Ctrl+C (si queda el simulador viejo
corriendo, el robot se comporta de forma erratica).

### Cambiar la trayectoria

Editar `lab1/config/poses.txt` (formato: `x, y, theta` por linea,
poses relativas a la pose anterior del robot). Si se compilo con
`--symlink-install` no hace falta recompilar; en otro caso:

```bash
colcon build --packages-select lab1
```

### Datos registrados

`pose_recorder` genera, en la carpeta desde donde se ejecuto el
launch, dos archivos:
- `real_pose_log.csv` (columnas: x,y) - posicion real
- `odom_log.csv` (columnas: x,y) - posicion segun odometria

### Factor de corrección (1.2)

El tiempo de los giros se multiplica por el parámetro `factor`,
calibrado en 1.115 (valor por defecto del launch).
Para usar otro valor:
```bash
ros2 launch lab1 avanzar_y_rotar.xml factor:=1.0
```
Resultados (5 corridas de 3 vueltas):
- Sin factor: error de cierre promedio 1.25 m
- Con factor 1.115: error de cierre promedio 9.3 cm

## Parte 2: Teleoperacion

Nodo: `teleop`. Se lanza en su propia terminal (xterm) para poder leer el teclado.
```bash
ros2 launch lab1 teleop.xml
```
Hacer clic en la ventana xterm y usar:

| Tecla | Movimiento                  |
|-------|-----------------------------|
| i     | avanzar (0.2 m/s)           |
| j     | retroceder (-0.2 m/s)       |
| a     | girar izquierda (1.0 rad/s) |
| s     | girar derecha (-1.0 rad/s)  |
| q     | avanzar + girar izquierda   |
| w     | avanzar + girar derecha     |

Al soltar la tecla, el simulador detiene al robot a los 0.6 s sin comandos.
Ctrl+C en la ventana para salir.

## Parte 3: Percepcion basica y unión

Nodos: `obstacle_detector` y `dead_reckoning_nav` (modificado).

- `obstacle_detector` se suscribe a `/camera/depth/image_raw`, divide la
  imagen de profundidad en tres regiones (izquierda, centro, derecha) y
  publica en `/occupancy_state` un `Vector3` con 1 si la region esta
  ocupada y 0 si esta libre. Una region esta ocupada si algun pixel valido
  esta a 0.5 m o menos.
- `dead_reckoning_nav` escucha `/occupancy_state`: ante un obstaculo publica
  velocidad cero, deja de contar el tiempo del tramo y escribe en la
  terminal `obstacle left`, `obstacle center` u `obstacle right`. Cuando el
  camino se despeja, retoma el tramo donde quedo.

### Ejecucion

```bash
ros2 launch lab1 accion_y_percepcion.xml
```

Levanta el simulador, `dead_reckoning_nav`, `pose_loader` y
`obstacle_detector`. El robot sigue la trayectoria de `poses.txt`.

En la ventana del mapa:
- `w` y arrastrar con el mouse: agregar una pared.
- `d` y clic sobre una pared: borrarla.

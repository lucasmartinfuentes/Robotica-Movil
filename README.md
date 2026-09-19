# Robotica-Movil

Laboratorio 1 - IIC2685 Robotica Movil

## Requisitos previos

- ROS2 Humble instalado.
- Dependencias del sistema (instalar una sola vez):
```bash
  sudo apt install ros-humble-tf-transformations
  pip install --user --upgrade transforms3d opencv-python
```
- Clonar este repo dentro de la carpeta `src/` de un workspace de ROS2:
```bash
  cd ~/tu_workspace/src
  git clone https://github.com/lucasmartinfuentes/Robotica-Movil.git
```
- Instalar dependencias del workspace (incluye el simulador):
```bash
  cd ~/tu_workspace
  rosdep install --from-paths src --ignore-src -r -y
```
- Compilar:
```bash
  colcon build
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
poses relativas a la pose anterior del robot) y recompilar:

```bash
colcon build --packages-select lab1
```

### Datos registrados

`pose_recorder` genera, en la carpeta desde donde se ejecuto el
launch, dos archivos:
- `real_pose_log.csv` (columnas: x,y) - posicion real
- `odom_log.csv` (columnas: x,y) - posicion segun odometria

## Parte 2: Teleoperacion

(pendiente)

## Parte 3: Percepcion basica

(pendiente)
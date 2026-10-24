# Lab 2: Control en lazo cerrado y comportamientos reactivos

IIC2685 Robotica Movil. Presentacion: miercoles 28 de octubre de 2026.

Paquete: `lab2_rm` (carpeta `lab2/`). Esta en el mismo workspace que el simulador
(ver el README de la raiz para instalarlo).

## Compilar

```bash
cd ~/lab1_ws
colcon build --symlink-install --packages-select lab2_rm
source install/setup.bash
```

## Estructura

```
lab2/
  lab2_rm/     nodos (.py)
  launch/      archivos launch, se instalan todos los que esten aqui
  setup.py
  package.xml
```

`setup.py` ya instala todo lo que este en `launch/`. Lo que cada uno agrega en
`setup.py` es su linea en `console_scripts` (y en `data_files` si su parte necesita
instalar otros archivos):

```python
'nombre_nodo = lab2_rm.nombre_nodo:main',
```

Si agregan una dependencia nueva, va en `package.xml` como `<depend>`. Ya estan:
`rclpy`, `std_msgs`, `geometry_msgs`, `nav_msgs`, `sensor_msgs` y `cv_bridge`.

## Nombres

Todos salen del enunciado; no cambiarlos.

| Parte | Que | Nombre |
|---|---|---|
| Todas | Paquete | `lab2_rm` |
| 1 | Launch | `avanzar_y_rotar_ctrl.xml` |
| 2 | Nodo Follow The Carrot | `follow_the_carrot` |
| 2 | Topico de la trayectoria | `nav_plan`, tipo `nav_msgs/Path` |
| 2 | Launch | `follow_the_carrot.xml` |
| 3 | Nodo detector | `detector_de_objeto` |
| 3 | Nodo seguidor | `seguidor_de_objeto` |
| 3 | Topico de la camara | `/camera/rgb/image_color`, tipo `sensor_msgs/Image` |
| 3 | Topico de la deteccion | `blue_square_position` |
| 3 | Launch | `seguimiento_de_objeto.launch` |

El enunciado no fija el nombre del nodo de la Parte 1, el del cliente que publica la
trayectoria en la Parte 2, ni el tipo de mensaje de `blue_square_position`; los elige
quien hace esa parte y los agrega a esta tabla.

Cada launch tiene que levantar el experimento completo (simulador o drivers del robot
incluidos) con un solo comando:

```bash
ros2 launch lab2_rm <archivo>
```

La extension `.launch` de la Parte 3 la exige el enunciado. Se probo en Humble y
`ros2 launch` la reconoce.

## PController (compartido)

La clase `PController` se baja del portal del curso y va en `lab2_rm/`. Viene como
controlador P; hay que agregarle:

- termino integral (para el PI de la Parte 1),
- saturacion de la actuacion (0.2 m/s en la Parte 1).

Las Partes 2 y 3 pueden partir con la clase P tal como viene.

## Que pide cada parte

### Parte 1: Navegacion con control P y PI (simulador)

- Nodo con la misma jerarquia que `dead_reckoning_nav` del Lab 1:
  - Nivel 3 `accion_mover_cb(msg)`: sin cambios.
  - Nivel 2 `mover_robot_a_destino(goal_pose)`: descompone `(x, y, theta)` en
    desplazamientos de a uno. Ejemplo: `(1, 1, pi/2)` -> `[(1,0), (0,pi/2), (1,0)]`.
  - Nivel 1 `aplicar_velocidad(displacement_list)`: cada desplazamiento es la
    referencia de un controlador lineal o de uno angular.
- 4 controladores: P lineal, P angular, PI lineal, PI angular. Ajuste por prueba y
  error partiendo de Kp, Ki del orden de 0.01.
- Velocidad maxima 0.2 m/s con saturacion.
- Repetir la rutina Avanzar y Rotar del Lab 1 con P y con PI.
- Presentacion: 4 graficos con Pref(t), Vs(t) y Preal(t) (P/PI x lineal/angular), y
  un grafico 2D de la trayectoria con P, PI y el dead reckoning del Lab 1.
- Demo: cuadrado con control.

### Parte 2: Follow The Carrot (simulador)

- Un cliente lee cada uno de los 3 .txt del portal (puntos `x,y` en metros) y publica la
  trayectoria como `nav_msgs/Path` en `nav_plan`.
- `follow_the_carrot` controla solo la orientacion con un controlador P, PI o PID, con
  velocidad lineal fija de 0.1 m/s.
  - y(t): orientacion del robot desde la odometria.
  - r(t): angulo entre el centro del robot y la zanahoria.
  - u(t): velocidad angular.
- Presentacion: trayectoria lograda vs. original y error cuadratico para las 3
  trayectorias.
- Demo: las 3 trayectorias, con una ventana que muestre el camino a seguir y el
  recorrido real mientras avanza.

### Parte 3: Seguimiento de objeto con control P (TurtleBot real)

- `detector_de_objeto`: detecta un cuadrado azul de 14x14 cm sobre fondo blanco en la
  imagen RGB y publica en `blue_square_position` la posicion horizontal x respecto al
  centro de la imagen. Se recomienda pasar a HSV.
- `seguidor_de_objeto`: controlador P (clase PController) con referencia 0 y salida
  y(t) = posicion del cuadrado; rota el robot para centrarlo. Una vez centrado, avanza
  a 0.2 m/s constante.
- Demo: guiar al robot por el espacio mostrandole el cuadrado.

## Antes de entregar

- `colcon build` limpio.
- Probar los 3 launch tal como los pide el enunciado.

#!/usr/bin/env python3
"""
Nodo lazo_cerrado_nav (Parte 1).
Implementa navegación con control P/PI usando odometría.
"""

import math
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseArray
from nav_msgs.msg import Odometry
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import csv

# Importar controlador 
from lab2_rm.controller import PIDController


class LazoCerradoNav(Node):

    def __init__(self):
        super().__init__('lazo_cerrado_nav')
        
        self.grupo_movimiento = MutuallyExclusiveCallbackGroup()
        self.grupo_percepcion = MutuallyExclusiveCallbackGroup()

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.goal_list_sub = self.create_subscription(
            PoseArray, 'goal_list', self.accion_mover_cb, 
            10, callback_group=self.grupo_movimiento)
            
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_cb, 
            10, callback_group=self.grupo_percepcion)

        # Estado actual
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0

        # Parámetros de Control PID 
        # kp = 0.5 y ki = 0.5 en angular y lineal para PI
        # kp = 1.0 angular y lineal para P
        self.pid_lineal = PIDController(kp=1.0, ki=0.0, sat=0.2)
        self.pid_angular = PIDController(kp=1.0, ki=0.0, sat=1.0)

        # Crear archivo CSV para guardar los datos de control
        self.csv_file = open('datos_control.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['tipo', 'tiempo', 'referencia', 'salida_real', 'actuacion'])


    def odom_cb(self, msg):
        # Actualiza la pose actual con odometría
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Orientación (cuaternion)  
        q = msg.pose.pose.orientation

        # Convertir a Euler
        seno_theta = 2 * (q.w*q.z + q.x*q.y)
        coseno_theta = 1 - 2 * (q.y*q.y + q.z*q.z)
        self.current_theta = math.atan2(seno_theta, coseno_theta)

    # --- Nivel 1 ---
    def aplicar_velocidad(self, displacement_list):

        for d_lin, d_ang in displacement_list:
            
            # Guardamos la posición inicial al arrancar el movimiento
            start_x = self.current_x
            start_y = self.current_y
            start_theta = self.current_theta
            
            msg = Twist()
            tolerancia_error = 0.005 # 2 cm de tolerancia

            # Movimiento lineal
            if abs(d_lin) > 0.0:
                # Indicar al PID la distancia a recorrer
                self.pid_lineal.set_target(abs(d_lin))
                error = abs(d_lin)

                # Ejecutar hasta que el error sea menor a la tolerancia definida 
                tiempo_inicio = time.time()
                while error > tolerancia_error:
                    # Distancia euclidiana recorrida desde el inicio 
                    dist_recorrida = math.sqrt((self.current_x - start_x)**2 + (self.current_y - start_y)**2)
                    
                    actuacion = self.pid_lineal.set_state(dist_recorrida)

                    t_actual = time.time() - tiempo_inicio
                    self.csv_writer.writerow(['lineal', t_actual, abs(d_lin), dist_recorrida, actuacion])
                    
                    # Aplicar velocidad manteneniendo el signo original
                    msg.linear.x = actuacion if d_lin > 0 else -actuacion
                    msg.angular.z = 0.0
                    self.cmd_vel_pub.publish(msg)

                    # Actualizar error
                    error = abs(abs(d_lin) - dist_recorrida)

                    time.sleep(0.01)

            # Movimiento angular
            elif abs(d_ang) > 0.0:
                # Indicar al PID el giro a realizar
                self.pid_angular.set_target(d_ang)
                error = abs(d_ang)

                # Ejecutar hasta que el error sea menor a la tolerancia definida 
                tiempo_inicio = time.time()
                while error > tolerancia_error:
                    # Diferencia angular recorrida
                    giro_recorrido = self.current_theta - start_theta
                    # Normalizar ángulo entre -pi y pi
                    giro_recorrido = math.atan2(math.sin(giro_recorrido), math.cos(giro_recorrido))
                    
                    actuacion = self.pid_angular.set_state(giro_recorrido)

                    t_actual = time.time() - tiempo_inicio
                    self.csv_writer.writerow(['angular', t_actual, d_ang, giro_recorrido, actuacion])
                    
                    msg.linear.x = 0.0
                    msg.angular.z = actuacion
                    self.cmd_vel_pub.publish(msg)

                    # Actualizar error
                    error = abs(d_ang - giro_recorrido)

                    time.sleep(0.01)
            
            # Detener al terminar el comando
            self.cmd_vel_pub.publish(Twist())
            time.sleep(0.5) 

    # --- Nivel 2 ---
    def mover_robot_a_destino(self, goal_pose):
        x, y, theta = goal_pose

        # Girar apuntando al objetivo
        angulo_inicial = math.atan2(y, x)
        
        # Avanzar línea recta
        distancia = math.sqrt(x**2 + y**2)
        
        # Girar al theta final y normalizar
        theta_restante = theta - angulo_inicial
        theta_restante = math.atan2(math.sin(theta_restante), math.cos(theta_restante))

        displacement_list = [
            (0.0, angulo_inicial),
            (distancia, 0.0),
            (0.0, theta_restante)
        ]

        self.aplicar_velocidad(displacement_list)

    # --- Nivel 3 ---
    def accion_mover_cb(self, msg):
        for pose in msg.poses:
            x = pose.position.x
            y = pose.position.y
            theta = pose.orientation.z  
            self.mover_robot_a_destino((x, y, theta))


def main(args=None):
    rclpy.init(args=args)
    node = LazoCerradoNav()

    exec = MultiThreadedExecutor()
    exec.add_node(node)

    try:
        exec.spin()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
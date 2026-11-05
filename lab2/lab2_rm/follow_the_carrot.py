#!/usr/bin/env python3
import rclpy
import math
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from tf_transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from lab2_rm.controller import PIDController


class FollowTheCarrot(Node):

    def __init__(self):
        super().__init__('follow_the_carrot')
        self.get_logger().info('follow_the_carrot iniciado')
        self.path = []
        self.indice = 0 #hasta donde avanzo el robot en el camino
        self.create_subscription(Path, 'nav_plan', self.path_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.lookahead = 0.1 #distancia a la zanahoria [m]
        self.pid = PIDController(kp=2.0, sat=1.0) #control P, satura el giro en 1 rad/s
        self.pid.set_target(0.0) #referencia del pid 0
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.terminado = False

    def path_cb(self, msj): #guarda lo recibido en self.path
        self.path = []
        self.get_logger().info('Recibiendo path...')
        for pose in msj.poses:
            x = pose.pose.position.x
            y = pose.pose.position.y
            self.path.append((x, y))

        self.get_logger().info('Path recibido: %d puntos' % len(self.path))



    def odom_cb(self, msj): #ciclo de control: corre con cada mensaje de odometria
        if len(self.path) == 0:
            return
        if self.terminado:
            self.cmd_pub.publish(Twist()) #quedarse quieto
            return
        distancia_min = 999999
        x = msj.pose.pose.position.x + self.path[0][0]
        y = msj.pose.pose.position.y + self.path[0][1] #suma offset, odom parte en (0, 0)
        qx = msj.pose.pose.orientation.x
        qy = msj.pose.pose.orientation.y
        qz = msj.pose.pose.orientation.z
        qw = msj.pose.pose.orientation.w
        roll, pitch, yaw = euler_from_quaternion([qx, qy, qz, qw])

        #paso 1: punto mas cercano, solo hacia adelante
        final = min(self.indice + 30, len(self.path)) #con correccion para herradura
        for i in range(self.indice, final):
            p_x, p_y = self.path[i]
            distance = math.hypot(p_x - x, p_y - y) #distancia al robot
            if distance < distancia_min:
                distancia_min = distance
                self.indice = i

        #se detiene al llegar al final del camino
        fin_x, fin_y = self.path[-1]
        distancia_fin = math.hypot(fin_x - x, fin_y - y)
        cerca_del_final = self.indice >= len(self.path) - 30
        if self.indice == len(self.path) - 1 or (cerca_del_final and distancia_fin < 0.05):
            self.terminado = True
            self.cmd_pub.publish(Twist())
            self.get_logger().info('Trayectoria completada')
            return

        #paso 2: zanahoria, primer punto a lookahead o mas del robot
        zx, zy = self.path[-1] #si no quedan puntos lejos, es el ultimo
        for i in range(self.indice, len(self.path)):
            p_x, p_y = self.path[i]
            distance = math.hypot(p_x - x, p_y - y)
            if distance >= self.lookahead:
                zx, zy = self.path[i] #setea el punto de la zanahoria
                break
        self.get_logger().info('indice=%d zanahoria=(%.2f, %.2f)' % (self.indice, zx, zy))

        #pasos 3 y 4: angulo a la zanahoria y error de orientacion
        angulo = math.atan2(zy - y, zx - x) #r(t)
        error = angulo - yaw #e(t) = r(t) - y(t)
        error = math.atan2(math.sin(error), math.cos(error)) #normaliza error

        #paso 5: el controlador entrega el giro, la velocidad lineal es fija
        pedir = self.pid.set_state(-error) #pid recibe el error, con ref 0 queda kp * error
        vel = Twist()
        vel.linear.x = 0.1
        vel.angular.z = pedir
        self.cmd_pub.publish(vel)

def main():
    rclpy.init()
    node = FollowTheCarrot()
    rclpy.spin(node)


if __name__ == '__main__':
    main()

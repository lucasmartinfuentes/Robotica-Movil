#!/usr/bin/env python3
import matplotlib.pyplot as plt
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry


class Visualizador(Node):

    def __init__(self):
        super().__init__('visualizador')
        self.path = []
        self.xs = [] #recorrido del robot
        self.ys = []
        plt.ion() #ventana sin bloquear el nodo
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.linea_path, = self.ax.plot([], [], '--') #camino a seguir
        self.linea_robot, = self.ax.plot([], []) #recorrido real
        self.create_subscription(Path, 'nav_plan', self.path_cb, 10)
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_timer(0.2, self.dibujar)

    def path_cb(self, msj): #dibuja el camino una sola vez
        if len(self.path) > 0:
            return
        for pose in msj.poses:
            self.path.append((pose.pose.position.x, pose.pose.position.y))
        xs = [p[0] for p in self.path]
        ys = [p[1] for p in self.path]
        self.linea_path.set_data(xs, ys)
        self.ax.set_xlim(min(xs) - 0.5, max(xs) + 0.5)
        self.ax.set_ylim(min(ys) - 0.5, max(ys) + 0.5)

    def odom_cb(self, msj): #guarda la pose con el mismo offset de follow_the_carrot
        if len(self.path) == 0:
            return
        self.xs.append(msj.pose.pose.position.x + self.path[0][0])
        self.ys.append(msj.pose.pose.position.y + self.path[0][1])

    def dibujar(self): #actualiza la linea y refresca la ventana
        self.linea_robot.set_data(self.xs, self.ys)
        plt.pause(0.001)


def main():
    rclpy.init()
    node = Visualizador()
    rclpy.spin(node)


if __name__ == '__main__':
    main()

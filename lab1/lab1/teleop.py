#!/usr/bin/env python3
"""
Nodo teleop (Parte 2): mueve el robot con el teclado.
lee una tecla a la vez y publica un twist en /cmd_vel.
"""
import sys
import termios
import tty
import rclpy
from geometry_msgs.msg import Twist

TECLAS = {
    'i': (0.2, 0.0),
    'j': (-0.2, 0.0),
    'a': (0.0, 1.0),
    's': (0.0, -1.0),
    'q': (0.2, 1.0),
    'w': (0.2, -1.0),
}


def read():
    config = termios.tcgetattr(sys.stdin)            # guarda como esta la terminal
    tty.setraw(sys.stdin.fileno())                   # modo crudo, tecla por tecla
    tecla = sys.stdin.read(1)                       
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, config) 
    return tecla


def main():
    rclpy.init()
    nodo = rclpy.create_node('teleop')
    pub = nodo.create_publisher(Twist, '/cmd_vel', 10)
    print('Teclas: i j a s q w , CtrlC para salir')

    while True:
        tecla = read()
        if tecla == '\x03':          # Ctrl C 
            break
        if tecla in TECLAS:
            msg = Twist()
            msg.linear.x, msg.angular.z = TECLAS[tecla]
            pub.publish(msg)

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
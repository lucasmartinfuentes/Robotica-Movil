import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float64, Bool
from cv_bridge import CvBridge

AZUL_BAJO = np.array([100, 80, 50])    # H, S, V mínimos
AZUL_ALTO = np.array([130, 255, 255])  # H, S, V máximos
AREA_MIN = 500                         # área mínima del cuadrado [px]
AREA_MAX = 20000                       # área [px] desde la cual la hoja está "cerca"


class DetectorDeObjeto(Node):
    def __init__(self):
        super().__init__('detector_de_objeto')
        self.bridge = CvBridge()
        self.pub = self.create_publisher(Float64, 'blue_square_position', 1)
        self.pub_cerca = self.create_publisher(Bool, 'blue_square_cerca', 1)
        self.create_subscription(Image, '/camera/rgb/image_color', self.imagen_cb, 1)

    def imagen_cb(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(hsv, AZUL_BAJO, AZUL_ALTO)
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        x = float('nan')  # NaN = no se ve el cuadrado
        cerca = False
        if contornos:
            c = max(contornos, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > AREA_MIN:
                m = cv2.moments(c)
                mitad = img.shape[1] / 2
                x = (m['m10'] / m['m00'] - mitad) / mitad  # -1 izquierda, 0 centro, +1 derecha
                cerca = area > AREA_MAX
        self.pub_cerca.publish(Bool(data=cerca))
        self.pub.publish(Float64(data=x))


def main():
    rclpy.init()
    rclpy.spin(DetectorDeObjeto())

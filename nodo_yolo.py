import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
import numpy as np
import json
from ultralytics import YOLO

class NodoYolo(Node):
    def __init__(self):
        super().__init__('nodo_yolo')

        self.modelo = YOLO('yolov8n.pt')
        self.get_logger().info('Modelo YOLO cargado')

        self.sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.callback,
            10
        )

        # Publica las detecciones para que otros nodos las lean
        self.pub = self.create_publisher(String, '/yolo/detecciones', 10)

        self.contador = 0

    def callback(self, msg):
        self.contador += 1
        if self.contador % 3 != 0:
            return

        frame = self.imagen_a_numpy(msg)
        if frame is None:
            return

        resultados = self.modelo(frame, verbose=False)
        detecciones = []

        for r in resultados:
            for box in r.boxes:
                clase = self.modelo.names[int(box.cls[0])]
                confianza = float(box.conf[0])
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0]]
                centro_x = (x1 + x2) // 2
                centro_y = (y1 + y2) // 2

                detecciones.append({
                    'clase': clase,
                    'confianza': round(confianza, 2),
                    'centro_px': [centro_x, centro_y],
                    'bbox': [x1, y1, x2, y2]
                })

                self.get_logger().info(
                    f'{clase} ({confianza:.0%}) — centro: ({centro_x}, {centro_y})'
                )

        # Publica siempre, aunque la lista esté vacía
        msg_out = String()
        msg_out.data = json.dumps(detecciones)
        self.pub.publish(msg_out)

    def imagen_a_numpy(self, msg):
        try:
            datos = np.frombuffer(msg.data, dtype=np.uint8)
            if msg.encoding == 'rgb8':
                return datos.reshape((msg.height, msg.width, 3))
            elif msg.encoding == 'bgr8':
                return datos.reshape((msg.height, msg.width, 3))
            else:
                self.get_logger().warn(f'Encoding no soportado: {msg.encoding}')
                return None
        except Exception as e:
            self.get_logger().error(f'Error: {e}')
            return None

def main():
    rclpy.init()
    nodo = NodoYolo()
    rclpy.spin(nodo)

if __name__ == '__main__':
    main()

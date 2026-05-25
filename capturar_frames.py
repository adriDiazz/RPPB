import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import os

try:
    import cv2
except ImportError:
    raise SystemExit("Falta opencv: pip3 install opencv-python")

CARPETA_SALIDA = '/root/robot_ws/capturas'
NUM_FRAMES = 10
INTERVALO = 1  # captura 1 de cada N frames recibidos


class CapturarFrames(Node):
    def __init__(self):
        super().__init__('capturar_frames')
        os.makedirs(CARPETA_SALIDA, exist_ok=True)
        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.callback, 10
        )
        self.contador = 0
        self.guardados = 0
        self.get_logger().info(
            f'Capturando {NUM_FRAMES} frames en {CARPETA_SALIDA} ...'
        )

    def callback(self, msg):
        self.contador += 1
        if self.contador % INTERVALO != 0:
            return
        if self.guardados >= NUM_FRAMES:
            self.get_logger().info('Capturas completas. Puedes cerrar con Ctrl+C')
            return

        try:
            datos = np.frombuffer(msg.data, dtype=np.uint8)
            encoding = msg.encoding.lower()
            if encoding == 'rgb8':
                frame = datos.reshape((msg.height, msg.width, 3))
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            elif encoding == 'bgr8':
                frame = datos.reshape((msg.height, msg.width, 3))
            else:
                self.get_logger().warn(f'Encoding no soportado: {msg.encoding}')
                return

            ruta = os.path.join(CARPETA_SALIDA, f'frame_{self.guardados:03d}.jpg')
            cv2.imwrite(ruta, frame)
            self.guardados += 1
            self.get_logger().info(f'Guardado {ruta} ({self.guardados}/{NUM_FRAMES})')
        except Exception as e:
            self.get_logger().error(f'Error: {e}')


def main():
    rclpy.init()
    nodo = CapturarFrames()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.get_logger().info(f'Total guardados: {nodo.guardados} frames')
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

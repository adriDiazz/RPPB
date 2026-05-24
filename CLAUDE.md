# Proyecto: Brazo Robótico con Visión Artificial

## Resumen ejecutivo

Sistema de simulación de brazo robótico inteligente que combina ROS 2, MoveIt2 y visión por computador (YOLO) para detectar objetos en tiempo real y mover el brazo de forma autónoma hacia ellos. Fase actual: simulación software. Fase futura: robot físico impreso en 3D.

---

## Equipo

- **Ingeniero informático** — arquitectura software, ROS 2, Python, IA
- **Ingeniero industrial** — diseño mecánico, modelo 3D para impresión, conocimiento de procesos físicos

---

## Stack tecnológico

| Capa                | Tecnología           | Propósito                                                  |
| ------------------- | -------------------- | ---------------------------------------------------------- |
| Simulación robótica | ROS 2 Humble         | Sistema nervioso del robot, comunicación entre componentes |
| Planificación       | MoveIt2              | Calcula trayectorias y mueve las 7 articulaciones          |
| Visualización       | Foxglove Studio      | Ver el brazo en 3D en tiempo real                          |
| Visión artificial   | YOLOv8 + OpenCV      | Detectar y clasificar objetos con la cámara                |
| Deep Learning       | PyTorch              | Entrenamiento y ejecución de modelos IA                    |
| Simulador físico    | Gazebo Harmonic      | Simular física, cámara virtual y entorno                   |
| Infraestructura     | Docker (ARM64)       | Entorno ROS 2 aislado en Mac Apple Silicon                 |
| Diseño 3D           | FreeCAD / Fusion 360 | Diseño de piezas para impresión 3D (fase hardware)         |
| Lenguaje            | Python 3.10          | Toda la lógica de IA y control                             |

---

## Modelo del robot

**Brazo Panda de Franka Robotics**

- 7 grados de libertad (articulaciones J1-J7)
- Modelo URDF open source incluido en `moveit_resources`
- Simulado con controladores fake (sin hardware real)
- Configuración: `moveit_resources_panda_moveit_config`

---

## Arquitectura del sistema

```
Cámara virtual (Gazebo)
        │
        │ topic: /camera/image_raw
        ▼
Nodo YOLO (Python)
  - Detecta objetos en imagen
  - Calcula coordenadas 3D del objeto
        │
        │ coordenadas XYZ
        ▼
Nodo Lógica IA (Python)
  - Decide qué objeto agarrar
  - Genera goal para MoveIt2
        │
        │ MoveIt action
        ▼
MoveIt2
  - Planifica trayectoria
  - Evita colisiones
        │
        │ topic: /panda_arm_controller/joint_trajectory
        ▼
Controladores ROS 2 Control
  - panda_arm_controller
  - panda_hand_controller
        │
        ▼
Brazo Panda (simulado en Gazebo / físico en fase 2)
```

---

## Estado actual del entorno

### ✅ Completado

- [x] Docker ARM64 con ROS 2 Humble funcionando
- [x] MoveIt2 instalado y operativo
- [x] Brazo Panda cargado con 9 articulaciones activas
- [x] Foxglove Studio conectado y visualizando brazo en 3D
- [x] URDF servido por HTTP para visualización de meshes
- [x] Foxglove Bridge en puerto 8765
- [x] Servidor HTTP de meshes en puerto 8080
- [x] Workspace compilado en `/root/robot_ws`
- [x] Script de arranque automático `~/arrancar_robot.sh`
- [x] Dev Container configurado para VSCode

### 🔄 En progreso

- [ ] Script Python para mover brazo a posiciones predefinidas
- [ ] Integración cámara virtual en Gazebo

### ⏳ Pendiente

- [ ] Detección de objetos con YOLOv8
- [ ] Nodo ROS 2 que publica detecciones como topics
- [ ] Lógica de decisión: qué objeto agarrar y cuándo
- [ ] Transformación coordenadas imagen → coordenadas robot (TF2)
- [ ] Pipeline completo: ver objeto → planificar → mover → agarrar
- [ ] Diseño mecánico del brazo físico (FreeCAD)
- [ ] Impresión 3D de piezas
- [ ] Integración hardware (servos, Raspberry Pi o similar)

---

## Estructura del proyecto

```
~/robot_ws/
├── .devcontainer/
│   ├── devcontainer.json       # Config Dev Containers VSCode
│   └── docker-compose.yml      # Config Docker
├── .vscode/
│   └── tasks.json              # Tasks: ejecutar scripts, lanzar brazo...
├── src/
│   └── moveit_resources/       # Modelo URDF del brazo Panda
├── install/                    # Paquetes compilados (colcon build)
├── build/                      # Archivos de compilación
├── log/                        # Logs de compilación
└── mover_brazo.py              # ← Tu código Python aquí
```

---

## Dependencias Python

Las librerías de IA/visión se instalan dentro del contenedor Docker (no en el Mac):

```bash
docker exec -it ros2_humble bash

# Dentro del contenedor:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics opencv-python numpy matplotlib
```

El archivo `requirements.txt` del repo documenta todas las dependencias.

---

## Comandos de arranque

### Script automático (recomendado)

```bash
~/arrancar_robot.sh
```

### Manual — orden correcto

**Terminal 1 — Brazo:**

```bash
docker exec -it ros2_humble bash
source /opt/ros/humble/setup.bash && source /root/robot_ws/install/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

**Terminal 2 — Foxglove bridge:**

```bash
docker exec -it ros2_humble bash
source /opt/ros/humble/setup.bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765
```

**Terminal 3 — Servidor meshes:**

```bash
docker exec -it ros2_humble bash
cd /root/robot_ws/install/moveit_resources_panda_description/share/moveit_resources_panda_description/
python3 -m http.server 8080
```

**Terminal 4 — Tu código:**

```bash
docker exec -it ros2_humble bash
source /opt/ros/humble/setup.bash && source /root/robot_ws/install/setup.bash
python3 /root/robot_ws/tu_script.py
```

### Foxglove Studio

- URL conexión: `ws://localhost:8765`
- URDF URL: `http://localhost:8080/urdf/panda_web.urdf`

---

## Fases del proyecto

### Fase 1 — Software (actual)

Construir y validar toda la lógica en simulación sin gastar nada en hardware.

```
Semanas 1-2  ✅  Entorno ROS 2 + MoveIt2 + Foxglove funcionando
Semanas 3-4  🔄  Mover brazo con Python (posiciones predefinidas)
Semanas 5-6  ⏳  Integrar cámara virtual en Gazebo
Semanas 7-8  ⏳  YOLO detecta objetos en imagen de cámara virtual
Semanas 9-10 ⏳  Brazo se mueve autónomamente hacia objetos detectados
Semanas 11+  ⏳  Refinamiento, logging, casos edge
```

### Fase 2 — Hardware

Una vez la simulación funcione al 100%.

```
- Diseño del brazo en FreeCAD (ingeniero industrial)
- Impresión 3D de piezas
- Selección de servomotores y controlador (Raspberry Pi / Arduino)
- Instalación de cámara real (webcam USB o Pi Camera)
- Migración del código de simulación a hardware real
```

---

## Próximos pasos inmediatos

1. **Completar `mover_brazo.py`** — publicar trayectorias al topic `/panda_arm_controller/joint_trajectory` y ver el brazo moverse en Foxglove
2. **Añadir Gazebo** — lanzar entorno de simulación con mesa y objetos
3. **Cámara virtual** — suscribirse al topic `/camera/image_raw` desde Python
4. **Primer YOLO** — detectar objetos en imagen de cámara virtual
5. **Conectar todo** — pipeline completo de detección a movimiento

---

## Notas técnicas importantes

### Docker en Mac Apple Silicon (M1/M2/M3)

- Usar siempre imagen `arm64v8/ros:humble-ros-base` (no amd64)
- Flag obligatorio: `--platform linux/arm64`
- RViz2 no funciona por limitaciones OpenGL → usar Foxglove Studio

### Topics clave del brazo Panda

```
/joint_states                              → posición actual de articulaciones
/panda_arm_controller/joint_trajectory    → enviar movimientos al brazo
/tf y /tf_static                          → transformaciones entre frames
/robot_description                        → modelo URDF del robot
```

### Articulaciones del Panda

```python
joint_names = [
    'panda_joint1',  # Base (rotación horizontal)
    'panda_joint2',  # Hombro (arriba/abajo)
    'panda_joint3',  # Rotación brazo
    'panda_joint4',  # Codo
    'panda_joint5',  # Rotación antebrazo
    'panda_joint6',  # Muñeca
    'panda_joint7',  # Rotación muñeca
]
# Posición "ready" (reposo): [0.0, -0.5, 0.0, -1.5, 0.0, 1.0, 0.0]
```

---

## Contexto para Claude Code

Este proyecto usa ROS 2 Humble dentro de Docker. Todo el código Python debe:

- Importar `rclpy` para comunicarse con ROS 2
- Usar los topics listados arriba para controlar el brazo
- Ejecutarse dentro del contenedor con `source /opt/ros/humble/setup.bash && source /root/robot_ws/install/setup.bash`

El workspace está en `/root/robot_ws` dentro del contenedor, que corresponde a `~/robot_ws` en el Mac del usuario.

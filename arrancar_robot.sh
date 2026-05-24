#!/bin/bash
echo "🤖 Arrancando entorno robótico..."

# Abrir XQuartz
open -a XQuartz
sleep 2
xhost +localhost

# Arrancar contenedor si no está corriendo
docker start ros2_humble 2>/dev/null

# Terminal 1 - Brazo
osascript -e 'tell app "Terminal" to do script "docker exec -it ros2_humble bash -c \"source /opt/ros/humble/setup.bash && source /root/robot_ws/install/setup.bash && ros2 launch moveit_resources_panda_moveit_config demo.launch.py\""'

sleep 3

# Terminal 2 - Foxglove bridge
osascript -e 'tell app "Terminal" to do script "docker exec -it ros2_humble bash -c \"source /opt/ros/humble/setup.bash && ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765\""'

sleep 2

# Terminal 3 - Servidor meshes
osascript -e 'tell app "Terminal" to do script "docker exec -it ros2_humble bash -c \"cd /root/robot_ws/install/moveit_resources_panda_description/share/moveit_resources_panda_description/ && python3 -m http.server 8080\""'

echo "✅ Todo arrancado. Conecta Foxglove a ws://localhost:8765"
echo "📐 URDF: http://localhost:8080/urdf/panda_web.urdf"
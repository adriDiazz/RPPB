#!/bin/bash
echo "Arrancando entorno robotico completo..."

# Arrancar contenedor si no esta corriendo
docker start ros2_humble 2>/dev/null
sleep 2

# Matar procesos anteriores que puedan ocupar puertos
docker exec ros2_humble bash -c "pkill -f foxglove_bridge 2>/dev/null; pkill -f 'http.server' 2>/dev/null; pkill -f parameter_bridge 2>/dev/null; pkill -f 'ign gazebo' 2>/dev/null; pkill Xvfb 2>/dev/null; pkill x11vnc 2>/dev/null; pkill websockify 2>/dev/null; sleep 1" 2>/dev/null

# Terminal 1 - Brazo Panda (MoveIt2)
osascript -e 'tell app "Terminal" to do script "echo \"[1/5] Brazo Panda (MoveIt2)\" && docker exec -it ros2_humble bash -c \"source /opt/ros/humble/setup.bash && source /root/robot_ws/install/setup.bash && ros2 launch moveit_resources_panda_moveit_config demo.launch.py\""'

sleep 3

# Terminal 2 - Foxglove bridge
osascript -e 'tell app "Terminal" to do script "echo \"[2/5] Foxglove Bridge\" && docker exec -it ros2_humble bash -c \"source /opt/ros/humble/setup.bash && ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765\""'

sleep 2

# Terminal 3 - Servidor HTTP de meshes del Panda
osascript -e 'tell app "Terminal" to do script "echo \"[3/5] Servidor meshes HTTP\" && docker exec -it ros2_humble bash -c \"cd /root/robot_ws/install/moveit_resources_panda_description/share/moveit_resources_panda_description/ && python3 -m http.server 8080\""'

sleep 2

# Terminal 4 - Gazebo servidor headless + VNC para ver la GUI
osascript -e 'tell app "Terminal" to do script "echo \"[4/5] Gazebo servidor\" && docker exec -it ros2_humble bash -c \"Xvfb :99 -screen 0 1280x1024x24 & sleep 1 && x11vnc -display :99 -nopw -listen 0.0.0.0 -xkb -forever -shared -bg -o /tmp/x11vnc.log 2>/dev/null; websockify --web /usr/share/novnc 6080 localhost:5900 & sleep 1 && DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ign gazebo -r -s /root/robot_ws/worlds/camara_robot.sdf\""'

sleep 5

# Terminal 5 - Bridge camara Ignition -> ROS 2
osascript -e 'tell app "Terminal" to do script "echo \"[5/5] Bridge camara Ignition->ROS2\" && docker exec -it ros2_humble bash -c \"source /opt/ros/humble/setup.bash && ros2 run ros_gz_bridge parameter_bridge /camara/image@sensor_msgs/msg/Image[ignition.msgs.Image --ros-args -r /camara/image:=/camera/image_raw\""'

echo ""
echo "Todo arrancado. Servicios disponibles:"
echo ""
echo "  Foxglove Studio  -> ws://localhost:8765"
echo "  URDF meshes      -> http://localhost:8080/urdf/panda_web.urdf"
echo "  Camara en Foxglove -> panel Image -> /camera/image_raw"
echo ""

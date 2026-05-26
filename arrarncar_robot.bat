@echo off
echo Arrancando entorno robotico completo...

docker start ros2_humble
timeout /t 2 /nobreak

start cmd /k docker exec -it ros2_humble bash -c "source /opt/ros/humble/setup.bash && source /root/robot_ws/install/setup.bash && ros2 launch moveit_resources_panda_moveit_config demo.launch.py"
timeout /t 3 /nobreak

start cmd /k docker exec -it ros2_humble bash -c "source /opt/ros/humble/setup.bash && ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765"
timeout /t 2 /nobreak

start cmd /k docker exec -it ros2_humble bash -c "cd /root/robot_ws/install/moveit_resources_panda_description/share/moveit_resources_panda_description/ && python3 -m http.server 8080"
timeout /t 2 /nobreak

start cmd /k docker exec -it ros2_humble bash -c "pkill Xvfb 2>/dev/null; pkill x11vnc 2>/dev/null; pkill websockify 2>/dev/null; Xvfb :99 -screen 0 1280x1024x24 & sleep 2 && x11vnc -display :99 -nopw -listen 0.0.0.0 -xkb -forever -shared -bg && websockify --web /usr/share/novnc 6080 localhost:5900 & sleep 1 && DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 ign gazebo /root/robot_ws/worlds/worlds/camara_robot.sdf"
timeout /t 5 /nobreak

start cmd /k docker exec -it ros2_humble bash -c "source /opt/ros/humble/setup.bash && ros2 run ros_gz_bridge parameter_bridge /camara/image@sensor_msgs/msg/Image[ignition.msgs.Image --ros-args -r /camara/image:=/camera/image_raw"

echo.
echo Todo arrancado. Servicios disponibles:
echo   Foxglove Studio  -^> ws://localhost:8765
echo   URDF meshes      -^> http://localhost:8080/urdf/panda_web.urdf
echo   Gazebo (VNC)     -^> http://localhost:6080/vnc.html
echo   Camara topic     -^> /camera/image_raw
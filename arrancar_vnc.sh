#!/bin/bash
# Levanta display virtual + VNC + noVNC para ver Gazebo desde el navegador

echo "=== Arrancando display virtual (Xvfb) ==="
pkill Xvfb 2>/dev/null
pkill x11vnc 2>/dev/null
pkill websockify 2>/dev/null

Xvfb :99 -screen 0 1280x1024x24 &
sleep 2

echo "=== Arrancando servidor VNC ==="
x11vnc -display :99 -nopw -listen 0.0.0.0 -xkb -forever -shared -bg -o /tmp/x11vnc.log

echo "=== Arrancando noVNC (navegador web) ==="
websockify --web /usr/share/novnc 6080 localhost:5900 &

echo ""
echo "✓ Listo. Abre en el navegador del Mac:"
echo "  http://localhost:6080/vnc.html"
echo ""
echo "=== Lanzando Gazebo ==="
export DISPLAY=:99
export LIBGL_ALWAYS_SOFTWARE=1
ign gazebo /root/robot_ws/worlds/camara_robot.sdf

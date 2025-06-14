#!/bin/bash

# Start VNC server
echo "🚀 Starting VNC Server..."
vncserver :1 -geometry $VNC_RESOLUTION -depth 24 -localhost no

# Start noVNC
echo "🌐 Starting noVNC..."
websockify --web=/usr/share/novnc/ $NOVNC_PORT localhost:$((5900 + 1)) &

# Start desktop environment
echo "🖥️ Starting Xfce Desktop..."
export DISPLAY=:1
xfce4-session &

echo "✅ GUI Environment Ready!"
echo "🔗 noVNC: http://localhost:6080"
echo "🔗 VNC: localhost:5901"
echo "🔑 Password: $VNC_PW"

# Keep container running
tail -f /dev/null

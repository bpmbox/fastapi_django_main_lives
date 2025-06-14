FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install Docker-in-Docker
RUN curl -fsSL https://get.docker.com | sh

# Note: Node.js is installed via devcontainer features in devcontainer.json

# Install GUI dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    # VNC & GUI
    tigervnc-standalone-server \
    tigervnc-common \
    tigervnc-xorg-extension \
    dbus-x11 \
    # Desktop Environment  
    xfce4 \
    xfce4-goodies \
    # noVNC
    novnc \
    websockify \
    # Browser & Tools
    firefox-esr \
    chromium \
    # Utilities
    x11-apps \
    x11-utils \
    x11vnc \
    xvfb \
    && apt-get autoremove -y && apt-get clean -y

# Install Python dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Install Playwright browsers
RUN pip install playwright \
    && playwright install \
    && playwright install-deps

# Setup VNC
RUN mkdir -p /home/vscode/.vnc \
    && echo "copilot123" | vncpasswd -f > /home/vscode/.vnc/passwd \
    && chmod 600 /home/vscode/.vnc/passwd \
    && chown -R vscode:vscode /home/vscode/.vnc

# Setup noVNC
RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# VNC startup script
COPY .devcontainer/start-vnc.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-vnc.sh

# Environment
ENV DISPLAY=:1
ENV VNC_PORT=5900
ENV NOVNC_PORT=6080
ENV VNC_RESOLUTION=1920x1080
ENV VNC_PW=copilot123

USER vscode

# Xfce configuration
RUN mkdir -p /home/vscode/.config/xfce4/xfconf/xfce-perchannel-xml \
    && echo '<?xml version="1.0" encoding="UTF-8"?>\n<channel name="xfce4-desktop" version="1.0">\n  <property name="backdrop" type="empty">\n    <property name="screen0" type="empty">\n      <property name="monitor0" type="empty">\n        <property name="workspace0" type="empty">\n          <property name="color-style" type="int" value="0"/>\n          <property name="image-style" type="int" value="5"/>\n          <property name="last-image" type="string" value=""/>\n        </property>\n      </property>\n    </property>\n  </property>\n</channel>' > /home/vscode/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml

EXPOSE 5900 6080

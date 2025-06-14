#!/bin/bash

# VS Code インストールスクリプト
echo "🚀 VS Codeのインストールを開始します..."

# Microsoft GPGキーを追加
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/packages.microsoft.gpg

# VS Codeリポジトリを追加
echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list

# パッケージリストを更新
apt-get update

# VS Codeをインストール
apt-get install -y code

# 日本語フォントをインストール
apt-get install -y fonts-noto-cjk fonts-takao

# デスクトップディレクトリを作成
mkdir -p /home/ubuntu/Desktop

# VS Codeデスクトップアイコンを作成
cat > /home/ubuntu/Desktop/vscode.desktop << 'EOF'
[Desktop Entry]
Name=Visual Studio Code
Comment=Code Editing. Redefined.
GenericName=Text Editor
Exec=/usr/bin/code --no-sandbox --unity-launch %F
Icon=visual-studio-code
Type=Application
StartupNotify=true
StartupWMClass=Code
Categories=TextEditor;Development;IDE;
MimeType=text/plain;inode/directory;application/x-code-workspace;
Actions=new-empty-window;
Keywords=vscode;

[Desktop Action new-empty-window]
Name=New Empty Window
Exec=/usr/bin/code --no-sandbox --new-window %F
Icon=visual-studio-code
EOF

# デスクトップアイコンに実行権限を付与
chmod +x /home/ubuntu/Desktop/vscode.desktop
chown ubuntu:ubuntu /home/ubuntu/Desktop/vscode.desktop

# ターミナルアイコンも作成
cat > /home/ubuntu/Desktop/terminal.desktop << 'EOF'
[Desktop Entry]
Name=Terminal
Comment=Use the command line
TryExec=lxterminal
Exec=lxterminal
Icon=utilities-terminal
Type=Application
Categories=GTK;System;TerminalEmulator;
StartupNotify=true
EOF

chmod +x /home/ubuntu/Desktop/terminal.desktop
chown ubuntu:ubuntu /home/ubuntu/Desktop/terminal.desktop

echo "✅ VS Codeのインストールが完了しました！"

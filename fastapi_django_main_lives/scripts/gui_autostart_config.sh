# AI GUI Desktop Auto-Startup Configuration
# Place this file in your user's .bashrc or .profile for auto-startup

# Uncomment the following lines to enable GUI auto-startup on terminal launch
# if [ -z "$GUI_AUTOSTART_DISABLED" ] && [ -f "/workspaces/fastapi_django_main_lives/scripts/start_gui_auto.sh" ]; then
#     echo "🚀 Auto-starting AI GUI Desktop Environment..."
#     /workspaces/fastapi_django_main_lives/scripts/start_gui_auto.sh
# fi

# To disable auto-startup, set this environment variable:
# export GUI_AUTOSTART_DISABLED=1

# Quick aliases for GUI management
alias gui-start='make -C /workspaces/fastapi_django_main_lives gui-auto'
alias gui-stop='make -C /workspaces/fastapi_django_main_lives gui-stop'
alias gui-restart='make -C /workspaces/fastapi_django_main_lives gui-restart'
alias gui-logs='make -C /workspaces/fastapi_django_main_lives gui-logs'

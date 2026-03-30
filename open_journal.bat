@echo off
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
python "%PROJECT_ROOT%\.dev-tools\_app-journal\launch_ui.py" --project-root "%PROJECT_ROOT%"

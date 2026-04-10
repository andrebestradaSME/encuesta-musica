@echo off
chcp 65001 >nul
title Sound Survey

:: ╔══════════════════════════════════════╗
:: ║   SOUND SURVEY — Iniciar en Windows  ║
:: ╚══════════════════════════════════════╝

:: Ir a la carpeta donde está este archivo
cd /d "%~dp0"

set PORT=8080

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python no está instalado.
    echo  Descárgalo de https://python.org
    echo  Activa la opción "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b 1
)

:: Matar proceso previo en el puerto
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%PORT%"') do (
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 1 /nobreak >nul

:: Obtener IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /r "IPv4.*192\."') do (
    set LOCAL_IP=%%a
    set LOCAL_IP=!LOCAL_IP: =!
)

echo.
echo  ╔══════════════════════════════════════╗
echo  ║        SOUND SURVEY — Live           ║
echo  ╚══════════════════════════════════════╝
echo.
echo  Abre en tu navegador:
echo.
echo    Este equipo:   http://localhost:%PORT%
echo    Red local:     http://%LOCAL_IP%:%PORT%
echo.
echo  Contraseña: 444
echo.
echo  Presiona Ctrl+C para detener.
echo  ─────────────────────────────────────────
echo.

:: Abrir navegador después de 2 segundos
start "" /min cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:%PORT%"

:: Iniciar servidor
python server.py

pause

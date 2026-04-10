#!/bin/bash

# ╔══════════════════════════════════════╗
# ║   SOUND SURVEY — Iniciar en Mac      ║
# ╚══════════════════════════════════════╝

# Ir a la carpeta donde está este archivo
cd "$(dirname "$0")"

# Puerto
PORT=8080

# Verificar que Python3 esté instalado
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python no encontrado" message "Instala Python 3 desde python.org para continuar." as critical'
    exit 1
fi

# Matar cualquier proceso previo en el mismo puerto
lsof -ti:$PORT | xargs kill -9 2>/dev/null
sleep 0.5

# Obtener IP local
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

# Mostrar notificación
osascript -e "display notification \"Abriendo en http://localhost:$PORT\" with title \"Sound Survey\" subtitle \"IP red local: http://$LOCAL_IP:$PORT\""

# Abrir el navegador después de 1.5 segundos
(sleep 1.5 && open "http://localhost:$PORT") &

# Iniciar servidor Python
python3 server.py


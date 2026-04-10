#!/usr/bin/env python3
"""
SOUND SURVEY — Servidor Local
==============================
No necesitas usar este archivo directamente.
Haz doble clic en:
  • INICIAR_MAC.command     (en Mac)
  • INICIAR_WINDOWS.bat     (en Windows)
"""

import http.server
import socketserver
import os
import json
import socket
import threading
import time
import webbrowser
from pathlib import Path

PORT = 8080
BASE_DIR = Path(__file__).parent.resolve()
AUDIO_EXTENSIONS = {'.wav', '.mp3', '.aac', '.flac', '.ogg', '.m4a'}


class SurveyHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        # Bloquear acceso fuera del proyecto
        try:
            full_path = (BASE_DIR / path.lstrip('/')).resolve()
            full_path.relative_to(BASE_DIR)
        except ValueError:
            self.send_error(403, "Acceso denegado")
            return
        # Bloquear server.py
        if path.endswith('server.py'):
            self.send_error(403, "Acceso denegado")
            return
        super().do_GET()

    def guess_type(self, path):
        ext = Path(str(path)).suffix.lower()
        mime_types = {
            '.wav':  'audio/wav',
            '.mp3':  'audio/mpeg',
            '.aac':  'audio/aac',
            '.flac': 'audio/flac',
            '.ogg':  'audio/ogg',
            '.m4a':  'audio/mp4',
        }
        if ext in mime_types:
            return mime_types[ext]
        return super().guess_type(path)

    def log_message(self, format, *args):
        # Silenciar logs — los audios son confidenciales
        ext = Path(self.path.split('?')[0]).suffix.lower()
        if ext not in AUDIO_EXTENSIONS:
            pass  # silencio total


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


def open_browser(port, delay=1.5):
    """Abre el navegador después de un delay."""
    def _open():
        time.sleep(delay)
        webbrowser.open(f"http://localhost:{port}")
    t = threading.Thread(target=_open, daemon=True)
    t.start()


def check_tracks():
    """Verifica que los tracks tengan audio."""
    if not (BASE_DIR / 'tracks.json').exists():
        return [], 0, 0

    with open(BASE_DIR / 'tracks.json') as f:
        tracks = json.load(f)

    ok = 0
    missing = 0

    # Check general intro
    if (BASE_DIR / 'audio' / 'intro_general.wav').exists():
        ok += 1
    else:
        missing += 1

    for track in tracks:
        # Check track intro
        intro = track.get('intro', '')
        if intro:
            if (BASE_DIR / intro).exists():
                ok += 1
            else:
                missing += 1
        # Check fragments
        for frag in track.get('fragmentos', []):
            if not frag:
                continue
            if (BASE_DIR / frag).exists():
                ok += 1
            else:
                missing += 1
    return tracks, ok, missing


if __name__ == '__main__':
    local_ip = get_local_ip()
    tracks, ok, missing = check_tracks()

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║        SOUND SURVEY — Live           ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    print(f"  🟢 Servidor activo:")
    print(f"     Este equipo →  http://localhost:{PORT}")
    print(f"     Red local   →  http://{local_ip}:{PORT}")
    print()
    print(f"  🔒 Contraseña: 444")
    print()

    if missing > 0:
        print(f"  ⚠  {missing} fragmentos de audio no encontrados")
        print(f"     Asegúrate de tener los WAV en las carpetas /audio/trackXX/")
        print()
    elif ok > 0:
        print(f"  ✓  {ok} fragmentos de audio listos")
        print()

    print("  Abriendo navegador...")
    print("  Presiona Ctrl+C para detener.")
    print()

    # Abrir navegador automáticamente
    open_browser(PORT, delay=1.5)

    with socketserver.TCPServer(("", PORT), SurveyHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print()
            print("  Servidor detenido. ¡Hasta luego!")
            print()

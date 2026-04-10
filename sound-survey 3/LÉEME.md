# SOUND SURVEY

## Cómo iniciar

**En Mac:**
→ Doble clic en `INICIAR_MAC.command`

Si Mac dice "no se puede abrir porque es de un desarrollador no identificado":
→ Clic derecho → Abrir → Abrir de todas formas
(solo la primera vez)

**En Windows:**
→ Doble clic en `INICIAR_WINDOWS.bat`

---

El navegador se abre solo en http://localhost:8080
Contraseña: **444**

Para compartir con alguien en tu misma red WiFi:
→ Dales la URL http://[IP que aparece en pantalla]:8080

Para detener: cierra la ventana negra / terminal.

---

## Agregar los audios

Coloca tus archivos WAV en las carpetas:
```
audio/intro_general.wav              ← audio general de instrucciones
audio/track01/intro.wav              ← presentación del track 01
audio/track01/fragmento_a.wav
audio/track01/fragmento_b.wav
audio/track02/intro.wav              ← presentación del track 02
audio/track02/fragmento_a.wav
audio/track02/fragmento_b.wav
```

Edita `tracks.json` para cambiar los nombres de los tracks.

---

## Requisitos

- Python 3 instalado
  - Mac: ya viene incluido. Si no, escribe `python3` en Terminal.
  - Windows: descargar de python.org → activar "Add to PATH"

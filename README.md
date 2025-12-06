# 🎮 Camera Vision - Control por Gestos con MediaPipe

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-success?style=flat-square)
![Arduino](https://img.shields.io/badge/Arduino-UNO-00979D?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**Sistema de control de dispositivos mediante reconocimiento de gestos de mano en tiempo real.** Utiliza inteligencia artificial (MediaPipe Hands) para detectar y clasificar gestos, controlando LEDs y dispositivos mediante Arduino de forma inalámbrica.

## ✨ Características

- **🤖 Detección de manos con IA** - MediaPipe Hands con precisión de 99%
- **🖐️ 6 gestos multimodales** - Reconoce desde puño cerrado (0 dedos) hasta mano abierta (5 dedos)
- **💡 Control de hasta 4 LEDs/relés** - Conexión directa con Arduino UNO
- **📷 Interfaz visual en tiempo real** - Visualización de landmarks y gestos detectados
- **🔗 Comunicación serial bidireccional** - Protocolo robusto Python ↔ Arduino
- **⚡ Baja latencia** - Procesamiento < 300ms por frame
- **🎯 Configuración flexible** - Parámetros ajustables mediante JSON

## 📋 Requisitos del Sistema

### Hardware Requerido

| Componente | Especificación | Cantidad |
|-----------|----------------|----------|
| **Arduino** | Arduino UNO R3 | 1 |
| **Cámara** | Webcam USB (640x480 mín.) | 1 |
| **LEDs** | LED 3-5mm (cualquier color) | 4 |
| **Resistencias** | 220Ω ±5% | 4 |
| **Relés** | Módulo de relés 4-canales (opcional) | 1 |
| **Cable USB** | Arduino ↔ PC | 1 |
| **Protoboard** | Estándar 830 puntos | 1 |
| **Cables de conexión** | Macho/Hembra | ~20 |

### Software Requerido

| Software | Versión | Notas |
|----------|---------|-------|
| **Python** | 3.10.x | Requerido. No compatible con 3.11+ |
| **MediaPipe** | 0.10.14 | Reconocimiento de manos |
| **OpenCV** | 4.8.1.78 | Captura y procesamiento de video |
| **PySerial** | 3.5 | Comunicación con Arduino |
| **Arduino IDE** | 2.0+ | Para cargar sketch en Arduino |

### Requisitos del Sistema Operativo

- **Windows 10/11** con PowerShell 5.1+, o
- **Linux** (Ubuntu 20.04+), o
- **macOS** 11+
- Acceso a puertos USB
- 4GB RAM mínimo, 8GB recomendado

## 🚀 Guía de Instalación

### Paso 1️⃣: Clonar el Repositorio

```bash
git clone https://github.com/PALOESPINOSA/camera_vision.git
cd camera_vision
```

### Paso 2️⃣: Configurar Entorno Python 3.10

Es **crítico** usar Python 3.10 exactamente. MediaPipe no es compatible con versiones posteriores.

#### Opción A: Usar `uv` (Recomendado - Más rápido)

```powershell
# Crear entorno virtual con Python 3.10.19
uv venv --python 3.10.19

# Activar entorno (Windows PowerShell)
.venv\Scripts\activate.ps1

# En caso de error de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Opción B: Usar `venv` (Alternativa)

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows PowerShell)
.venv\Scripts\activate.ps1

# En Linux/Mac
source .venv/bin/activate
```

### Paso 3️⃣: Instalar Dependencias del Proyecto

```bash
# Instalar el paquete en modo desarrollo
uv pip install -e .

# O con pip estándar
pip install -e .
```

Esto instalará automáticamente:
- opencv-python (4.8.1.78)
- mediapipe (0.10.14)
- pyserial (3.5)
- numpy (1.24.3)

### Paso 4️⃣: Configurar y Cargar Firmware en Arduino

#### Carga del Código Arduino

1. Conectar Arduino UNO al PC mediante cable USB
2. Abrir **Arduino IDE** (v2.0 o superior)
3. Ir a **Archivo** → **Abrir** → Seleccionar `arduino/led_control.ino`
4. Configurar placa y puerto:
   - **Herramientas** → **Placa** → Seleccionar **Arduino UNO**
   - **Herramientas** → **Puerto** → Seleccionar **COM3** (o el puerto disponible)
   
   > **💡 Nota:** En Windows, verificar el puerto en Administrador de dispositivos → Puertos COM

5. Hacer clic en **Subir** (botón con flecha →)
6. Esperar confirmación: "Subido exitosamente"

### Paso 5️⃣: Conexiones Eléctricas en la Protoboard

```
Arduino UNO Pins → Protoboard
┌─────────────────────────────────────┐
│ Pin Digital 2 → LED 1 (Rojo)        │
│ Pin Digital 3 → LED 2 (Amarillo)    │
│ Pin Digital 4 → LED 3 (Verde)       │
│ Pin Digital 5 → LED 4 (Azul)        │
│ Pin GND       → Riel negativo        │
└─────────────────────────────────────┘

Para cada LED:
LED Ánodo (+) → Arduino Pin digital
LED Cátodo (-) → Resistor 220Ω → Riel negativo (GND)
```

**Diagrama de conexión:**

```
Arduino             Protoboard              LEDs
═══════             ══════════              ════
 Pin 2  ─────────→  LED1 Ánodo ──[220Ω]──→ GND
 Pin 3  ─────────→  LED2 Ánodo ──[220Ω]──→ GND
 Pin 4  ─────────→  LED3 Ánodo ──[220Ω]──→ GND
 Pin 5  ─────────→  LED4 Ánodo ──[220Ω]──→ GND
 GND    ─────────→  Riel negativo
```

### Paso 6️⃣: Configurar Parámetros de la Aplicación

Editar `config/settings.json`:

```json
{
    "camera_index": 1,           // 0=Cámara integrada, 1=Cámara USB
    "camera_width": 640,         // Ancho de captura (px)
    "camera_height": 480,        // Alto de captura (px)
    "arduino_port": "COM3",      // Puerto serial (verificar en Dispositivos)
    "arduino_baudrate": 9600,    // Velocidad de comunicación (no cambiar)
    "gesture_delay": 0.3         // Retraso entre gestos (segundos)
}
```

**Parámetros recomendados por escenario:**

| Escenario | camera_index | gesture_delay | Notas |
|-----------|------------|--------------|-------|
| Laptop integrada | 0 | 0.5 | Más estable |
| USB externa | 1 | 0.3 | Más rápida |
| Producción | 1 | 0.2 | Máxima responsividad |
| Bajo rendimiento | 0 | 1.0 | PC lento |


## 🎮 Cómo Usar la Aplicación

### Ejecutar el Sistema

Una vez configurado, ejecutar:

```bash
python src/main.py
```

La aplicación abrirá una ventana con:
- **Visualización en vivo** de la cámara
- **Landmarks de mano** detectados por MediaPipe
- **Gestos reconocidos** con porcentaje de confianza
- **Estado de LEDs** indicado en tiempo real

### Tabla de Gestos Soportados

| Gesto | Dedos | Acción | LEDs | Emoji |
|-------|-------|--------|------|-------|
| **Puño cerrado** | 0 | Apagar todo | Todos OFF | ✊ |
| **Índice solo** | 1 | Activar LED 1 | LED1 ON | ☝️ |
| **Índice + Mayor** | 2 | Activar LED 2 | LED2 ON | ✌️ |
| **3 dedos** | 3 | Activar LED 3 | LED3 ON | 🤟 |
| **4 dedos** | 4 | Activar LED 4 | LED4 ON | 🖖 |
| **Mano abierta** | 5 | Activar todo | Todos ON | 🖐️ |

### Controles en Pantalla

| Tecla | Función |
|-------|---------|
| **Q** o **ESC** | Salir de la aplicación |
| **C** | Limpiar historial de gestos (opcional) |
| **Espacio** | Pausar/Reanudar captura (opcional) |

### Interfaz Visual Explicada

```
┌─────────────────────────────────────────────┐
│ Camera Vision - Control por Gestos          │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │   [Video Feed con landmarks]        │   │
│  │   ·                                 │   │
│  │    · ····  (puntos de mano)        │   │
│  │   ··· ····                          │   │
│  │                                     │   │
│  │   Gesto detectado: ✌️ (2 dedos)   │   │
│  │   Confianza: 94%                    │   │
│  │   LED Status: [🟢🔴🟢🔴]            │   │
│  │                                     │   │
│  │   Presiona Q para salir              │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

## 🔧 Configuración Avanzada

### Ajustar Sensibilidad de Detección

En `src/main.py`, modificar los valores en la clase `GestureControl.__init__()`:

```python
self.hands = self.mp_hands.Hands(
    max_num_hands=1,              # Máximo 1 mano a la vez
    min_detection_confidence=0.7, # 0.0-1.0: Qué tan segura es la detección
    min_tracking_confidence=0.7   # 0.0-1.0: Consistencia del tracking
)
```

**Guía de valores:**
- `0.5` - Detección muy sensible (falsos positivos comunes)
- `0.7` - Equilibrio recomendado (valor actual)
- `0.9` - Muy exigente (requiere posición perfecta)

### Cambiar Velocidad de Comunicación Serial

En `config/settings.json`, modificar `arduino_baudrate`:

```json
{
    "arduino_baudrate": 9600    // Opciones: 9600, 14400, 19200, 38400, 57600, 115200
}
```

> **Nota:** El Arduino está configurado para 9600 baud. Si lo cambias aquí, también debes cambiar en `led_control.ino` la línea `Serial.begin(9600)` al mismo valor.

## 🐛 Solución de Problemas Común

## 🔧 Personalización y Extensiones

### Cambiar Pines de Arduino

Editar `arduino/led_control.ino`:

```cpp
const int LED_PINS[LED_COUNT] = {2, 3, 4, 5};  // Cambiar números de pines
```

### Controlar Relés en lugar de LEDs

Para módulos de relés (típicamente activos en bajo):

```cpp
// En led_control.ino, modificar:
digitalWrite(LED_PINS[i], LOW);   // Encender relé
digitalWrite(LED_PINS[i], HIGH);  // Apagar relé
```

### Agregar Más Dispositivos

1. Agregar pines en `LED_PINS[]`
2. Actualizar `LED_COUNT`
3. Modificar tabla de gestos o agregar nueva lógica en `processCommand()`

## 📁 Estructura Completa del Proyecto

```
camera_vision/
├── README.md                           # Documentación (este archivo)
├── LICENSE                             # Licencia MIT
├── pyproject.toml                      # Configuración del paquete
├── .gitignore                          # Archivos ignorados
│
├── config/
│   └── settings.json                   # Parámetros configurables
│
├── src/
│   ├── main.py                         # Script principal Python
│   └── camera_vision.egg-info/         # Información de instalación
│       ├── PKG-INFO
│       ├── SOURCES.txt
│       ├── requires.txt
│       ├── top_level.txt
│       └── dependency_links.txt
│
└── arduino/
    ├── led_control.ino                 # Firmware principal (✓ Usar)
    └── gesture_control.ino             # Firmware alterno (no usado)
```

## 🧪 Checklist de Verificación

Antes de reportar problemas, verificar:

- [ ] Python 3.10.x instalado (`python --version`)
- [ ] Todas las dependencias instaladas (`pip list | findstr mediapipe`)
- [ ] Arduino conectado y detectado (`Administrador de dispositivos`)
- [ ] `led_control.ino` subido exitosamente a Arduino
- [ ] LEDs conectados en pines 2-5 con resistencias 220Ω
- [ ] `config/settings.json` con puerto correcto
- [ ] Entorno virtual activado antes de ejecutar

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | ~300 |
| **Dependencias** | 4 principales |
| **Pines Arduino usados** | 5 (4 + GND) |
| **Gestos disponibles** | 6 (0-5) |
| **Compatibilidad SO** | Windows / Linux / macOS |
| **Python requerido** | 3.10.x exacto |

## 🎓 Conceptos Técnicos

### MediaPipe Hands

MediaPipe Hands utiliza una red neuronal convolucional (CNN) para detectar 21 landmarks en la mano:

```
Puntos clave de la mano (MediaPipe):
0: Muñeca
1-4: Pulgar
5-8: Índice
9-12: Mayor
13-16: Anular
17-20: Meñique
```

Este proyecto calcula cuántos dedos están extendidos comparando las posiciones Y de los landmarks.

### Protocolo Serial Arduino

Comunicación unidireccional Python → Arduino:
- **Baud Rate:** 9600 bps
- **Data bits:** 8
- **Stop bits:** 1
- **Parity:** None
- **Comandos:** Dígito simple (0-5) + newline

## 🔮 Futuras Mejoras Potenciales

- [ ] Interfaz gráfica mejorada (PyQt/Tkinter)
- [ ] Grabación de gestos personalizados
- [ ] Integración con Home Automation (MQTT)
- [ ] Soporte para dos manos
- [ ] Reconocimiento de gestos dinámicos
- [ ] Logging y estadísticas
- [ ] Calibración automática de cámara

## 📞 Soporte y Contacto

**GitHub Issues:** [Reportar problemas](https://github.com/PALOESPINOSA/camera_vision/issues)

**Autor:** PALOESPINOSA  
**Repositorio:** https://github.com/PALOESPINOSA/camera_vision

## 📄 Licencia y Atribuciones

**Licencia:** MIT License

**Créditos:**
- 🤖 **Google MediaPipe** - Librería de detección de manos
- 📷 **OpenCV** - Procesamiento de video
- 🔌 **Arduino** - Plataforma de hardware
- 🐍 **Python** - Lenguaje de programación

---

**Versión:** 0.1.0  
**Última actualización:** Diciembre 2025  
**Estado:** ✅ Funcional y mantenido  
**Contribuciones:** ¡Bienvenidas!
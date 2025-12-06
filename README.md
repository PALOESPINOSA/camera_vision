# 🎮 Control por Gestos - MediaPipe + Arduino

Sistema completo de control de dispositivos mediante gestos de mano. Detecta dedos con MediaPipe y controla LEDs/relés mediante Arduino.

## ✨ Características

- **🤖 Detección precisa** con MediaPipe Hands
- **🖐️ 6 gestos reconocidos** (0-5 dedos)
- **💡 Control de 4 LEDs/relés** mediante Arduino
- **📷 Interfaz visual en tiempo real**
- **🔗 Comunicación serial** Python → Arduino
- **⚡ Baja latencia** (< 300ms)
- **🎯 Fácil calibración** automática

## 📋 Requisitos

### Hardware
- Cámara web USB
- Arduino UNO
- 4 LEDs + resistencias 220Ω
- Protoboard y cables
- (Opcional) Módulo de 4 relés para control de dispositivos

### Software
- Python 3.10.x (obligatorio para MediaPipe)
- MediaPipe 0.10.14
- OpenCV 4.8.1.78
- PySerial 3.5
- Arduino IDE (para subir código al Arduino)

## 🚀 Instalación Rápida

### 1. Clonar repositorio
```bash
git clone https://github.com/tuusuario/camera_vision.git
cd camera_vision
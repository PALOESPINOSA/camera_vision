"""
Sistema de control por gestos con MediaPipe.
Basado en las capturas originales, adaptado para Arduino.
"""
import cv2
import mediapipe as mp
import serial
import time
import json
from pathlib import Path
import sys

class GestureControl:
    def __init__(self, config_path="config/settings.json"):
        self.config = self.load_config(config_path)
        self.cap = None
        self.running = False
        
        # Inicializar MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Definir puntos de referencia para dedos (basado en tus capturas)
        self.finger_points = {
            "thumb": [2, 3, 4],      # Pulgar
            "index": [5, 6, 8],      # Índice
            "middle": [9, 10, 12],   # Mayor
            "ring": [13, 14, 16],    # Anular
            "pinky": [17, 18, 20]    # Meñique
        }
        
        # Inicializar comunicación Arduino (simulada por ahora)
        self.arduino = None
        
    def load_config(self, config_path):
        """Cargar configuración desde JSON."""
        default_config = {
            "camera_index": 0,
            "camera_width": 640,
            "camera_height": 480,
            "arduino_port": "COM3",
            "arduino_baudrate": 9600
        }
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
        except FileNotFoundError:
            print(f"Config no encontrada. Creando {config_path}")
            Path(config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def initialize_camera(self):
        """Inicializar cámara."""
        self.cap = cv2.VideoCapture(self.config["camera_index"])
        if not self.cap.isOpened():
            print(f"Error: No se puede abrir cámara {self.config['camera_index']}")
            return False
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config["camera_width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config["camera_height"])
        
        print(f"Cámara: {self.config['camera_width']}x{self.config['camera_height']}")
        return True
    
    def connect_arduino(self):
        """Conectar con Arduino."""
        try:
            self.arduino = serial.Serial(
                self.config["arduino_port"],
                self.config["arduino_baudrate"],
                timeout=1
            )
            time.sleep(2)  # Esperar inicialización
            print(f"Conectado a Arduino en {self.config['arduino_port']}")
            return True
        except serial.SerialException as e:
            print(f"Error conectando Arduino: {e}")
            self.arduino = None
            return False
    
    def detect_fingers(self, landmarks):
        """Detectar dedos extendidos (basado en tus capturas)."""
        if landmarks is None:
            return 0
        
        finger_count = 0
        
        # Coordenada Y de la base de la palma (landmark 0)
        palm_base_y = landmarks.landmark[0].y
        
        # Revisar cada dedo (excepto pulgar que tiene lógica diferente)
        for finger_name, points in self.finger_points.items():
            if finger_name == "thumb":
                # Lógica especial para pulgar (comparación en eje X)
                tip_x = landmarks.landmark[points[2]].x
                joint_x = landmarks.landmark[points[0]].x
                
                if tip_x < joint_x:  # Pulgar extendido (a la izquierda)
                    finger_count += 1
            else:
                # Para los otros 4 dedos: comparar Y de punta con Y de articulación
                tip_y = landmarks.landmark[points[2]].y
                joint_y = landmarks.landmark[points[0]].y
                
                if tip_y < joint_y:  # Dedo extendido (punta más arriba que articulación)
                    finger_count += 1
        
        return finger_count
    
    def send_to_arduino(self, finger_count):
        """Enviar comando a Arduino basado en dedos detectados."""
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(f"{finger_count}\n".encode())
                print(f"Enviado a Arduino: {finger_count} dedos")
            except Exception as e:
                print(f"Error enviando a Arduino: {e}")
        else:
            # Simular comando si no hay Arduino conectado
            commands = {
                0: "Apagar todos los reles",
                1: "Rele 1 ON",
                2: "Rele 2 ON",
                3: "Rele 3 ON",
                4: "Rele 4 ON",
                5: "Encender todos los reles"
            }
            if finger_count in commands:
                print(f"COMANDO ARDUINO (simulado): {commands[finger_count]}")
    
    def draw_info(self, frame, finger_count, landmarks=None):
        """Dibujar información en el frame."""
        # Información principal
        info_y = 30
        cv2.putText(frame, f"Dedos: {finger_count}", (10, info_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Nombre del gesto
        gestures = {
            0: "PUÑO - Apagar todo",
            1: "UNO - Rele 1",
            2: "DOS - Rele 2",
            3: "TRES - Rele 3",
            4: "CUATRO - Rele 4",
            5: "MANO ABIERTA - Encender todo"
        }
        gesture_name = gestures.get(finger_count, "Desconocido")
        cv2.putText(frame, f"Gesto: {gesture_name}", (10, info_y + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Leyenda de controles
        cv2.rectangle(frame, (10, 180), (300, 280), (50, 50, 50), -1)
        cv2.putText(frame, "CONTROLES:", (15, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "0 dedos (puño): APAGAR TODO", (15, 220), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 200, 255), 1)
        cv2.putText(frame, "5 dedos (mano abierta): ENCENDER TODO", (15, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        cv2.putText(frame, "1-4 dedos: Control individual Rele 1-4", (15, 260), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        
        # Dibujar landmarks de MediaPipe
        if landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
        
        return frame
    
    def run(self):
        """Bucle principal de ejecución."""
        if not self.initialize_camera():
            return
        
        # Intentar conectar Arduino (opcional)
        self.connect_arduino()
        
        self.running = True
        print("\n=== SISTEMA DE CONTROL POR GESTOS ===")
        print("Versión: MediaPipe + Python 3.10")
        print("=" * 40)
        print("\nControles:")
        print("• Mostrar 0 dedos (puño): Apagar todo")
        print("• Mostrar 5 dedos (mano abierta): Encender todo")
        print("• Mostrar 1-4 dedos: Controlar relé individual")
        print("• Presiona 'q' para salir")
        print("=" * 40)
        
        last_finger_count = -1
        last_time = time.time()
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error leyendo frame")
                break
            
            # Voltear horizontalmente para modo espejo
            frame = cv2.flip(frame, 1)
            
            # Convertir BGR a RGB (MediaPipe requiere RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Procesar con MediaPipe
            results = self.hands.process(rgb_frame)
            
            finger_count = 0
            landmarks = None
            
            if results.multi_hand_landmarks:
                # Tomar la primera mano detectada
                landmarks = results.multi_hand_landmarks[0]
                finger_count = self.detect_fingers(landmarks)
            
            # Dibujar información
            frame = self.draw_info(frame, finger_count, landmarks)
            
            # Mostrar frame
            cv2.imshow('Control por Gestos - MediaPipe', frame)
            
            # Manejar teclas
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
            
            # Enviar comando solo si cambia el conteo de dedos (cada 0.3 segundos)
            current_time = time.time()
            if current_time - last_time > 0.3 and finger_count != last_finger_count:
                self.send_to_arduino(finger_count)
                last_finger_count = finger_count
                last_time = current_time
        
        self.cleanup()
    
    def cleanup(self):
        """Limpiar recursos."""
        if self.cap:
            self.cap.release()
        
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        
        cv2.destroyAllWindows()
        print("\nSistema cerrado correctamente")


def main():
    """Función principal."""
    try:
        detector = GestureControl()
        detector.run()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

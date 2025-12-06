/*
  Control de 5 LEDs por gestos de mano
  Arduino UNO - Versión para LEDs
  
  Comandos seriales desde Python:
  0 - Apagar todos los LEDs
  1 - LED 1 ON
  2 - LED 2 ON  
  3 - LED 3 ON
  4 - LED 4 ON
  5 - Encender todos los LEDs
*/

const int LED_COUNT = 5;
const int LED_PINS[LED_COUNT] = {2, 3, 4, 5, 6}; // Pines para 5 LEDs

bool ledStates[LED_COUNT] = {false, false, false, false, false};
String inputString = "";
bool stringComplete = false;

void setup() {
  // Inicializar pines de LEDs como salida
  for (int i = 0; i < LED_COUNT; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW); // Apagar todos al inicio
  }
  
  // Inicializar comunicación serial
  Serial.begin(9600);
  while (!Serial) {
    ; // Esperar a que se conecte el puerto serial
  }
  
  Serial.println("SISTEMA DE CONTROL POR GESTOS - LEDs");
  Serial.println("===================================");
  Serial.println("Comandos recibidos de Python:");
  Serial.println("0: Apagar todos los LEDs");
  Serial.println("1: LED 1 ON");
  Serial.println("2: LED 2 ON");
  Serial.println("3: LED 3 ON");
  Serial.println("4: LED 4 ON");
  Serial.println("5: Encender todos los LEDs");
  Serial.println();
  
  // Secuencia de prueba inicial
  testSequence();
}

void loop() {
  // Leer comandos seriales
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      stringComplete = true;
    } else if (isDigit(inChar)) {
      inputString += inChar;
    }
  }
  
  // Procesar comando cuando esté completo
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void processCommand(String cmd) {
  if (cmd.length() == 0) return;
  
  int command = cmd.toInt();
  Serial.print("Comando recibido: ");
  Serial.println(command);
  
  switch(command) {
    case 0:
      // Apagar todos los LEDs
      for (int i = 0; i < LED_COUNT; i++) {
        ledStates[i] = false;
        digitalWrite(LED_PINS[i], LOW);
      }
      Serial.println("Accion: Todos los LEDs APAGADOS");
      break;
      
    case 5:
      // Encender todos los LEDs
      for (int i = 0; i < LED_COUNT; i++) {
        ledStates[i] = true;
        digitalWrite(LED_PINS[i], HIGH);
      }
      Serial.println("Accion: Todos los LEDs ENCENDIDOS");
      break;
      
    case 1:
    case 2:
    case 3:
    case 4:
      {
        int ledIndex = command - 1; // Convertir 1-4 a 0-3
        
        // Primero apagar todos
        for (int i = 0; i < LED_COUNT; i++) {
          ledStates[i] = false;
          digitalWrite(LED_PINS[i], LOW);
        }
        
        // Luego encender solo el seleccionado
        ledStates[ledIndex] = true;
        digitalWrite(LED_PINS[ledIndex], HIGH);
        
        Serial.print("Accion: LED ");
        Serial.print(command);
        Serial.println(" activado (otros apagados)");
      }
      break;
      
    default:
      Serial.println("Error: Comando no reconocido (0-5 solamente)");
      return;
  }
  
  // Mostrar estado actual
  showStatus();
}

void showStatus() {
  Serial.print("Estado LEDs: ");
  for (int i = 0; i < LED_COUNT; i++) {
    Serial.print(i + 1);
    Serial.print(":");
    Serial.print(ledStates[i] ? "ON " : "OFF ");
  }
  Serial.println();
  Serial.println("---");
}

void testSequence() {
  // Secuencia de prueba al iniciar
  Serial.println("Prueba de LEDs...");
  
  // Encender uno por uno
  for (int i = 0; i < LED_COUNT; i++) {
    digitalWrite(LED_PINS[i], HIGH);
    delay(300);
    digitalWrite(LED_PINS[i], LOW);
    delay(200);
  }
  
  // Encender todos brevemente
  for (int i = 0; i < LED_COUNT; i++) {
    digitalWrite(LED_PINS[i], HIGH);
  }
  delay(500);
  
  // Apagar todos
  for (int i = 0; i < LED_COUNT; i++) {
    digitalWrite(LED_PINS[i], LOW);
  }
  
  Serial.println("Prueba completada");
  Serial.println("Esperando comandos por gestos...");
  Serial.println();
}

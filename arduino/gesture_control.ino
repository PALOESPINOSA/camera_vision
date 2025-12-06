/*
  Control de relés por gestos de mano
  Comunicación serial con Python + MediaPipe
  
  Comandos:
  0 - Apagar todos los relés
  1 - Rele 1 ON
  2 - Rele 2 ON  
  3 - Rele 3 ON
  4 - Rele 4 ON
  5 - Encender todos los relés
*/

const int RELAY_COUNT = 4;
const int RELAY_PINS[RELAY_COUNT] = {2, 3, 4, 5};

bool relayStates[RELAY_COUNT] = {false, false, false, false};
String inputString = "";
bool stringComplete = false;

void setup() {
  // Inicializar pines de relé
  for (int i = 0; i < RELAY_COUNT; i++) {
    pinMode(RELAY_PINS[i], OUTPUT);
    digitalWrite(RELAY_PINS[i], HIGH); // HIGH = relé apagado (depende del módulo)
  }
  
  // Inicializar comunicación serial
  Serial.begin(9600);
  Serial.println("SISTEMA DE CONTROL POR GESTOS");
  Serial.println("=============================");
  Serial.println("Comandos recibidos de Python:");
  Serial.println("0: Apagar todos");
  Serial.println("1-4: Control individual");
  Serial.println("5: Encender todos");
  Serial.println();
  
  // Prueba inicial
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
      // Apagar todos los relés
      for (int i = 0; i < RELAY_COUNT; i++) {
        relayStates[i] = false;
        digitalWrite(RELAY_PINS[i], HIGH);
      }
      Serial.println("Accion: Todos los relés APAGADOS");
      break;
      
    case 5:
      // Encender todos los relés
      for (int i = 0; i < RELAY_COUNT; i++) {
        relayStates[i] = true;
        digitalWrite(RELAY_PINS[i], LOW);
      }
      Serial.println("Accion: Todos los relés ENCENDIDOS");
      break;
      
    case 1:
    case 2:
    case 3:
    case 4:
      {
        int relayIndex = command - 1; // Convertir 1-4 a 0-3
        
        // Primero apagar todos
        for (int i = 0; i < RELAY_COUNT; i++) {
          relayStates[i] = false;
          digitalWrite(RELAY_PINS[i], HIGH);
        }
        
        // Luego encender solo el seleccionado
        relayStates[relayIndex] = true;
        digitalWrite(RELAY_PINS[relayIndex], LOW);
        
        Serial.print("Accion: Rele ");
        Serial.print(command);
        Serial.println(" activado (otros apagados)");
      }
      break;
      
    default:
      Serial.println("Error: Comando no reconocido");
      return;
  }
  
  // Mostrar estado actual
  showStatus();
}

void showStatus() {
  Serial.print("Estado: ");
  for (int i = 0; i < RELAY_COUNT; i++) {
    Serial.print(i + 1);
    Serial.print(":");
    Serial.print(relayStates[i] ? "ON " : "OFF ");
  }
  Serial.println();
  Serial.println("---");
}

void testSequence() {
  // Secuencia de prueba al iniciar
  Serial.println("Prueba de relés...");
  
  for (int i = 0; i < RELAY_COUNT; i++) {
    digitalWrite(RELAY_PINS[i], LOW); // Encender
    delay(300);
    digitalWrite(RELAY_PINS[i], HIGH); // Apagar
    delay(200);
  }
  
  // Encender todos brevemente
  for (int i = 0; i < RELAY_COUNT; i++) {
    digitalWrite(RELAY_PINS[i], LOW);
  }
  delay(500);
  
  // Apagar todos
  for (int i = 0; i < RELAY_COUNT; i++) {
    digitalWrite(RELAY_PINS[i], HIGH);
  }
  
  Serial.println("Prueba completada");
  Serial.println("Esperando comandos...");
  Serial.println();
}

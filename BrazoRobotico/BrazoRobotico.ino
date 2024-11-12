#include <WiFi.h>
#include <ESP32Servo.h>

// Configuración de WiFi
const char* ssid = "nombreRed";
const char* password = "contrasena";

// Pines de los servos
const int pinBase = 23;
const int pinCodo = 17;
const int pinAntebrazo = 16;
const int pinMuneca = 4;
const int pinPinza = 2;
const int pinInvisible = 22;  //No se hará uso de este pin en la ejecución


Servo servoBase;
Servo servoCodo;
Servo servoAntebrazo;
Servo servoMuneca;
Servo servoPinza;
Servo servoInvisible;

// Iniciar servidor web
WiFiServer server(80);


//Función para limitar la velocidad de posicionamiento de los servomotores
void moverServoGradualmente(Servo& servo, int posicionFinal, int tiempoMov) {
  int posicionActual = servo.read();
  int pasos = abs(posicionFinal - posicionActual);

  if (pasos > 20) {
    pasos = 20;
  }

  int delayPorPaso = max(5, tiempoMov / pasos);

  for (int i = 0; i <= pasos; i++) {
    int nuevaPosicion = posicionActual + (posicionFinal - posicionActual) * i / pasos;  // Interpolación lineal
    servo.write(nuevaPosicion);
    delay(delayPorPaso);
  }

  void setup() {
    Serial.begin(115200);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Conectando a WiFi...");
    }

    Serial.println("Conectado a WiFi");
    Serial.print("Dirección IP: ");
    Serial.println(WiFi.localIP());

    servoInvisible.attach(pinInvisible);  // Pin sin usar
    servoBase.attach(pinBase);
    servoCodo.attach(pinCodo);
    servoAntebrazo.attach(pinAntebrazo);
    servoMuneca.attach(pinMuneca);
    servoPinza.attach(pinPinza);

    // Iniciar servidor
    server.begin();
  }

  void loop() {
    WiFiClient client = server.available();

    if (client) {
      Serial.println("Nuevo cliente conectado");

      String request = client.readStringUntil('\r');
      Serial.println("Solicitud recibida: " + request);

      client.flush();

      if (request.startsWith("GET /?")) {
        String params = request.substring(5, request.indexOf(" HTTP"));
        Serial.println("Parametros recibidos: " + params);

        char str[params.length() + 1];
        params.toCharArray(str, sizeof(str));

        int values[6];
        int index = 0;
        char* token = strtok(str, ",");

        while (token != NULL && index < 6) {
          values[index] = atoi(token);
          index++;
          token = strtok(NULL, ",");
        }

        Serial.println("Valores procesados:");
        for (int i = 0; i < 6; i++) {
          Serial.print("Servo ");
          Serial.print(i);
          Serial.print(": ");
          Serial.println(values[i]);
        }

        if (index == 6) {
          moverServoGradualmente(servoPinza, values[1], 500);
          moverServoGradualmente(servoMuneca, values[2], 500);
          moverServoGradualmente(servoAntebrazo, values[3], 500);
          moverServoGradualmente(servoCodo, values[4], 500);
          moverServoGradualmente(servoBase, values[5], 500);
        }

        // Enviar respuesta HTTP de confirmación
        client.println("HTTP/1.1 200 OK");
        client.println("Content-Type: text/html");
        client.println();
        client.println("<html><body><h1>Movimientos completados!</h1></body></html>");

        // Cerrar la conexión
        client.stop();
        Serial.println("Cliente desconectado");
      }
    }
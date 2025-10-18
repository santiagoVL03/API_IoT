#include <SPI.h>
#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>

char ssid[] = "wifi-CsComputacion";
char pass[] = "EPCC2022$";
int status = WL_IDLE_STATUS;

char server[] = "10.7.134.119"; // IP del servidor
int port = 5000;
WiFiClient client;

float ax, ay, az;
float gx, gy, gz;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 500; // ms entre envíos

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("No se detectó módulo WiFi");
    while (true);
  }

  // Conectar a WiFi
  while (status != WL_CONNECTED) {
    Serial.print("Conectando a ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }

  Serial.println("Conectado a WiFi");
  Serial.print("IP local: ");
  Serial.println(WiFi.localIP());

  if (!IMU.begin()) {
    Serial.println("Error al inicializar IMU (LSM6DS3)");
    while (1);
  }
  Serial.println("IMU iniciada correctamente");
}

void loop() {
  // Leer datos del acelerómetro y giroscopio
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);
  }

  // Enviar cada 500 ms
  if (millis() - lastSendTime >= sendInterval) {
    enviarDatosAPI(ax, ay, az, gx, gy, gz);
    lastSendTime = millis();
  }
}

// Función para enviar datos al servidor
void enviarDatosAPI(float ax, float ay, float az, float gx, float gy, float gz) {
  if (client.connect(server, port)) {
    // Crear URL con parámetros GET
    String url = "/api/v1/iotgiroscopio/?";
    url += "&ay=" + String(ay, 3);
    url += "&az=" + String(az, 3);
    url += "&gx=" + String(gx, 3);
    url += "&gy=" + String(gy, 3);
    url += "&gz=" + String(gz, 3);

    Serial.print("📡 Enviando a: ");
    Serial.println(url);

    // Enviar petición HTTP
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + server + "\r\n" +
                 "Connection: close\r\n\r\n");
    delay(500); // pequeña pausa para estabilidad
    client.stop();
  } else {
    Serial.println("Error al conectar con el servidor");
  }
}

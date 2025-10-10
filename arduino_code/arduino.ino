#include <Arduino_MKRIoTCarrier.h>
#include <WiFiNINA.h>
#include <HTTPClient.h>

//// ==== CONFIGURACIÓN WIFI ====
char ssid[] = "wifi-CsComputacion";       // <<-- pon aquí tu red WiFi
char pass[] = "EPCC2022$";   // <<-- pon aquí tu contraseña

//// ==== OBJETOS ====
MKRIoTCarrier carrier;

//// ==== PIN DEL SENSOR DE HUMEDAD ====
int soilPin = A6;

void setup() {
  Serial.begin(9600);
  delay(1500);

  CARRIER_CASE = false;
  if (!carrier.begin()) {
    Serial.println("Error iniciando Carrier");
    while (1);
  }

  //// ==== Conexión WiFi ====
  Serial.print("Conectando a WiFi: ");
  Serial.println(ssid);

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConectado a WiFi!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  //// ==== Lecturas de sensores ====
  float temp = carrier.Env.readTemperature();
  float hum  = carrier.Env.readHumidity();
  float pres = carrier.Pressure.readPressure();

  int soilRaw = analogRead(soilPin);
  float soilPercent = map(soilRaw, 1023, 0, 0, 100); 
  // Nota: ajusta según calibración real de tu sensor

  //// ==== Mostrar en consola ====
  Serial.print("Temp: "); Serial.println(temp);
  Serial.print("Hum: ");  Serial.println(hum);
  Serial.print("Pres: "); Serial.println(pres);
  Serial.print("Soil: "); Serial.print(soilPercent); Serial.println(" %");
  Serial.println("-----");

  //// ==== Enviar datos al API ====
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Temp
    String urlTemp = "http://10.7.135.142:5000/api/v1/iotinsert/?type_sensor=temperature&sensor_value=" + String(temp);
    http.begin(urlTemp);
    int httpCode = http.GET();
    Serial.println("Temp-> HTTP Code: " + String(httpCode));
    http.end();

    // Humedad
    String urlHum = "http://10.7.135.142:5000/api/v1/iotinsert/?type_sensor=humidity&sensor_value=" + String(hum);
    http.begin(urlHum);
    httpCode = http.GET();
    Serial.println("Hum-> HTTP Code: " + String(httpCode));
    http.end();

    // Presión
    String urlPres = "http://10.7.135.142:5000/api/v1/iotinsert/?type_sensor=pressure&sensor_value=" + String(pres);
    http.begin(urlPres);
    httpCode = http.GET();
    Serial.println("Pres-> HTTP Code: " + String(httpCode));
    http.end();

    // Soil
    String urlSoil = "http://10.7.135.142:5000/api/v1/iotinsert/?type_sensor=soil&sensor_value=" + String(soilPercent);
    http.begin(urlSoil);
    httpCode = http.GET();
    Serial.println("Soil-> HTTP Code: " + String(httpCode));
    http.end();
  } else {
    Serial.println("WiFi desconectado!");
  }

  delay(5000); // cada 5 segundos
}
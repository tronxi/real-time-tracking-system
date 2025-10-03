#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <Adafruit_BMP3XX.h>

#define SS    5
#define RST   27
#define DIO0  26
#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28); 
Adafruit_BMP3XX bmp;
float baseAltitude = NAN;
int warmupCount = 0;


void setup() {
  Serial.begin(115200);
  while (!Serial);

  LoRa.setPins(SS, RST, DIO0);
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(250E3);
  LoRa.setCodingRate4(5);
  LoRa.setTxPower(14);  
  LoRa.enableCrc();
 
  Serial.println("LoRa init OK!");

  if (!bno.begin()) {
    Serial.println("No se detecta BNO055 :(");
    while (1);
  }
  bno.setExtCrystalUse(true);

  if (!bmp.begin_I2C()) {
    Serial.println("No se detecta BMP388 :(");
    while (1);
  }
  bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
  bmp.setOutputDataRate(BMP3_ODR_50_HZ);

  Serial.println("Sensores inicializados");
}

void loop() {
  sensors_event_t event;
  bno.getEvent(&event);

  if (!bmp.performReading()) {
    Serial.println("Error al leer datos del BMP388");
    return;
  }

  float heading = event.orientation.x;
  float roll    = event.orientation.y;
  float pitch   = event.orientation.z;
  float temp    = bmp.temperature;
  float pres    = bmp.pressure / 100.0;
  float altAbs  = bmp.readAltitude(SEALEVELPRESSURE_HPA);

  if (warmupCount < 5) {
    warmupCount++;
    return;
  }

  if (isnan(baseAltitude)) {
    baseAltitude = altAbs;
  }
  float altRel = altAbs - baseAltitude;

  String json = "{";
  json += "\"yaw\":" + String(heading, 2) + ",";
  json += "\"roll\":" + String(roll, 2) + ",";
  json += "\"pitch\":" + String(pitch, 2) + ",";
  json += "\"temperature\":" + String(temp, 2) + ",";
  json += "\"pressure\":" + String(pres, 2) + ",";
  json += "\"altitude\":" + String(altRel, 2);
  json += "}";

  LoRa.beginPacket();
  LoRa.print(json);
  LoRa.endPacket();

  Serial.println("Sending: " + json);

  delay(500);
}

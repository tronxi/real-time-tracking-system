#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

void setup()
{
  Serial.begin(9600);
  ss.begin(GPSBaud);
}

void loop()
{
  StaticJsonDocument<200> doc;
  doc["stalleites"] = gps.satellites.value();
  doc["hdop"] = gps.hdop.hdop();
  doc["lat"] = gps.location.lat();
  doc["long"] = gps.location.lng();
  doc["altitude"] = gps.altitude.meters();
  doc["speed"] = gps.speed.kmph();
  serializeJson(doc, Serial);
  Serial.println();
  smartDelay(1000);

  if (millis() > 5000 && gps.charsProcessed() < 10)
    Serial.println(F("No GPS data received: check wiring"));
}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}


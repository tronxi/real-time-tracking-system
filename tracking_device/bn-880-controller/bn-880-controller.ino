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
  StaticJsonDocument<200> positionEvent;
  positionEvent["type"] = "POSITION";
  positionEvent["satellites"] = gps.satellites.value();
  positionEvent["hdop"] = gps.hdop.hdop();
  positionEvent["lat"] = gps.location.lat();
  positionEvent["long"] = gps.location.lng();
  positionEvent["altitude"] = gps.altitude.meters();
  positionEvent["speed"] = gps.speed.kmph();
  serializeJson(positionEvent, Serial);
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


#include <SPI.h>
#include <LoRa.h>

#define SS    5
#define RST   27
#define DIO0  26

int count;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  count = 0;

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("LoRa init OK!");
}

void loop() {
  Serial.println("Sending packet...");
  LoRa.beginPacket();
  LoRa.print("Package: " + String(count));
  LoRa.endPacket();
  count++;
  delay(2000);
}

#include <SPI.h>
#include <LoRa.h>

#define SS    5
#define RST   27
#define DIO0  26

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("LoRa Receiver");

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
  Serial.println("LoRa init OK, waiting for packets...");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {

    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
    Serial.println();

    // Serial.println(LoRa.packetRssi());
  }
}

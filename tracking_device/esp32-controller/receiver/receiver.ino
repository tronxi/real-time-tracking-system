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

  if (!LoRa.begin(433E6)) {  // frecuencia en Hz
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  Serial.println("LoRa init OK, waiting for packets...");
}

void loop() {
  // int packetSize = LoRa.parsePacket();
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    Serial.print("Received packet '");

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }

    // print RSSI (fuerza de señal recibida)
    Serial.print("' with RSSI ");
    Serial.println(LoRa.packetRssi());
  }
}

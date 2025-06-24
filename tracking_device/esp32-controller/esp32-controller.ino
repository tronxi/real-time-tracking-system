#include "esp_camera.h"
#include <WiFi.h>
#include "FS.h"
#include "SD_MMC.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "driver/rtc_io.h"

#define PWDN_GPIO_NUM  32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  0
#define SIOD_GPIO_NUM  26
#define SIOC_GPIO_NUM  27
#define FLASH_GPIO_NUM 4
#define RED_LED        33

#define Y9_GPIO_NUM    35
#define Y8_GPIO_NUM    34
#define Y7_GPIO_NUM    39
#define Y6_GPIO_NUM    36
#define Y5_GPIO_NUM    21
#define Y4_GPIO_NUM    19
#define Y3_GPIO_NUM    18
#define Y2_GPIO_NUM    5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM  23
#define PCLK_GPIO_NUM  22

unsigned long fotoCount = 0;
String sessionFolder;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  Serial.begin(115200);
  delay(1000);

  pinMode(RED_LED, OUTPUT);
  digitalWrite(RED_LED, LOW);

  camera_config_t config = {};
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size   = FRAMESIZE_SVGA;
  config.fb_location  = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count     = 2;

  if (!psramFound()) {
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Cam error");
    while (1) delay(1000);
  }

  if (!SD_MMC.begin("/sdcard", true)) {
    Serial.println("SD error");
    while (1) delay(1000);
  }
  initSessionFolder();

}

void loop() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Foto error");
    delay(1000);
    return;
  }

  String filename = sessionFolder + "/" + String(fotoCount++) + ".jpg";
  File file = SD_MMC.open(filename.c_str(), FILE_WRITE);
  if (!file) {
    Serial.println("Error opening " + filename);
      delay(1000);
  } else {
    file.write(fb->buf, fb->len);
    file.close();
    Serial.println("Saved: " + filename);
    digitalWrite(RED_LED, HIGH);
    delay(1000);
    digitalWrite(RED_LED, LOW);
  }

  esp_camera_fb_return(fb);
}

void initSessionFolder() {
  uint32_t maxNum = 0;
  File root = SD_MMC.open("/");
  if (!root || !root.isDirectory()) return;
  File file;
  while ((file = root.openNextFile())) {
    if (file.isDirectory()) {
      String name = file.name();
      name.replace("/", "");
      bool allDigits = true;
      for (char c : name) if (!isDigit(c)) allDigits = false;
      if (allDigits) {
        uint32_t n = name.toInt();
        if (n >= maxNum) maxNum = n + 1;
      }
    }
    file.close();
  }
  sessionFolder = "/" + String(maxNum);
  if (SD_MMC.mkdir(sessionFolder.c_str())) {
    Serial.printf("Created folder: %s\n", sessionFolder.c_str());
  } else {
    Serial.printf("Error creating folder: %s\n", sessionFolder.c_str());
  }
}

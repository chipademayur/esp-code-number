#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_camera.h"

const char* ssid = "YourWiFi";
const char* password = "YourPassword";
const char* serverUrl = "http://your_server_ip:5000/upload";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
}

void loop() {
    // Capture image and send to backend
    delay(10000);
}

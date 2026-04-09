#include <SPI.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WIFI
char ssid[] = "wifi name";
char password[] = "wifi pass";

// MQTT
char mqtt_server[] = "mqtt ip address";

WiFiClient wifiClient;
PubSubClient client(wifiClient);

int sensorPin = A0;
int pumpPin = 5;


int dryThreshold = 600;  
int wetThreshold = 400;   
bool pumpState = false;
bool autoMode = true;


unsigned long lastPublish = 0;
const long publishInterval = 2000;

//WIFI----------------
void setup_wifi() {
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(5000);
  }
}

//MQTT----------------
void callback(char* topic, byte* payload, unsigned int length) {
  String msg;

  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  String topicStr = String(topic);

  if (topicStr == "plant/pump") {
    if (msg == "ON") {
      autoMode = false;
      digitalWrite(pumpPin, HIGH);
      pumpState = true;
    }
    else if (msg == "OFF") {
      autoMode = false;
      digitalWrite(pumpPin, LOW);
      pumpState = false;
    }
    else if (msg == "AUTO") {
      autoMode = true;
    }
  }
}

//MQTT RECONNECT ----------------
void reconnect() {
  while (!client.connected()) {
    if (client.connect("LeonardoClient")) {
      client.subscribe("plant/pump");
    } else {
      delay(3000);
    }
  }
}

// ----------------
void setup() {
  pinMode(pumpPin, OUTPUT);
  digitalWrite(pumpPin, LOW);

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int moisture = analogRead(sensorPin);


  if (autoMode) {
    if (moisture > dryThreshold && !pumpState) {
      digitalWrite(pumpPin, HIGH);
      pumpState = true;
    }
    else if (moisture < wetThreshold && pumpState) {
      digitalWrite(pumpPin, LOW);
      pumpState = false;
    }
  }

 
  if (millis() - lastPublish > publishInterval) {
    lastPublish = millis();

    client.publish("plant/moisture", String(moisture).c_str());
    client.publish("plant/status", pumpState ? "ON" : "OFF");
    client.publish("plant/mode", autoMode ? "AUTO" : "MANUAL");
  }
}
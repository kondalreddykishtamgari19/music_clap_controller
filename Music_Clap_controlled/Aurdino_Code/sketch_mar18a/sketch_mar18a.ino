#include <WiFi.h>
#include <FirebaseESP32.h>

// WiFi credentials
const char* ssid = "realme c15";  // Your WiFi SSID
const char* password = "12345678.";      // Your WiFi password

// Firebase configuration
FirebaseConfig config;
FirebaseAuth auth;
FirebaseData firebaseData;

// Sound Sensor Pin
#define SOUND_SENSOR_D0 3
int count = 0;  
bool clapDetected = false;  // Flag to track new claps

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Set Firebase configuration
  config.host = "clap-9b5d9-default-rtdb.asia-southeast1.firebasedatabase.app";   // Firebase Realtime Database URL
  config.signer.tokens.legacy_token = "JUUNp0shp5FmGHArqYXKbbZfgB6dlM4gVOQ4SOB0";  // Secret key

  // Initialize Firebase
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  // Initialize Sound Sensor
  pinMode(SOUND_SENSOR_D0, INPUT);
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Reconnecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Waiting for WiFi...");
    }
    Serial.println("Reconnected to WiFi");
  }

  if (Firebase.ready()) {
    int soundStatus = digitalRead(SOUND_SENSOR_D0);

    if (soundStatus == HIGH && !clapDetected) { 
      // New clap detected
      clapDetected = true;
      count++;  

      Serial.print("Clap detected: ");
      Serial.println(count);

      // Send clap count to Firebase
      String path = "/clap";
      if (Firebase.setInt(firebaseData, path, count)) {
        Serial.println("Firebase updated successfully");
      } else {
        Serial.print("Firebase update failed: ");
        Serial.println(firebaseData.errorReason());
      }

      delay(500);  // Prevents multiple detections for the same clap
    } 
    else if (soundStatus == LOW) { 
      // Reset clap detection flag when no sound is detected
      clapDetected = false;
    }

    // If 3 claps detected, reset count to 0
    if (count >= 3) {
      Serial.println("3 claps detected! Resetting count to 0...");
      count = 0;  

      // Send reset value to Firebase
      String path = "/clap";
      Firebase.setInt(firebaseData, path, count);
    }
  }
}

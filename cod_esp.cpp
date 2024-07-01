#include <WiFi.h>
#include <ESP32Servo.h>

const char* ssid = "Adda";             
const char* password = "alexandra";     
WiFiServer server(80);

Servo servo1;  
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

const int servoPin1 = 25;  
const int servoPin2 = 26; 
const int servoPin3 = 27; 
const int servoPin4 = 14; 
const int servoPin5 = 12;

void moveServos(int randomNumber);

void setup() {
  Serial.begin(115200);
  delay(2000);
  
  Serial.println();
  Serial.println("Conexiunea WIFI...");
  WiFi.begin(ssid, password);

  Serial.println("");
  Serial.println("S-a realizat conexiunea WIFI!");
  Serial.print("Adresa IP: ");
  Serial.println(WiFi.localIP()); 
  
  server.begin();
  Serial.println("S-a inceput o conexiune server!");

  servo1.attach(servoPin1);  
  servo2.attach(servoPin2); 
  servo3.attach(servoPin3);
  servo4.attach(servoPin4); 
  servo5.attach(servoPin5);  
}

void loop() {
  int numar;
  WiFiClient client = server.available(); 

  if (client) { 
    Serial.println("Un client nou s-a conectat!");
    
    while (client.connected()) { 
      if (client.available()) { 
        String request = client.readString(); 
        numar = request.toInt(); 
        
        Serial.print("Numarul primit: ");
        Serial.println(randomNumber);
        
        gest(numar);
      }
    }
    client.stop(); 
    Serial.println("Clientul s-a deconectat!");
  }
}

void gest(int numar){
  if (numar == 1){  //piatra
    servo1.write(180);
    delay(1700);
    servo1.write(90);
    delay(3000);

    servo2.write(0);
    delay(1800);
    servo2.write(90);
    delay(3000);

    servo3.write(180);
    delay(1500);
    servo3.write(90);
    delay(3000);

    servo4.write(0);
    delay(1700);
    servo4.write(90);
    delay(3000);

    servo5.write(0);
    delay(1650);
    servo5.write(90);
    delay(3000);

    servo1.write(0);
    delay(500);
    servo1.write(90);

    servo2.write(180);
    delay(1600);
    servo2.write(90);

    servo3.write(0);
    delay(980);
    servo3.write(90);

    servo4.write(180);
    delay(1600);
    servo4.write(90);

    servo5.write(180);
    delay(1500);
    servo5.write(90);

    }else if (numar == 2){  //foarfeca
      servo1.write(180);
      delay(1700);
      servo1.write(90);
      delay(3000);

      servo4.write(0);
      delay(1700);
      servo4.write(90);
      delay(3000);

      servo5.write(0);
      delay(1650);
      servo5.write(90);
      delay(3000);

      servo1.write(0);
      delay(500);
      servo1.write(90);

      servo4.write(180);
      delay(1600);
      servo4.write(90);

      servo5.write(180);
      delay(1500);
      servo5.write(90);
    }
}

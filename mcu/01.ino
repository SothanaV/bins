#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

Servo servo;

const char* ssid     = "Com-Lab";                   //Set ssid
const char* password = "";            //Set Password
const char* Server   = "192.168.88.245";          //set Server Domain or Server
ESP8266WiFiMulti WiFiMulti;

void setup()
{
    Serial.begin(115200); 
    servo.attach(15); // pin
    servo.write(0);
    WiFiMulti.addAP(ssid, password);    //Set SSID and Password (SSID, Password)
    WiFi.begin(ssid, password);         //Set starting for Wifi
    for(uint8_t t = 6; t > 0; t--) 
    {
        Serial.printf("[SETUP] WAIT %d...\n", t);
        Serial.flush();
        delay(1000);
    }
}

void loop()
{
    // if((WiFiMulti.run() == WL_CONNECTED))
    if(true) 
    {
        HTTPClient http;
        String str = "http://" +String(Server)+":5000"+"/mcu";
        Serial.println(str);
        http.begin(str);
        int httpCode = http.GET();
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);
        if(httpCode > 0) 
        {
            if(httpCode == HTTP_CODE_OK) 
            {
                String payload = http.getString();
                Serial.printf("%s \n","Payload");
                Serial.println(payload);
                if (payload=="0")
                {
                    servo.write(0);
                }
                else if(payload=="1")
                {
<<<<<<< HEAD
                    servo.write(170);
=======
                    servo.write(90);
                    delay(500);
>>>>>>> 8fd61e0391b4035ba864ddd20f7733e7cb9ee9a0
                }
            } 
        }
    }
    delay(500);
}
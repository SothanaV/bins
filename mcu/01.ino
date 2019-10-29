#include <servo.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

Servo servo;

const char* ssid     = "ois";                   //Set ssid
const char* password = "ilovestudy";            //Set Password
const char* Server   = "192.168.1.6";          //set Server Domain or Server
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
    if((WiFiMulti.run() == WL_CONNECTED)) 
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
                Serial.printf("%s : %s \n","Payload",payload);
                if (payload=='0')
                {
                    servo.write(0);
                }
                else if(payload=='1')
                {
                    servo.write(90);
                }
            } 
        }
    }
    delay(100);
}
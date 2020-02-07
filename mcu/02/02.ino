#include <Servo.h>
Servo servo;
int angle = 0;
void setup()
{
    Serial.begin(115200); 
    servo.attach(15); // pin
    servo.write(180);
    for(uint8_t t = 3; t > 0; t--) 
    {
        Serial.printf("[SETUP] WAIT %d...\n", t);
        Serial.flush();
        delay(1000);
    }
}

void loop()
{
    // if (Serial.available() > 0) 
    // {
        String payload = Serial.readString();
        Serial.printf("%s \n","Payload");
        Serial.println(payload);
        angle = payload.toInt();
        servo.write(angle);
        delay(100);
    // }
}
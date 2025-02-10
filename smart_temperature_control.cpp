#include <DHTStable.h>

#define DHT11_pin 8
#define tmp 2000
#define PIR_pin 7

int flag = 0;
int temperature;
DHTStable dht11_sensor;

void setup() {
    Serial.begin(9600);
    pinMode(PIR_pin, INPUT);
    delay(tmp);
}

void loop() {

    // Reads DHT11 sensor data from the input pin
    dht11_sensor.read11(DHT11_pin);

    // Read PIR sensor data from the input pin
    bool status_PIR = digitalRead(PIR_pin);

    if (status_PIR) {

        // Get the temperature data
        temperature = dht11_sensor.getTemperature();
        
        // Flag to indicate presence
        flag = 1;

        // Sends the data types with the format "int,int"
        Serial.print(flag);
        Serial.print(",");
        Serial.println(temperature);

    } else {

        // Get the temperature data
        temperature = dht11_sensor.getTemperature();

        // Flag to indicate absence
        flag = 0;

        // Sends the data types with the format "int,int"
        Serial.print(flag);
        Serial.print(",");
        Serial.println(temperature);

    }

    // Delay that allows the DHT11 sensor to send the data properly
    delay(tmp);
    
}

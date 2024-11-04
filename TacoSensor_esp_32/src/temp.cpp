#include "temp.h"

Temp::Temp(uint8_t pin) {
    this->wire = OneWire(pin); 
    this->sensors = DallasTemperature(&this->wire);
}

void Temp::init() {
    this->sensors.begin(); 
    Serial.println("SENSORS START");
    this->n_devices = this->sensors.getDeviceCount(); 
    Serial.print("Number of devices: "); 
    Serial.print(this->n_devices); 
    Serial.println("");

}

void Temp::reload() {

}

float Temp::getTempC(uint8_t idx) {
    this->sensors.requestTemperatures(); 
    float t = this->sensors.getTempCByIndex(idx); 
    return t; 
}

void Temp::getTemperatures() {
    this->sensors.requestTemperatures(); 

}

Temp::~Temp() {

}
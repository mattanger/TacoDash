#ifndef TEMP_H
#define TEMP_H

#include <OneWire.h>
#include <DallasTemperature.h>


class Temp
{
private:
    OneWire wire; 
    DallasTemperature sensors; 
    uint8_t n_devices; 

public:
    Temp(uint8_t pin);
    ~Temp();
    void init();  
    void reload(); 
    void getTemperatures(); 
    float getTempC(uint8_t idx);
};


#endif
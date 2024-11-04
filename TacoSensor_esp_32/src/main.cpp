#include <Arduino.h>
#include <WiFi.h>
#include <Wire.h>
// #include <SSD1306Wire.h>
#include "SSD1306.h"        
#include <OneWire.h>
#include <DallasTemperature.h>
#include "temp.h"
#include "bluetooth.h"


const int I2C_DISPLAY_ADDRESS = 0x3c;
const int SDA_PIN = 4;
const int SCL_PIN = 15; 
const int RST_PIN = 16; 
const int ONE_WIRE_PIN = 17; 

#define PI_RELAY_1 2

SSD1306  display(I2C_DISPLAY_ADDRESS, SDA_PIN, SCL_PIN);
// OneWire wire(ONE_WIRE_PIN); 
// DallasTemperature sensor(&wire); 
DeviceAddress address; 
// OLEDDisplayUi ui     ( &display );
void printAddress(DeviceAddress DeviceAddress); 
void initDisplay(); 

void drawSensor1Temp(float_t temp); 
void drawSensor2Temp(float_t temp); 

char temp1[20];
char temp2[20]; 

Temp temp_sensors(ONE_WIRE_PIN);
BluetoothInterface bluetooth; 

void ign_interrupt()
{
  Serial.println("ignition off detected!"); 
}

void init_relay_pins() 
{
  pinMode(PI_RELAY_1, OUTPUT); 
  digitalWrite(PI_RELAY_1, LOW); 
}

void pi_poweron() 
{

}

void setup() {
  Serial.begin(115200); 
  delay(1000); 
  Serial.println("Booting up...");
  init_relay_pins(); 
  bluetooth.init(); 
  temp_sensors.init();
  initDisplay(); 
  pinMode()
}


void loop() {

  double outside = temp_sensors.getTempC(0); 
  drawSensor1Temp(outside); 
  bluetooth.set_outside_temp(outside); 

  double inside = temp_sensors.getTempC(1); 
  drawSensor2Temp(inside);
  bluetooth.set_inside_temp(inside); 

  display.display();
  bluetooth.check(); 
  delay(2000); 
}

void printAddress(DeviceAddress deviceAddress) {
  for (uint8_t i = 0; i < 8; i++) {
    if (deviceAddress[i] < 16) Serial.print("0");
      Serial.print(deviceAddress[i], HEX);
  }
}

void drawSensor1Temp(float_t temp) {
  snprintf(temp1, sizeof(temp1), "Outside: %.2f C", temp);  
  display.drawString(0, 0, temp1); 
}

void drawSensor2Temp(float_t temp) {
  snprintf(temp2, sizeof(temp2), "Inside: %.2f C", temp);  
  display.drawString(0, 18, temp2); 
}



void initDisplay() {
  pinMode(RST_PIN, OUTPUT);
  digitalWrite(RST_PIN, HIGH); 
  delay(1); 
  digitalWrite(RST_PIN, LOW);
  delay(100);
  digitalWrite(RST_PIN, HIGH);

  display.init();
  Serial.println(display.width()); 
  Serial.println(display.height()); 
  display.flipScreenVertically();
  display.clear(); 
  display.display(); 

  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.setContrast(255);
}
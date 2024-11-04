#ifndef BLUETOOTH_H
#define BLUETOOTH_H
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>
#include "helpers.h"

#define SERVICE_UUID "c72127c8-db8f-4efa-9849-e237e4e26ff7"
#define TEMP_CHARACTERISTIC_UUID "ca45d77d-a1d0-4122-881c-aa189a4c32f3"
#define COMMAND_CAHRACTERISTIC_UUID "1a299ca7-5942-4c35-a43e-87b5ee08a1b4"
#define DEVICE_NAME "Taco_Sensors"
#define PACKET_BODY_LEN 20


class CommandCharacteristicCB : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* commandCharacteristic) {
    std::string val = commandCharacteristic->getValue(); 
    Serial.println("Received: "); 
    Serial.println(val.c_str()); 

    // String value = pLedCharacteristic->getValue();
    // if (value.length() > 0) {
    //   Serial.print("Characteristic event, written: ");
    //   Serial.println(static_cast<int>(value[0])); // Print the integer value

    //   int receivedValue = static_cast<int>(value[0]);
    //   if (receivedValue == 1) {
    //     digitalWrite(ledPin, HIGH);
    //   } else {
    //     digitalWrite(ledPin, LOW);
    //   }
    // }
  }
};

class TempCharacteristicsCB : public BLECharacteristicCallbacks {
    void onNotify(BLECharacteristic *pCharacteristic) {}
}; 

class SecurityCallbacks: public BLESecurityCallbacks {
    uint32_t onPassKeyRequest(){
        Serial.println("PassKeyRequest!");
        return 123456;
    }

    void onPassKeyNotify(uint32_t pass_key){
        Serial.println("On passkey Notify!");
    }

    bool onSecurityRequest(){
        Serial.println("On Security Request!");
        return true;
    }

    void onAuthenticationComplete(esp_ble_auth_cmpl_t cmpl){
        if(cmpl.success){
            Serial.println("onAuthenticationComplete!");
            uint16_t length;
            esp_ble_gap_get_whitelist_size(&length);
        } else {
            Serial.println("onAuthentication not Complete!");
        }
    }

    bool onConfirmPIN(uint32_t pin){
        Serial.println("onConfirmPIN!");
        return true;
    }
}; 


class BluetoothInterface
{
private:
    BLEServer *bl_server; 
    BLEService *bl_service; 
    BLECharacteristic *tempCharacteristic; 
    BLECharacteristic *commandCharacteristic; 
    BLEAdvertising *advertising; 
    bool deviceConnected = false; 
    bool startAdvertising = false; 
    double inside_temp = 0; 
    double outiside_temp = 0; 


public:
    BluetoothInterface(/* args */);
    ~BluetoothInterface();
    void init(); 
    void check(); 
    void connected(bool connected); 
    void set_inside_temp(double temp); 
    void set_outside_temp(double temp); 
};


class ServerCallbacks: public BLEServerCallbacks {

    private: 
        BluetoothInterface *bluetooth; 

    public: 
        ServerCallbacks(BluetoothInterface *bluetooth); 
        void onConnect(BLEServer* pServer);
        void onDisconnect(BLEServer* pServer); 
};

BluetoothInterface::BluetoothInterface(/* args */)
{
}

void BluetoothInterface::set_inside_temp(double temp) 
{
    this->inside_temp = temp; 
}

void BluetoothInterface::set_outside_temp(double temp) 
{
    this->outiside_temp = temp; 
}

void BluetoothInterface::connected(bool connected) {
    this->deviceConnected = connected; 
    this->startAdvertising = !connected; 
}



void BluetoothInterface::check() {
    if (this->deviceConnected) {
        char buffer[100];

        snprintf(buffer, sizeof(buffer), "outside|%.2f,inside|%.2f", this->outiside_temp, this->inside_temp); 
        buffer[strlen(buffer)] = 0x04; 
        chunkedStringActionL(buffer, strlen(buffer), 20, this->tempCharacteristic, sendChunk); 
        delay(10); 
    }
    if (!this->deviceConnected && this->startAdvertising) {
        delay(500); 
        this->advertising->start(); 
        Serial.println("Advertising restarted"); 
        this->startAdvertising = false; 
    }
}


void BluetoothInterface::init() 
{
    Serial.println("Initializing bluetooth"); 
    BLEDevice::init(DEVICE_NAME);
    
    this->bl_server = BLEDevice::createServer();
    this->bl_server->setCallbacks(new ServerCallbacks(this)); 
    this->bl_service = this->bl_server->createService(SERVICE_UUID);
    this->commandCharacteristic = this->bl_service->createCharacteristic(
        COMMAND_CAHRACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_WRITE
    ); 
    this->commandCharacteristic->setCallbacks(new CommandCharacteristicCB()); 

    this->tempCharacteristic = this->bl_service->createCharacteristic(
                                        TEMP_CHARACTERISTIC_UUID,
                                        BLECharacteristic::PROPERTY_NOTIFY 
                                        );
    this->tempCharacteristic->setCallbacks(new TempCharacteristicsCB()); 

    this->tempCharacteristic->addDescriptor(new BLE2902());
    BLEDescriptor tempDescriptor(BLEUUID((uint16_t)0x9202)); 
    tempDescriptor.setValue("Temperatures");  
    this->tempCharacteristic->addDescriptor(&tempDescriptor); 
    


    this->bl_service->start(); 

    this->advertising = this->bl_server->getAdvertising(); 

    this->advertising->addServiceUUID(SERVICE_UUID);
    this->advertising->setScanResponse(true);
    this->advertising->start(); 

    Serial.println("Bluetooth initialized and advertising.."); 
}

BluetoothInterface::~BluetoothInterface()
{
}


ServerCallbacks::ServerCallbacks(BluetoothInterface *bluetooth) {
        this->bluetooth = bluetooth; 
    }

void ServerCallbacks::onConnect(BLEServer* pServer) {
    this->bluetooth->connected(true); 
    Serial.println("device connected");
    
};

void ServerCallbacks::onDisconnect(BLEServer* pServer) {
    this->bluetooth->connected(false); 
    Serial.println("device disconnected"); 
}


#endif

#include <Arduino.h>
#include "bluetooth.h"

// https://forum.arduino.cc/t/split-char-array-into-chunks/344112/8
uint8_t chunkedStringActionL(char* ptrData, uint8_t dataLength, uint8_t chunkLength,  BLECharacteristic* characteristic, void(*action)(char*, BLECharacteristic*)) {
    char chunkData[chunkLength +1];
    chunkData[chunkLength] = 0;                             //terminate chunk buffer
    
    uint8_t chunks = dataLength / chunkLength;             //complete chunks
    uint8_t lastChunkLength = dataLength % chunkLength;    //partial or empty

    ptrData[dataLength] = 0;                                //prevent buffer overrun
    
    if(chunks) {
        for(uint8_t i = 0; i < chunks; i++) {
            memcpy(chunkData, ptrData, chunkLength);
            ptrData += chunkLength;
            action(chunkData, characteristic);
        }
        if(lastChunkLength) {
            memcpy(chunkData, ptrData, lastChunkLength +1);      //copy terminator from source
            action(chunkData, characteristic);
            chunks++;
        }
    }
    return chunks;
}

void sendChunk(char* chunk, BLECharacteristic* characteristic) {
    Serial.println(chunk);
    characteristic->setValue(chunk); 
    characteristic->notify();
}
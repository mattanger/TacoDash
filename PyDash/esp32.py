import asyncio
import sys
from itertools import count, takewhile
from typing import Iterator
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from BluetoothAgent import BluetoothAgent
from state import State
import contextlib

SENSOR_DEVICE = "Taco_Sensors"
SERVICE_UUID = "c72127c8-db8f-4efa-9849-e237e4e26ff7"
TEMP_CHARACTERISTIC_UUID = "ca45d77d-a1d0-4122-881c-aa189a4c32f3"
COMMAND_CAHRACTERISTIC_UUID = "1a299ca7-5942-4c35-a43e-87b5ee08a1b4"

async def event_wait(evt, timeout):
    # suppress TimeoutError because we'll return False in case of timeout
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(evt.wait(), timeout)
    return evt.is_set()

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """ 
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

async def get_device_by_name(name): 
    device = await BleakScanner.find_device_by_name(name)
    print(device)
    if device is None:
        print("could not connect to {}".format(SENSOR_DEVICE))
        return None
    return device


def handle_disconnect(_: BleakClient):
    print("disconnected")


def build_notifiy_cb(event: asyncio.Event, container): 
    async def notify_callback(sender: BleakGATTCharacteristic, data: bytearray): 
        vals = data.decode('utf-8')
        event.set()
        if data[-1] == 64: 
            vals = vals[:-1]
        container['buffer'] += vals 
        return data.decode('utf-8')
    return notify_callback

def handle_temp_message(data: str, state: State):
    parts = data.split(',')
    for temp in parts: 
        sensor, tmp = temp.split('|')
        state.put("temperatures.{}".format(sensor), tmp)
        

async def start_sensors(loop, dash_state: State): 
    event = asyncio.Event()

    device = await get_device_by_name(SENSOR_DEVICE)
    if device is None: 
        return
    print(device)
    
    client = BleakClient(device, disconnected_callback=handle_disconnect)
    await client.connect()

    print("connected")

    container = {'buffer': ''}
    await client.start_notify(TEMP_CHARACTERISTIC_UUID, build_notifiy_cb(event, container))
    
    async def wait(): 
        is_set = await event_wait(event, 0.5)
        buffer = container['buffer']
        if is_set and len(buffer) > 0: 
            if ord(buffer[-1]) == 0x04: # received a full message 
                handle_temp_message(buffer, dash_state)
                container['buffer'] = ''
        loop.create_task(wait())
    
    async def on_quit(): 
        print('quit called')
        await client.disconnect()

    return wait, on_quit



if __name__ == '__main__':
    print("looking for {}".format(SENSOR_DEVICE))
    loop = asyncio.get_event_loop()
    wait = start_sensors(loop)
    asyncio.run(wait())
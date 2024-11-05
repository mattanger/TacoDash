import obd
import math
connection = obd.OBD('/dev/rfcomm0', baudrate=115200) # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(obd.commands['FUEL_LEVEL']) # send the command, and parse the response

# print(response.value) # returns unit-bearing values thanks to Pint
# print(response.value.to("mph")) # user-friendly unit conversions
print(math.radians(-90))
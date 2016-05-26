import time
from Adafruit_BNO055 import BNO055

# Connect to the motion sensor (BNO055)
bno = BNO055.BNO055()

bnoConnected = False

while not bnoConnected:
    try:
        bno.begin()
        bnoConnected = True

    except:
        print("BNO not connected")
        time.sleep(1)
        continue

print("BNO Connected !!!")

# Get BNO status
status, self_test, error = bno.get_system_status()
print("System status: {0}".format(status))

while True:
    heading, roll, pitch = bno.read_euler()
    print("Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}".format(heading % 360, roll % 360, pitch % 360))
    time.sleep(5)
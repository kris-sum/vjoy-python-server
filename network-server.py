from threading import Thread
from time import sleep
import pyvjoy
import socket

# setup the joystick devices

vjoyDevices = { }

for i in range (1,5):
    try:
        vjoyDevices[i] = pyvjoy.VJoyDevice(i)
        vjoyDevices[i].reset()
        vjoyDevices[i].reset_buttons()
        vjoyDevices[i].reset_povs()
        print("Joystick device " + str(i) + " found")
    except:
        print("Joystick device " + str(i) + " not found")

# listen to network

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", 5001))

print("Server listening on port 5001")

def handleResponse( dataString ):
    dataString = data.decode("utf-8")
    parts = dataString.split(',')

    try:
        joystickId = int(parts[0])
    except:
        print ("Joystick " + parts[0] + " not available")
        return

    if (not (joystickId in vjoyDevices)):
        print ("Joystick " + str(joystickId) + " not available")
        return

    j = vjoyDevices[joystickId]

    if parts[1] == "button":
        try:
            buttonNumber = int(parts[2])
        except:
             print ("Button " + parts[2] + " not valid")
             return
        if parts[3] == "1":
            buttonOn = 1
        else:
            buttonOn = 0

        if (len(parts)>4):
            try:
                delay = int(parts[4])
                myThread = Thread(target=resetButton, args=(delay, j, buttonNumber))
                myThread.start()
            except:
                print ("unknown delay " +parts[4])

        j.set_button(buttonNumber, buttonOn)
        return

    if parts[1] == "axis":
        if parts[2] == "x":
            axis = pyvjoy.HID_USAGE_X
        if parts[2] == "y":
            axis = pyvjoy.HID_USAGE_Y
        if parts[2] == "z":
            axis = pyvjoy.HID_USAGE_Z
        
        if axis is None:
            return

        if parts[3] == "1":
            value = 0x8000        
        elif parts[3] == "-1":
            value = 0x1
        else:
            value = 0x4000

        if (len(parts)>4):
            try:
                delay = int(parts[4])
                myThread = Thread(target=resetAxis, args=(delay, j, axis))
                myThread.start()
            except:
                print ("unknown delay " +parts[4])

        j.set_axis(axis, value)

    if parts[1] == "reset":
        j.reset()
        j.reset_buttons()
        j.reset_povs()
        j.set_axis(pyvjoy.HID_USAGE_X,  0x4000)
        j.set_axis(pyvjoy.HID_USAGE_Y,  0x4000)
        j.set_axis(pyvjoy.HID_USAGE_Z,  0x4000)

    return


def resetAxis(delay, j, axis):
    sleep(delay / 1000.0)
    j.set_axis(axis,  0x4000)

def resetButton(delay, j, buttonNumber):
    sleep(delay / 1000.0)
    j.set_button(buttonNumber, 0)


# start listening loop

while True: 
    data, addr = sock.recvfrom(1024)

    dataString = data.decode("utf-8")
    parts = dataString.split(';')
    for command in parts:
        handleResponse(command)

    handleResponse(data)
    print ("<:", data)

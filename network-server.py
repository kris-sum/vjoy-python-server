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

    joystickId = int(parts[0])

    if (not (joystickId in vjoyDevices)):
        print ("Joystick " + str(joystickId) + " not available")
        return

    j = vjoyDevices[joystickId]

    if parts[1] == "button":
        buttonNumber = int(parts[2])
        if parts[3] == "1":
            buttonOn = 1
        else:
            buttonOn = 0

        j.set_button(buttonNumber, buttonOn)
        return

    if parts[1] == "axis":
        if parts[2] == "x":
            axis = pyvjoy.HID_USAGE_X
        if parts[2] == "y":
            axis = pyvjoy.HID_USAGE_Y
        if parts[2] == "z":
            axis = pyvjoy.HID_USAGE_Z

        if parts[3] == "1":
            value = 0x8000        
        elif parts[3] == "-1":
            value = 0x1
        else:
            value = 0x4000

        j.set_axis(axis, value)

    return

# start listening loop

while True: 
    data, addr = sock.recvfrom(1024)

    dataString = data.decode("utf-8")
    parts = dataString.split(';')
    for command in parts:
        handleResponse(command)

    handleResponse(data)
    print ("<:", data)

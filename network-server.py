import pyvjoy
import socket

#Pythonic API, item-at-a-time

j = pyvjoy.VJoyDevice(1)
j.reset()
j.reset_buttons()
j.reset_povs()

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", 5001))

def handleResponse( dataString ):
    dataString = data.decode("utf-8")
    parts = dataString.split(',')

    if parts[0] == "button":

        buttonNumber = int(parts[1])
        if parts[2] == "1":
            buttonOn = 1
        else:
            buttonOn = 0

        j.set_button(buttonNumber, buttonOn)
        return
    if parts[0] == "axis":

        if parts[1] == "x":
            axis = pyvjoy.HID_USAGE_X
        if parts[1] == "y":
            axis = pyvjoy.HID_USAGE_Y
        if parts[1] == "z":
            axis = pyvjoy.HID_USAGE_Z

        if parts[2] == "1":
            value = 0x8000        
        elif parts[2] == "-1":
            value = 0x1
        else:
            value = 0x4000

        j.set_axis(axis, value)


    return


while True: 
    data, addr = sock.recvfrom(1024)

    dataString = data.decode("utf-8")
    parts = dataString.split(';')
    for command in parts:
        handleResponse(command)

    handleResponse(data)
    print ("<:", data)

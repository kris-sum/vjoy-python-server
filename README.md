Network Server
===

> Pre-requisite: vJoy from http://vjoystick.sourceforge.net/

The server listens to UDP on port 5001. The format is pretty simple, send ascii strings in the following format:

    joystick,inputType,context,state[,resetDelay]

| joystick | inputType | context | state | resetDelay (optional) | description |
| -| - | - | - | - | - | 
| [1-4] | button | [1-9] | [0-1] | - | turns button [1-9] [off-on] on joystick [1-4] |
| [1-4] | button | [1-9] | [0-1] | 100 | presses button [1-9] [off-on] on joystick [1-4] for 100ms |
| [1-4] | axis | [x,y,z] | [-1,0,1] | - | makes joystick [1-4] axis [x,y,z] move [left, neutral, right] |
| [1-4] | axis | [x,y,z] | [-1,0,1] | 200 | makes joystick [1-4] axis [x,y,z] move [left, neutral, right] for 200ms |
| [1-4] | reset |  |  |  | resets joystick [1-4] buttons/pov/axis to neutral |

Examples:

    1,reset: resets joystick 1
    1,button,1,1 : turns joystick 1 button 1 on
    1,button,1,0 : turns joystick 1 button 1 off
    1,button,2,1,50 : taps joystick 1 button 1 (button down for 50ms)
    2,axis,x,-1 : moves joystick 2 left 
    2,axis,x,1 : moves joystick 2 right
    2,axis,y,-1 : moves joystick 2 up 
    2,axis,y,1 : moves joystick 2 down
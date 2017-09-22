Network Server
===

The server listens to UDP on port 5001. The format is pretty simple, send ascii strings in the following format:

    joystick,inputType,context,state

| joystick | inputType | context | state | description |
| -| - | - | - | - | 
| [1-4] | button | [1-9] | [0-1] | turns button [1-9] [off-on] on joystick [1-4], e.g. |
| [1-4] | axis | [x,y,z] | [-1,0,1] | makes joystick [1-4] axis [x,y,z] move [left, neutral, right], e.g. |


    1,button,1,1 : turns joystick 1 button 1 on
    1,button,1,0 : turns joystick 1 button 1 off
    2,axis,x,-1 : moves joystick 2 left 
    2,axis,x,1 : moves joystick 2 right
    2,axis,y,-1 : moves joystick 2 up 
    2,axis,y,1 : moves joystick 2 down
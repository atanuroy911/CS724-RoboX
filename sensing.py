import serial
import time
from pynput import keyboard

evenement=""
print("Start")
port="/dev/cu.HC-05" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick
result = str(0)

def on_key_release(key):
    global result
    #print('released %s' % key)
    #result ='released %s' % key+'\n'
    if result !='stop': #or result == str(2)+'\n' or result == str(3)+'\n' or result == str(4)+'\n':
       result = 'stop'
       print(result)
       result_bytes = result.encode('utf_8')
       bluetooth.write(result_bytes)

def on_key_pressed(key):
    global result       
    #print('pressed %s' % key)
    result1 ='%s' % key
    if result == 'stop':
        if result1=='Key.up' :
           result = 'avant'
           print(result)
        if result1=='Key.down' :
           result = 'backwards'
           print(result)
        if result1=='Key.left' :
           result = 'left'
           print(result)
        if result1=='Key.right' :
           result = 'right'
           print(result)         
        result_bytes = result.encode('utf_8')
        bluetooth.write(result_bytes)

with keyboard.Listener(on_release = on_key_release,on_press=on_key_pressed) as listener:
    listener.join()
from nanpy import (ArduinoApi, SerialManager)
from time import sleep
from nanpy.measure import Measure
def main():
    try:
        connection = SerialManager()
        a = ArduinoApi(connection=connection)
        m = Measure(connection=connection)
    except:
        print("Faild to connect to Arduino Firas")

    # setup the pinMode as is we were in the arduino IDE

    a.pinMode(2, a.OUTPUT)
    a.pinMode(3, a.OUTPUT)
    a.pinMode(4, a.OUTPUT)
    a.pinMode(5, a.OUTPUT)

    try:
        while True:
            forward(a)
            if distance(m,6,7) < 30:
                print("right")
                reverse(a)
                right(a)
            elif distance(m,8,9) < 30:
                print("left")
                reverse(a)
                left(a)
             
    except:
        print("Faild2 ")
        a.digitalWrite(2, a.LOW)
        a.digitalWrite(3, a.LOW)
        a.digitalWrite(4, a.LOW)
        a.digitalWrite(5, a.LOW)

def reverse(a):
    a.digitalWrite(2, a.LOW)
    a.digitalWrite(3, a.HIGH)
    a.digitalWrite(4, a.HIGH)
    a.digitalWrite(5, a.LOW)
    sleep(0.2)
    stop(a)

def forward(a):
    a.digitalWrite(2, a.HIGH)
    a.digitalWrite(3, a.LOW)
    a.digitalWrite(4, a.LOW)
    a.digitalWrite(5, a.HIGH)
    
def right(a):
    a.digitalWrite(2, a.LOW)
    a.digitalWrite(3, a.HIGH)
    a.digitalWrite(4, a.LOW)
    a.digitalWrite(5, a.HIGH)
    sleep(0.2)
    stop(a)

def left(a):
    a.digitalWrite(2, a.HIGH)
    a.digitalWrite(3, a.LOW)
    a.digitalWrite(4, a.HIGH)
    a.digitalWrite(5, a.LOW)
    sleep(0.2)
    stop(a)
    
def stop(a):
    a.digitalWrite(2, a.LOW)
    a.digitalWrite(3, a.LOW)
    a.digitalWrite(4, a.LOW)
    a.digitalWrite(5, a.LOW)

def distance(m,trg,ech):
    distance = m.getMeasure(trg,ech)
    sleep(0.3)
    if(distance < 0):
        distance = distance * -1
        print(distance)
    return distance

main()

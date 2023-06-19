#!usr/bin/python3

# imports
import os
import sys
sys.path.append(os.path.abspath("/home/criti/Documents/Raspberry-PiDal-Switcher/libregpio/src"))
import libregpio as GPIO
import time
import pickle
import pygame


# pedal class
class Loop:
    switch = 0
    saved_pins = []

    def __init__(self, switch, saved_pins):
        self.switch = switch
        self.saved_pins = saved_pins
# end class

# saving to file using pickle
def SaveFile(filename, obj):
    with open(filename, 'wb') as outf:
        pickle.dump(obj, outf, -1)
# end method

# reading file using pickle
def ReadFile(filename):
    with open(filename, 'rb') as inf:
        return pickle.load(inf)
# end method

# Initializing the "savedLoop" variables
def InitializePedals(switch):
    filename = "loop" + str(switch) + ".pkl"
    try:
        return ReadFile(filename)
    except Exception as e:
        return Loop(switch, [])
# end method

# turning pedals on and off based on which switch was pressed 
def ActivatePedals():
    SwitchPedals(loop_pins[
                     int(current) - 1])  # switch pedal based on current key pressed as int  - 1 to account for indexing in python
    print(activePedals)  # debug
# end method

# toggling pedal state
def SwitchPedals(loop):  # loop = pedal loop to be switched
    if loop in activePedals:
        loop.low()
        activePedals.remove(loop)
        print("Loop " + current + " removed")  # debug
    else:
        loop.high()
        activePedals.append(loop)
        print("Loop " + current + " activated")  # debug
# end method

# saving pedals to array and file
def SavePedals():
    savedPedals[int(current) - 1].saved_pins = CopyArr(savedPedals[int(current) - 1].saved_pins, activePedals)
    # save each pedal to its respective file
    for pedal in savedPedals:
        filename = "loop" + str(pedal.switch) + ".pkl"
        SaveFile(filename, pedal)
        print(pedal.switch, pedal.saved_pins)
# end method

# copies contents of one array to another
def CopyArr(arr1, arr2):  # arr1 = target, arr2 = source
    arr1 = []
    for item in arr2:
        arr1.append(item)
    return arr1
# end method

# initialize performance mode
def InitPerformance():
    global activePedals
    for pedal in activePedals:  # turn off current pedals
        pedal.low()
    activePedals = []
# end method

# activates pedals in performance mode
def ActivatePedalsPMode():
    global activePedals

    # turn off current pedals
    for pedal in activePedals:
        pedal.low()
        print("Pin ", pedal, " turned off.")
    if performance_current == current:  # switch pressed was the last one pressed
        return -1

    # copy the saved pedals array into the active pedals array
    activePedals = CopyArr(activePedals, savedPedals[int(current) - 1].saved_pins)

    # turn on current pedals
    for pedal in activePedals:
        pedal.high()
        print("Pin ", pedal, " turned on.")
    return current
# end method

# GPIO Pin Vars
loop_pins = [GPIO.OUT('GPIOX_12'), GPIO.OUT('GPIOX_13'), GPIO.OUT('GPIOX_14'), GPIO.OUT('GPIOX_15'), GPIO.OUT('GPIOX_8'), GPIO.OUT('GPIOX_9'), GPIO.OUT('GPIOX_11'), GPIO.OUT('GPIOX_10')]

# init pygame
pygame.init()
window = pygame.display.set_mode((300, 300))

current = 0  # current switch pressed
performance_current = 0  # previous switch pressed
pressed_time = 0  # time the switch was pressed

performance_mode = False  # performance mode loads the loops created

# loads the loops (either creates a new object or loads the file)
saveLoop = [InitializePedals(1), InitializePedals(2), InitializePedals(3), InitializePedals(4), InitializePedals(5),
            InitializePedals(6), InitializePedals(7), InitializePedals(8)]

# stores the loops for performance mode
savedPedals = [saveLoop[0], saveLoop[1], saveLoop[2], saveLoop[3], saveLoop[4], saveLoop[5], saveLoop[6],
               saveLoop[7]]
activePedals = []  # stores the currently used pedals

mainloop = True
while mainloop:
    for event in pygame.event.get():  # pygame loop
        if event.type == pygame.QUIT:  # debug option force quit
            mainloop = False

        if event.type == pygame.KEYDOWN and current == 0:  # pressed down loop
            current = pygame.key.name(event.key)
            pressed_time = time.time()

            if current == "escape":
                mainloop = False  # debug option force quit
            if current == "/":
                performance_mode = not performance_mode  # toggles performance mode
                InitPerformance()
                current = 0

        if not performance_mode :  # regular mode
            if event.type == pygame.KEYUP and current == pygame.key.name(event.key):
                final_time = time.time() - pressed_time

                if final_time > 1:  # switch held for longer than a second
                    SavePedals()
                else:
                    ActivatePedals()

                current = 0
                pressed_time = 0
        else:  # performance mode
            if event.type == pygame.KEYUP and current == pygame.key.name(event.key):
                performance_current = ActivatePedalsPMode()
                current = 0
    # end loop
# end loop
pygame.quit()
GPIO.cleanup()

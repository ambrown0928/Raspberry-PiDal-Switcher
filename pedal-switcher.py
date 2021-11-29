#!usr/bin/python3

#imports
import RPi.GPIO as GPIO
import time
import _pickle as pickle
import pygame

#pedal class
class Loop:
    switch = 0
    saved_pins = []
    
    def __init__(self, switch, saved_pins):
        self.switch = switch
        self.saved_pins = saved_pins

#Saving to file using pickle
def SaveFile(filename, obj):
    with open (filename, 'wb') as outf:
        pickle.dump(obj, outf, -1)
#end method
        
#Reading File using pickle
def ReadFile(filename) :
    with open (filename, 'rb') as inf:
        return pickle.load(inf)
#end method
    
#Initializing the "savedLoop" variables
def InitializePedals(switch):
    filename = "loop" + str(switch) + ".pkl"
    try:
        return ReadFile(filename)
    except Exception as e:
        return Loop(switch, [])
#end method
    
#Turning pedals on and off based on which switch was pressed 
def ActivatePedals():
    if current == "1":
        SwitchPedals(loop1)
    elif current == "2":
        SwitchPedals(loop2)
    elif current == "3":
        SwitchPedals(loop3)
    elif current == "4":
        SwitchPedals(loop4)
    print(activePedals)
#end method
    
#Toggling pedal state
def SwitchPedals(loop):
    if loop in activePedals:
        GPIO.output(loop, GPIO.LOW)
        activePedals.remove(loop)
        print("Loop " + current + " removed")
    else:
        GPIO.output(loop, GPIO.HIGH)
        activePedals.append(loop)
        print("Loop " + current + " activated")
#end method
        
#Saving pedals to array and file
def SavePedals():
    if current == "1":
        savedPedals[0].saved_pins = CopyArr(savedPedals[0].saved_pins, activePedals)
    elif current == "2":
        savedPedals[1].saved_pins = CopyArr(savedPedals[1].saved_pins, activePedals)
    elif current == "3":
        savedPedals[2].saved_pins = CopyArr(savedPedals[2].saved_pins, activePedals)
    elif current == "4":
        savedPedals[3].saved_pins = CopyArr(savedPedals[3].saved_pins, activePedals)
    #save each pedal to its respective file
    for pedal in savedPedals:
        filename = "loop" + str(pedal.switch) + ".pkl"
        SaveFile(filename, pedal)
        print(pedal.switch, pedal.saved_pins)
#end method
        
#copies contents of one array to another
def CopyArr(arr1, arr2):
    arr1 = []
    for item in arr2:
        arr1.append(item)
    return arr1
#end method

#Initialize Performance Mode
def InitPerformance() :
    global activePedals
    for pedal in activePedals:
        GPIO.output(pedal, GPIO.LOW)
    activePedals = []
#end method
    
#Activates pedals in performance mode
def ActivatePedalsPMode():
    global activePedals
    
    #turn off current pedals
    for pedal in activePedals:
        GPIO.output(pedal, GPIO.LOW)
        print("Pin ", pedal, " turned off.")
    if performance_current == current :
        #switch pressed was the last one pressed
        return -1
    if current == "1":
        activePedals = CopyArr(activePedals, savedPedals[0].saved_pins)
    elif current == "2":
        activePedals = CopyArr(activePedals, savedPedals[1].saved_pins)
    elif current == "3":
        activePedals = CopyArr(activePedals, savedPedals[2].saved_pins)
    elif current == "4":
        activePedals = CopyArr(activePedals, savedPedals[3].saved_pins)
    
    #turn on current pedals
    for pedal in activePedals:
        GPIO.output(pedal, GPIO.HIGH)
        print("Pin ", pedal, " turned on.")
    return current
#end method

#GPIO Pin Vars
loop1 = 3
loop2 = 5
loop3 = 7
loop4 = 11

#init RPi.GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(loop1, GPIO.OUT)
GPIO.setup(loop2, GPIO.OUT)
GPIO.setup(loop3, GPIO.OUT)
GPIO.setup(loop4, GPIO.OUT)

#init pygame (better keeb input and expandablity to display in the future)
pygame.init()
window = pygame.display.set_mode((300,300))

current = 0 # current switch pressed
performance_current = 0 # previous switch pressed
pressed_time = 0 # time the switch was pressed

performance_mode = False # performance mode loads the loops created

#loads the loops (either creates a new object or loads the file)
saveLoop1 = InitializePedals(1)
saveLoop2 = InitializePedals(2)
saveLoop3 = InitializePedals(3)
saveLoop4 = InitializePedals(4)

savedPedals = [saveLoop1, saveLoop2, saveLoop3, saveLoop4] # stores the loops for pmode
activePedals = [] # stores the currently used pedals

mainloop = True
while mainloop:
    if performance_mode == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                
            if event.type == pygame.KEYDOWN and current == 0:
                current = pygame.key.name(event.key)
                pressed_time = time.time()
                if current == "escape":
                    mainloop = False # debug option
                if current == "/":
                    performance_mode = True # changes pedal to pmode 
                    InitPerformance()
                    current = 0
                    
            if event.type == pygame.KEYUP and current == pygame.key.name(event.key):
                final_time = time.time() - pressed_time
                if final_time > 1: # switch held for longer than a second
                    SavePedals()
                else:
                    ActivatePedals()
                current = 0
                pressed_time = 0
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                
            if event.type == pygame.KEYDOWN and current == 0:
                current = pygame.key.name(event.key)

                if current == "escape":
                    mainloop = False
                if current == "/":
                    performance_mode = False
                    current = 0
                    
            if event.type == pygame.KEYUP and current == pygame.key.name(event.key):
                performance_current = ActivatePedalsPMode()
                current = 0
              
pygame.quit()
GPIO.cleanup()
              
              
              
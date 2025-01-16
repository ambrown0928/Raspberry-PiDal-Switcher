#!usr/bin/python3

#imports
import gpiod
import time
import _pickle as pickle
import pygame

# pedal class
class Loop:
    switch = 0
    saved_pins = []
    
    def __init__(self, switch, saved_pins):
        self.switch = switch
        self.saved_pins = saved_pins

# saving to file using pickle
def SaveFile(filename, obj):
    with open (filename, 'wb') as outf:
        pickle.dump(obj, outf, -1)
# end method
        
# reading file using pickle
def ReadFile(filename) :
    with open (filename, 'rb') as inf:
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
    if current == "1":
        SwitchPedals(loop1)
    elif current == "2":
        SwitchPedals(loop2)
    elif current == "3":
        SwitchPedals(loop3)
    elif current == "4":
        SwitchPedals(loop4)
    elif current == "5":
        SwitchPedals(loop5)
    elif current == "6":
        SwitchPedals(loop6)
    elif current == "7":
        SwitchPedals(loop7)
    elif current == "8":
        SwitchPedals(loop8)
    print(activePedals) # debug
# end method
    
# toggling pedal state
def SwitchPedals(loop): # loop = pedal loop to be switched
    if loop in activePedals:
        GPIO.output(loop, GPIO.LOW)
        activePedals.remove(loop)
        print("Loop " + current + " removed") # debug
    else:
        GPIO.output(loop, GPIO.HIGH)
        activePedals.append(loop)
        print("Loop " + current + " activated") # debug
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
def CopyArr(arr1, arr2): # arr1 = target, arr2 = source
    arr1 = []
    for item in arr2:
        arr1.append(item)
    return arr1
# end method

# initialize performance mode
def InitPerformance() :
    global activePedals
    for pedal in activePedals: # turn off current pedals
        GPIO.output(pedal, GPIO.LOW)
    activePedals = []
# end method
    
# activates pedals in performance mode
def ActivatePedalsPMode():
    global activePedals
    
    # turn off current pedals
    for pedal in activePedals:
        GPIO.output(pedal, GPIO.LOW)
        print("Pin ", pedal, " turned off.")
    if performance_current == current : # switch pressed was the last one pressed
        return -1
    
    # copy the saved pedals array into the active pedals array
    activePedals = CopyArr(activePedals, savedPedals[int(current) - 1].saved_pins)

    # turn on current pedals
    for pedal in activePedals:
        GPIO.output(pedal, GPIO.HIGH)
        print("Pin ", pedal, " turned on.")
    return current
# end method

# GPIO Pin Vars
loop1 = 3
loop2 = 5
loop3 = 7
loop4 = 11
loop5 = 13
loop6 = 15
loop7 = 19
loop8 = 21

# init RPi.GPIO and setup pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(loop1, GPIO.OUT)
GPIO.setup(loop2, GPIO.OUT)
GPIO.setup(loop3, GPIO.OUT)
GPIO.setup(loop4, GPIO.OUT)
GPIO.setup(loop5, GPIO.OUT)
GPIO.setup(loop6, GPIO.OUT)
GPIO.setup(loop7, GPIO.OUT)
GPIO.setup(loop8, GPIO.OUT)

# init pygame
pygame.init()
window = pygame.display.set_mode((300,300))

current = 0 # current switch pressed
performance_current = 0 # previous switch pressed
pressed_time = 0 # time the switch was pressed

performance_mode = False # performance mode loads the loops created

# loads the loops (either creates a new object or loads the file)
saveLoop1 = InitializePedals(1)
saveLoop2 = InitializePedals(2)
saveLoop3 = InitializePedals(3)
saveLoop4 = InitializePedals(4)
saveLoop5 = InitializePedals(5)
saveLoop6 = InitializePedals(6)
saveLoop7 = InitializePedals(7)
saveLoop8 = InitializePedals(8)

savedPedals = [saveLoop1, saveLoop2, 
            saveLoop3, saveLoop4,
            saveLoop5, saveLoop6,
            saveLoop7, saveLoop8] # stores the loops for pmode
activePedals = [] # stores the currently used pedals

mainloop = True
while mainloop:
    for event in pygame.event.get(): # pygame loop

        if event.type == pygame.QUIT: # debug option force quit
            mainloop = False

        if event.type == pygame.KEYDOWN and current == 0: # pressed down loop
            current = pygame.key.name(event.key)
            pressed_time = time.time()

            if current == "escape":
                mainloop = False # debug option force quit
            if current == "/":
                performance_mode = not performance_mode # toggles performance mode 
                InitPerformance()
                current = 0

        if performance_mode == False: # regular mode
            if event.type == pygame.KEYUP and current == pygame.key.name(event.key):
                final_time = time.time() - pressed_time
                
                if final_time > 1: # switch held for longer than a second
                    SavePedals()
                else:
                    ActivatePedals()
                
                current = 0
                pressed_time = 0
        else: # performance mode
            if event.type == pygame.KEYUP and current == pygame.key.name(event.key):
                performance_current = ActivatePedalsPMode()
                current = 0

pygame.quit()
GPIO.cleanup()
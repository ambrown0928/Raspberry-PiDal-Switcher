#!usr/bin/python3

# imports
import RPi.GPIO as GPIO
import time
import pickle
import pygame
import os
import errno

# pedal class used to save a performance loop
class Loop:
    switch = 0 # switch associated with this class
    saved_pins = [] # the saved pins inside this
    
    def __init__(self, switch, saved_pins):
        self.switch = switch
        self.saved_pins = saved_pins

# saving to file using pickle
def SaveFile(filename, obj):
    if not os.path.exists(os.path.dirname(filename)): # check directory exists
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # guard against race condition
            if exc.errno != errno.EXIST:
                raise
    # end directory check
    with open (filename, 'wb') as outf:
        pickle.dump(obj, outf, -1)
# end method
        
# reading file using pickle
def ReadFile(filename) :
    with open (filename, 'rb') as inf:
        return pickle.load(inf)
# end method
      
# copies contents of one array to another
def CopyArray(copy_arr):
    arr1 = []
    for item in copy_arr:
        arr1.append(item)
    return arr1
# end method

# initializes the pedal banks by reading the associated file, 
# or returning an empty Loop
def InitializePedalBank(bank, switch):
    filename = f'/bank{bank}/loop{switch}.pkl'
    try:
        return ReadFile(filename)
    except Exception as e:
        return Loop(switch, [])
# end method
    
# activate an individual pedal based on the switch pressed
def ActivatePedalNormalMode():        
    switch =  int(current_switch_pressed) - 1;
    SwitchPedalsNormalMode(switch);
    print(active_pedals) # debug
# end method
    
# toggling pedal state
def SwitchPedalsNormalMode(loop): # loop = pedal to be switched
    if loop >= max_switch_count:
        return
    if loops[loop] in active_pedals:
        GPIO.output(loop, GPIO.LOW)
        active_pedals.remove(loops[loop])
        print(f'Pin {loops[loop]} at switch {current_switch_pressed} removed') # debug
    else:
        GPIO.output(loop, GPIO.HIGH)
        active_pedals.append(loops[loop])
        print(f'Pin {loops[loop]} at switch {current_switch_pressed} added') # debug
# end method
        
# saves pedals to array and file
def SavePedalsToFile():
    bank_key = f'bank{current_bank}'
    index = int(current_switch_pressed) - 1
    if index >= max_switch_count:
        return
    banks[bank_key][index].saved_pins = CopyArray(active_pedals)
    # save each pedal to its respective file
    for pedal in banks[bank_key]:
        filename = f'/{bank_key}/loop{pedal.switch}.pkl'
        SaveFile(filename, pedal)
        print(pedal.switch, pedal.saved_pins) # debug
# end method

# used when toggling performance mode
def ResetActivePedals() :
    global active_pedals
    for pedal in active_pedals: # turn off current pedals
        GPIO.output(pedal, GPIO.LOW)
    active_pedals = []
# end method

# iterate through the active pedals array and
# set the state to the parameter proviced
def SetActivePedalsState(gpio_state):
    for pedal in active_pedals:
        GPIO.output(pedal, gpio_state)
        print(f'Pin {pedal} is set to { gpio_state }') # debug
# end method

# passes is_temp bool to check for a temporary 
# pedal switch
def ActivatePedalsPerformanceMode(is_temp):
    # necessary bc python sucks :(
    global active_pedals
    global previous_pedals
    global performance_previous_switch_pressed
    
    SetActivePedalsState(GPIO.LOW)

    if performance_current_switch_pressed == current_switch_pressed : # switch pressed was the last one pressed
        if is_temp and performance_previous_switch_pressed != -1: # switching between 2 loops
            active_pedals = CopyArray(previous_pedals);
            SetActivePedalsState(GPIO.HIGH)
            return performance_previous_switch_pressed
        # end temporary check
        active_pedals = []
        return -1
    # end off check

    previous_pedals = CopyArray(active_pedals);
    # copy banked pedals into the active pedals
    bank_key = f'bank{current_bank}'
    index = int(current_switch_pressed) - 1
    active_pedals = CopyArray(banks[bank_key][index].saved_pins)

    # activate pedals
    SetActivePedalsState(GPIO.HIGH)
    print(active_pedals) # debug
    performance_previous_switch_pressed = performance_current_switch_pressed
    return current_switch_pressed
# end method

# stores a reference to the GPIO pins used. whenever we
# want to toggle a pedal in normal mode, we need to reference 
# this array. 
loops = [3, 5, 7, 11, 13, 15, 19, 21];

# init RPi.GPIO and setup pins
GPIO.setmode(GPIO.BOARD)
for loop in loops:
    GPIO.setup(loop, GPIO.OUT)
# end loop

# init pygame
pygame.init()
window = pygame.display.set_mode((300,300))

previous_switch_pressed = 0
performance_previous_switch_pressed = 0 # previous performance loop activated
current_switch_pressed = 0
performance_current_switch_pressed = 0 # current active performance loop

max_switch_count = 8 # adjust depending on number of switches desired

pressed_time = 0 
released_time = 0 
press_release_interval = 0 # time between release and press

performance_mode = False # performance mode loads the loops created

banks = { }
max_bank_count = 16 # change this to increase the maximum number of banks
current_bank = 0

# init banks
for x in range(max_bank_count):
    bank_key = f'bank{x}'
    banked_pedals = []
    for y in range(max_switch_count):
        banked_pedals.append(InitializePedalBank(x, y + 1))
    # end loop
    banks[bank_key] = banked_pedals
# end loop

active_pedals = [] # stores the currently used pedals as GPIO pins
previous_pedals = [] # used in performance mode to save previous pedals

mainloop = True
while mainloop:
    for event in pygame.event.get(): # pygame loop
        if event.type == pygame.QUIT: # debug option force quit
            mainloop = False
        # end force quit check
        if event.type == pygame.KEYDOWN and current_switch_pressed == 0:

            # get current switch and mark the time it was pressed
            current_switch_pressed = pygame.key.name(event.key)
            pressed_time = time.time()
            press_release_interval = pressed_time - released_time;

            # if user pressed a switch again in a short time, and the previous switch
            # is equal to the current switch, then the user was trying to save
            # a pedal configuration to the switch pressed (or toggle performance
            # mode if the switch was the bank switch.) 
            # 
            # note: due to the way this program works, we have to reset the state of
            # whatever switch was pressed, otherwise the pedal will run into
            # weird bugs with if the pedal is currently activated or the bank is the 
            # correct, current bank.
            if press_release_interval < 0.3 and previous_switch_pressed == current_switch_pressed:
                if current_switch_pressed == "/":  # toggle performance mode 
                    current_bank = current_bank - 1 # reduce bank to previous one
                    performance_mode = not performance_mode
                    ResetActivePedals()
                    current_switch_pressed = 0
                elif not performance_mode: # save pedal bank
                    ActivatePedalNormalMode() # retoggle pedal associated w/switch
                    SavePedalsToFile()
                continue # skip the rest of the code
            # end save pedals check

            if current_switch_pressed == "escape":
                mainloop = False # debug option force quit
            elif current_switch_pressed == "/": # move up in bank
                if current_bank == max_bank_count - 1:
                    current_bank = 0
                else:
                    current_bank = current_bank + 1
                print(f'bank{current_bank}')
            elif performance_mode:
                performance_current_switch_pressed = ActivatePedalsPerformanceMode(False)
            else:
                ActivatePedalNormalMode()
            # end key check
        # end pressed check
        if event.type == pygame.KEYUP and current_switch_pressed == pygame.key.name(event.key):
            released_time = time.time();
            time_difference = released_time - pressed_time

            if time_difference > 0.5: # switch held for longer than half a second, meaning its a temporary activation
                if current_switch_pressed == "/": # go down on the banks
                    # we go down 2 because the bank is always increased
                    # when the footswitch is pressed, regardless of 
                    # how long it was held down
                    if current_bank == 1:
                        current_bank = max_bank_count - 1
                    elif current_bank == 0:
                        current_bank = max_bank_count - 2
                    else:
                        current_bank = current_bank - 2;
                    print(f'bank{current_bank}') # debug
                elif performance_mode:
                    performance_current_switch_pressed = ActivatePedalsPerformanceMode(True)
                else:
                    ActivatePedalNormalMode() # toggle pedal
                # end performance mode check
            # end temporary activation check
            
            previous_switch_pressed = current_switch_pressed
            current_switch_pressed = 0
        # end released check
    # end pygame loop
# end main loop
pygame.quit()
GPIO.cleanup()
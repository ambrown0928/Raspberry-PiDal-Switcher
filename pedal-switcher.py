#!usr/bin/python3

# imports
import RPi.GPIO as GPIO
import led_controller
import time
import pickle
import pygame
import os
import errno

class Loop:
    """
    This class is used in the saving and loading of performance
    loops. It stores the switch associated with the loop, and the
    pins that are saved on that switch.
    """
    switch = 0 # switch associated with this loop
    saved_pins = [] # the saved pins inside this loop
    
    def __init__(self, switch, saved_pins):
        self.switch = switch
        self.saved_pins = saved_pins

# saving to file using pickle
def SaveFile(filename, obj):
    """
    This method is used to save a performance loop to a file.
    We use Python's Pickle library when saving.

    Args:
        filename (string): The directory and filename to save the performance loop to.
        obj (Loop): The loop to save in the file.
    """
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
        
def ReadFile(filename) :
    """
    This method reads an object at the given filename
    and returns the data stored there. We use Python's
    Pickle library when saving.

    Args:
        filename (string): The directory and filename to load from.
    Returns:
        Loop: the performance loop stored in the file.
    """
    with open (filename, 'rb') as inf:
        return pickle.load(inf)
# end method
      
def CopyList(list):
    """
    Creates a copy of a list to replace another list. 

    Args:
        list (List): The list to copy.

    Returns:
        List: a copied version of the list.
    """
    arr1 = []
    for item in list:
        arr1.append(item)
    return arr1
# end method

def InitializePedalBank(bank, switch):
    """
    Initialize a pedal bank and switch by reading the 
    file at the given location. If there's no file 
    associated with that location, return a new loop
    with the switch and an empty list of pins.

    Args:
        bank (int): The bank the loop is saved in.
        switch (int): The switch the loop is saved in.

    Returns:
        Loop: returns either the saved loop or a new loop
        with the switch and an empty list of saved pins.
    """
    filename = f'/bank{bank}/loop{switch}.pkl'
    try:
        return ReadFile(filename)
    except Exception as e:
        return Loop(switch, [])
# end method
    
def TogglePedalNormalMode():        
    """
    Toggles a pedal in normal mode. The pedal to toggle is gotten
    from the current_switch_pressed field, which is global and 
    assigned based on the switch the user presses.
    """
    switch =  int(current_switch_pressed) - 1;
    pin = loops[switch] # GPIO pin associated with switch/pedal
    if switch >= max_switch_count:
        return
    if pin in active_pedals: # turn pedal off
        GPIO.output(pin, GPIO.LOW)
        active_pedals.remove(pin)
        print(f'Pin {pin} at switch {current_switch_pressed} removed') # debug
    else: # turn pedal on
        GPIO.output(pin, GPIO.HIGH)
        active_pedals.append(pin)
        print(f'Pin {pin} at switch {current_switch_pressed} added') # debug
    led_controller.ToggleLEDNormalMode(switch)
    print(active_pedals) # debug
# end method
        
def SavePedalsToFile():
    """
    Saves the current configuration of active pedals to the 
    current bank and switch. Uses the current_bank and the
    current_switch_pressed fields, which are defined and 
    manipulated outside of this method.
    """
    bank_key = f'bank{current_bank}'
    index = int(current_switch_pressed) - 1
    if index >= max_switch_count:
        return
    banks[bank_key][index].saved_pins = CopyList(active_pedals)
    led_controller.FlashLEDOnSave(index);
    # save each pedal to its respective file
    for pedal in banks[bank_key]:
        filename = f'/{bank_key}/loop{pedal.switch}.pkl'
        SaveFile(filename, pedal)
        print(pedal.switch, pedal.saved_pins) # debug
# end method

def ResetActivePedals() :
    """
    Turns off all the active pedals in the active_pedals
    list, and then clears the list of all pedals. This 
    method is mostly used when toggling performance mode,
    so as to avoid any overlap with currently active pedals.
    """
    global active_pedals
    SetActivePedalsState(GPIO.LOW)
    led_controller.TurnOffAllLEDs()
    active_pedals = []
# end method

# iterate through the active pedals array and
# set the state to the parameter proviced
def SetActivePedalsState(gpio_state):
    """
    Changes the state of all the pedals in the active_pedals
    list to be the state provided. Before using this function,
    make sure that the active_pedals list is set to the pedals
    you want to turn on or off.

    Args:
        gpio_state (GPIO): The state to set the pedals to. Make sure to only pass GPIO.LOW or GPIO.HIGH.
    """
    for pedal in active_pedals:
        GPIO.output(pedal, gpio_state)
        print(f'Pin {pedal} is set to { gpio_state }') # debug
# end method

# passes is_temp bool to check for a temporary 
# pedal switch
def TogglePedalsPerformanceMode(is_temp : bool):
    """
    Toggles a performance loop on or off. If the is_temp parameter
    is true, that means that we're releasing the switch, and we
    want to re-activate the previous performance loop.

    Args:
        is_temp (bool): If true, then we're performing a temporary activation.

    Returns:
        int: We return the current_switch_pressed and set it to the current_performance_loop, 
        which is used to store the current performance loop that is active. If we're deactivating
        a performance loop, then we return -1, so that the program is aware that we don't have an
        active performance loop.
    """
    # necessary bc python sucks :(
    global active_pedals
    global previous_pedals
    global previous_performance_loop
    
    SetActivePedalsState(GPIO.LOW)
    led_controller.ToggleLEDPerformanceMode(current_performance_loop)

    if current_performance_loop == current_switch_pressed : # switch pressed was the last one pressed
        if is_temp and previous_performance_loop != -1: # switching between 2 loops
            active_pedals = CopyList(previous_pedals);
            SetActivePedalsState(GPIO.HIGH)
            led_controller.ToggleLEDPerformanceMode(previous_performance_loop)
            return previous_performance_loop
        # end temporary check
        active_pedals = []
        return -1
    # end off check

    previous_pedals = CopyList(active_pedals);
    # copy banked pedals into the active pedals
    bank_key = f'bank{current_bank}'
    index = int(current_switch_pressed) - 1
    active_pedals = CopyList(banks[bank_key][index].saved_pins)

    # activate pedals
    SetActivePedalsState(GPIO.HIGH)
    led_controller.ToggleLEDPerformanceMode(current_switch_pressed)
    print(active_pedals) # debug
    previous_performance_loop = current_performance_loop
    return current_switch_pressed
# end method

# use to move up or down in banks. when using, pass a 
# bool to tell the function whether you're moving up
# or down in the banks.
def ChangeBank(move_up : bool):
    """
    Change the current bank. 

    Args:
        move_up (bool): lets the function know whether we're moving up or down in the bank.
    """
    if move_up:
        if current_bank == max_bank_count - 1: # loop
            current_bank = 0
        else:
            current_bank = current_bank + 1
    else:
        # we go down by 2 because the bank is always increased
        # when the footswitch is pressed, regardless of 
        # how long it was held down
        if current_bank == 1:
            current_bank = max_bank_count - 1
        elif current_bank == 0:
            current_bank = max_bank_count - 2
        else:
            current_bank = current_bank - 2;
    led_controller.ChangeCurrentColor(current_bank)
    print(f'bank{current_bank}') # debug

    # if we're in performance mode, we want to
    # reset the active pedals, so we don't get 
    # any weirdness with the active pedal bank
    # not being associated with the current 
    # switch/bank combo.
    if performance_mode:
        ResetActivePedals()
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
window = pygame.display.set_mode((800,480))

previous_switch_pressed = 0
previous_performance_loop = 0 # previous performance loop activated
current_switch_pressed = 0
current_performance_loop = 0 # current active performance loop

max_switch_count = 8 # adjust depending on number of switches desired

pressed_time = 0 
released_time = 0 
press_release_interval = 0 # time between release and press

performance_mode = False # performance mode loads the loops created
active_pedals = [] # stores the currently used pedals as GPIO pins
previous_pedals = [] # used in performance mode to save previous pedals

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
                    TogglePedalNormalMode() # retoggle pedal associated w/switch
                    SavePedalsToFile()
                continue # skip the rest of the code
            # end save pedals check

            if current_switch_pressed == "escape":
                mainloop = False # debug option force quit
            elif current_switch_pressed == "/": # move up in bank
                ChangeBank(True)
            elif performance_mode:
                current_performance_loop = TogglePedalsPerformanceMode(False)
            else:
                TogglePedalNormalMode()
            # end key check
        # end pressed check
        if event.type == pygame.KEYUP and current_switch_pressed == pygame.key.name(event.key):
            released_time = time.time();
            time_difference = released_time - pressed_time

            if time_difference > 0.5: # switch held for longer than half a second, meaning its a temporary activation
                if current_switch_pressed == "/": # go down on the banks
                    ChangeBank(False)
                elif performance_mode:
                    current_performance_loop = TogglePedalsPerformanceMode(True)
                else:
                    TogglePedalNormalMode() # toggle pedal
                # end performance mode check
            # end temporary activation check
            
            previous_switch_pressed = current_switch_pressed
            current_switch_pressed = 0
        # end released check
    # end pygame loop
# end main loop
pygame.quit()
GPIO.cleanup()
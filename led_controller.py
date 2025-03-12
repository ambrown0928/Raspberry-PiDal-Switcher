import time
import board
import neopixel
import atexit

leds = neopixel.NeoPixel(board.D18, 30, brightness=1)

RGB_OFF = (0, 0, 0)
# bank color definitions
RGB_YELLOW = (255, 255, 0)
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_BLUE = (0, 0, 255)
RGB_ORANGE = (255, 96, 0)
RGB_PURPLE = (147, 0, 255)
RGB_CYAN = (0, 255, 255)
RGB_SALMON = (255, 100, 100)
RGB_FOREST = (0, 70, 0)
RGB_NAVY = (0, 0, 59)
RGB_MAGENTA = (255, 0, 255)
RGB_BRICK = (220, 20, 60)
RGB_LEAF = (127, 255, 0)
RGB_TEAL = (0, 130, 130)
RGB_BROWN = (129, 59, 9)
RGB_WHITE = (255, 255, 255)

# array storing all colors in order of how we want
# them to be displayed as bank colors
colors = [RGB_RED, RGB_BLUE, RGB_GREEN, RGB_YELLOW,
          RGB_PURPLE, RGB_LEAF, RGB_TEAL, RGB_NAVY,
          RGB_BROWN, RGB_FOREST,  RGB_MAGENTA, RGB_SALMON,
          RGB_CYAN, RGB_BRICK, RGB_ORANGE, RGB_WHITE]

current_bank_color = colors[0] 
normal_color = colors[0] # RGB_RED is the color for normal mode.
bank_switch = 8 # index of LED for bank switch. change depending on number of switches.

def TurnOffAllLEDs():
    """ 
    This method is used to turn off all the LEDs
    except for the bank switch, which is set to the
    current bank color.
    """
    leds.fill(RGB_OFF)
    leds[bank_switch] = current_bank_color
# end method

def SetLED(current_switch, color):
    """
    This method is used to change the color a specific LED
    currently has.

    Args:
        current_switch (int): The current LED index to change.
        color (Tuple): The color to set the LED to.
    """
    leds[current_switch] = color
# end method 

def ChangeCurrentBankColor(bank):
    """ 
    This method is used to change the current
    bank color.

    Args:
        bank (int): The index of the current bank. 
    """
    global current_bank_color
    if bank > len(colors):
        return
    current_bank_color = colors[bank]
    leds[bank_switch] = current_bank_color
# end method

def ChangeNormalColor(second_layer : bool) :
    """
    This method is used to change the current normal
    color. It switches between blue and red depending 
    on what layer the user is on.

    Args:
        second_layer (bool): Whether the user is on layer one or layer two.
    """
    global normal_color
    FlashLED(bank_switch)
    if second_layer:
        normal_color = RGB_BLUE
    else:
        normal_color = RGB_RED
# end method 

def FlashLED(current_switch):
    """
    This method is called when a performance loop is saved. 
    When the loop is saved, we want to flash the LED with the 
    current bank color to show that the save went through successfully.
    After that, we change the LED back to whatever previous state it was in.

    Args:
        current_switch (int): The current switch LED to flash.
    """
    saved_color = leds[current_switch];
    for x in range(5):
        leds[current_switch] = current_bank_color;
        time.sleep(0.1)
        leds[current_switch] = RGB_OFF;
        time.sleep(0.1)
    # end loop
    leds[current_switch] = saved_color;
# end method

def TogglePerformanceMode(performance_mode):
    """
    This method is called when toggling performance mode.
    Args:
        performance_mode (bool): whether performance mode is on or off.
    """
    color = normal_color
    if performance_mode:
        color = current_bank_color
    Wave(color, 0.25)
# end method

def Startup():
    """
    This method is called on startup.
    """
    Wave(RGB_FOREST, 0.5)
    TurnOffAllLEDs()
# end method

def Shutdown():
    """
    This method is called on shutdown.
    """
    Wave(RGB_RED, 0.5)
# end method

def Wave(color, wait_time):
    for i in range(9):
        leds[i] = color
        wait_time.sleep(0.05)
    time.sleep(wait_time)
    for i in range(9):
        leds[i] = RGB_OFF
        wait_time.sleep(0.05)
    time.sleep(wait_time)
# end method

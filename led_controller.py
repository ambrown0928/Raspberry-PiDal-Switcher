import time
import board
import neopixel

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
RGB_SALMON = (245, 141, 149)
RGB_FOREST = (20, 71, 0)
RGB_NAVY = (12, 12, 59)
RGB_MAGENTA = (255, 0, 255)
RGB_BRICK = (130, 0, 0)
RGB_LEAF = (191, 255, 191)
RGB_SKY = (191, 254, 255)
RGB_PINK = (255, 191, 255)
RGB_WHITE = (255, 255, 255)

# array storing all colors in order of how we want
# them to be displayed as bank colors
colors = [RGB_RED, RGB_BLUE, RGB_GREEN, RGB_YELLOW,
          RGB_PURPLE, RGB_LEAF, RGB_ORANGE, RGB_NAVY,
          RGB_PINK, RGB_FOREST, RGB_SKY, RGB_SALMON,
          RGB_CYAN, RGB_MAGENTA, RGB_BRICK, RGB_WHITE]

current_bank_color = colors[0] 
normal_color = colors[0] # RGB_RED is the color for normal mode.
bank_switch = 8 # index of LED for bank switch. change depending on number of switches.

leds.fill(RGB_OFF)
leds[bank_switch] = current_bank_color

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
async def ChangeNormalColor(second_layer : bool) :
    global normal_color
    await FlashLEDOnSave(bank_switch)
    if second_layer:
        normal_color = RGB_BLUE
    else:
        normal_color = RGB_RED

def TurnOffAllLEDs():
    """ 
    This method is used to turn off all the LEDs
    except for the bank switch, which is set to the
    current bank color.
    """
    leds.fill(RGB_OFF)
    leds[bank_switch] = current_bank_color

def Shutdown():
    leds.fill(RGB_OFF)

def ToggleLED(current_switch, color):
    """
    This method is used to toggle an LED in normal
    mode. The default LED color in normal mode is red.

    Args:
        current_switch (int): The current switch LED to toggle.
        color (Tuple): The color to set the LED to.
    """
    leds[current_switch] = color
# end method 

def FlashLEDOnSave(current_switch):
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
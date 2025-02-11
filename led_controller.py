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

# used to change the bank color. called by the ChangeBank function 
# in pedal-switcher.py
def ChangeCurrentColor(bank):
    global current_bank_color
    if bank > colors.count:
        return
    current_bank_color = colors[bank]
    leds[bank_switch] = current_bank_color

# used to turn off all the switch LEDs except for the bank LED
def TurnOffAllLEDs():
    leds.fill(RGB_OFF)
    leds[bank_switch] = current_bank_color

# toggles the LED in normal mode, which is the red color
def ToggleLEDNormalMode(current_switch):
    if leds[current_switch] == normal_color:
        leds[current_switch] = RGB_OFF
    else:
        leds[current_switch] = normal_color

# when a performance loop is saved, we flash the led associated
# with the switch pressed. we use the color associated with the 
# current bank. after flashing, it returns the led to its previous
# color
def FlashLEDOnSave(current_switch):
    saved_color = leds[current_switch];
    for x in range(5):
        leds[current_switch] = current_bank_color;
        time.sleep(0.1)
        leds[current_switch] = RGB_OFF;
        time.sleep(0.1)
    leds[current_switch] = saved_color;

# toggle the LED in performance mode, which uses the current bank color
def ToggleLEDPerformanceMode(current_switch):
    if leds[current_switch] == current_bank_color:
        leds[current_switch] = RGB_OFF
    else:
        leds[current_switch] = current_bank_color
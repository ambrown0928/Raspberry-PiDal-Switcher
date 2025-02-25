# Raspberry-PiDal-Switcher

Hello everyone! This project is an open source Raspbery Pi-based programmable guitar pedal loop switcher. The idea behind this was to create a fairly easy to understand program for a DIY programmable loop switcher. This project is still under development, and so there's going to be kinks, missing parts, and other issues. If you run into anything, please let me know through GitHub!

## Definitions

Here we define some commonly used terms to help keep everyone on the same page:

- Loop: a loop is defined as a send and return signal that can be toggled on and off. 
- Normal mode: normal mode is the setting that allows the user to activate a loop that corresponds to the adjacent switch. By default, the pedal is in normal mode.
- Normal loop: a normal loop means that one switch is related to one loop, and activating that switch activates the corresponding loop. 
- Performance mode: performance mode is the setting that allows the user to activate a series of loops with one switch. By default, the pedal is *not* in performance mode.
- Performance loop: a performance loop means that one switch is related to one saved set of pedals, and activating that switch activates all the loops that correspond to that switch.
- Bank: a bank contains the saved performance loops for each switch on the looper. 

## Current Features

This is the current features this program supports:

- Support for up to 8 loops.
- Both a normal loop switcher mode and a performance mode.
- 16 banks that store 8 peformance loops per bank. This is a total of 128 presets.
- Temporary activation for both normal and performance loops.
- Effects loop support at any point in board.

## Upcoming Features

These are features that are either currently planned for the future, something to like to implement at some point, or is an interesting idea to consider as this project develops over time.

- Screen support. Some good candidates for screens are [here](https://www.crystalfontz.com/product/cfam800480a1050tr-800x480-resistive-touch-tft), [here](https://www.crystalfontz.com/product/cfaf800480h0043sn-800x480-4-point-3-inch-tft-display#variant), and [here](https://www.crystalfontz.com/product/cfaf800480e3050sn-5-inch-sunlight-readable-tft#variant). For the last two, we'd need a decoder board found [here](https://www.adafruit.com/product/2218), which will take the 40 pin connector and translate it to Mini HDMI, allowing for the RasPi to read the screen.
    - For this, we'd also want to use PyGame to display graphics relating to pedals, and ideally allow for users to name each loop, both normal and performance.
- Crosspoint matrix chip integration and a control interface, which would first require screen support and the implementation of some kind of control mechanism to manage messing with loops. A crosspoint matrix chip would allow for the user to change the signal path of the pedals dynamically, and we could then save that configuration into the performance loop and load them dynamically, allowing for an even wider range of pedal configurations. The control mechanism could be implemented with a rotary encoder and/or a touchscreen, depending on which method seems better. Some options for this chip are the [AD75019](https://www.mouser.com/ProductDetail/Analog-Devices/AD75019JPZ?qs=sGAEpiMZZMsjXX4loUgemlnmSwwFOzcQth1JP4lDvw4%3D) or the [AD8113](https://www.mouser.com/ProductDetail/Analog-Devices/AD8113JSTZ?qs=sGAEpiMZZMsjXX4loUgemlnmSwwFOzcQ7J3VrJvWq5g%3D).
    - An important note / extra feature to consider: if we want to add the ability to add parallel pedals, then we should go for the AD75019, as it allows for multiple outputs and inputs to be connected to each other, whereas the AD8113 can only connect one input to one output. 
- A smoother build process and a build guide. This includes proper mounting for components, better drilling templates for consistency, and a comprehensive BOM with links to the necessary parts. 
    - Ideally, we'd also have multiple stages / parts to the build guide, depending on what features the builder wants. For example, if someone doesn't want screen support or the crosspoint matrix chip, they could choose to exclude them, and we should have a part in the build guide that explains how to do that. 
- DC Output Jack. Currently, this project uses the RasPi USB-C connector for power. The main desirability for this is to provide easy implementation with existing pedalboard power supplies, and to add power for multiple different voltages and current, which is a much, much larger task.
    - Currently being worked on, though this will probably require 12-18v and 1.5A of power.
- 2 enclosure support (separate footswitch and loop modules, the main thing that we'd need for this is QMK LED support)
- Support for RasPi alternatives

Current items being worked on

- Build guide & documentation for code
- Drill templates

# Usage

To use this pedal, you must first plug in the power supply. The pedal takes a few seconds to start up, due to the Raspberry Pi booting up. Make sure your guitar is plugged into the "in" jack and the "out" jack goes to your amp. 

Initially, the pedal starts in normal mode. Pressing a switch will toggle a normal loop on and off. If you hold a switch down for more than half a second, the normal loop will toggle back to the previous state (if you turned the pedal on with the initial press, it will turn off, and vice versa for the pedal being off with the initial press.) Double tapping a switch will save the current pedal configuration to that switch in that bank.

You will notice that there are 9 switches total, with one of the switches being offset from the other switches. That switch is the bank switch, and controls the current bank and access to performance mode. Pressing the switch moves up in the bank, and holding the switch down for more than half a second moves down in the bank. Double tapping the switch toggles performance mode.

When the pedal is in performance mode, pressing a switch will toggle the performance loop associated with that switch in that bank. If the same switch is held for longer than half a second, the performance loop will toggle back to the previous state. If one performance loop is active, and another switch is held for longer than half a second, the performance loop associated with the second switch will be active as long as that switch is held, and once that switch is released, the previous performance loop will be re-activated.

# Getting Started

Here are some of the things you will need to build this project:

Required Hardware:

- Raspberry Pi 4 (w/Power Supply)
- Relays:
    - 1 [Relay PCB](https://oshpark.com/shared_projects/E13yHJUb)
    - 8 PIC12F675 Microcontrollers (or PIC16F18313 microcontrollers)
    - 8 Takamisawa NA05W-K Relays
    - PICKit (Any version should work fine)
    - 8 LED Diodes (any color works fine, as long as they're only 2 pin. Red Recommended)
    - 8 10k Ohm Resistors
    - 8 1n4148 Resistors
    - 1 1n5817 Resistor
    - 1 100uF 10V Electrolytic Capacitor
- Switches:
    - 1 [Switch PCB](https://oshpark.com/shared_projects/9jM2bbMc)
    - 1 Pro Micro
    - 9 SPST Switches
    - 9-10 1n4148 Diodes
    - 1 Micro USB to USB-A Cable
- An at least 17" x 4" Enclosure (here's a [link](https://www.mouser.com/ProductDetail/546-1441-20BK3) to one I recommend, as well as the [bottom plate](https://www.mouser.com/ProductDetail/546-1431-20BK3))
- A lot of wire (a few with pin ends to connect to the Raspberry Pi)
- Soldering Iron
- Solder

Optional Hardware
- Rotary Encoder with Push Button Switch

Software and Dependencies:

- MPLabX IDE
- XC8 Compiler
- Python 3.13 (or latest version)
- RPi.GPIO
- Pickle
- PyGame
- QMK Firmware
- Time
- Board
- Neopixel

BUILD GUIDE UNDER CONSTRUCTION
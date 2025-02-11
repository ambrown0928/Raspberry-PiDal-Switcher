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

## Planned Features

These are features that are planned to be implemented in the future:

- 2 enclosure support (separate footswitch and loop modules, the main thing that we'd need for this is QMK LED support)
- Screen support 
- Send-Return for effects loops integration. This would entail adding a split in the loops, meaning 4 loops outside of the effects loop and 4 loops inside the effects loop. You'd also want to use switching jacks, so if nothing is plugged in, the pedal will still work.
- Smoother build process
- 9V Output Jack (currently uses RasPi USB-C connector. The main desirability for this is to provide easy implementation with existing pedalboard power supplies.)
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
- 1 PCB ([Link Here](https://oshpark.com/shared_projects/JoNTOCQh))
- 8 PIC12F675 Microcontrollers
- 8 Takamisawa NA05W-K Relays
- PICKit (Any version should work fine)
- 8 LED Diodes (any color works fine, as long as they're only 2 pin)
- 8 10k Ohm Resistors
- 8 1n4148 Resistors
- 1 1n5817 Resistor
- 1 100uF Electrolytic Capacitor
- 1 Pro Micro
- 9 SPST Switches
- 1 Micro
- A lot of wire (a few with pin ends to connect to the Raspberry Pi)
- Soldering Iron
- Solder

Software and Dependencies:

- MPLabX IDE
- XC8 Compiler
- Python 3.13 (or latest version)
- RPi.GPIO
- Pickle
- Pygame
- QMK Firmware

BUILD GUIDE UNDER CONSTRUCTION
# Raspberry-PiDal-Switcher

Hello all! This project is an open source Raspbery Pi-based programmable guitar pedal loop switcher. The idea behind this was to create a fairly easy to understand program for a DIY programmable loop switcher. This is still under development. 

Current Features:

- Support for up to 8 different guitar pedal loops.
- Both a standard and a programmable mode (aka performance mode)

Planned Features:

- 2 enclosure support (separate footswitch and main module)
- Screen Support
- Smoother Build Process
- 9V Output Jack (currently uses RasPi Re)

## Getting Started

Here are some of the things you will need to build this project:

Hardware:

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

Software:

- MPLabX IDE
- XC8 Compiler
- RPi.GPIO
- _Pickle (Pickle but written in C)
- Pygame
- QMK Firmware

BUILD GUIDE UNDER CONSTRUCTION
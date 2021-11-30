/* 
 * File:   newmain.c
 * Author: The_N
 *
 * Created on October 1, 2021, 10:43 PM
 */

#include <stdio.h>
#include <stdlib.h>

// Extra Libraries
#include <stdint.h>
#include <xc.h>

// Config File
#include "header.h"
/*
 * Design for this inspired by CODA Effects
 */
void main(void)
{
    ANSEL = 0; // no analog GPIO
    CMCON = 0x07; // comparator off 
    ADCON0 = 0; // ADC and DAC converters off
    
    uint8_t state; // pedal's state
    state = 0;
    
    uint8_t change_state;
    change_state = 0;
    
    uint8_t press_switch;
    press_switch = 0;
    
    TRISIO0 = 0; // pin 7 is an output (0 like "Output")
    TRISIO3 = 1;
    TRISIO2 = 0;
    TRISIO4 = 0;
    TRISIO5 = 0;
    TRISIO1 = 1; // pin 6 is an input (1 as "Input")
    
    GPIO=0; // all the GPIOs are in low state (0V) when starting
    
    while(1)
    {
        
        if(GP1 == 1)
        { // on
            GP0 = 1;
            GP5 = 1;
            GP4 = 0;
        }
        else
        { // off
            GP0 = 0;
            GP5 = 0;
            GP4 = 0;
        }
    }
}
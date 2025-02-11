/* 
 * File:   newmain.c
 * Author: Tony Brown
 *
 * Created on October 1, 2021, 10:43 PM
 * Last Updated on April 6th, 2023, 5:45pm
 */

#include <stdio.h>
#include <stdlib.h>

// Extra Libraries
#include <stdint.h>
#include <xc.h>

// Config File
#include "header.h"
/*
 * 
 */
void main(void)
{
    ANSEL = 0; // no analog GPIO
    CMCON = 0x07; // comparator off 
    ADCON0 = 0; // ADC and DAC converters off
    
    state = 0; // pedal's state
    TRISIO0 = 0; // pin 7 is an output (0 like "Output")
    TRISIO4 = 0;
    TRISIO5 = 0;
    TRISIO1 = 1; // pin 6 is an input (1 as "Input")
    GPIO=0; // all the GPIOs are in low state (0V) when starting
    
    while(1)
    {
        if(GP1 == 0)
        {
            __delay_ms(15); // debounce
            
            if(GP1 == 0)
            {
                __delay_ms(200);
                if(GP1 == 1)
                {
                    if(state == 1)
                    {
                        state = 0;
                    }
                    else
                    {
                        state = 1;
                    }
                }
                
            }
        }
            }
}
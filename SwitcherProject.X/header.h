/* 
 * File:   header.h
 * Author: The_N
 *
 * Created on September 30, 2021, 5:58 PM
 */

// CONFIG
#pragma config FOSC = INTRCIO   // Oscillator Selection Bits
#pragma config WDTE = OFF       // Watchdog Timer Enable Bit
#pragma config PWRTE = OFF      // Power-Up Timer Enable Bit
#pragma config MCLRE = OFF      // GP3/MCLR pin function select
#pragma config BOREN = OFF      // Brown-out Detect Enable bit
#pragma config CP = OFF         // Code Protection bit
#pragma config CPD = OFF        // Data Code Protection bit

// Define oscillator frequency
#define _XTAL_FREQ 4000000
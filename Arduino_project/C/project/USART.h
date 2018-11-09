/*
 * USART.c
 *
 * Created: 29/10/2018 10:48:17
 * Author : justin
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16E6
#include <avr/sfr_defs.h>
#define UBBRVAL 51
#include <util/delay.h>

uint8_t receive_data;
extern uint8_t receive_data;

//Declaratie van functies
void USART_init(void);
void receive(void);
void send( unsigned char data);
void USART_putstring(char* StringPtr);


void USART_init(void){
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
	
}

void led_init()
{
	DDRB = 0xFF;
	DDRD = 0xFF;
}

// verzenden van data via UART
void send(unsigned char data){
	
	while(!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

// verzenden van strings via UART
void USART_putstring(char* StringPtr){
	
	while(*StringPtr != 0x00){
	send(*StringPtr);
	StringPtr++;}
	
}

// versturen van getallen via UART
void UU_PutNumber(uint32_t x)
{
	char value[10]; //a temp array to hold results of conversion
	int i = 0; //loop index
	
	do
	{
		value[i++] = (char)(x % 10) + '0'; //convert integer to character
		x /= 10;
	} while(x);
	
	while(i) //send data
	{
		send(value[--i]);
	}
}

void knipperlicht(uint8_t x){
	while(x < 10){
		PORTB |= 0b00000100;
		_delay_ms(250);
		PORTB &= 0b00000011;
		_delay_ms(250);
		x ++;
	}
}

void naar_boven(){
	PORTB = 0b00000001;
	knipperlicht(0);
}

void naar_beneden(){
	PORTB = 0b00000010;
	knipperlicht(0);
}

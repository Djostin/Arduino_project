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



//Declaratie van functies
void USART_init(void);
unsigned char receive(void);
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
	DDRB |= _BV(DDB0);
	DDRB |= _BV(DDD1);
}

unsigned char receive(void){
	//check of bit is gezet en return de waarde.
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
	//check wat er doorgestuurd wordt door python en zet daar de juiste led mee aan.
	if(UDR0 == 0x31)
	{
		PORTB = 0b00000001;
	}
	if(UDR0 == 0x30)
	{
		PORTB = 0b00000010;
	}
	if(UDR0 == 0x32){
		PORTB = 0b00000000;
	}
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
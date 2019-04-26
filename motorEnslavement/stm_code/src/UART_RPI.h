/*
 * UART.h
 *
 *  Created on: Feb 14, 2019
 *      Author: crouman
 */

#include "stm32f4xx.h"
#include "stm32f4_discovery.h"



#ifndef UART_RPI_H_
#define UART_RPI_H_


#define BUFFERSIZE 9

typedef struct __attribute__((__packed__))
{
	char type; // T or R			1 byte
	float rotation; // -360 to 360	4 byte
	float translation; // > 0		4 byte
} command_struct; // 9 bytes

typedef struct
{
	uint8_t byteTable[BUFFERSIZE];
	uint8_t * readHead;
	uint8_t * writeHead;
} circularBuffer;

void UART5_init(void);
int fetchCommandBytes(uint8_t *command_bytes);
void sendBytes(uint8_t *data);

#endif /* UART_RPI_H_ */

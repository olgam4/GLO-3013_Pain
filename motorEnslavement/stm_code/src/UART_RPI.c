/*
 * UART.c
 *
 *  Created on: Feb 14, 2019
 *      Author: crouman
 */

#include "UART_RPI.h"
#include <stdio.h>


//char received_buffer[9] = 0;

 circularBuffer data_buffer;
int receivedByteQuantity = 0;

void UART5_init(void)
{
		NVIC_InitTypeDef NVIC_InitStructure;

		/* Configure the NVIC Preemption Priority Bits */
	    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_0);

	    /* Enable the USART5 Interrupt */
	    NVIC_InitStructure.NVIC_IRQChannel = UART5_IRQn;
	    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 15;
	    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 15;
	    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	    NVIC_Init(&NVIC_InitStructure);

	    data_buffer.readHead = data_buffer.byteTable;
	    data_buffer.writeHead = data_buffer.byteTable;

	    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, ENABLE);  // Cause d'erreur
	    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE);
	    RCC_APB1PeriphClockCmd(RCC_APB1Periph_UART5, ENABLE);

	    // UART Pins initialization
	    GPIO_InitTypeDef GPIO_InitStructRXTX;
		GPIO_InitStructRXTX.GPIO_Mode = GPIO_Mode_AF;
		GPIO_InitStructRXTX.GPIO_Speed = GPIO_Speed_50MHz;
		GPIO_InitStructRXTX.GPIO_OType = GPIO_OType_PP;     // Cause d'erreur
		GPIO_InitStructRXTX.GPIO_PuPd = GPIO_PuPd_NOPULL;


		GPIO_InitStructRXTX.GPIO_Pin = GPIO_Pin_12; // TX
		GPIO_Init(GPIOC, &GPIO_InitStructRXTX);
		GPIO_InitStructRXTX.GPIO_Pin = GPIO_Pin_2; // RX
		GPIO_Init(GPIOD, &GPIO_InitStructRXTX);

		// Configuration of the alternate functions of each pins
		GPIO_PinAFConfig(GPIOC, GPIO_PinSource12, GPIO_AF_UART5);
		GPIO_PinAFConfig(GPIOD, GPIO_PinSource2, GPIO_AF_UART5);

		USART_InitTypeDef USART_InitStruct5;
		USART_StructInit(&USART_InitStruct5);
		USART_InitStruct5.USART_BaudRate = 9600;
		USART_InitStruct5.USART_Parity = USART_Parity_Even;
		USART_InitStruct5.USART_Mode = USART_Mode_Rx;
		USART_Init(UART5, &USART_InitStruct5);

		// activate the UART
		USART_Cmd(UART5, ENABLE);
	    // We activate the Interrupt
		USART_ITConfig(UART5, USART_IT_RXNE, ENABLE);
}

void UART5_IRQHandler(void) // UART ou USART? cause d'erreur
{

	if(USART_GetITStatus(UART5, USART_IT_RXNE) != RESET)
	{

		uint16_t received_byte = USART_ReceiveData(UART5);
		*(data_buffer.writeHead) = (uint8_t) received_byte;
		data_buffer.writeHead++;
		receivedByteQuantity++;

		if ((data_buffer.writeHead - data_buffer.byteTable) / BUFFERSIZE) // If the write head address is 9 addresses from the command_buffer address
		{
			data_buffer.writeHead = data_buffer.byteTable; // reset of writeHead position after 9 byte filling
		}
	}
	USART_ClearITPendingBit(UART5, USART_IT_RXNE);// Clears the USART5's interrupt pending bits.

}


// TO return 9: writeHead has reached 9 address further and readhead is at the data_buffer address
// Must return 9 to have a full command



// fills the command_bytes array with data_buffer array content
int fetchCommandBytes(uint8_t *command_bytes)
{
    if (receivedByteQuantity < 9) // Do nothing until we have full command(9 bytes)
    {
    	return 0;
    }

    else
    {
    	for (int i = 0; i < 9; i++)
    	{
    		command_bytes[i] = *(data_buffer.readHead);
    		data_buffer.readHead++; // Move the readhead all along the data_buffer content
    		if ((data_buffer.readHead - data_buffer.byteTable) / BUFFERSIZE) //When 9 bytes have been read
    		{
    			data_buffer.readHead = data_buffer.byteTable; //  Reset the readhead adress
    		}
    	}
    	receivedByteQuantity = 0;
        return 1;
    }
}

void sendBytes(uint8_t *data) {
	while(data != NULL) {
		USART_SendData(UART5, *data);
		data++;
	}
}



    /* ------------------------------------------------------------ */
    /* Other USART1 interrupts handler can go here ...             */

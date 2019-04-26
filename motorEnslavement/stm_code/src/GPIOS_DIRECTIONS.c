/*
 * GPIOS_DIRECTIONS.c
 *
 *  Created on: Mar 7, 2019
 *      Author: crouman
 */


	/*
	 *
	 *			forward    __
	 * 		----------------  M2
	 * M1 | |				|
	 * 		|				|
	 * 		|	  robot		|
	 * 		|				|
	 * 		|				|
	 * 		|				| | M4
	 * 	M3  -----------------
	 *		--
	 *
	 *
	 */

#include "GPIOS_DIRECTIONS.h"

void GPIO_init()
{
	  GPIO_InitTypeDef  GPIO_InitStructure;

	  /* GPIOC Periph clock enable */
	  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOC, ENABLE);

	  /* Configure PC1 to PC8 in output pushpull mode */
	  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_5 | GPIO_Pin_6 | GPIO_Pin_7 | GPIO_Pin_8;
	  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
	  GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
	  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	  GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;
	  GPIO_Init(GPIOC, &GPIO_InitStructure);
}

void GPIO_toggle(int pin_id)
{
	switch(pin_id)
	{

		case 1:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_1); // Moteur 1 CH1
				break;
		case 2:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_2); // Moteur 1 CH2
				break;
		case 3:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_3); // Moteur 2 CH1
				break;
		case 4:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_4); // Moteur 2 CH2
				break;
		case 5:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_5); // Moteur 3 CH1
				break;
		case 6:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_6); // Moteur 3 CH2
				break;
		case 7:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_7); // Moteur 4 CH1
				break;
		case 8:
				GPIO_ToggleBits(GPIOC, GPIO_Pin_8); // Moteur 4 CH2
				break;
	}
}

void GPIO_reset(int pin_id)
{
	switch(pin_id)
	{

		case 1:
				GPIO_ResetBits(GPIOC, GPIO_Pin_1); // Moteur 1 CH1
				break;
		case 2:
				GPIO_ResetBits(GPIOC, GPIO_Pin_2); // Moteur 1 CH2
				break;
		case 3:
				GPIO_ResetBits(GPIOC, GPIO_Pin_3); // Moteur 2 CH1
				break;
		case 4:
				GPIO_ResetBits(GPIOC, GPIO_Pin_4); // Moteur 2 CH2
				break;
		case 5:
				GPIO_ResetBits(GPIOC, GPIO_Pin_5); // Moteur 3 CH1
				break;
		case 6:
				GPIO_ResetBits(GPIOC, GPIO_Pin_6); // Moteur 3 CH2
				break;
		case 7:
				GPIO_ResetBits(GPIOC, GPIO_Pin_7); // Moteur 4 CH1
				break;
		case 8:
				GPIO_ResetBits(GPIOC, GPIO_Pin_8); // Moteur 4 CH2
				break;
	 }
}

void GPIO_set(int pin_id)
{
	switch(pin_id)
	{

		case 1:
				GPIO_SetBits(GPIOC, GPIO_Pin_1); // Moteur 1 CH1
				break;
		case 2:
				GPIO_SetBits(GPIOC, GPIO_Pin_2); // Moteur 1 CH2
				break;
		case 3:
				GPIO_SetBits(GPIOC, GPIO_Pin_3); // Moteur 2 CH1
				break;
		case 4:
				GPIO_SetBits(GPIOC, GPIO_Pin_4); // Moteur 2 CH2
				break;
		case 5:
				GPIO_SetBits(GPIOC, GPIO_Pin_5); // Moteur 3 CH1
				break;
		case 6:
				GPIO_SetBits(GPIOC, GPIO_Pin_6); // Moteur 3 CH2
				break;
		case 7:
				GPIO_SetBits(GPIOC, GPIO_Pin_7); // Moteur 4 CH1
				break;
		case 8:
				GPIO_SetBits(GPIOC, GPIO_Pin_8); // Moteur 4 CH2
				break;
	}
}

void GPIO_reset_all(void)
{
	GPIO_ResetBits(GPIOC, GPIO_Pin_1);
	GPIO_ResetBits(GPIOC, GPIO_Pin_2);
	GPIO_ResetBits(GPIOC, GPIO_Pin_3);
	GPIO_ResetBits(GPIOC, GPIO_Pin_4);
	GPIO_ResetBits(GPIOC, GPIO_Pin_5);
	GPIO_ResetBits(GPIOC, GPIO_Pin_6);
	GPIO_ResetBits(GPIOC, GPIO_Pin_7);
	GPIO_ResetBits(GPIOC, GPIO_Pin_8);

}


void ENABLE_turn_CW(void) // Peut être inversé, pas testé
{
    GPIO_reset(1);
	GPIO_set(2);

    GPIO_reset(3);
    GPIO_set(4);

    GPIO_reset(5);
    GPIO_set(6);

	GPIO_reset(7);
	GPIO_set(8);
}

void ENABLE_turn_CCW(void) // Peut être inversé, pas testé
{
	GPIO_set(1);
    GPIO_reset(2);

    GPIO_set(3);
    GPIO_reset(4);

    GPIO_set(5);
    GPIO_reset(6);

	GPIO_set(7);
	GPIO_reset(8);
}

void ENABLE_left(void)// Peut être inversé, pas testé
{
	GPIO_set(3);
	GPIO_reset(4);

	GPIO_reset(5);
	GPIO_set(6);
}
void ENABLE_right(void)// Peut être inversé, pas testé
{
    GPIO_reset(3);
	GPIO_set(4);

	GPIO_set(5);
	GPIO_reset(6);
}
void ENABLE_forward(void)//// Enables forward translation //Peut être inversé, pas testé
{
    GPIO_reset(1);
	GPIO_set(2);

	GPIO_set(7);
	GPIO_reset(8);


}
void ENABLE_backward(void)// Enables backward translation // Peut être inversé, pas testé
{

	GPIO_set(1);
    GPIO_reset(2);

	GPIO_reset(7);
	GPIO_set(8);

}
void BREAK_Y(void) // Stops M1 and M4 (the Y axis translation)
{
	GPIO_reset(1);
    GPIO_reset(2);

	GPIO_reset(7);
	GPIO_reset(8);

}
void BREAK_X(void)// Stops M2 and M3 (the X axis translation)
{
	GPIO_reset(3);
	GPIO_reset(4);

	GPIO_reset(5);
	GPIO_reset(6);

}




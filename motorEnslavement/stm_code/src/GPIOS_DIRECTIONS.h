/*
 * GPIOS_DIRECTIONS.h
 *
 *  Created on: Mar 7, 2019
 *      Author: crouman
 */

#ifndef GPIOS_DIRECTIONS_H_
#define GPIOS_DIRECTIONS_H_

#include "stm32f4_discovery.h"

void GPIO_init(void);
void GPIO_toggle(int pin_id);
void GPIO_reset(int pin_id);
void GPIO_set(int pin_id);
void GPIO_reset_all(void);

void ENABLE_turn_CW(void);
void ENABLE_turn_CCW(void);
void ENABLE_left(void);
void ENABLE_right(void);
void ENABLE_forward(void);
void ENABLE_backward(void);
void BREAK_Y(void);
void BREAK_X(void);


#endif /* GPIOS_DIRECTIONS_H_ */

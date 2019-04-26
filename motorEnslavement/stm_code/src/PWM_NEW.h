/*
 * PWM_NEW.h
 *
 *  Created on: Mar 13, 2019
 *      Author: crouman
 */

#ifndef PWM_NEW_H_
#define PWM_NEW_H_

#include "tm_stm32f4_gpio.h"
#include "tm_stm32f4_pwm.h"
#include "tm_stm32f4_timer_properties.h"


void PWM_INIT(void);
void PWM_SET_DUCY(int channel,int percentage);

#endif /* PWM_NEW_H_ */

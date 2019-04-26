/*
 * PWM_NEW.c
 *
 *  Created on: Mar 13, 2019
 *      Author: crouman
 */


#include "PWM_NEW.h"

	TM_PWM_TIM_t TIM1_Data;

void PWM_INIT()
{

    /* Set PWM to 1kHz frequency on timer TIM1 */
    /* 1 kHz = 1ms = 1000us */
    TM_PWM_InitTimer(TIM1, &TIM1_Data, 1000); // To have a frequency of about 32 kHz

    /* Initialize PWM on TIM1, Channel 1 and PinsPack 2 = PE9 */
    TM_PWM_InitChannel(&TIM1_Data, TM_PWM_Channel_1, TM_PWM_PinsPack_2);
    /* Initialize PWM on TIM1, Channel 2 and PinsPack 2 = PE10 */   // Peut causer problème: E10 ou E11 est la bonne ??
    TM_PWM_InitChannel(&TIM1_Data, TM_PWM_Channel_2, TM_PWM_PinsPack_2);
    /* Initialize PWM on TIM1, Channel 3 and PinsPack 2 = PE13 */
    TM_PWM_InitChannel(&TIM1_Data, TM_PWM_Channel_3, TM_PWM_PinsPack_2);
    /* Initialize PWM on TIM1, Channel 4 and PinsPack 2 = PE14 */
    TM_PWM_InitChannel(&TIM1_Data, TM_PWM_Channel_4, TM_PWM_PinsPack_2);

    /* Set channel 1 value, 50% duty cycle */
    TM_PWM_SetChannelPercent(&TIM1_Data, TM_PWM_Channel_1, 0); // TM_PWM_SetChannel(&TIM1_Data, TM_PWM_Channel_1, TIM1_Data.Period / 2);
    /* Set channel 2 value, 33% duty cycle */
    TM_PWM_SetChannelPercent(&TIM1_Data, TM_PWM_Channel_2, 0); // Faire 100 - Ce qu'on veut... f*cking weird
    /* Set channel 3 value, 25% duty cycle */
    TM_PWM_SetChannelPercent(&TIM1_Data, TM_PWM_Channel_3, 0);
    /* Set channel 4 value, 5% duty cycle*/
    TM_PWM_SetChannelPercent(&TIM1_Data, TM_PWM_Channel_4, 0);


}

void PWM_SET_DUCY(int channel, int percentage)
{
	   TM_PWM_SetChannelPercent(&TIM1_Data, channel, percentage);

}








/* Includes */

//#include <PWM_OLD.h>
#include "stm32f4xx.h"
#include "stm32f4_discovery.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>


#include "UART_RPI.h"
#include "ENCODERS.h"
#include "PWM_NEW.h"
#include "GPIOS_DIRECTIONS.h"


/* Private macro */

#define sample_time 0.050;


/* Private variables */



command_struct *the_command;
uint8_t command_bytes[9] = {0}; // 9 byte array which contains the 9 bytes commands after 9 UART interrupts


//Used in the Systick handler to count 50ms
int handler_counter = 0;
int time_locker = 0;

//Number of tics the robot have to do to reach destination
int tics_until_destination = 0;
int ticsX_until_destination = 0;
int ticsY_until_destination = 0;

const int middle_tic_value = 32768;

//Number of tics each wheels have to do to reach destination
int tics_remaining_M1 = 0;int tics_remaining_M2 = 0;int tics_remaining_M3 = 0;int tics_remaining_M4 = 0;

//Number of tics each wheels have done
int tics_done_M1 = 32768;int tics_done_M2 = 32768; int tics_done_M3 = 32768; int tics_done_M4 = 32768;

//Actual and previous PWM duty cycle sent to the 4 wheels engines
float pwm_ducy_M1 = 0; float pwm_ducy_M2 = 0; float pwm_ducy_M3 = 0; float pwm_ducy_M4 = 0;              	   			 				  // uMx(k)
float previous_pwm_ducy_M1 = 0; float previous_pwm_ducy_M2 = 0; float previous_pwm_ducy_M3 = 0; float previous_pwm_ducy_M4 = 0;			  // uMx(k-1)

// The speed error is the difference between the order speed and the previous speed
float speed_error_M1 = 0; float speed_error_M2 = 0; float speed_error_M3 = 0;	float speed_error_M4 = 0;	 				 // eMx(k)
float previous_speed_error_M1 = 0;float previous_speed_error_M2 = 0; float previous_speed_error_M3 = 0;float previous_speed_error_M4 = 0;// eMx(k-1)

// The ordered speed in centimeters per second
float order_speed = 15;
const float speed_translation = 15;
const float speed_careful = 5;
const float speed_rotation = 5;
const float circumference = 60;



/* Private function prototypes */

void SysTick_Handler(void);

/* Private functions */

/**
  * @brief  This function handles SysTick Handler.
  * @param  None
  * @retval None
  */

void SysTick_Handler()  // Once every 50 ms
{
	handler_counter ++;
	time_locker = 0;

/*	if(handler_counter == 50)
	{
		time_locker = 0; // Unlock the time_locker, 2.5 seconds have passed; (SAMPLE TIME)
		handler_counter = 0;
	}
*/

}

double get_speed_error(int tics_done)
{
	double previous_speed = tics_done * (22 / 6400.0) / sample_time;
	return (order_speed - previous_speed);
}

int get_tics_done_from_register(TIM_TypeDef *reg)
{
	int tics_count = reg->CNT;
	reg->CNT = middle_tic_value;
	return abs(middle_tic_value - tics_count);
}

void bound_check_ducy(float *ducy)
{
	if (*ducy < 0) {*ducy = 0;}
	if (*ducy > 1) {*ducy = 1;}
}
void reinitialize_stuff()
{
	handler_counter = 0;
	time_locker = 0;
	tics_until_destination = 0;
	ticsX_until_destination = 0;
	ticsY_until_destination = 0;
//	middle_tic_value = 32768;
	tics_remaining_M1 = 0;
	tics_remaining_M2 = 0;
	tics_remaining_M3 = 0;
	tics_remaining_M4 = 0;
	tics_done_M1 = 32768;
	tics_done_M2 = 32768;
	tics_done_M3 = 32768;
	tics_done_M4 = 32768;
	pwm_ducy_M1 = 0.40;
	pwm_ducy_M2 = 0.55;
	pwm_ducy_M3 = 0.50;
	pwm_ducy_M4 = 0.35;
	previous_pwm_ducy_M1 = 0;
	previous_pwm_ducy_M2 = 0;
	previous_pwm_ducy_M3 = 0;
	previous_pwm_ducy_M4 = 0;
	speed_error_M1 = 0;
	speed_error_M2 = 0;
	speed_error_M3 = 0;
	speed_error_M4 = 0;
	previous_speed_error_M1 = 0;
	previous_speed_error_M2 = 0;
	previous_speed_error_M3 = 0;
	previous_speed_error_M4 = 0;

	TIM2->CNT = middle_tic_value;
	TIM3->CNT = middle_tic_value;
	TIM4->CNT = middle_tic_value;
	TIM5->CNT = middle_tic_value;

	PWM_SET_DUCY(TM_PWM_Channel_1,40);
	PWM_SET_DUCY(TM_PWM_Channel_2,55);
	PWM_SET_DUCY(TM_PWM_Channel_3,50);
	PWM_SET_DUCY(TM_PWM_Channel_4,35);


}



/**
**===========================================================================
**
**  Abstract: main program
**
**===========================================================================
*/


//1 UART pour la commande du rpi, 							(RX,TX)
//1 timers pour les 4 pwm vers le PCB des ponts en H,		(4 GPIO)
//4 timer pour la lecture des 8 input gpio des encodeurs	(8 GPIO)
//8 GPIO pour l'�criture des 8 output de sens vers le PCB	(8 GPIO)
//1 systick pour la base de temps

// 1 ADC pour les condensateurs



int main(void)
{
	//INIT FUNCTIONS//

	SystemInit();  /* Initialize system */

	UART5_init();
	PWM_INIT();
	GPIO_init();
	ENCODER1_init();
	ENCODER2_init();
	ENCODER3_init();
	ENCODER4_init();


	SysTick_Config(SystemCoreClock/20); // Interrupt once every 50 ms

	//END INIT FUNCTIONS//


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


	// Put counters to half of max value, We will use 32768 - TIMx->CNT to find the quantity of tics done
/*	TIM2->CNT = middle_tic_value;
	TIM3->CNT = middle_tic_value;
	TIM4->CNT = middle_tic_value;
	TIM5->CNT = middle_tic_value;

	PWM_SET_DUCY(TM_PWM_Channel_1,40);
	PWM_SET_DUCY(TM_PWM_Channel_2,55);
	PWM_SET_DUCY(TM_PWM_Channel_3,50);
	PWM_SET_DUCY(TM_PWM_Channel_4,35);*/
	int in_progress = 0;

	while(1)
	{
		if(fetchCommandBytes(command_bytes))
		{
//			in_progress = 1;
			reinitialize_stuff();

		/*	the_command.type = (char)command_bytes[0];
			the_command.rotation = *((float*)(command_bytes+1));
			the_command.translation = *((float*)(command_bytes+5));*/


			the_command = (command_struct*)command_bytes;


			if (the_command->type == 'R')
			{
				order_speed = speed_rotation;

				tics_until_destination = abs(the_command->rotation / (2*M_PI) * circumference * 6400/22);

				tics_remaining_M1 = tics_remaining_M2 = tics_remaining_M3 = tics_remaining_M4 = tics_until_destination;

				if (the_command->rotation < 0) {
					ENABLE_turn_CCW();
				}else {
					ENABLE_turn_CW();
				}
			}

			if (the_command->type == 'T')
			{
				order_speed = speed_translation;

				tics_until_destination = (the_command->translation) * 6400/22; //Hypotenuse

				ticsX_until_destination = tics_until_destination * sin(the_command->rotation);
				ticsY_until_destination = tics_until_destination * cos(the_command->rotation);


				// 0 tic est une valeur tr�s pr�cise et une cause d'erreur

				tics_remaining_M2 = abs(ticsX_until_destination);
				tics_remaining_M3 = abs(ticsX_until_destination);

				tics_remaining_M1 = abs(ticsY_until_destination);
				tics_remaining_M4 = abs(ticsY_until_destination);

				if(ticsX_until_destination < 0)
				{
					ENABLE_left();
				}
				else if(ticsX_until_destination > 0)
				{
					ENABLE_right();
				}
				else
				{
					BREAK_X(); // Si translation seulement
				}

				if(ticsY_until_destination < 0)
				{
					ENABLE_backward();
				}
				else if(ticsY_until_destination > 0)
				{
					ENABLE_forward();
				}
				else
				{
					BREAK_Y(); // Si translation seulement
				}
			}

			if (the_command->type == 'C')
			{
				order_speed = speed_careful;

				tics_until_destination = (the_command->translation) * 6400/22; //Hypotenuse

				ticsX_until_destination = tics_until_destination * sin(the_command->rotation);
				ticsY_until_destination = tics_until_destination * cos(the_command->rotation);


				// 0 tic est une valeur tres precise et une cause d'erreur

				tics_remaining_M2 = tics_remaining_M3 = abs(ticsX_until_destination);
				tics_remaining_M1 = tics_remaining_M4 = abs(ticsY_until_destination);

				if(ticsX_until_destination < 0)
				{
					ENABLE_left();
				}
				else if(ticsX_until_destination > 0)
				{
					ENABLE_right();
				}

				if(ticsY_until_destination < 0)
				{
					ENABLE_backward();
				}
				else if(ticsY_until_destination > 0)
				{
					ENABLE_forward();
				}
			}
		}


		SysTick->VAL = 0;   // reload systick value to 0
		time_locker = 1;
		while(time_locker == 1)
		{
			//wait until 50 milliseconds have passed
		}


		if (tics_remaining_M1 > 0)// Moteur 1 : y
		{
			tics_done_M1 = get_tics_done_from_register(TIM2);
			speed_error_M1 = get_speed_error(tics_done_M1);
			tics_remaining_M1 -= tics_done_M1;
			pwm_ducy_M1 = (0.1213 * speed_error_M1) - (0.1022 * previous_speed_error_M1) + previous_pwm_ducy_M1; // Moteur 1 // Y
			bound_check_ducy(&pwm_ducy_M1);
			PWM_SET_DUCY(TM_PWM_Channel_1, pwm_ducy_M1 * 100);
			previous_speed_error_M1 = speed_error_M1;
			previous_pwm_ducy_M1 = pwm_ducy_M1;
		}

		if (tics_remaining_M2 > 0)// Moteur 2 : x
		{
			tics_done_M2 = get_tics_done_from_register(TIM3);
			speed_error_M2 = get_speed_error(tics_done_M2);
			tics_remaining_M2 -= tics_done_M2;
			pwm_ducy_M2 = (0.1671 * speed_error_M2) - (0.1574 * previous_speed_error_M2) + previous_pwm_ducy_M2; // Moteur 2  // X
			bound_check_ducy(&pwm_ducy_M2);
			PWM_SET_DUCY(TM_PWM_Channel_2,pwm_ducy_M2 * 100);
			previous_speed_error_M2 = speed_error_M2;
			previous_pwm_ducy_M2 = pwm_ducy_M2;
		}

		if (tics_remaining_M3 > 0) // Moteur 3 : x
		{
			tics_done_M3 = get_tics_done_from_register(TIM4);
			speed_error_M3 = get_speed_error(tics_done_M3);
			tics_remaining_M3 -= tics_done_M3;
			pwm_ducy_M3 = (0.1606 * speed_error_M3) - (0.1483 * previous_speed_error_M3) + previous_pwm_ducy_M3; // Moteur 3
			bound_check_ducy(&pwm_ducy_M3);
			PWM_SET_DUCY(TM_PWM_Channel_3,pwm_ducy_M3 * 100);
			previous_speed_error_M3 = speed_error_M3;
			previous_pwm_ducy_M3 = pwm_ducy_M3;
		}

		if (tics_remaining_M4 > 0)  // Moteur 4 : y
		{
			tics_done_M4 = get_tics_done_from_register(TIM5);
			speed_error_M4 = get_speed_error(tics_done_M4);
			tics_remaining_M4 -= tics_done_M4;
			pwm_ducy_M4 = (0.1330 * speed_error_M4) - (0.1190 * previous_speed_error_M4) + previous_pwm_ducy_M4; // Moteur 4
			bound_check_ducy(&pwm_ducy_M4);
			PWM_SET_DUCY(TM_PWM_Channel_4,pwm_ducy_M4 * 100);
			previous_speed_error_M4 = speed_error_M4;
			previous_pwm_ducy_M4 = pwm_ducy_M4;
		}

		if (tics_remaining_M1 <= 0 && tics_remaining_M4 <= 0)
		{
			BREAK_Y();
		}

		if (tics_remaining_M2 <= 0 && tics_remaining_M3 <= 0)
		{
			BREAK_X();
		}

		if (in_progress && tics_remaining_M1 <= 0 && tics_remaining_M4 <= 0
						&& tics_remaining_M2 <= 0 && tics_remaining_M3 <= 0)
		{
			uint8_t bytes[1] = {0x37}; // b'7'
//			sendBytes(bytes);
			in_progress = 0;
		}


	}


}







/*
 * Callback used by stm32f4_discovery_audio_codec.c.
 * Refer to stm32f4_discovery_audio_codec.h for more info.
 */
void EVAL_AUDIO_TransferComplete_CallBack(uint32_t pBuffer, uint32_t Size){
  /* TODO, implement your code here */
  return;
}

/*
 * Callback used by stm324xg_eval_audio_codec.c.
 * Refer to stm324xg_eval_audio_codec.h for more info.
 */
uint16_t EVAL_AUDIO_GetSampleCallBack(void){
  /* TODO, implement your code here */
  return -1;
}

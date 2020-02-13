# Information on STM32 Board/Hardware, and Code Used

## Hardware
- STM32F429I-DISC1 with STM32F429ZIT6U Processor
- Adafruit Electret Microphone Amplifier - MAX9814 with Auto Gain Control with product number 1713
- 2 External LEDs (with resistors) (GPIO Pins PC2 and PC4)
- 2 Internal LEDs (GPIO Pins PG13 and PC14
- ADC1 Channel 5 (GPIO Pin PA5)

## Code
- Programmed with STM32CubeIDE (https://www.st.com/en/development-tools/stm32cubeide.html)
- Utilizes ADC to read in microphone value on GPIO Pin PA5 using ADC 1/Channel 5
-- Most settings are default
-- 12 Bit Resolution
-- Clock PCLK2 divided by 8
-- Scan Continuous Mode
-- Currently working in extremely poor way of restarting the ADC on each read
- GPIO Pins configured in default mode
- 4 LEDs used to threshold between 4 values: >2000, >1000, >500, and default
-- Thresholding done in LED_Thresholding function
-- When one threshold is hit, that LED will turn on and clear the other LEDs
- Microphone configured with floating AR pin and gain tried to input voltage (3.3V) 

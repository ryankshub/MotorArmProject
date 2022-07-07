# Motorized Arm Project

Currently a work-in-progress

## Setup:

1. Ensure you're using odrive == 0.5.4 version
2. Disconnect every peripheral except USB and power
3. Run `odrivetool dfu`; Respond yes to both prompts
4. Reattach peripherals 
5. run `config/arm_config.py`; this only has to be run once. 
6. If you hear the motor running and it resist motion; you're good
#!/usr/bin/env python3
"""
Interface for MPU6050 on GY-521 interface
"""

# IMU I2C Information

IMU_ADDR = 0x68

# Configuration register Addr

CONFIG = 0x1A       #Configures Frame Synchronization and Digital Low Pass Filter
GYRO_CONFIG = 0x1B  #Changes self-test response and gyroscope precision
ACCEL_CONFIG = 0x1C #Changes self-test response and accelerometer precision
PWR_MGMT_1 = 0x6B   #Disable Temp sensor and adjust clock
SMPRT_DIV = 0x19    #Sample Rate Divider (Sample Rate is Gyro/(1+this))

# Data Register Addr

# Max Sample rate is 1KHz
ACCEL_XOUT_H = 0x3B # MSBs of the Accel readout (x-axis)
ACCEL_XOUT_L = 0x3C # LSBs of the Accel readout (x-axis)
ACCEL_YOUT_H = 0x3D # MSBs of the Accel readout (y-axis)
ACCEL_YOUT_L = 0x3E # LSBs of the Accel readout (y-axis)
ACCEL_ZOUT_H = 0x3F # MSBs of the Accel readout (z-axis)
ACCEL_ZOUT_L = 0x40 # LSBs of the Accel readout (z-axis)

# Default Sample rate is 8kHz
GYRO_XOUT_H = 0x43  # MSBs of Gyro x
GYRO_XOUT_L = 0x44  # LSBs of Gyro x
GYRO_YOUT_H = 0x45  # MSBs of Gyro y
GYRO_YOUT_L = 0x46  # LSBs of Gyro y
GYRO_ZOUT_H = 0x47  # MSBs of Gyro z
GYRO_ZOUT_L = 0x48  # LSBs of Gyro z

# ID Register
WHO_AM_I = 0x75     # Contants I2C addr; reg val should be 0x68

# Constants
SAMPLE_DIV = 0x07 # Divide Sample Rate by 8; 
ACCEL_CONV = 6.103515625e-05 # For 2+-, 16384 LSB/g
GYRO_CONV = 0.06097560975609757 # for 2000 deg/s, 16.4 LSB/deg/s

# Establish I2C Connection
# Use smBus2 for this

# Configure Device
def init_device():
    # Wake up device, disable temp sensor, and set Gyro Z PLL for clock reference
    # Write_I2C(IMU_ADDR, PWR_MGMT_1, 0x0B) 
    
    # Config Accel with +-2g precision
    # Write_I2C(IMU_ADDR, ACCEL_CONFIG, 0x00)

    # Config Gryo with 2000 deg/s
    # Write_I2C(IMU_ADDR, GYRO_CONFIG, 0x18)

    # Config Sample Rate for both to be 1kHz
    # Write_I2C(IMU_ADDR, SMPRT_DIV, SAMPLE_DIV)
    pass

def read_data():
    # Burst Read Data
    pass


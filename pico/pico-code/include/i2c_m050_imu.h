#ifndef M050_IMU__H__
#define M050_IMU__H__

#include "hardware/i2c.h"
// Header file for IMU interface with MPU-6050 IMU

// Addr of IMU device
#define IMU_ADDR 0x68

// Configuration register Addr
#define CONFIG 0x1A        //Configures Frame Synchronization and Digital Low Pass Filter
#define GYRO_CONFIG 0x1B   //Changes self-test response and gyroscope precision
#define ACCEL_CONFIG 0x1C  //Changes self-test response and accelerometer precision
#define PWR_MGMT_1 0x6B    //Disable Temp sensor and adjust clock
#define SMPRT_DIV 0x19     //Sample Rate Divider (Sample Rate is Gyro/(1+this))

// Data Register Addr

//Accelerometer: Max Sample rate 1kHz
#define ACCEL_XOUT_H 0x3B // MSBs of the Accel readout (x-axis)
#define ACCEL_XOUT_L 0x3C // LSBs of the Accel readout (x-axis)
#define ACCEL_YOUT_H 0x3D // MSBs of the Accel readout (y-axis)
#define ACCEL_YOUT_L 0x3E // LSBs of the Accel readout (y-axis)
#define ACCEL_ZOUT_H 0x3F // MSBs of the Accel readout (z-axis)
#define ACCEL_ZOUT_L 0x40 // LSBs of the Accel readout (z-axis)

//Gyroscope: Default Sample rate is 8kHz
#define GYRO_XOUT_H 0x43  // MSBs of Gyro x
#define GYRO_XOUT_L 0x44  // LSBs of Gyro x
#define GYRO_YOUT_H 0x45  // MSBs of Gyro y
#define GYRO_YOUT_L 0x46  // LSBs of Gyro y
#define GYRO_ZOUT_H 0x47  // MSBs of Gyro z
#define GYRO_ZOUT_L 0x48  // LSBs of Gyro z

// ID Register
#define WHO_AM_I 0x75 // Constants I2C addr; reg val should be 0x68

// Constants
#define SAMPLE_DIV 0x4F // Divide Sample Rate by 80; 
#define ACCEL_CONV 0.000598 // For 2+-, 9.81/16384 LSB/g
#define GYRO_CONV 0.01527 // for 500 deg/s, 65.5 LSB/deg/s
#define BAUDRATE 115200
#define READ_RATE_MS 10 // length of execution loop in milliseconds

// Init I2C Hardware
void init_i2c_hw(void);

//Configuration Function
void init_device(void);

/*
Read acceleration and gyroscope data from the mpu6050

Args:
    accel[] - array to pipe acceleration values into
    gyro[] - array to pipe gyroscope values into
*/
void read_data(float accel[3], float gyro[3]);

/*
Reads only acceleration values from the mpu6050

Args:
    accel[] - array to pipe acceleration values into
*/
void read_accel_data(float accel[3]);

/*
Convert the six 8-bits numbers from the mpu6050 into 3 floats representing
acceleration for x, y, and z direction

Args:
    accel[] - array to pipe acceleration values into
    read_buf[] - array containing bytes from the mpu6050
*/
float convert_accel(float accel[3], uint8_t read_buf[6]);

/*
Convert the six 8-bits numbers from the mpu6050 into 3 floats representing
gyroscope readings for x, y, and z direction

Args:
    gyro[] - array to pipe acceleration values into
    read_buf[] - array containing bytes from the mpu6050
*/
float convert_gyro(float gyro[3], uint8_t read_buf[6]);

#endif
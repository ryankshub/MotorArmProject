/*
Main file for pico code
- Grabs IMU data from MPU6050
*/
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "i2c_m050_imu.h"

int main() {
    // Set up UART connection
    stdio_init_all();
    
    // Init i2c
    init_i2c_hw();

    // Init MPU6050
    init_device();

    // Init array
    float accel[3];
    float gyro[3];

    while(true){
        read_data(accel, gyro);
        printf("%f %f %f %f %f %f\n", accel[0], accel[1], accel[2], gyro[0], gyro[1], gyro[2]);
    }
}
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "i2c_m050_imu.h"

/* 
Start up the I2C hardware with GP16 and 17 
*/
void init_i2c_hw(void) {
    i2c_init(i2c0, BAUDRATE);
    gpio_set_function(16, GPIO_FUNC_I2C);
    gpio_set_function(17, GPIO_FUNC_I2C);
    gpio_pull_up(16);
    gpio_pull_up(17);
}

/*
Configure the MPU6050
*/
void init_device(void) {
    // Wake up device, disable temp sensor, set clock ref
    uint8_t write_buf[] = {PWR_MGMT_1, 0x0B};
    i2c_write_blocking(i2c0, IMU_ADDR, write_buf, 2, false);

    // Set Accel with +- 2g precision
    write_buf = {ACCEL_CONFIG, 0x00};
    i2c_write_blocking(i2c0, IMU_ADDR, write_buf, 2, false);

    // Set Gyro with 2000 deg/s
    write_buf = {GYRO_CONFIG, 0x18};
    i2c_write_blocking(i2c0, IMU_ADDR, write_buf, 2, false);

    // Config Sample Rate to both to be 1kHz
    write_buf = {SMPRT_DIV, SAMPLE_DIV};
    i2c_write_blocking(i2c0, IMU_ADDR, write_buf, 2, false);

}

/*

*/
void read_data(float accel[3], float gyro[3]){
    uint8_t read_buf[6]; // buffer for reading values

    // Read acceleration
    uint8_t val = ACCEL_XOUT_H;
    i2c_write_blocking(i2c0, IMU_ADDR, &val, 1, true);
    i2c_read_blocking(i2c0, IMU_ADDR, read_buf, 6, false);

    //Convert acceleration to float
    convert_accel(accel, read_buf);

    // Read gyroscope
    val = GYRO_XOUT_H;
    i2c_write_blocking(i2c0, IMU_ADDR, &val, 1, true);
    i2c_read_blocking(i2c0, IMU_ADDR, read_buf, 6, false);

    // Conver gyroscope to float
    convert_gyro(gyro, read_buf);
}

float convert_accel(float accel[3], uint8_t read_buf[6]){
    for(int i = 0; i < 3; i++) {
        int16_t accel_val = (read_buf[i*2] << 8 | read_buf[i*2 + 1]);
        float accel_float = (float)(accel_val*ACCEL_CONV);
        accel[i] = accel_float; 
    }

}

float convert_gyro(float gyro[3], uint8_t read_buf[6]){
    for(int i = 0; i < 3; i++) {
        int16_t gyro_val = (read_buf[i*2] << 8 | read_buf[i*2 + 1]);
        float gyro_float = (float)(gyro_val*GYRO_CONV);
        gyro[i] = gyro_float; 
    }
}
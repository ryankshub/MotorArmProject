/*
Main file for pico code
- Grabs IMU data from MPU6050
*/
#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "i2c_m050_imu.h"

/*
Repeating timer that reads the acceleration values from the mpu6050 and sends
them over serial
*/
bool read_accel_callback(repeating_timer_t *t) {
    float accel_arr[3];
    read_accel_data(accel_arr);
    printf("%f %f %f\n", accel_arr[0], accel_arr[1], accel_arr[2]);
    return true;
}

int main() {
    // Set up UART connection
    stdio_init_all();
    
    // Init i2c
    init_i2c_hw();

    // Init MPU6050
    init_device();

    // Turn LED to show running
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_put(LED_PIN, 1);


    // Create repeating timer object
    struct repeating_timer timer;
    add_repeating_timer_ms(-READ_RATE_MS, read_accel_callback, NULL, &timer);

    while(true) {
        //This is an infinite while for device
        //operation
    }
    
    //Turn light off 
    //If we got here, then something went wrong
    gpio_put(LED_PIN, 0);
}
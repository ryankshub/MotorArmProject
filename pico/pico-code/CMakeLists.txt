cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(bio_arm C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_executable(imu_inf
    main.c
    i2c_m050_imu.c
)

target_link_libraries(imu_inf pico_stdlib hardware_i2c)

target_include_directories(imu_inf PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

pico_enable_stdio_usb(imu_inf 1)

pico_add_extra_outputs(imu_inf)
# Project_IMU-Car-Racing

```
/*
Version:		V1.1
Author:			Vincent
Create Date:	2020/8/6
Note：
```

![main](md_pic/show.gif)

[toc]

# Overview

[Makerfabs home page](https://www.makerfabs.com/)

[Makerfabs Wiki](https://makerfabs.com/wiki/index.php?title=Main_Page)



Using the MPU6050 gyroscope to obtain its own tilt Angle to simulate the arrow keys, the control of a simple Python racing game.Realized the car up and down left and right movement.



# ESP32 IMU Module V1.1

## Product link ：[ESP32 6- Axis IMU](https://www.makerfabs.com/esp32-6-axis-imu.html) 

## Detail Info: [ESP32_IMU_Module](https://github.com/Makerfabs/ESP32_IMU_Module)

The Makerfabs IMU Module features the 6-axis MPU-6050 MEMS sensor from InvenSense. Each of these 6DoF IMU feature an ESP32 with a MPU-6050 which contains a 3-axis gyroscope as well as a 3-axis accelerometer. The MPU-6050 uses 16-bit analog-to-digital converters (ADCs) for digitizing 6 axes. By combining a MEMS 3-axis gyroscope and a 3-axis accelerometer on the same silicon die together with an onboard Digital Motion Processor™ (DMP™) .It can be used as a helicopter/quadcopter.

# STEPS

## Prepare And Burn ESP32_IMU

**If you have any questions，such as how to install the development board, how to download the code, how to install the library. Please refer to :[Makerfabs_FAQ](https://github.com/Makerfabs/Makerfabs_FAQ)**

- Connect esp32 to PC .
- Use uPyCraft upload code in "/Project_IMU-Car-Racing/ESP32_mpu6050/workSpace"



## Prepare Upper Computer Software

- Install pygame library, like use : pip install pygame.

- Use command line run: Python /Project_IMU-Car-Racing/car_racing_py/car_racing.py
- 
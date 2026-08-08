import rclpy
import threading
from . import board_interface
from .board_interface import BoardInterface
from . import cv_interface
from .cv_interface import CVInterface

#START USER CODE IMPORTS

import time
import math
import numpy as np
from collections import deque

import matplotlib.pyplot as plt


#END USER CODE IMPORTS

_stop_event = threading.Event()
def _rclpy_handler(board,cv):
    try:
        while rclpy.ok() and not _stop_event.is_set():
            rclpy.spin_once(board, timeout_sec=0.05)
            rclpy.spin_once(cv, timeout_sec=0.05)
    finally:
        if rclpy.ok():
            rclpy.shutdown()
def main() -> None:
    rclpy.init()
    board = BoardInterface()
    cv = CVInterface()
    _spin_thread = threading.Thread(
        target=_rclpy_handler,
        daemon=True,
        args=[board, cv]
    )
    _spin_thread.start()

#START USER CODE INITIALIZATION

        #Constants
    yaw_id = 6
    shoulder_id = 5
    elbow_id = 4
    wrist_id = 3

    line_follow_pos = [0.0,0.0,0.0,-90.0,-90.0,90.0,0.0]


    MOTOR_SPD_SCALER = 100
    OFF_CENTER_SPIN_SHIFT = 0

        #Initializations

    last_error = 0.0
    error_sum = 0.0
    
    movement_state = 'normal'
    state_start_time = 0

    #plt.ion()
    #fig, ax = plt.subplots()
    #line, = ax.plot([], [], lw=2)

    #y_buf = deque(maxlen=10000)
    #x_buf = deque(maxlen=10000)

    #ax.set_xlabel("Time")
    #ax.set_ylabel("Centroid")
    #ax.set_title("Current Centroid")
    #t=0

#END USER CODE INITIALIZATION
    while(True):
#START USER CODE LOOP
        
            #Hold arm in basic line tracking position
        
        board.set_rgb1(255.0,0.0,0.0,0.5)

        board.set_servo_position_deg(yaw_id,line_follow_pos[yaw_id])

        board.set_servo_position_deg(shoulder_id,line_follow_pos[shoulder_id])

        board.set_servo_position_deg(elbow_id,line_follow_pos[elbow_id])

        board.set_servo_position_deg(wrist_id,line_follow_pos[wrist_id])

        board.set_claw(s='0')


    #Control logic for mechanums

        x_vel = 0.0
        y_vel = 0.0
        z_vel = 0.0

        print(f"Current State: {movement_state}")

        match movement_state:

            case 'normal':

                #x1,y1,x2,y2 = cv.green_line


                print(f"Normal State!")


                #Find centroid of the line for lateral strafe P control
                x_centroid = cv.line_centroid_x

                #t+=1
                #y_buf.append(x_centroid)
                #x_buf.append(t)
                
                #line.set_data(x_buf,y_buf)
                #ax.relim()
                #ax.autoscale_view()
                #plt.pause(0.005)

                #Error from center screen to target (normalized) 
                error = -x_centroid/320.0


                #Derivative for pid
                d_error = error-last_error
                last_error = error


                #Integral for pid
                error_sum += error
                error_sum = min(error_sum,1.0)
                error_sum = max(error_sum,-1.0)


                #Set velocities
                x_vel = 0


                if abs(error) < 0.7:
                    y_vel = 0.25
                else:
                    y_vel = 0.0


                z_vel = error * (0.20) - d_error * (0.0)

                if board.sonar/10 < 10 and not board.sonar == 0:
                    movement_state = 'move_left'
                    state_start_time = time.time_ns()/1000000

            
            case 'move_left':
                
                print(f"Left State!")

                x_vel = -1.0
                y_vel = 0.0
                z_vel = 0.0

                if (time.time_ns()/1000000-state_start_time) > 700:
                    movement_state = 'move_forward'
                    state_start_time = time.time_ns()/1000000

            case 'move_forward':
                
                print(f"Forward State!")

                x_vel = 0.0
                y_vel = 1.0
                z_vel = 0.0

                if (time.time_ns()/1000000-state_start_time) > 1300:
                    movement_state = 'move_right'
                    state_start_time = time.time_ns()/1000000

            case 'move_right':
                
                print(f"Right State!")

                x_vel = 1.0
                y_vel = 0.0
                z_vel = 0.0

                if (time.time_ns()/1000000-state_start_time) > 700:
                    movement_state = 'normal'
                    state_start_time = time.time_ns()/1000000


        #print(f"z_vel: {z_vel:.2f}")


            #Basic mechanum mapping with spin centered around arm joint 0
        board.set_dc_motor_duty(1,int(-y_vel*MOTOR_SPD_SCALER-x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER-OFF_CENTER_SPIN_SHIFT)))
        board.set_dc_motor_duty(2,int(y_vel*MOTOR_SPD_SCALER-x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER-OFF_CENTER_SPIN_SHIFT)))
        board.set_dc_motor_duty(3,int(y_vel*MOTOR_SPD_SCALER+x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER+OFF_CENTER_SPIN_SHIFT)))
        board.set_dc_motor_duty(4,int(-y_vel*MOTOR_SPD_SCALER+x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER+OFF_CENTER_SPIN_SHIFT)))
            

        #time.sleep(0.05)
#END USER CODE LOOP
    _stop_event.set()
    if _spin_thread.is_alive():
        _spin_thread.join(timeout=2.0)


if __name__ == '__main__':
    main()

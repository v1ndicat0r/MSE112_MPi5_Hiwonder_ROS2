import rclpy
import threading
from . import board_interface
from .board_interface import BoardInterface
from . import cv_interface
from .cv_interface import CVInterface

#START USER CODE IMPORTS

import time
import math

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

    line_follow_pos = [0.0,0.0,0.0,-70.0,-90.0,90.0,0.0]


    MOTOR_SPD_SCALER = 100
    OFF_CENTER_SPIN_SHIFT = 50

        #Initializations



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
        
        x1,y1,x2,y2 = cv.green_lines



        #print(f"CV lines:")


        #Find centroid of the line for lateral strafe P control
        x_centroid = (x1+x2)/2

        #Error from center screen to target (normalized) 
        error = x_centroid/320.0


        #Find angle of the line for yaw P control
            #Shift the line into the cartesian plane centered on x1, y1
        shifted_y = y2 - y1
        shifted_x = x2 - x1

            #Apply vertical atan for angle
        if shifted_y==0:
            line_ang = 0
        else:
            line_ang = math.atan((-shifted_x)/shifted_y)/3.14*2

        print(f"Line ang: {line_ang*90:.2f}")
        
        
        
        #Set velocities
        x_vel = error * (0.17)

        if abs(line_ang) < 0.30:
            y_vel = 0.17
        else:
            y_vel = 0.0

        z_vel = line_ang * (0.80)
	
        #print(f"z_vel: {z_vel:.2f}")

            #Basic mechanum mapping with spin centered around arm joint 0
        board.set_dc_motor_duty(1,int(-y_vel*MOTOR_SPD_SCALER-x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER-OFF_CENTER_SPIN_SHIFT)))
        board.set_dc_motor_duty(2,int(y_vel*MOTOR_SPD_SCALER-x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER-OFF_CENTER_SPIN_SHIFT)))
        board.set_dc_motor_duty(3,int(y_vel*MOTOR_SPD_SCALER+x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER+OFF_CENTER_SPIN_SHIFT)))
        board.set_dc_motor_duty(4,int(-y_vel*MOTOR_SPD_SCALER+x_vel*MOTOR_SPD_SCALER+z_vel*(MOTOR_SPD_SCALER+OFF_CENTER_SPIN_SHIFT)))



        

        time.sleep(0.05)
#END USER CODE LOOP
    _stop_event.set()
    if _spin_thread.is_alive():
        _spin_thread.join(timeout=2.0)


if __name__ == '__main__':
    main()

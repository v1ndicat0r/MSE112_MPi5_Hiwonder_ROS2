import rclpy
import threading
from . import board_interface
from .board_interface import BoardInterface
from . import cv_interface
from .cv_interface import CVInterface

#START USER CODE IMPORTS

import time

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
        
        lines = cv.green_lines

        print(f"CV lines:")

            #Find the first line that crosses the y=400 line
        x_intersection = 320

        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line

                #print(f"Start: {x1}, {y1}     End: {x2}, {y2}")

                if (y1>400 and y2<400) or (y1<400 and y2>400):
                    try:
                        m = (y2-y1)/(x2-x1)
                    except Exception as e:
                        m = 480
                    b = y1 - m*x1
                    try:
                        x_intersection = (400-b)/m
                    except Exception as e:
                        x_intersection = 320
                    print(f"Found: {x_intersection}, {400}")
            #Error from center screen to target     
        error = (x_intersection - 320)/320


        x_vel = 0.0
        y_vel = 0.2
        z_vel = error * 0.5


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

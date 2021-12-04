# https://pollen-robotics.github.io/reachy-simulator/
from time import sleep
from reachy import parts, Reachy
import logging
import threading
import sys
import os


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = "p_dSAag80F3raThL1Hy3CLTZdf_YOCaJXkHH2hOYF5zTuGUuAcmE-9RZcK7qUCh0hrTlAY-ttBb7v_arhfU7sg=="
org = "howest"
bucket = "iot_bucket"

client = InfluxDBClient(url="http://172.23.83.63:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)


def sendDataToInfluxDB(motor, temp):
    data = "Reachy,host={} used_percent={}".format(motor, temp)
    write_api.write(bucket, org, data)
    sleep(0.7)
    print(data)


r = Reachy(
    right_arm=parts.RightArm(io='ws', hand='force_gripper'),
    left_arm=parts.LeftArm(io='ws', hand='force_gripper'),
    head=parts.Head(io='ws'),
)

def temp_thread():
    GetMotorTemps()

TempThread = threading.Thread(target=temp_thread)


def NodHead():
    r.head.neck.disk_bottom.compliant = False
    for _ in range(3):
        r.head.look_at(0.5, 0, -0.2, duration=1, wait=True)
        r.head.look_at(0.5, 0, 0.2, duration=1, wait=True)
    r.head.look_at(0.5, 0, 0.05, duration=1, wait=False)

def ShakeHead():
    r.head.neck.disk_bottom.compliant = False
    for _ in range(2):
        r.head.look_at(0.5, 0.2, 0, duration=1, wait=True)
        r.head.look_at(0.5, -0.2, 0, duration=1, wait=True)
    r.head.look_at(0.5, 0.1, 0, duration=1, wait=False)

def CloseHands():
    r.left_arm.hand.close()
    r.right_arm.hand.close()

def MoveToStandard(arm):
    if arm == "left_arm":
        print("Moving left arm to standard positions")
        r.left_arm.hand.forearm_yaw.goto(goal_position=0, duration=2,interpolation_mode='minjerk', wait=False)
        r.left_arm.elbow_pitch.goto(goal_position=-0, duration=2,interpolation_mode='minjerk', wait=False)
        r.left_arm.shoulder_pitch.goto(goal_position=-0, duration=2,interpolation_mode='minjerk',wait=False)
        r.left_arm.shoulder_roll.goto(goal_position=-0, duration = 2,interpolation_mode='minjerk', wait=False)
        r.left_arm.arm_yaw.goto(goal_position = -0, duration=2,interpolation_mode='minjerk', wait=False)
        r.left_arm.hand.wrist_roll.goto(goal_position=0, duration=0.5, wait=False)
    else:
        print("Moving right arm to standard positions")
        r.right_arm.hand.forearm_yaw.goto(goal_position=-0, duration=2,interpolation_mode='minjerk', wait=False)
        r.right_arm.shoulder_pitch.goto(goal_position=-0, duration=2,interpolation_mode='minjerk',wait=False)
        r.right_arm.shoulder_roll.goto(goal_position=0, duration = 2,interpolation_mode='minjerk', wait=False)
        r.right_arm.arm_yaw.goto(goal_position = 0, duration=2,interpolation_mode='minjerk', wait=False)
        r.right_arm.elbow_pitch.goto(goal_position=-0, duration=2, interpolation_mode='minjerk', wait=False)
        r.right_arm.hand.wrist_roll.goto(goal_position=0, duration=0.5, wait=False)


def CrossingArms():
    r.left_arm.hand.forearm_yaw.goto(goal_position=120, duration=2,interpolation_mode='minjerk', wait=False)
    r.left_arm.elbow_pitch.goto(goal_position=-100, duration=2,interpolation_mode='minjerk', wait=False)
    r.left_arm.shoulder_pitch.goto(goal_position=-68, duration=2,interpolation_mode='minjerk',wait=False)
    r.left_arm.shoulder_roll.goto(goal_position=-180, duration = 2,interpolation_mode='minjerk', wait=False)
    r.left_arm.arm_yaw.goto(goal_position = -88, duration=2,interpolation_mode='minjerk', wait=False)
    r.left_arm.hand.wrist_roll.goto(goal_position=-30, duration=0.5, wait=False)

    r.right_arm.hand.forearm_yaw.goto(goal_position=-65, duration=2,interpolation_mode='minjerk', wait=False)
    r.right_arm.shoulder_pitch.goto(goal_position=-50, duration=2,interpolation_mode='minjerk',wait=False)
    r.right_arm.shoulder_roll.goto(goal_position=180, duration = 2,interpolation_mode='minjerk', wait=False)
    r.right_arm.arm_yaw.goto(goal_position = 148, duration=2,interpolation_mode='minjerk', wait=False)
    r.right_arm.elbow_pitch.goto(goal_position=-95, duration=2, interpolation_mode='minjerk', wait=False)
    r.right_arm.hand.wrist_roll.goto(goal_position=30, duration=0.5, wait=True)
    sleep(1)


def HandShake(Choice):
    if Choice == "left_arm":
        print("Beginning shake on left hand")
        r.head.look_at(45, 20, -20, duration=1, wait=True)
        r.left_arm.shoulder_pitch.goto(goal_position=-20, duration = 2,interpolation_mode='minjerk', wait=False)
        r.left_arm.elbow_pitch.goto(goal_position=-70, duration=2,interpolation_mode='minjerk', wait=False)
        r.left_arm.hand.open()
        r.head.look_at(0.5, 0, 0.05, duration=1, wait=False)
        r.left_arm.hand.forearm_yaw.goto(goal_position=-90, duration=2,interpolation_mode='minjerk', wait=True)
        r.left_arm.elbow_pitch.compliant = True #Zorgt er voor dat men echt de hand kan schudden
        for _ in range(3):
            r.left_arm.hand.wrist_roll.goto(goal_position=30, duration=0.5, wait=True)
            r.left_arm.hand.wrist_roll.goto(goal_position=-30, duration=0.5, wait=True)
        r.left_arm.hand.wrist_roll.goto(goal_position=0, duration=0.5, wait=True)
        r.left_arm.elbow_pitch.compliant = False #Arm terug naar non compliant
    else:
        print("Beginning shake on right hand")
        r.head.look_at(45, -20, -20, duration=1, wait=True)
        r.right_arm.shoulder_pitch.goto(goal_position=-20, duration = 2,interpolation_mode='minjerk', wait=False)
        r.right_arm.elbow_pitch.goto(goal_position=-70, duration=2,interpolation_mode='minjerk', wait=False)
        r.right_arm.hand.open()
        r.head.look_at(0.5, 0, 0.05, duration=1, wait=False)
        r.right_arm.hand.forearm_yaw.goto(goal_position=90, duration=2,interpolation_mode='minjerk', wait=True)
        r.right_arm.elbow_pitch.compliant = True #Zorgt er voor dat men echt de hand kan schudden
        for _ in range(3):
            r.right_arm.hand.wrist_roll.goto(goal_position=30, duration=0.5, wait=True)
            r.right_arm.hand.wrist_roll.goto(goal_position=-30, duration=0.5, wait=True)
        r.right_arm.hand.wrist_roll.goto(goal_position=0, duration=0.5, wait=True)
        r.right_arm.elbow_pitch.compliant = False #Arm terug naar non compliant


def MainHandShake():
    print("Running HandShake")
    choice2 = input("Handshake on left arm, or right? (left/right): ")
    choice2 = choice2.lower()
    if choice2 == "left":
        HandShake("left_arm")
        MoveToStandard("left_arm")
        CloseHands()
    elif choice2 == "right":
        HandShake("right_arm")
        MoveToStandard("right_arm")
        CloseHands()
    else:
        print("Invalid input! must be right/left")
        MainHandShake()

def MainChoice():
    CloseHands()
    choice = input("Does reachy agree? (yes/no): ")
    choice = choice.lower()
    if choice == "yes":
        print("Reachy agreed")
        NodHead()
    elif choice == "no":
        print("Running CrossingArms")
        CrossingArms()
        ShakeHead()
        MoveToStandard("right_arm")
        sleep(0.5)
        MoveToStandard("left_arm")
        sleep(3)
    else:
        print("Invalid input! must be yes/no")
        MainChoice()


def GetMotorTemps():
    while True:
        for motor in r.right_arm.motors:
            sleep(0.5)
            #sendDataToInfluxDB(motor.name, motor.temperature)
            if  motor.temperature > 45:
                print("Fan for", motor.name, "was triggered. Temp:", motor.temperature)
            if motor.temperature >= 53:
                print("Motor Temperature for", motor.name, "CRITICAL! Temp:", motor.temperature)
            
        for motor in r.left_arm.motors:
            sleep(0.5)
            #sendDataToInfluxDB(motor.name, motor.temperature)
            if  motor.temperature > 45:
                print("Fan for", motor.name, "was triggered. Temp:", motor.temperature)
            if motor.temperature >= 53:
                print("Motor Temperature for", motor.name, "CRITICAL! Temp:", motor.temperature)        

def main():
    try:
        TempThread.start()
        MainChoice()
        MainHandShake()
    except:
        print("Something went wrong!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
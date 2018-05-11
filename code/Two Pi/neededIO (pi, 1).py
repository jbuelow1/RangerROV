import pygame
import math
import subprocess
import socket

class Control:
    #functions to get joystick positions
    def XPosition(self, joystickXZ):
        axis = joystickXZ.get_axis(0)
        if axis < 0.06 and axis > -0.06:
            axis = 0
        return axis
    
    def ZPosition(self, joystickXZ):
        axis = joystickXZ.get_axis(1) * (-1)
        if axis < 0.06 and axis > -0.06:
            axis = 0
        return axis
    
    def YPosition(self, joystickY):
        axis = joystickY.get_axis(0)
        if axis < 0.06 and axis > -0.06:
            axis = 0
        return axis
    def YTilt(self, joystickY):
        axis = joystickY.get_axis(1)
        if axis < 0.06 and axis > -0.06:
            axis = 0
        return axis
    def ClawPosition(self, joystickXZ):
        axis = joystickXZ.get_axis(2) * (-1)
        return axis
    
    #Setup function to figure out which joystick to use.
    def findJoystick(self):
        numJoystick = pygame.joystick.get_count()
        if numJoystick > 1:
            print("Would you like to use:")
            for i in range(numJoystick):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()
                print(str(i) + ". " + name)
            while 1:
                try:
                    joystickNum = int(input())
                    joystick = pygame.joystick.Joystick(joystickNum)
                    joystick.init()
                    name = joystick.get_name()
                    break
                except:
                    print("Ints only and that int has to match one of the choices")
        elif numJoystick < 1:
            joystick = 0
            print("This feature is coming soon")
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            name = joystick.get_name()
        return joystick

    def DidPressExit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            return False
                

#Render statistics in the main window
class GUI:

    black = (0, 0, 0)
    white = (255, 255, 255)
    pygame.font.init()
    font = pygame.font.Font(None, 28)

    def joystickStats(self, Control, Motor, joystickXZ, joystickY, screen):
        Xspeed = GUI.font.render("X Axis: " + str(math.floor(Control.XPosition(joystickXZ)*100)), 1, GUI.black, GUI.white)
        Zspeed = GUI.font.render("Z Axis: " + str(math.floor(Control.ZPosition(joystickXZ)*100)), 1, GUI.black, GUI.white)
        YSpeed = GUI.font.render("Y Axis: " + str(math.floor(Control.YPosition(joystickY) * 100)), 1, GUI.black, GUI.white)
        YTilt = GUI.font.render("Y Tilt: " + str(math.floor(Control.YTilt(joystickY) * 100)), 1, GUI.black, GUI.white)
        Claw = GUI.font.render("Claw: " + str(math.floor(Control.ClawPosition(joystickXZ) * 100)), 1, GUI.black, GUI.white)
        screen.blit(Xspeed,(1,0))
        screen.blit(Zspeed,(1,25))
        screen.blit(YSpeed,(1,50))
        screen.blit(YTilt,(1,75))
        screen.blit(Claw,(1,100))
        
    def motorStats(self, Motors, Control, joystickXZ, joystickY, screen, AmpList, AmpPool):
        motorList = Motors.FindTotalSpeed(Motors, Control, joystickY, joystickXZ, AmpList, AmpPool)
        leftMotorSpeed = GUI.font.render("Left motor: " + str(motorList[0]), 1, GUI.black, GUI.white)
        rightMotorSpeed = GUI.font.render("Right motor: " + str(motorList[1]), 1, GUI.black, GUI.white)
        frontMotorSpeed = GUI.font.render("Front motor: " + str(motorList[2]), 1, GUI.black, GUI.white)
        backMotorSpeed = GUI.font.render("Back motor: " + str(motorList[3]), 1, GUI.black, GUI.white)
        AmpsUsed = GUI.font.render("Amps Used: " + str(motorList[4]), 1, GUI.black, GUI.white)
        screen.blit(leftMotorSpeed,(1,125))
        screen.blit(rightMotorSpeed,(1,150))
        screen.blit(frontMotorSpeed, (1,175))
        screen.blit(backMotorSpeed, (1,200))
        screen.blit(AmpsUsed, (1,225))
        
class Motors:
    #Find PWM data to run motors for desired speed
    def findTimeHigh(self, Input):
        if Input == 0:
            return 2458
        elif Input > 0 and Input <= 1:
            TimeHigh = math.floor((3112*Input)+(2458*(1-Input)))
            return TimeHigh
        elif Input <0 and Input >= -1:
            Input *= (-1)
            TimeHigh = math.floor((1802*Input)+(2458*(1-Input)))
            return TimeHigh
        else:
            print("Error: Input was not between -1 and 1 as it was: " + str(joystickAxis))
            return 2458

    #Aggregates the PWM data of all motors for pickle.
    def listOfTimeHigh(self, Control, motors, joystickXZ, joystickY):
        left, right = motors.FindXZSpeed(Control, joystickXZ, motors)
        front, back = motors.FindYSpeed(Control, joystickY, motors)
        motorList = [left, right, front, back]
        for num in range(len(motorList)):
            motorList[num] = motors.findTimeHigh(motorList[num])
        return motorList
    
    def FindMultiplier(self, firstMotor, secondMotor):
        multiplier = 1
    
        #Numbers can go above 1, need to reduce the highest number down to 1, while scaling the other down at the same rate
        if abs(firstMotor) > 1 or abs(secondMotor) > 1:
            
            #oneline check to find the highest number
            highestNum = max(abs(firstMotor), abs(secondMotor))
            
            #outcome will reduce highest number to 1 and scale other at the same rate
            multiplier = 1 / highestNum
            
        return multiplier
    
    def roundUp(self, x):
        return int(math.ceil(x / 10.0)) * 10

    def FindXZSpeed(self, Control, joystickXZ, Motors):
        leftMotor = (Control.ZPosition(joystickXZ))+(Control.XPosition(joystickXZ))
        rightMotor = (Control.ZPosition(joystickXZ))-(Control.XPosition(joystickXZ))
        multiplier = Motors.FindMultiplier(leftMotor, rightMotor)
        leftMotor *= multiplier
        rightMotor *= multiplier
            
        return leftMotor, rightMotor

    def FindYSpeed(self, Control, joystickY, Motors):
        frontMotor = (Control.YPosition(joystickY))+(Control.YTilt(joystickY))
        backMotor = (Control.YPosition(joystickY))-(Control.YTilt(joystickY))
        multiplier = Motors.FindMultiplier(frontMotor, backMotor)
        frontMotor *= multiplier
        backMotor *= multiplier
        return frontMotor, backMotor

    def FindAmpsUsed(self, PWMList, AmpList, Motors):
        totalAmpsUsed = 0.0
        for PWM in PWMList:
            try:
                num = float(AmpList[int(AmpList.index(str(Motors.roundUp(PWM*0.6103515625))))+1])
                totalAmpsUsed += num
            except:
                   print(PWM)
        return totalAmpsUsed

    def Forward(self, ampToFind, ampList):
        tickSpeed = 2458
        num = len(ampList) -1
        lastCheck = 0
        while num >= lastCheck:
            if float(ampList[num]) < ampToFind:
                tickSpeed = math.floor(float(ampList[num-1])/0.6103515625)
                break
            num -= 1
        return tickSpeed
    
    def Backward(self, ampToFind, ampList):
        tickSpeed = 2458
        for num in range(0, len(ampList)):
            if float(ampList[num]) < ampToFind:
                tickSpeed = math.floor(float(ampList[num-1])/0.6103515625)
                break
        return tickSpeed
                
    
    def FindNewTicks(self, Motors, AmpList, AmpPool, AmpsUsed, timesHigh ):
        listOfAmps = []
        for amp in timesHigh:
            ampList = [amp]
            listOfAmps.append(Motors.FindAmpsUsed(ampList, AmpList, Motors))
        multiplier = AmpPool/AmpsUsed
        newTickList= []
        for num in range(len(listOfAmps)):
            listOfAmps[num] *= multiplier
            if int(timesHigh[num]) > 2458:
                newTickList.append(Motors.Forward(listOfAmps[num], AmpList))
            elif int(timesHigh[num]) < 2458:
                newTickList.append(Motors.Backward(listOfAmps[num], AmpList))
            else:
                newTickList.append(2458)
        return newTickList
            
    def FindTotalSpeed(self, Motors, Control, joystickY, joystickXZ, AmpList, AmpPool):
        timesHigh = Motors.listOfTimeHigh(Control, Motors, joystickXZ, joystickY)        
        totalAmpsUsed = Motors.FindAmpsUsed(timesHigh, AmpList, Motors)
        if totalAmpsUsed > 20:
            newTickList = Motors.FindNewTicks(Motors, AmpList, AmpPool, totalAmpsUsed, timesHigh)
            NewAmpsUsed = Motors.FindAmpsUsed(newTickList, AmpList, Motors)
            newTickList.append(NewAmpsUsed)
            return newTickList
        elif totalAmpsUsed <= 20:
            timesHigh.append(totalAmpsUsed)
            return timesHigh

class Camera:

    def serverStart(self):
        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(0)

        #Accept a single connection and make a file-like object out of it
        #connection = server_socket.accept()[0].makefile('rb')
        return server_socket
        
    def clientStart(self):
        client_socket = socket.socket()
        client_socket.connect(('192.168.0.6', 8000))

        #Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        return connection

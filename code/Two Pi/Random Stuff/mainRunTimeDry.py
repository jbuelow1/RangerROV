import pygame
import neededIO as rovSTD
import pickle
import socket

pygame.init()

#Contoller SetUp
pygame.joystick.init()
Control = rovSTD.Control()
print("First pick a joystick for XZ movment")
joystickXZ = Control.findJoystick()
print("Now pick a joystick for Y movment")
joystickY = Control.findJoystick()


#Display SetUp
screen = pygame.display.set_mode((720,480))
GUI = rovSTD.GUI()
screen.fill(GUI.white)
pygame.display.flip()


#Motor SetUp
Motors = rovSTD.Motors()

#Socket SetUp
mainSocket = socket.socket()
host = '192.168.0.8'
port = 12332
mainSocket.connect((host, port))
print(mainSocket.recv(1024))

#Main Loop
clock = pygame.time.Clock()
crashed = False
while not crashed:
    clock.tick(30)
    screen.fill(GUI.white)
    GUI.joystickStats(Control, Motors, joystickXZ, joystickY, screen)
    GUI.motorStats(Motors, Control, joystickXZ, joystickY, screen)
    data = pickle.dumps(Motors.listOfTimeHigh(Control, Motors, joystickXZ, joystickY), -1)
    mainSocket.send(data)
    crashed = Control.DidPressExit()
    pygame.display.flip()


pygame.quit ()
mainSocket.close

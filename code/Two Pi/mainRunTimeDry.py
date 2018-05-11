import pygame
import neededIO as rovSTD
import pickle
import socket
import subprocess
import time
import threading

def startCamera():
    import CameraServer

pygame.init()

#Contoller setup
pygame.joystick.init()
Control = rovSTD.Control()
print("First pick a joystick for XZ movment")
joystickXZ = Control.findJoystick()
print("Now pick a joystick for Y movment")
joystickY = Control.findJoystick()

#Motor setup
Motors = rovSTD.Motors()
PWM = rovSTD.PWM()
AmpList = pickle.load(open("pickledAmpList.p", "rb"))
AmpPool = 600

#Socket setup
while True:
    try:
        mainSocket = socket.socket()
        host = '169.254.72.109'
        port = 12344
        mainSocket.connect((host, port))
        print(mainSocket.recv(1024))
        break

    except:
        print("Failed to connect, trying again")
        
threading.Thread(target=startCamera).start()

#Display setup
screen = pygame.display.set_mode((720,480))
GUI = rovSTD.GUI()
screen.fill(GUI.white)
pygame.display.flip()


#Loop setup
clock = pygame.time.Clock()
exiting = False

while not exiting:
    clock.tick(30)
    screen.fill(GUI.white)
    
        #Write statistics to window
    GUI.joystickStats(Control, Motors, joystickXZ, joystickY, screen)
    GUI.motorStats(Motors, Control, joystickXZ, joystickY, screen, AmpList, AmpPool, PWM)
        
        #Pickle data and send over network
    data = pickle.dumps(Motors.FindTotalSpeed(Motors, Control, joystickY, joystickXZ, AmpList, AmpPool, PWM), 1)
    mainSocket.send(data)
        
    exiting = Control.DidPressExit()
    pygame.display.flip()
    #except:
    #print("Ran into unknow error, exiting program")
    #exiting = True


pygame.quit ()
mainSocket.close

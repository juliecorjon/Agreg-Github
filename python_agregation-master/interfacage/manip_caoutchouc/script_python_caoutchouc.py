#!/usr/bin/python
# -*-coding:utf-8 -*

import serial
import matplotlib.pyplot as plt
import numpy as np
from time import time
import sys
plt.ion()

'''
README:

Commencez par lancer le logiciel Arduino IDE. Téléverser (petite icone en haut à gauche dans l'interface du programme) le code source ci-joint.
Ensuite, lancez ce programme après avoir choisi tmax le temps de mesure en secondes. À la fin de la mesure, un fichier .txt est exporté, que vous pouvez traiter sous QtiPlot ou Igor.
'''


#arduino = serial.Serial('/dev/ttyACM0',9600) #le port /dev/ttyACM0 n'est normalement pas à changer. Celui-ci est indiqué en bas à droite de l'interface Arduino.
arduino = serial.Serial('COM4',9600)

path='Bureau'

tmax=30

def trace(tmax):
    t0=time()
    texp=0
    x=[]
    y=[]

    while (texp<tmax):
        if (arduino.inWaiting()>0):
            texp=time()-t0
            myData = arduino.readline()
            
            try:
                # A du mal à syncrhoniser au début, et peut sortir des choses bizarres. Décommenter le "print" dans except pour l'observer
                myData = float(myData)
                x.append(texp)
                y.append(myData)

            except ValueError:
                #print 'Valeur à t=' + str(texp) + ' écartée : ' +myData
                pass
  
    plt.plot(x,y,'.')
    plt.axis([0, tmax, 0, 40])
    np.savetxt(path+'data_temps.txt', x)
    np.savetxt(path+'data_temperature.txt', y)
    input()

if __name__ == "__main__":
    trace(tmax)

arduino.close()

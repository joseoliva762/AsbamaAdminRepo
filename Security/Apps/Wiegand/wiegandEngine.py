#!/usr/bin/env python3

import RPi.GPIO as GPIO
from typing import List
import requests
import time
import os
from Apps.Wiegand.utils.printer import Printer
from Apps.Wiegand.CardList import CardList

class WiegandEngine(CardList):

    def __init__(self, bitCero=24, bitUno=23, pinLed=17, beeper=27, bitMaximo=26):
        super().__init__(maximunLenProtocol=26)
        self.bitCero = bitCero
        self.bitUno = bitUno
        self.pinLed = pinLed
        self.beeper = beeper
        self.bitMaximo = bitMaximo
        self.printer = Printer()
        self._pinModeInit(setMode="BCM", setWarnings=False)

    
    def _pinModeInit(self, setMode="BCM", setWarnings=False):
        GPIO.setwarnings(setWarnings)
        GPIO.setmode(self._piSetMode(setMode))

        self._piPinSetup(channel=self.bitCero, state="IN" )
        self._piPinSetup(channel=self.bitUno,  state="IN" )
        self._piPinSetup(channel=self.pinLed,  state="OUT")
        self._piPinSetup(channel=self.beeper,  state="OUT")
        # Inicializo el led y el beeper en OFF
        self.userCanAccess(status=False)


    def _piSetMode(self, setMode):
        self.printer.printBoardSetMode(setMode)
        return GPIO.BCM if setMode.lower() == "BCM".lower() else GPIO.BOARD
    
    def _piPinSetup(self, channel, state="OUT"):
        self.printer.printInitPin(channel, state)
        GPIO.setup(channel, GPIO.OUT if state.lower() == "OUT".lower() else GPIO.IN )        


    def userCanAccess(self, status): 
        self.setOutput(channel=self.pinLed, status=not status)
        self.setOutput(channel=self.beeper, status=not status)
    
    def togglesAccess(self):
        self.userCanAccess(True)
        time.sleep(0.5)
        self.userCanAccess(False)
            

    def setOutput(self, channel, status):
        GPIO.output(channel, status)

    def disable_interrupt(self):
        time.sleep(0.3)
        GPIO.remove_event_detect(self.bitCero)
        GPIO.remove_event_detect(self.bitUno)

    def enable_interrupt(self):
        time.sleep(0.3)
        GPIO.add_event_detect(self.bitCero, GPIO.FALLING)
        GPIO.add_event_detect(self.bitUno, GPIO.FALLING)
        GPIO.add_event_callback(self.bitCero, self.callback_data0)
        GPIO.add_event_callback(self.bitUno, self.callback_data1)
            
    def callback_data0(self, data0):
        self.AddBitToCardList(0)

    def callback_data1(self, data1):
        self.AddBitToCardList(1)
    
    def read_card(self, sleepTime=0.001):
        self.id = 0
        self.mask = 0
        self.code = list()
        self.togglesAccess()
        try:
            self.enable_interrupt()
        except RuntimeError:
            print("Interrupcion previamente encendida")
        print("Leyendo...")
        while(len(self.code) != self.maximunLenProtocol):            
            time.sleep(sleepTime) #esperando lectura de tarjeta
        self.disable_interrupt()
        self.getIdFromCode()
        return(self.id) 
    
    def getIdFromCode(self):
        self.code.pop( self.maximunLenProtocol - 1 )
        self.code.pop( 0 )
        try:
            for bit in self.code:
                if(bit == 1):
                    self.id = self.id + (1 << ( ( self.maximunLenProtocol - 3 ) - self.mask))
                self.mask += 1
            print("Code ID:\n", self.code)
            print("User ID: ", self.id)     
        except:
            print('Error obteniendo el Card ID...')
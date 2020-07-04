import serial
import time
import subprocess
import os

class Sim800l:
    def __init__(self, puerto = "ttyS0"):
        print("Inicializando SIM800L...")
        self.puerto = puerto
        self.phone = self._serialInit()
        print("Inicializado SIM800L [OK]")
                
    def _serialInit(self, baudios = 9600, timeout=1):
        return serial.Serial('/dev/{}'.format(self.puerto), baudios, timeout=timeout)
    
    
    def getPhone(self):
        return self.phone
    
    
    def sms(self, mensaje, numeroDeTelefono, encode='utf-8'):
        self._sendSMS("AT\r", encode, 1)
        self._sendSMS("AT+CMGF=1\r\n", encode, 1)
        self._sendSMS('AT+CMGS="+57{}"\r\n'.format(numeroDeTelefono), encode, 2)
        self._sendSMS(mensaje+chr(26), encode, 4)
        print("Mensaje enviado")
        
    def _sendSMS(self, codigoAT, encode, seg):
        self.phone.write(codigoAT.encode(encode))
        time.sleep(seg)
        
        
    def sim800Response(self, mensaje="CMTI"):
        while True:
            try:
                response = str(self.phone.readline())
                print(response)
                if mensaje in response:             
                    break
            except:
                print ("Ha ocurrido una excepcion")
                print ('-'*60)
                subprocess.call(['sudo', 'systemctl', 'stop', 'serial-getty@{}.service'.format(self.puerto)])
        
from Apps.Hilos.myThread import MyThread
from Apps.Wiegand.wiegandEngine import WiegandEngine

class Sim800Thread(MyThread):
    def __init__(self, threadName, modules=[ WiegandEngine() ]):
        super().__init__(threadName=threadName)
        self.service = modules[0]
        self.sim = modules[1]
        self.phones = modules[2]
        
    def runThread(self):
        for phone in self.phones:
            if(phone.required):
                print('Enviando aviso a: {}...'.format(phone.telefono))
                mensaje = ('Hola {}, ha irrumpido un intruso en la bananera.'.format(phone.telefono))
                self.sim.sms(mensaje, str(phone.telefono))
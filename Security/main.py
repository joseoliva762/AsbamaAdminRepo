import time
import subprocess
import RPi.GPIO as GPIO
from datetime import datetime
from Apps.Wiegand.wiegandEngine import WiegandEngine
from Apps.SIM800L.sim800l import Sim800l
from Apps.Camara.camara import Camara
from Apps.IntruderDetecter.intruderDetecter import IntruderDetecter
from Apps.service import Service

from Apps.Hilos.wiegandThread import WiegandThread
from Apps.Hilos.camaraThread import CamaraThread
from Apps.Hilos.sim800Thread import Sim800Thread

#Pruebas
import threading
try:
    import thread
except ImportError:
    import _thread as thread

def quitFunction(fn_name):
    thread.interrupt_main() # raises KeyboardInterrupt

def exitAfter():
    def outer(fn):
        def inner(*args, **kwargs):
            timeout = float(args[1])
            timer = threading.Timer(timeout, quitFunction, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

@exitAfter()
def readCard(wiegand, timeout):
    try:
        wiegand.read_card()
    except KeyboardInterrupt:
        print('Time Out')

def _modulesInit():
    wiegand = WiegandEngine(bitMaximo=26)
    sim = Sim800l()
    camara = Camara()
    IntruderD = IntruderDetecter()
    service = Service()
    return wiegand, sim, camara, IntruderD, service

def sistemRestart():
    GPIO.cleanup()
    time.sleep(0.3)
    wiegand, sim, camara, IntruderD, service = _modulesInit()
    return  wiegand, sim, camara, IntruderD, service

def _run(wiegand, sim, camara, intruderD, service):
    while(True):
        try:
            try:
                recognitionTime = 3.0
                intruderD.enable_interrupt()
                print("Esperando Ingreso...")
                while( True ):
                    if(intruderD.areThereIntruders):
                        time.sleep(0.3)
                        # Consulta a la base de datos
                        configutation = service.getConfiguration()
                        systemState = configutation.to_dict()['estadodelsistema']
                        resolution = configutation.to_dict()['resolucioncamara']
                        waitingTime = configutation.to_dict()['tiempodeespera']
                        print("Data Service: ", systemState, resolution, waitingTime)
                        if( systemState ): # si el sistema está encendido
                            intruderD.disable_interrupt()
                            intruderD.togglesLamp()
                            while(intruderD.areThereIntruders):
                                date = datetime.now()
                                # Hilo para la camara
                                camaraModules = [ camara, resolution, date, waitingTime ]
                                myCamaraThread = CamaraThread("camaraThread", camaraModules)
                                myCamaraThread.start()
                                #Lectura de Wiegand
                                readCard(wiegand, waitingTime)
                                # Intruders Validation
                                userValidate, user = service.wiegandIdValidate(str(wiegand.id))
                                if( wiegand.id != 0 and userValidate):
                                    service.createRegister("Ingreso Seguro [OK]", str(user.id), date)
                                    wiegand.id = 0
                                else:
                                    service.undefinedRegister("Intruso en la Zona [WARNING]", user, date)
                                   # Hilo para el Sim800L
                                    phones = service.getPhones()
                                    simModules = [ service, sim, phones]
                                    mySimThread = Sim800Thread("simThread", simModules)
                                    mySimThread.start()
                                    mySimThread.join()

                                myCamaraThread.join()
                                if(myCamaraThread.is_alive()):
                                    subprocess.call(['kill', '-9', '{}'.format(myCamaraThread.pid)])
                                try:
                                    intruderD.thereArentIntruders()
                                    intruderD.enable_interrupt()
                                    print("Validando...")
                                    time.sleep(recognitionTime)
                                    print("Esperando Ingreso...")
                                except RuntimeError:
                                    pass
                                if( intruderD.areThereIntruders ):
                                    intruderD.disable_interrupt()
                            intruderD.togglesLamp()
                        else:
                            try:
                                print("El sistema esta apagado, Ingrese al apartado de configuracion  de la aplicacion para encenderlo.")
                                intruderD.thereArentIntruders()
                            except RuntimeError:
                               wiegand, sim, camara, intruderD, service = sistemRestart()
            except google.api_core.exceptions.Unknown:
                wiegand, sim, camara, intruderD, service = sistemRestart()
        except NameError:
            wiegand, sim, camara, IntruderD, service = sistemRestart()

if __name__ == '__main__':
    wiegand, sim, camara, intruderD, service = _modulesInit()
    _run(wiegand, sim, camara, intruderD, service)

# 3408 en 80
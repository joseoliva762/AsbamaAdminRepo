from Apps.Hilos.myThread import MyThread
from Apps.Wiegand.wiegandEngine import WiegandEngine
import multiprocessing

class WiegandThread(multiprocessing.Process):
    def __init__(self, threadName, modules):
        self.wiegand = WiegandEngine()
        super().__init__(name=threadName, target=self.runThread, args=(self.wiegand,))
        

    def runThread(self, wiegand):
        #self.wiegand.togglesAccess()
        wiegand.read_card()
        
    def getWiegand(self):
        return self.wiegand
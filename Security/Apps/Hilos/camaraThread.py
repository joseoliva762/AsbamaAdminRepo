from Apps.Camara.camara import Camara
from datetime import datetime
from Apps.Hilos.myThread import MyThread

class CamaraThread(MyThread):
    def __init__(self, threadName, modules):
        super().__init__(threadName=threadName)
        self.camara = modules[0]
        self.resolution = modules[1]
        self.date = modules[2]
        self.recordingTime = int(modules[3])

    def runThread(self):
        # Start
        self.camara.getPacket(self.resolution, self.date, self.recordingTime)
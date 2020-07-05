from Apps.Hilos.myThread import MyThread
import subprocess

class ConvertThread(MyThread):
    def __init__(self, threadName, modules):
        super().__init__(threadName=threadName)
        self.ruta = modules[0]
        self.mp4ruta = modules[1]
        

    def runThread(self):
        # Start
        print("Convirtiendo video...")
        subprocess.call([ 'ffmpeg', '-i', self.ruta, self.mp4ruta ])
        subprocess.call([ 'rm', self.ruta ])
        print("Video convertido [OK]")

import time
import picamera
import os
import subprocess
from datetime import datetime
from Apps.Hilos.convertThread import ConvertThread

class Camara:
    def __init__(self, ruta = "../App/static/Security/Evidencias/", waitingTime = 3):
        print("Inicializando CAMARA...")
        self.waitingTime = waitingTime
        self.ruta = ruta
        print("Inicializada CAMARA [OK]")

    def getPacket(self, resolucion = "720x560", date = datetime.now(), recordingTime = 30):
        widht, heith = self.getResolucion(resolucion)
        recordingTime *= self.waitingTime
        self._camFoto(widht, heith , self.waitingTime, date)
        self._camVideo(widht, heith, recordingTime, date)

    def getResolucion(self, resolucion):
        res = resolucion.split("x")
        return int(res[0]), int(res[1])

    def _camFoto(self, widht, heith , seg, date):
        print("Tomando foto...")
        with picamera.PiCamera() as picam:
            picam.resolution = (widht, heith)
            picam.start_preview()
            time.sleep(seg)
            ruta = self.getRuta(date)
            picam.capture(ruta)
            picam.stop_preview()
            picam.close()
            print("Foto guardada en la ruta: {} [OK]".format(ruta))

    def getRuta(self, date = datetime.now(), extension = "jpg" ):
        enrutado = "{}\'{}+00:00\'/".format(self.ruta, str(date))
        try:
            os.mkdir(enrutado)
        except FileExistsError:
            print("Directorio encontrado")
        finally:
            return "{}\'{}+00:00\'.{}".format(enrutado, str(date), extension)

    def _camVideo(self, widht, heith , recordingTime, date):
        print("Grabando...")
        with picamera.PiCamera() as picam:
            picam.resolution = (widht, heith)
            picam.start_preview()
            ruta = self.getRuta(date, extension = "h264")
            picam.start_recording(ruta)
            totalTime = int(recordingTime)
            picam.wait_recording(totalTime)
            picam.stop_recording()
            picam.stop_preview()
            print("Video guardado en la ruta: {} [OK]".format(ruta))
            #subprocess.call([ 'ffmpeg', '-i', ruta, self.getRuta(date,extension="mp4") ])
            #print("Video convertido [OK]")
            #modules = [
             #   ruta,
             #   self.getRuta(date,extension="mp4")
            #]
            #convert = ConvertThread("convertHilo", modules)
            #convert.start()ggggg
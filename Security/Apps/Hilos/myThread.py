import multiprocessing


# Clase Abstracta.
class MyThread(multiprocessing.Process):
    def __init__(self, threadName):
        super().__init__(name=threadName, target=self.runThread)

    def runThread(self):
        # Debe ser sobre escrita en el extension.
        pass
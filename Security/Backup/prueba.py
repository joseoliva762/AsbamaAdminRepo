from subprocess import check_output
import threading
import time

def get_pid(name):
    return check_output(['ps', 'aux', '|', '{}'.format(name)])
    
      
def holi(name, tiempo):
  while(True):
    time.sleep(tiempo)
  print(name)


name = 'Hilo1'
tiempo = 2
t1 = threading.Thread(name=name, target=holi, args=(name, 5.0))
t1.start()
# t1.join(float(tiempo))
t1.join()
if(t1.is_alive()):
  # print(get_pid(name))
  pass
print('Termino el {}'.format(name))
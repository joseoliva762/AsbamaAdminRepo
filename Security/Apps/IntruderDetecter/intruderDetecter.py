import RPi.GPIO as GPIO
from Apps.Wiegand.utils.printer import Printer

class IntruderDetecter:
    def __init__(self, door=12, moveOne=13, moveTwo=6, lamp=16, setMode="BCM", setWarnings=False):
        self.door = door
        self.moveOne = moveOne
        self.moveTwo = moveTwo
        self.lamp = lamp
        self.lampState = False
        self.printer = Printer()
        self.areThereIntruders = False
        self._pinModeInit(setMode, setWarnings)
        
        
    def _pinModeInit(self, setMode="BCM", setWarnings=False):
        GPIO.setwarnings(setWarnings)
        GPIO.setmode(self._piSetMode(setMode))

        self._piPinSetup(channel=self.door, state="IN" )
        #GPIO.setup(self.door, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        #self._piPinSetup(channel=self.moveOne,  state="IN" )
        #self._piPinSetup(channel=self.moveTwo,  state="IN")
        self._piPinSetup(channel=self.lamp,  state="OUT")
    
    def _piSetMode(self, setMode):
        self.printer.printBoardSetMode(setMode)
        return GPIO.BCM if setMode.lower() == "BCM".lower() else GPIO.BOARD
    
    def _piPinSetup(self, channel, state="OUT"):
        self.printer.printInitPin(channel, state)
        GPIO.setup(channel, GPIO.OUT if state.lower() == "OUT".lower() else GPIO.IN)

    def disable_interrupt(self):
        time.sleep(0.3)
        GPIO.remove_event_detect(self.door)
        #GPIO.remove_event_detect(self.moveOne)
        #GPIO.remove_event_detect(self.moveTwo)

    def enable_interrupt(self):
        time.sleep(0.3)
        GPIO.add_event_detect(self.door, GPIO.FALLING)
        #GPIO.add_event_detect(self.moveOne, GPIO.FALLING)
        #GPIO.add_event_detect(self.moveTwo, GPIO.FALLING)
        GPIO.add_event_callback(self.door, self._thereAreIntruders)
        #GPIO.add_event_callback(self.moveOne, self._thereAreIntruders)
        #GPIO.add_event_callback(self.moveTwo, self._thereAreIntruders)
                    
    def _thereAreIntruders(self, chanel):
        self.areThereIntruders = True
        
    def thereArentIntruders(self):
        self.areThereIntruders = False
        
    def togglesLamp(self):
        self.lampState = not self.lampState
        GPIO.output(self.lamp, self.lampState)
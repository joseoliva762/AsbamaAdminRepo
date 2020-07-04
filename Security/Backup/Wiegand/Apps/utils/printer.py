class Printer():
    def __init__(self):
        print("Printer Status On...")

    def printInitPin(slef, pin, state):
        print("-> Pin {} inicializado como {}".format(pin, "Salida." if state.lower() == "OUT".lower() else "Entrada."))

    def printBoardSetMode(self, setMode):
        print("Board Seteada en la disposicion de pines: {}.".format(setMode))

class CardList():
    def __init__(self, cardList=list(), maximunLenProtocol=26):
        self.code = cardList
        self.maximunLenProtocol = maximunLenProtocol
        self.mask = 0
        self.id = 0

    def AddBitToCardList(self, bit):
        self.code.append(bit)

    def getCardList(self):
        return self.code
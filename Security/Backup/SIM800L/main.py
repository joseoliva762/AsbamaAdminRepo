from sim800l import Sim800l


if __name__=="__main__":
    sim800l = Sim800l()
    mens="Falso"
    num="3003355083"
    sim800l.sms(mens,num)
    
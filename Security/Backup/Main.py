from Service import Service
from datetime import datetime
if __name__=="__main__":
    service=Service()
    validate,res=service.wiegandIdValidate(0)
    if validate:
        service.createRegister("Tu tormento", res.id, datetime.now())
        print(validate,res.id)
    else:
        #service.undefinedRegister("Ya te robaron", res, datetime.now())
        phones = service.getPhones()
        for phone in phones:
            print(phone.telefono)
        print(validate,res)
        
    
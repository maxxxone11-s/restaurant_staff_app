from random import randint

from app.schemas.iiko import IikoRequest

def iiko_service():
    return IikoRequest(revenue=randint(1000, 20000)) # сумма потом будет подтягиваться
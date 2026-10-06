from math import floor
def desquantitzacio(imatge_quantitzada, delta):
    return imatge_quantitzada * delta + floor(delta/2)
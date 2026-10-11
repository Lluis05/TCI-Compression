import numpy as np

"""
from math import floor 
def desquantitzacio_escalar(imatge_quantitzada, delta):
    return imatge_quantitzada * delta + floor(delta / 2)
 """

def desquantitzacio_escalar(imatge_quantitzada, delta):
    imatge_desquantitzada = (imatge_quantitzada.astype(np.int64) * delta + delta // 2) #transformem a int64 per evitar overflow
    maxim = np.iinfo(imatge_quantitzada.dtype).max
    imatge_desquantitzada[imatge_desquantitzada > maxim] = maxim
    return imatge_desquantitzada.astype(imatge_quantitzada.dtype)

def desquantitzacio_regions(imatge_quantitzada, delta):
    imatge_desquantitzada = imatge_quantitzada.astype(np.int64)
    meitat = imatge_quantitzada.shape[0] // 2
    imatge_desquantitzada[meitat:, :, :] = (imatge_desquantitzada[meitat:, :, :] * delta + delta // 2)
    maxim = np.iinfo(imatge_quantitzada.dtype).max
    imatge_desquantitzada[imatge_desquantitzada > maxim] = maxim
    return imatge_desquantitzada.astype(imatge_quantitzada.dtype)

def desquantitzacio_blocs(imatge_quantitzada, mida_bloc, max_delta):
    imatge_desquantitzada = imatge_quantitzada.astype(np.int64)  # int64 per evitar overflow
    delta = 1
 
    for i in range(0, imatge_quantitzada.shape[0], mida_bloc):
        for j in range(0, imatge_quantitzada.shape[1], mida_bloc):
            bloc = imatge_desquantitzada[i:i + mida_bloc, j:j + mida_bloc, :]
            imatge_desquantitzada[i:i + mida_bloc, j:j + mida_bloc, :] = bloc * delta + delta // 2
 
            delta = delta + 2
            if delta > max_delta:
                delta = 1
        delta = delta + 2
        if delta > max_delta:
            delta = 1
    maxim = np.iinfo(imatge_quantitzada.dtype).max
    imatge_desquantitzada[imatge_desquantitzada > maxim] = maxim
    return imatge_desquantitzada.astype(imatge_quantitzada.dtype)
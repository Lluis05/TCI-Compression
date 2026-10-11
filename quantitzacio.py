import numpy as np

def quantitzacio_escalar(imatge, delta):
    return imatge // delta

def quantitzacio_regions(imatge, delta):
    imatge_quantitzada = np.empty_like(imatge)
    meitat = imatge.shape[0] // 2
    imatge_quantitzada[:meitat, :, :] = imatge[:meitat, :, :]  # delta = 1: no cal fer res
    imatge_quantitzada[meitat:, :, :] = imatge[meitat:, :, :] // delta  # delta passat per parametre
    return imatge_quantitzada

def quantitzacio_blocs(imatge, mida_bloc, max_delta):
    imatge_quantitzada = np.empty_like(imatge)
    delta = 1
 
    for i in range(0, imatge.shape[0], mida_bloc):
        for j in range(0, imatge.shape[1], mida_bloc):
            bloc = imatge[i:i + mida_bloc, j:j + mida_bloc, :]
            imatge_quantitzada[i:i + mida_bloc, j:j + mida_bloc, :] = bloc // delta
 
            delta = delta + 2
            if delta > max_delta:
                delta = 1

        delta = delta + 2
        if delta > max_delta:
            delta = 1
 
    return imatge_quantitzada
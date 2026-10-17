import numpy as np

def calcular_pae(original, reconstruida):
    # passem a int64 per evitar wrap-around en restar uint8 (p.ex. 3 - 5 = 254)
    original = original.astype(np.int64)
    reconstruida = reconstruida.astype(np.int64)
    return np.max(np.abs(original - reconstruida))

def calcular_mse(original, reconstruida):
    original = original.astype(np.float64)
    reconstruida = reconstruida.astype(np.float64)
    error_elevat = np.square(original-reconstruida)
    return np.mean(error_elevat)

def calcular_psnr(original, reconstruida, max):
    mse = calcular_mse(original,reconstruida)
    if mse == 0:
        return np.inf
    return 10*np.log10(np.square(max)/mse)
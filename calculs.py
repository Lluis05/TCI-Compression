import numpy as np

def calcular_pae(original, reconstruida):
    # passem a int64 per evitar wrap-around en restar uint8 (p.ex. 3 - 5 = 254)
    original = original.astype(np.int64)
    reconstruida = reconstruida.astype(np.int64)
    return np.max(np.abs(original - reconstruida))
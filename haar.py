from math import floor
import numpy as np

def haar(imatge):
    datos = imatge.flatten()
    d = []
    s = []
    for i in range(0, len(datos) - 1, 2):
        x0, x1 = datos[i], datos[i+1]
        d.append(x1 - x0)
        s.append(x0 + floor((x1-x0)/2))

    return np.concatenate((s,d))

def haar_2d(imatge):
    imatge = imatge.astype(np.int64)

    # Transformada 1D a cada fila
    files = np.apply_along_axis(haar, axis=1, arr=imatge)

    # Transformada 1D a cada columna
    resultat = np.apply_along_axis(haar, axis=0, arr=files)

    return resultat

def haar_invers(imatge):
    datos = imatge.flatten()
    n = len(datos) // 2
    s = datos[:n]
    d = datos[n:]
    resultat = []
    for i in range(0, n):
        x0 = s[i] - floor(d[i] / 2)
        x1 = d[i] + x0
        resultat.append(x0)
        resultat.append(x1)

    return np.array(resultat)

def haar_invers2d(imatge):
    imatge = imatge.astype(np.int64)

    # Transformada 1D a cada columna
    columnes = np.apply_along_axis(haar_invers, axis=0, arr=imatge)
    
    # Transformada 1D a cada fila
    resultat = np.apply_along_axis(haar_invers, axis=1, arr=columnes)

    return resultat
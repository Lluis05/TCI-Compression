from math import floor
from entropy import calcular_entropia0_raw
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

def haar_2d(imatge, nivell=1):
    forma_original = imatge.shape
    resultat = imatge.astype(np.int64).copy()

    # Passem a 2D (files, columnes)
    files = forma_original[0]
    columnes = forma_original[1]
    resultat = resultat.reshape(files, columnes)

    # Zona LL activa (al principi, tota la imatge)
    files_actives = files
    columnes_actives = columnes

    for n in range(nivell):
        # Transformar les files de la zona LL activa
        for i in range(files_actives):
            resultat[i, :columnes_actives] = haar(resultat[i, :columnes_actives])

        # Transformar les columnes de la zona LL activa
        for j in range(columnes_actives):
            resultat[:files_actives, j] = haar(resultat[:files_actives, j])

        H0 = calcular_entropia0_raw(resultat)
        print(f"Entropia ordre 0 després del nivell {n + 1}: {H0}")

        files_actives //= 2
        columnes_actives //= 2

    return resultat.reshape(forma_original)

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


def haar_invers2d(imatge, nivell=1):
    forma_original = imatge.shape
    resultat = imatge.astype(np.int64).copy()

    # Passem a 2D (files, columnes)
    files = forma_original[0]
    columnes = forma_original[1]
    resultat = resultat.reshape(files, columnes)

    # Dimensions de la zona LL a cada nivell
    dimensions = []
    files_actives = files
    columnes_actives = columnes

    for _ in range(nivell):
        dimensions.append((files_actives, columnes_actives))
        files_actives //= 2
        columnes_actives //= 2

    # Desfer els nivells del més profund al primer
    for files_actives, columnes_actives in reversed(dimensions):

        # Primer, inversa de les columnes
        for j in range(columnes_actives):
            resultat[:files_actives, j] = haar_invers(resultat[:files_actives, j])

        # Després, inversa de les files
        for i in range(files_actives):
            resultat[i, :columnes_actives] = haar_invers(resultat[i, :columnes_actives])

    # Tornem a la forma original (y, x, z)
    return resultat.reshape(forma_original)

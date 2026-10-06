import sys
from pathlib import Path
import numpy as np

from entropy import calcular_entropia0_raw, calcular_entropia1_raw
from quantitzacio import quantitzacio
from desquantitzacio import desquantitzacio

def carrega_imatge(ruta_imagen):
    parts=Path(ruta_imagen).name.split(".")
    
    format, z, y, x = parts[-2].split("_")
    x = x.removesuffix("raw")
    sign = format[0]
    bits = int(format[3:])

    z = int(z)
    y = int(y)
    x = int(x)

    tipo = "u" if sign == "u" else ""
    dtype = np.dtype(f"{tipo}int{bits}")
    imagen_raw = np.fromfile(ruta_imagen, dtype=dtype)

    imagen_raw = imagen_raw.reshape((x, y, z))

    return imagen_raw, parts[0], parts[1], parts[2]

if __name__ == "__main__":

    ruta = sys.argv[1]
    entropia = int(sys.argv[2])
    tipus_quantitzacio = sys.argv[3]

    imatge, part0, part1, part2 = carrega_imatge(ruta)

    if entropia == 0:
        H0 = calcular_entropia0_raw(imatge)
        print("Entropia ordre 0: " + str(H0))
    elif entropia == 1:
        H1 = calcular_entropia1_raw(imatge)
        print("Entropia ordre 1: " + str(H1))

    if tipus_quantitzacio == "escalar":
        delta = int(sys.argv[4])
        q = quantitzacio(imatge, delta)
        H0_q = calcular_entropia0_raw(q)
        H1_q = calcular_entropia1_raw(q)
        print("Entropia ordre 0 quantitzat: " + str(H0_q))
        print("Entropia ordre 1 quantitzat: " + str(H1_q))
        ruta_quantitzada = "Quantitzada"+ str(delta) +part0+"."+part1+".raw"
        q.tofile(ruta_quantitzada)
        imatge_quantitzada = carrega_imatge(ruta_quantitzada)[0]
        desq = desquantitzacio(imatge_quantitzada, delta)
        H0_desq= calcular_entropia0_raw(desq)
        H1_desq= calcular_entropia1_raw(desq)
        print("Entropia ordre 0 desquantitzat: " + str(H0_desq))
        print("Entropia ordre 1 desquantitzat: " + str(H1_desq))
        ruta_desquantitzada = "Desquantitzada"+ str(delta) + "."+part0+"."+part1+".raw"
        desq.tofile(ruta_desquantitzada)
        
        

    elif tipus_quantitzacio == "blocs":
        # quantització per blocs
        pass

    elif tipus_quantitzacio == "regions":
        # quantització per regions
        pass

    
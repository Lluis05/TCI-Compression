import sys
from pathlib import Path
import numpy as np

from entropy import calcular_entropia0_raw, calcular_entropia1_raw
from quantitzacio import quantitzacio_escalar, quantitzacio_regions, quantitzacio_blocs
from desquantitzacio import desquantitzacio_escalar, desquantitzacio_regions, desquantitzacio_blocs
from haar import haar_2d, haar_invers2d
from calculs import *

max = 255

def carrega_imatge(ruta_imagen):
    parts = Path(ruta_imagen).name.split(".")
    
    format, z, y, x = parts[-2].split("_")
    x = x.removesuffix("raw")
    sign = format[0]
    endian = format[1:3]  
    bits = int(format[3:])

    z = int(z)
    y = int(y)
    x = int(x)

    tipo = "u" if sign == "u" else ""
    dtype = np.dtype(f"{tipo}int{bits}")
    
    # canvi
    if endian == "be":
        dtype = dtype.newbyteorder('>')
    elif endian == "le":
        dtype = dtype.newbyteorder('<')

    imagen_raw = np.fromfile(ruta_imagen, dtype=dtype)
    imagen_raw = imagen_raw.reshape((y, x, z))

    return imagen_raw, parts[0], parts[1], parts[2]

if __name__ == "__main__":

    ruta = sys.argv[1]
    entropia = int(sys.argv[2])
    nivells = int(sys.argv[4])

    imatge, part0, part1, part2 = carrega_imatge(ruta)
    formato_original = imatge.dtype

    #HAAR
    y = haar_2d(imatge, nivells)
    format_coef = "sle16_" + str(imatge.shape[2]) + "_" + str(imatge.shape[0]) + "_" + str(imatge.shape[1])
    y.astype('<i2').tofile("Haar." + part0 + "." + format_coef + ".raw")
    H0_y = calcular_entropia0_raw(y)
    print("Entropia ordre 0 haar: " + str(H0_y))

    yInvers = haar_invers2d(y, nivells)

    print("PAE sense quantització:", calcular_pae(imatge, yInvers))
    print("Reconstrucció exacta:", np.array_equal(imatge, yInvers))

    #QUANTITZACIÓ BLOCS
    delta = int(sys.argv[3])

    ll_files = imatge.shape[0] // (2 ** nivells)
    ll_columnes = imatge.shape[1] // (2 ** nivells)

    q = y.copy()
    q[:ll_files, :ll_columnes, :] = quantitzacio_escalar(y[:ll_files, :ll_columnes, :], delta)
    H0_q = calcular_entropia0_raw(q)
    print("Entropia ordre 0 quantitzat: " + str(H0_q))

    LL = y[:ll_files, :ll_columnes, :]
    LL_q = q[:ll_files, :ll_columnes, :]

    H0_LL = calcular_entropia0_raw(LL)
    print("Entropia ordre 0 LL: " + str(H0_LL))

    H0_LL_q = calcular_entropia0_raw(LL_q)
    print("Entropia ordre 0 LL quantitzada: " + str(H0_LL_q))

    # # Entropia dels detalls (tot menys la LL)
    # mascara = np.ones(y.shape, dtype=bool)
    # mascara[:ll_files, :ll_columnes, :] = False

    # H0_detalls = calcular_entropia0_raw(y[mascara])
    # print("Entropia ordre 0 detalls: " + str(H0_detalls))

    ruta_quantitzada = ("QuantitzadaHaarEscalar." + part0 + "." + format_coef + ".raw")
    q.astype('<i2').tofile(ruta_quantitzada)

    desq = q.copy()
    desq[:ll_files, :ll_columnes, :] = desquantitzacio_escalar(q[:ll_files, :ll_columnes, :], delta)
    yInvers = haar_invers2d(desq, nivells)

    ruta_desquantitzada = ("DesquantitzadaHaarEscalar." + part0 + "." + part1 + ".raw")

    yInvers = np.clip(yInvers, 0, np.iinfo(formato_original).max) # evita "wrap-around" es a dir que doni valors fora de 0 o 255 que donarien un valor contrari
    yInvers.astype(formato_original).tofile(ruta_desquantitzada)
    reconstruida = yInvers.astype(formato_original)
    
    pae = calcular_pae(imatge, reconstruida)
    print("PAE: " + str(pae))
    mse = calcular_mse(imatge, reconstruida)
    print("MSE: " + str(mse))
    psnr = calcular_psnr(imatge, reconstruida,max)
    print("PSNR: " + str(psnr))
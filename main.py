import sys
from pathlib import Path
import numpy as np

from entropy import calcular_entropia0_raw, calcular_entropia1_raw
from quantitzacio import quantitzacio_escalar, quantitzacio_regions, quantitzacio_blocs
from desquantitzacio import desquantitzacio_escalar, desquantitzacio_regions, desquantitzacio_blocs

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
    tipus_quantitzacio = sys.argv[3]

    imatge, part0, part1, part2 = carrega_imatge(ruta)

    # Deducir el formato exacto para NumPy (ej: 'ube16' -> '>u2', 'ule8' -> '<u1')
    # format_str = part1.split('_')[0] # Extrae solo la parte "ube16"
    # signo = 'u' if format_str[0] == 'u' else 'i'
    # endian = '>' if format_str[1:3] == 'be' else '<'
    # bytes_img = int(format_str[3:]) // 8 # Ahora divide 16 // 8 = 2 correctamente
    # formato_original = f"{endian}{signo}{bytes_img}"
    formato_original = imatge.dtype

    # Entropia de la imatge original
    if entropia == 0:
        H0 = calcular_entropia0_raw(imatge)
        print("Entropia ordre 0: " + str(H0))

    elif entropia == 1:
        H1 = calcular_entropia1_raw(imatge)
        print("Entropia ordre 1: " + str(H1))


    # Quantització escalar
    if tipus_quantitzacio == "escalar":

        delta = int(sys.argv[4])

        q = quantitzacio_escalar(imatge, delta)
        H0_q = calcular_entropia0_raw(q)
        print("Entropia ordre 0 quantitzat: " + str(H0_q))

        ruta_quantitzada = ("Quantitzada" + str(delta) + "." + part0 + "." + part1 + ".raw")
        q.astype(formato_original).tofile(ruta_quantitzada)

        # Carreguem de nou la imatge quantitzada
        imatge_quantitzada = carrega_imatge(ruta_quantitzada)[0]
        desq = desquantitzacio_escalar(imatge_quantitzada,delta)
        H0_desq = calcular_entropia0_raw(desq)
        print("Entropia ordre 0 desquantitzat: " + str(H0_desq))

        ruta_desquantitzada = ("Desquantitzada" + str(delta) + "." + part0 + "." + part1 + ".raw")
        desq.astype(formato_original).tofile(ruta_desquantitzada)


    # Quantització per regions
    elif tipus_quantitzacio == "regions":

        delta = int(sys.argv[4])

        q = quantitzacio_regions(imatge,delta)
        H0_q = calcular_entropia0_raw(q)
        print("Entropia ordre 0 quantitzat: " + str(H0_q))

        ruta_quantitzada = ("QuantitzadaRegions" + str(delta) + "." + part0 + "." + part1 + ".raw")
        q.astype(formato_original).tofile(ruta_quantitzada)

        # Carreguem de nou la imatge quantitzada
        imatge_quantitzada = carrega_imatge(ruta_quantitzada)[0]
        desq = desquantitzacio_regions(imatge_quantitzada,delta)
    
        H0_desq = calcular_entropia0_raw(desq)
        print("Entropia ordre 0 desquantitzat: " + str(H0_desq))

        ruta_desquantitzada = ("DesquantitzadaRegions" + str(delta) + "." + part0 + "." + part1 + ".raw")
        desq.astype(formato_original).tofile(ruta_desquantitzada)


    # Quantització per blocs
    elif tipus_quantitzacio == "blocs":

        mida_bloc = int(sys.argv[4])
        max_delta = int(sys.argv[5])

        q = quantitzacio_blocs(imatge,mida_bloc, max_delta)
        H0_q = calcular_entropia0_raw(q)
        print("Entropia ordre 0 quantitzat: " + str(H0_q))

        ruta_quantitzada = ("QuantitzadaBlocs" + str(mida_bloc) + "." + part0 + "." + part1 + ".raw")
        q.tofile(ruta_quantitzada)

        # Carreguem de nou la imatge quantitzada
        imatge_quantitzada = carrega_imatge(ruta_quantitzada)[0]
        desq = desquantitzacio_blocs(imatge_quantitzada,mida_bloc, max_delta)
        H0_desq = calcular_entropia0_raw(desq)
        print("Entropia ordre 0 desquantitzat: " + str(H0_desq))

        ruta_desquantitzada = ("DesquantitzadaBlocs" + str(mida_bloc) + "." + part0 + "." + part1 + ".raw")
        desq.tofile(ruta_desquantitzada)

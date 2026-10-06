import numpy as np

def calcular_entropia0_raw(imagen_raw):
    
    datos = imagen_raw.flatten()

    valores, conteos = np.unique(datos, return_counts=True)

    probabilidades = conteos/len(datos)

    entropia = -np.sum(probabilidades*np.log2(probabilidades))

    return entropia

def calcular_entropia1_raw(imagen_raw):
    
    datos = imagen_raw.flatten()

    list_anteriors = datos[:-1]
    list_actuals = datos[1:]

    list_parelles = np.column_stack((list_anteriors, list_actuals))

    probabilitats_condicionades = []

    for valor in np.unique(list_anteriors):
        parelles_valor = list_parelles[list_anteriors==valor]
        parelles, conteos = np.unique(parelles_valor[:, 1], return_counts=True)

        probabilitat_parella = conteos/len(parelles_valor)

        entropia = -np.sum(probabilitat_parella*np.log2(probabilitat_parella))

        prob_valor = len(parelles_valor) / len(list_parelles)

        probabilitats_condicionades.append(prob_valor*entropia)

    entropia_total = np.sum(probabilitats_condicionades)
    return entropia_total

if __name__ == "__main__":

    ruta_imagen = sys.argv[2] #"../imatges/n1_GRAY.ube8_1_2560_2048raw.raw"
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

    if sys.argv[1] == "1":
        resultado = calcular_entropia1_raw(imagen_raw)
    elif sys.argv[1] == "0":
        resultado = calcular_entropia0_raw(imagen_raw)

    print(f"Entropía de la imagen RAW: {resultado:.4f} bits por píxel")

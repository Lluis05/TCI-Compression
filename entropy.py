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

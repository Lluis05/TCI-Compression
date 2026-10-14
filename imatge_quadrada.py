import numpy as np

# Carreguem la imatge original
ruta = "../imatges/n1_GRAY.ube8_1_2560_2048.raw"

imatge = np.fromfile(ruta, dtype=np.uint8)
imatge = imatge.reshape((2048, 2560))

# Retallem 256 píxels de cada costat
imatge_quadrada = imatge[:, 256:2304]

# Guardem la imatge quadrada
imatge_quadrada.tofile("n1_GRAY_quadrada.ube8_1_2048_2048.raw")

print("Dimensions originals:", imatge.shape)
print("Dimensions quadrades:", imatge_quadrada.shape)
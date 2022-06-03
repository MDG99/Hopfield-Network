import cv2
import random
import numpy as np


def matrix_shape(matrix):
    return np.shape(matrix)[0], np.shape(matrix)[1]


def hamming_distance(x, y):
    return np.sum(x != y)


def preprocessing(path):
    # Realizamos un tratameinto previo para tener las imágenes en un rango discreto de [-1, +1]
    # En esta Función lo que hacemos es pasar una imagen que está en un rango de [0, 255] a [-1, +1],
    # Otras opciones que se pueden aplicar son: cambiarle el tamaño a la imagen o cambiar el threshold, aunque esto
    # último no tiene tanto sentido ya que las imágenes son binarias.

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    rows, cols = matrix_shape(img)

    img2 = np.zeros(shape=(rows, cols))

    for i in range(rows):
        for j in range(cols):
            if img[i, j] > 127:
                img2[i, j] = 1
            else:
                img2[i, j] = -1
    return img2


def learning_vectors(matrix):
    # Esta función pasa nuestra imagen de entrada a un vector de tamaño filas x columnas
    rows, cols = matrix_shape(matrix)
    V_size = rows * cols
    V = np.zeros(V_size)
    a = 0
    for i in range(rows):
        for j in range(cols):
            V[a] = matrix[i, j]
            a += 1
    return V


def weights(X):
    # Esta función crea la matriz de pesos W donde se realizará el aprendizaje
    N = np.shape(X)[0]
    W = np.zeros(shape=(N, N))

    for i in range(N):
        for j in range(N):
            if i == j:
                W[i, j] = 0
            else:
                W[i, j] = X[i]*X[j]
                W[j, i] = W[i, j]
    return W


def finding_patterns(W, Y, bias=0.5, epochs=100):
    # Esta función realiza la actualización del vector de características que se desea inferir

    m = len(Y)
    for e in range(epochs):
        i = random.randint(0, m-1)
        u = W[i][:]@Y - bias

        if u > 0:
            Y[i] = 1
        if u < 0:
            Y[i] = -1

    return Y


import numpy as np
import os
import cv2
import random
from utils import *


def hopfield(train_paths, test_paths):
    Vectors = []
    initial = True
    qty = 0

    #Fase de entrenamiento
    for path in train_paths:
        img = preprocessing(path)
        V = learning_vectors(img)
        Vectors.append(V)

        if initial:
            # Creamos la matriz de pesos
            W = weights(V)
            initial = False
        else:
            # Modificamos la matriz de pesos
            W = W + weights(V)

        qty+=1

    print("Aprendizaje terminado")
    print(f"Patrones aprendidos: {qty}")

    #Fase de prueba
    for path in test_paths:
        img = preprocessing(path)
        Y = learning_vectors(img)
        Y = finding_patterns(W, Y, bias=0.5, epochs=100)

        H_distance = []

        index = 0
        index_min = 0
        cost = np.inf

        for vector in Vectors:
            H = hamming_distance(vector, Y)
            if H < cost:
                cost = H
                index_min = index
            H_distance.append(H)
            index += 1

        print(f"{path} Corresponde a {train_paths[index_min]}")


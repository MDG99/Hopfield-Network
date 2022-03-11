from model import hopfield

train_path = ["train_imgs/Imagen50Pixeles19.bmp",
              "train_imgs/Imagen50Pixeles20.bmp",
              "train_imgs/Imagen50Pixeles21.bmp"]

test_path = ["test_imgs/DatosImagen19_15.bmp",
             "test_imgs/DatosImagen19_37.bmp",
             "test_imgs/DatosImagen19_40.bmp",
             "test_imgs/DatosImagen21_10.bmp",
             "test_imgs/DatosImagen21_12.bmp",
             "test_imgs/DatosImagen20_48.bmp",
             "test_imgs/DatosImagen20_4.bmp"]

hopfield(train_path, test_path)

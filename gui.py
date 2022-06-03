import tkinter as tk
import tkinter.font as TkFont

from model import *
from tkinter import *
from tkinter import ttk
from pathlib import Path
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog


class gui():

    def __init__(self):

        self.Vectors = []
        self.Patrones = []
        self.test_img = []
        self.Weights = 0
        self.col_sb = 0
        self.h = 100 #Alto de las imágenes patrón
        self.w = 100 #Ancho de las imágenes patrón

        self.h_test = 300  # Alto de las imágenes de prueba
        self.w_test = 300  # Ancho de las imágenes de prueba

        self.ventana = Tk()
        #self.ventana.geometry("600x600")
        #self.ventana.resizable(width=0, height=0) #Ventana no redimensionable
        self.ventana.title("Red Hopfield")

        #componentes del GUI
        self.fontformat_title =TkFont.Font(family="Arial", size=15, weight="bold")
        self.fontformat_sub = TkFont.Font(family="Arial", size=12)

        #Control para desplegar las imágenes de los patrones aprendidos
        self.lbfImgs = LabelFrame(self.ventana, text="Patrones Aprendidos", labelanchor='n')
        self.lbfImgs.grid(column=0, row=1, padx=5, pady=5, columnspan=3, rowspan=2)
        self.lbfImgs.grid_propagate(False)

        self.canvas = tk.Canvas(self.lbfImgs, height=self.h + 30, width=self.w*4)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self.lbfImgs, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.vsb.set)

        self.vsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)


        #Botones
        self.btnSelecImgs = Button(self.ventana, text="Seleccionar Imágenes", width=20, command=self.upload_imgs)
        self.btnSelecImgs.grid(column=3, row=1, padx=5, pady=5)

        self.btnResetImgs = Button(self.ventana, text="Limpiar", width=20, command=self.remove_imgs)
        self.btnResetImgs.grid(column=3, row=2, padx=5, pady=5)

        self.btnResetNN = Button(self.ventana, text="Reset NN", width=20, command=self.reset_NN)
        self.btnResetNN.grid(column=0, row=4, padx=5, pady=10)

        self.btnSelectImgs = Button(self.ventana, text="Seleccionar Imagen", width=20, command=self.select_test_img)
        self.btnSelectImgs.grid(column=0, row=5, padx=5, pady=10)

        self.btnTrain = Button(self.ventana, text="Entrenar", width=20, command=self.train_NN)
        self.btnTrain.grid(column=0, row=7, padx=5, pady=10)

        self.btnRun= Button(self.ventana, text="Correr", width=20, command=self.run_NN)
        self.btnRun.grid(column=0, row=8, padx=5, pady=10)

        #Elementos estéticos (Espaciados)
        spacer1 = tk.Label(self.ventana, text="")
        spacer1.grid(column=0, row=6, pady=70)
        #Texto
        #self.lbltitle0 = Label(self.ventana, text="Patrones Aprendidos", font=self.fontformat_title)
        #self.lbltitle0.grid(column=0, row=0, padx=5, pady=5, columnspan=4)


        #Textboxes
        #self.txt_angle = Entry(self.ventana, width=10)
        #self.txt_angle.grid(column=1, row=6)

        #Combobox
        #self.cmbPorts = ttk.Combobox(self.ventana, width=10, values=self.port_names)
        #self.cmbPorts.grid(column=1, row=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reset_NN(self):
        self.Weights = 0
        self.Vectors = []

    def train_NN(self):
        self.Weights, self.Vectors, qty = hopfield_train(self.Patrones)
        messagebox.showinfo(message=f"Se han aprendido {qty} patrones", title="Aprendizaje Finalizado")

    def run_NN(self):
        index = hopfield_test(self.test_img, self.Vectors, self.Weights)
        #Es necesario sumarle 1 al valor de index ya que empieza en 0
        messagebox.showinfo(message=f"La imagen corresponde al patrón: {index+1} ", title="Patrón Reconocido")

    def upload_imgs(self):
        f_types = [('BMP Files', '*.bmp'), ('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
        filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
        for f in filename:
            self.Patrones.append(f)
            name = Path(f).stem
            img = Image.open(f)  #Leemos la imagen
            img = img.resize((self.h, self.w))  #Redimensionamos a un tamaño de 100x100
            img = ImageTk.PhotoImage(img)
            e0 = Label(self.frame, text=f"{name}")
            e0.grid(row=0, column=self.col_sb, sticky="wens")
            e1 = Label(self.frame)
            e1.grid(row=1, column=self.col_sb, sticky="wens")
            e1.image = img
            e1['image'] = img  # garbage collection
            self.col_sb = self.col_sb + 1

    def remove_imgs(self):
        self.Patrones = []
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def select_test_img(self):
        f_types = [('BMP Files', '*.bmp'), ('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
        filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
        for f in filename:
            self.test_img.append(f)
            name = Path(f).stem
            img = Image.open(f)  # Leemos la imagen
            img = img.resize((self.h_test, self.w_test))  # Redimensionamos a un tamaño de 300x300
            img = ImageTk.PhotoImage(img)

            g0 = Label(self.ventana, text=f"{name}")
            g0.grid(row=4, column=1, columnspan=3)
            g1 = Label(self.ventana)
            g1.grid(row=5, column=1, columnspan=3, rowspan=4)
            g1.image = img
            g1['image'] = img  # garbage collection


my_app = gui()
my_app.ventana.mainloop()

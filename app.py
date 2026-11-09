import tkinter as tk
from tkinter import messagebox


def mensaje_boton_1():
    messagebox.showinfo("Botón 1", "¡Hola! Este es el mensaje del primer botón.")


def mensaje_boton_2():
    messagebox.showinfo("Botón 2", "¡Genial! Este es el mensaje del segundo botón.")


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Primera App — DeepSeek + GitHub")
ventana.geometry("340x220")
ventana.resizable(False, False)

# Título decorativo dentro de la ventana
titulo = tk.Label(
    ventana,
    text="Prueba de dos botones",
    font=("Segoe UI", 12, "bold")
)
titulo.pack(pady=10)

# Botón 1
boton1 = tk.Button(
    ventana,
    text="Presióname (Botón 1)",
    width=28,
    command=mensaje_boton_1
)
boton1.pack(pady=10)

# Botón 2
boton2 = tk.Button(
    ventana,
    text="Presióname (Botón 2)",
    width=28,
    command=mensaje_boton_2
)
boton2.pack(pady=10)

# Bucle principal
ventana.mainloop()
import tkinter as tk
from tkinter import messagebox
import requests

# Dirección IP del ESP32
ESP32_IP = "http://192.168.1.41"

# Función para enviar los datos de los sliders al servidor
def mover_servos():
    try:
        # Obtener los valores de los sliders
        pinza = slider_pinza.get()
        muneca = slider_muneca.get()
        antebrazo = slider_antebrazo.get()
        codo = slider_codo.get()
        base = slider_base.get()

        # Valor de pin invisible que no se considera
        invisible = 90
        
        # Formatear la URL con los valores de los servos en formato CSV
        url = f"{ESP32_IP}/?{invisible},{pinza},{muneca},{antebrazo},{codo},{base}"
        
        # Enviar la solicitud HTTP al servidor ESP32
        response = requests.get(url)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            messagebox.showinfo("Éxito", "Movimientos completados!")
        else:
            messagebox.showerror("Error", "No se pudo mover los servos.")
    except Exception as e:
        messagebox.showerror("Error", f"Error de conexión: {e}")

# Función para guardar la secuencia de movimientos
def guardar_secuencia():
    try:
        # Obtener los valores de los sliders
        secuencia = [
            90,  # Valor del servo invisible
            slider_pinza.get(),
            slider_muneca.get(),
            slider_antebrazo.get(),
            slider_codo.get(),
            slider_base.get()
        ]
        
        # Guardar la secuencia en un archivo
        with open("secuencia.txt", "a") as file:
            file.write(",".join(map(str, secuencia)) + "\n")
        
        messagebox.showinfo("Éxito", "Secuencia guardada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar la secuencia: {e}")

# Función para reproducir las secuencias guardadas en el archivo
def reproducir_secuencia():
    try:
        # Leer las secuencias guardadas desde el archivo
        with open("secuencia.txt", "r") as file:
            lineas = file.readlines()
        
        # Reproducir cada secuencia
        for linea in lineas:
            # Dividir los valores de la secuencia
            secuencia = list(map(int, linea.strip().split(",")))
            
            # Formatear la URL con los valores de la secuencia
            url = f"{ESP32_IP}/?{','.join(map(str, secuencia))}"
            
            # Enviar la solicitud HTTP para mover los servos
            response = requests.get(url)
            
            if response.status_code != 200:
                messagebox.showerror("Error", "Error al reproducir la secuencia.")
                break
        
        messagebox.showinfo("Éxito", "Secuencia reproducida correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al reproducir la secuencia: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Control de Servos")

# Crear sliders para controlar cada servo
slider_pinza = tk.Scale(ventana, from_=0, to=180, orient="horizontal", label="Pinza", length=400)
slider_pinza.set(90)
slider_pinza.pack()

slider_muneca = tk.Scale(ventana, from_=0, to=180, orient="horizontal", label="Muñeca", length=400)
slider_muneca.set(90)
slider_muneca.pack()

slider_antebrazo = tk.Scale(ventana, from_=0, to=180, orient="horizontal", label="Antebrazo", length=400)
slider_antebrazo.set(90)
slider_antebrazo.pack()

slider_codo = tk.Scale(ventana, from_=0, to=180, orient="horizontal", label="Codo", length=400)
slider_codo.set(90)
slider_codo.pack()

slider_base = tk.Scale(ventana, from_=0, to=180, orient="horizontal", label="Base", length=400)
slider_base.set(90)
slider_base.pack()

# Botones para guardar, mover y reproducir secuencias
btn_mover = tk.Button(ventana, text="Mover Servos", command=mover_servos)
btn_mover.pack(pady=10)

btn_guardar = tk.Button(ventana, text="Guardar Secuencia", command=guardar_secuencia)
btn_guardar.pack(pady=10)

btn_reproducir = tk.Button(ventana, text="Reproducir Secuencia", command=reproducir_secuencia)
btn_reproducir.pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()
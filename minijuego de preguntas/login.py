import tkinter as tk
import sqlite3

# Conectar o crear la base de datos
def conectar_bd():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Guardar nombre si es válido
def guardar_nombre():
    nombre = entry_nombre.get().strip()

    if not nombre:
        etiqueta_error.config(text="El nombre esta vacío...")
        return
    else:
        etiqueta_error.config(text="")

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

    etiqueta_error.config(text=f"¡Bienvenido, {nombre}!", fg="green")
    entry_nombre.delete(0, tk.END)

# Crear ventana principal
def crear_ventana():
    ventana = tk.Tk()
    ventana.title("Ingreso de Usuario")
    ventana.geometry("350x200")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Ingresa tu nombre:", font=("Arial", 12)).pack(pady=10)

    global entry_nombre
    entry_nombre = tk.Entry(ventana, font=("Arial", 12), width=30)
    entry_nombre.pack()

    global etiqueta_error
    etiqueta_error = tk.Label(ventana, text="", fg="red", font=("Arial", 10))
    etiqueta_error.pack(pady=5)

    tk.Button(ventana, text="Comenzar", font=("Arial", 12), fg="white", command=guardar_nombre).pack(pady=10)

    ventana.mainloop()

# Ejecutar programa
conectar_bd()
crear_ventana()

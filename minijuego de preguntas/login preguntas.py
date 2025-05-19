import tkinter as tk
import sqlite3

# Base de datos
def conectar_bd():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            pregunta TEXT,
            respuesta TEXT,
            correcta INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()

# Preguntas
preguntas = [
    {"pregunta": "¿A qué tipo pertenece el monstruo 'Blue-Eyes White Dragon'?", "opciones": ["Dragón", "Guerrero", "Bestia"], "correcta": "Dragón"},
    {"pregunta": "¿Cuál es el atributo del monstruo 'Dark Magician'?", "opciones": ["Luz", "Oscuridad", "Fuego"], "correcta": "Oscuridad"},
    {"pregunta": "¿Qué tipo de carta es 'Monster Reborn'?", "opciones": ["Trampa", "Hechizo", "Monstruo"], "correcta": "Hechizo"},
    {"pregunta": "¿Cuál es el nivel del monstruo 'Kuriboh'?", "opciones": ["Nivel 1", "Nivel 4", "Nivel 3"], "correcta": "Nivel 1"},
    {"pregunta": "¿Qué atributo tiene el monstruo 'Red-Eyes Black Dragon'?", "opciones": ["Oscuridad", "Tierra", "Luz"], "correcta": "Oscuridad"},
    {"pregunta": "¿Cuál es la categoría del monstruo 'Exodia the Forbidden One'?", "opciones": ["Bestia", "Guerrero", "Legendario"], "correcta": "Guerrero"},
    {"pregunta": "¿Qué tipo de carta es 'Mirror Force'?", "opciones": ["Trampa", "Hechizo", "Monstruo"], "correcta": "Trampa"},
    {"pregunta": "¿Cuál es el atributo del monstruo 'Elemental HERO Neos'?", "opciones": ["Luz", "Oscuridad", "Fuego"], "correcta": "Luz"},
    {"pregunta": "¿Cuál es la rareza típica de la carta 'Dark Magician Girl' en su versión original?", "opciones": ["Ultra Rara", "Común", "Secreta"], "correcta": "Ultra Rara"},
    {"pregunta": "¿Qué tipo de monstruo es 'Summoned Skull'?", "opciones": ["Demonio", "Dragón", "Guerrero"], "correcta": "Demonio"}
]

# Variables globales
usuario_id = None
indice_pregunta = 0
puntuacion = 0

# Función guardar usuario
def guardar_nombre():
    global usuario_id, entry_nombre
    nombre = entry_nombre.get().strip()

    if not nombre:
        etiqueta_error.config(text="El nombre esta vacío...")
        return
    else:
        etiqueta_error.config(text="")

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
    usuario_id = cursor.lastrowid
    conn.commit()
    conn.close()

    frame_inicio.destroy()
    mostrar_pregunta()

# Función mostrar preguntas 
def mostrar_pregunta():
    global frame_pregunta, pregunta_label, botones_opciones, etiqueta_feedback

    frame_pregunta = tk.Frame(ventana)
    frame_pregunta.pack(pady=20)

    pregunta_actual = preguntas[indice_pregunta]
    pregunta_label = tk.Label(frame_pregunta, text=pregunta_actual["pregunta"], font=("Arial", 12))
    pregunta_label.pack(pady=10)

    botones_opciones = []
    for opcion in pregunta_actual["opciones"]:
        b = tk.Button(frame_pregunta, text=opcion, width=20, command=lambda o=opcion: verificar_respuesta(o))
        b.pack(pady=3)
        botones_opciones.append(b)

#  Verificación y avance  #
def verificar_respuesta(respuesta):
    global indice_pregunta, puntuacion

    pregunta_actual = preguntas[indice_pregunta]
    correcta = 1 if respuesta == pregunta_actual["correcta"] else 0

    if correcta:
        puntuacion += 1

    # Guardar resultado en la base de datos
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resultados (usuario_id, pregunta, respuesta, correcta)
        VALUES (?, ?, ?, ?)
    ''', (usuario_id, pregunta_actual["pregunta"], respuesta, correcta))
    conn.commit()
    conn.close()

    # Avanzar
    frame_pregunta.destroy()
    indice_pregunta += 1

    if indice_pregunta < len(preguntas):
        mostrar_pregunta()
    else:
        mostrar_resultado()

#  Resultado final  
def mostrar_resultado():
    frame_resultado = tk.Frame(ventana)
    frame_resultado.pack(pady=20)

    tk.Label(frame_resultado, text=f"Puntuación final: {puntuacion}/10", font=("Arial", 14, "bold"), fg="green").pack(pady=10)
    tk.Button(frame_resultado, text="Salir", command=ventana.destroy).pack(pady=10)

#  Ventana principal  
def crear_ventana():
    global ventana, entry_nombre, etiqueta_error, frame_inicio

    ventana = tk.Tk()
    ventana.title("Test Pokémon")
    ventana.geometry("450x300")
    ventana.resizable(False, False)

    frame_inicio = tk.Frame(ventana)
    frame_inicio.pack(pady=40)

    tk.Label(frame_inicio, text="Ingresa tu nombre:", font=("Arial", 12)).pack(pady=5)

    entry_nombre = tk.Entry(frame_inicio, font=("Arial", 12), width=30)
    entry_nombre.pack()

    etiqueta_error = tk.Label(frame_inicio, text="", fg="red", font=("Arial", 10))
    etiqueta_error.pack(pady=5)

    tk.Button(frame_inicio, text="Comenzar", font=("Arial", 12), command=guardar_nombre).pack(pady=10)

    ventana.mainloop()

# Ejecutar 
conectar_bd()
crear_ventana()

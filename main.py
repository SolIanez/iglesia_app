import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Crear tablas en SQLite
def crear_tablas():
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Miembros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        direccion TEXT,
        telefono TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha TEXT NOT NULL,
        descripcion TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Donaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        miembro_id INTEGER,
        cantidad REAL NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY(miembro_id) REFERENCES Miembros(id)
    )
    ''')

    conexion.commit()
    conexion.close()

crear_tablas()

# Funciones CRUD para Miembros
def agregar_miembro(nombre, direccion, telefono):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Miembros (nombre, direccion, telefono) VALUES (?, ?, ?)', (nombre, direccion, telefono))
    conexion.commit()
    conexion.close()

def obtener_miembros():
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Miembros')
    miembros = cursor.fetchall()
    conexion.close()
    return miembros

def actualizar_miembro(id, nombre, direccion, telefono):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('UPDATE Miembros SET nombre = ?, direccion = ?, telefono = ? WHERE id = ?', (nombre, direccion, telefono, id))
    conexion.commit()
    conexion.close()

def eliminar_miembro(id):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Miembros WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()

# Manejo de Usuarios y Login
def registrar_usuario(nombre, email, password):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO Usuarios (nombre, email, password) VALUES (?, ?, ?)', (nombre, email, hashed_password))
    conexion.commit()
    conexion.close()

def autenticar_usuario(email, password):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM Usuarios WHERE email = ? AND password = ?', (email, hashed_password))
    usuario = cursor.fetchone()
    conexion.close()
    return usuario

# Interfaz Gráfica 
def registrar():
    nombre = entry_nombre.get()
    email = entry_email.get()
    password = entry_password.get()
    registrar_usuario(nombre, email, password)
    messagebox.showinfo("Registro", "Usuario registrado exitosamente")

def login():
    email = entry_email.get()
    password = entry_password.get()
    usuario = autenticar_usuario(email, password)
    if usuario:
        messagebox.showinfo("Login", "Login exitoso")
    else:
        messagebox.showerror("Login", "Email o contraseña incorrectos")

root = tk.Tk()
root.title("Herramientas para lìderes")

tk.Label(root, text="Nombre").grid(row=0)
tk.Label(root, text="Email").grid(row=1)
tk.Label(root, text="Password").grid(row=2)

entry_nombre = tk.Entry(root)
entry_email = tk.Entry(root)
entry_password = tk.Entry(root, show="*")

entry_nombre.grid(row=0, column=1)
entry_email.grid(row=1, column=1)
entry_password.grid(row=2, column=1)

tk.Button(root, text="Registrar", command=registrar).grid(row=3, column=0)
tk.Button(root, text="Login", command=login).grid(row=3, column=1)

root.mainloop()


# Segunda interfaz gráfica
def agregar():
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    agregar_miembro(nombre, direccion, telefono)
    messagebox.showinfo("Información", "Miembro agregado exitosamente")
    mostrar_miembros()

def mostrar_miembros():
    for row in tree.get_children():
        tree.delete(row)
    miembros = obtener_miembros()
    for miembro in miembros:
        tree.insert("", tk.END, values=miembro)

def actualizar():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    actualizar_miembro(id, nombre, direccion, telefono)
    messagebox.showinfo("Información", "Miembro actualizado exitosamente")
    mostrar_miembros()

def eliminar():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    eliminar_miembro(id)
    messagebox.showinfo("Información", "Miembro eliminado exitosamente")
    mostrar_miembros()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Miembros")

# Entradas de texto
tk.Label(root, text="Nombre").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Dirección").grid(row=1, column=0)
entry_direccion = tk.Entry(root)
entry_direccion.grid(row=1, column=1)

tk.Label(root, text="Teléfono").grid(row=2, column=0)
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=2, column=1)

# Botones
tk.Button(root, text="Agregar", command=agregar).grid(row=3, column=0)
tk.Button(root, text="Actualizar", command=actualizar).grid(row=3, column=1)
tk.Button(root, text="Eliminar", command=eliminar).grid(row=3, column=2)

# Tabla para mostrar los miembros
tree = tk.ttk.Treeview(root, columns=("ID", "Nombre", "Dirección", "Teléfono"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Dirección", text="Dirección")
tree.heading("Teléfono", text="Teléfono")
tree.grid(row=4, column=0, columnspan=3)

mostrar_miembros()

root.mainloop()


# Funciones CRUD
def agregar_miembro(nombre, direccion, telefono):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('INSERT INTO Miembros (nombre, direccion, telefono) VALUES (?, ?, ?)', (nombre, direccion, telefono))
    conexion.commit()
    conexion.close()

def obtener_miembros():
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Miembros')
    miembros = cursor.fetchall()
    conexion.close()
    return miembros

def actualizar_miembro(id, nombre, direccion, telefono):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('UPDATE Miembros SET nombre = ?, direccion = ?, telefono = ? WHERE id = ?', (nombre, direccion, telefono, id))
    conexion.commit()
    conexion.close()

def eliminar_miembro(id):
    conexion = sqlite3.connect('iglesia.db')
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM Miembros WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()

# Funciones de la interfaz gráfica
def agregar():
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    agregar_miembro(nombre, direccion, telefono)
    messagebox.showinfo("Información", "Miembro agregado exitosamente")
    mostrar_miembros()

def mostrar_miembros():
    for row in tree.get_children():
        tree.delete(row)
    miembros = obtener_miembros()
    for miembro in miembros:
        tree.insert("", tk.END, values=miembro)

def actualizar():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    actualizar_miembro(id, nombre, direccion, telefono)
    messagebox.showinfo("Información", "Miembro actualizado exitosamente")
    mostrar_miembros()

def eliminar():
    selected_item = tree.selection()[0]
    id = tree.item(selected_item)['values'][0]
    eliminar_miembro(id)
    messagebox.showinfo("Información", "Miembro eliminado exitosamente")
    mostrar_miembros()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Gestión de Miembros")

# Entradas de texto
tk.Label(root, text="Nombre").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Dirección").grid(row=1, column=0)
entry_direccion = tk.Entry(root)
entry_direccion.grid(row=1, column=1)

tk.Label(root, text="Teléfono").grid(row=2, column=0)
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=2, column=1)

# Botones
tk.Button(root, text="Agregar", command=agregar).grid(row=3, column=0)
tk.Button(root, text="Actualizar", command=actualizar).grid(row=3, column=1)
tk.Button(root, text="Eliminar", command=eliminar).grid(row=3, column=2)

# Tabla para mostrar los miembros
tree = ttk.Treeview(root, columns=("ID", "Nombre", "Dirección", "Teléfono"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Dirección", text="Dirección")
tree.heading("Teléfono", text="Teléfono")
tree.grid(row=4, column=0, columnspan=3)

mostrar_miembros()

root.mainloop()
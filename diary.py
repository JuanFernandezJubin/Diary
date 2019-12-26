import datetime
import sys
import os
#importamos peewee
from peewee import *
#Importamos un diccionario ordenado,eso es OrdererDict de collections
from collections import OrderedDict
#Hacemos la conexion con nuestra base de datos
db = SqliteDatabase("diary.db")

#entrada en nuestro diario
class Entry(Model):
    #Fecha
    #Contenido
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)

    #Class Meta
    class Meta:
        database = db

def add_entry():
    """Aderir una entrada"""
    print("Intruduzca su registro y cuando termine presione Ctrl + Z + Enter")
    #En vez de usar el clasico input sys.stdin.read() nos permite registrar
    #cuando el usuario ingrese Ctrl + D
    data = sys.stdin.read().strip()
    if data :
        if input("Guardar entrada? [Yn]").lower() != "n":
            Entry.create(content = data)
            print("Guardado exitosamente")

def view_entry(search_query = None):
    """Despliega tus registros"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    #Este if sirve para la accion de buscar texto en nuestras entradas
    if search_query:
        entries =  entries.where(Entry.content.contains(search_query))
    for entry in entries:
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M %p")
        clear()
        print("-"*len(timestamp))
        print(timestamp)
        print(entry.content)
        print("\n\n" + "-"*len(timestamp))
        print("n | Siguiente entrada")
        print("d | Borrar entrada")
        print("q | Salir del menu")
        next_action = input("Accion a realizar: [Nq]").lower().strip()
        if next_action == "q":
            break
        elif next_action == "d":
            delete_entry(entry)

def search_entries():
    """Busca una entrada con cierto Texto"""
    option = input("Buscar por Texto o buscar por Fecha [Tf]").lower()
    view_entry(input("Texto a buscar"))

def delete_entry(entry):
    """Borra un Registro"""
    response = input("Esta Seguro?  [Yn]").lower()
    if response == "y":
        entry.delete_instance()
        print("Entrada Borrada")

#definir nuestro menu como un diccionario ordenado
menu = OrderedDict([
    ("a", add_entry),
    ("v", view_entry),
    ("s", search_entries),
])

def menu_loop():
    """Muestra el menu con las opciones"""
    choice = None
    while choice != "q":
        clear()
        print("presiona 'q' para salir")
        #menu.items() es el metodo que nos regresa estas llaves y valores
        for key , value in menu.items():
            #llamammos a la documentacion de nuestros metodos con __doc__
            print("{} || {}".format(key,value.__doc__))
        #el .lower lo vuelve todo en minusculas y el .strip borra los espacios
        #adicionales
        choice = input("Eleccion: ").lower().strip()
        #Corroborar si la opcion esta dentro de nuestro menu S
        if choice in menu:
            #buscamos dentro de nuestro menu la eleccion
            clear()
            menu[choice]()

def initialize():
    db.connect()
    db.create_tables([Entry], safe = True)

def clear():
    os.system("cls" #vamos a llamar a un comando del sistema operativo
    #este caso es cls
    #nt comunmente significa windows y clear es en Mac o Linux
    if os.name == "nt" else "clear")

if __name__ == '__main__':
    initialize()
    menu_loop ()

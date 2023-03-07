from customtkinter import *
from tkinter import messagebox, ttk
from tkinter.font import BOLD, Font
import math
import requests
import random



#Ventana
ventana = CTk()
ventana.config(width = 500, height = 150)
ventana.title("By Giuseppe")
#Etiquetas: et
ettitulo = CTkLabel(ventana, text = "------------- Cuentas Claras -------------")
ettitulo.grid(row = 0, columnspan = 2) 

set_default_color_theme("dark-blue")

def getCatFact():
    numero = random.randint(30, 100)
    print(numero)
    r = requests.get(f'https://catfact.ninja/fact?max_length={numero}')
    r = r.json()
    return f"{r['fact']} 🐾"

def calcular():

    sueldo1 = reemplazarPuntoyComa(cajauno)
    sueldo2 = reemplazarPuntoyComa(cajados)
    totalapagar = reemplazarPuntoyComa(cajatres)
    try:
        sueldo1 = float(sueldo1)
        sueldo2 = float(sueldo2)
        totalapagar = float(totalapagar)
    except ValueError:
        messagebox.showerror(message = "Escribí solamente números, reina", title = "Error")

    sumaSueldos = sueldo1 + sueldo2

    #calculoPrimerPorcentaje = (sueldo1 * 100) / sumaSueldos
    primerPortentaje = (sueldo1 * 100) / sumaSueldos

    #calculoSegundoPorcentaje = (sueldo2 * 100) / sumaSueldos
    segundoPorcentaje = (sueldo2 * 100) / sumaSueldos

    # Calculo a pagar
    primerPago =round(((totalapagar * primerPortentaje) / 100),2)
    segundoPago =round(((totalapagar * segundoPorcentaje) / 100),2)

    global etcuatro
    etcuatro = CTkLabel(ventana, text = "Sueldo 1:")
    etcuatro.grid(row = 4, column = 0, pady=10)

    global etcinco
    etcinco = CTkLabel(ventana, text = "Sueldo 2:")
    etcinco.grid(row = 5, column = 0, pady=10)

    global etseis
    etseis = CTkLabel(ventana, text = f"${str(primerPago).replace('.',',')}", font = ("Arial", 15), text_color= "red")
    etseis.grid(row = 4, column = 1)

    global etsiete
    etsiete = CTkLabel(ventana, text = f"${str(segundoPago).replace('.',',')}", font = ("Arial", 15), text_color= "green")
    etsiete.grid(row = 5, column = 1)

    if sumaSueldos < totalapagar:
        messagebox.showerror(message = "El total a pagar no puede ser mayor a ambos sueldos", title = "Error")
        limpiar()


def reemplazarPuntoyComa(arg0):
    result = arg0.get()
    result = result.replace('.', '')
    result = result.replace(',', '.')

    return result
    
def limpiar():

    etseis.destroy()
    etsiete.destroy()
    etcinco.destroy()
    etcuatro.destroy()
    
    cajauno.delete(0, END)
    cajados.delete(0, END)
    cajatres.delete(0, END)

def change_appearance_mode_event(new_appearance_mode):
    set_appearance_mode(new_appearance_mode)
    if new_appearance_mode == "Light":
        etuno.configure(text_color = "white")
        etdos.configure(text_color = "white")
        ettres.configure(text_color = "white")
        cajauno.configure(text_color= "black")
        cajados.configure(text_color= "black")
        cajatres.configure(text_color= "black")

    

#####################################################################

#Cajas
cajauno = CTkEntry(ventana, width= 300, height= 40, text_color= "silver", font=("Arial", 15)) #Sueldo 1
cajauno.grid(row = 1, column = 1, padx=10)

cajados = CTkEntry(ventana, width= 300, height= 40, text_color= "silver", font=("Arial", 15)) #Sueldo 2
cajados.grid(row = 2, column = 1, pady=10)

cajatres = CTkEntry(ventana, width= 300, height= 40, text_color= "silver", font=("Arial", 15)) #Total a pagar
cajatres.grid(row = 3, column = 1, pady=10)


#Label
etuno = CTkLabel(ventana, text = "Sueldo 1", fg_color="red",corner_radius=8)
etuno.grid(row = 1, column = 0, pady=10)

etdos = CTkLabel(ventana, text = "Sueldo 2",  fg_color="green", corner_radius=8)
etdos.grid(row = 2, column = 0, pady=10)

ettres = CTkLabel(ventana, text = "A pagar", fg_color="blue", corner_radius=8)
ettres.grid(row = 3, column = 0, pady=10)


#####################################################################
#Label
my_labelframe = CTkFrame(ventana, corner_radius= 10)
my_labelframe.grid(row = 6, columnspan = 2)

#Botones
bcalcular = CTkButton(my_labelframe, text = "Calcular", command=calcular)
bcalcular.grid(row =0, column= 0, pady=10, padx = 10)

blimpiar = CTkButton(my_labelframe, text = "Limpiar", command=limpiar)
blimpiar.grid(row = 0, column=1, pady=10, padx =10)

appearance_mode_optionemenu = CTkOptionMenu(my_labelframe, values=["Dark", "Light"],command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=0, column=3, padx =10)

catFrame = CTkFrame(ventana, corner_radius= 50)
catFrame.grid(row = 7, columnspan = 2)

catLabel = CTkLabel(catFrame, text= getCatFact())
catLabel.grid(row=0, columnspan = 2, padx = 5)


ventana.mainloop()

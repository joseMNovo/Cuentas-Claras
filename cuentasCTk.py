# pyinstaller --onefile --windowed --noconsole --icon=icon.ico cuentasCTk.py
from customtkinter import CTk, set_default_color_theme, set_appearance_mode, CTkLabel, CTkEntry, CTkFrame, CTkButton, CTkOptionMenu
from tkinter import messagebox, ttk
from tkinter.font import BOLD, Font
import math
import requests
import random
import os

class CuentasClaras:
    def __init__(self):
        self.ventana = CTk()
        self.ventana.config(width=500, height=150)
        self.ventana.title("By Giuseppe")
        
        self.setup_ui()
        self.setup_bindings()
        set_default_color_theme("dark-blue")
        
    def setup_ui(self):
        # Título
        self.ettitulo = CTkLabel(self.ventana, text="------------- Cuentas Claras -------------")
        self.ettitulo.grid(row=0, columnspan=2)
        
        # Entradas
        vcmd = (self.ventana.register(self.solo_numeros), '%S')
        self.cajauno = self.crear_entrada(1, "Sueldo 1", "red", vcmd)
        self.cajados = self.crear_entrada(2, "Sueldo 2", "green", vcmd) 
        self.cajatres = self.crear_entrada(3, "A pagar", "blue", vcmd)
        
        # Frame de botones
        self.crear_frame_botones()
        
        # Frame de datos de gato
        self.crear_frame_cat()
        
    def crear_entrada(self, row, label_text, color, vcmd):
        # Label
        label = CTkLabel(self.ventana, text=label_text, fg_color=color, corner_radius=8)
        label.grid(row=row, column=0, pady=10)
        
        # Entry
        entry = CTkEntry(self.ventana, width=300, height=40, text_color="silver", 
                        font=("Arial", 15), validate='key', validatecommand=vcmd)
        entry.grid(row=row, column=1, pady=10, padx=10)
        
        return entry
        
    def crear_frame_botones(self):
        frame = CTkFrame(self.ventana, corner_radius=10)
        frame.grid(row=6, columnspan=2)
        
        bcalcular = CTkButton(frame, text="Calcular", command=self.calcular)
        bcalcular.grid(row=0, column=0, pady=10, padx=10)
        
        blimpiar = CTkButton(frame, text="Limpiar", command=self.limpiar)
        blimpiar.grid(row=0, column=1, pady=10, padx=10)
        
        appearance_menu = CTkOptionMenu(frame, values=["Dark", "Light"], 
                                      command=self.change_appearance_mode_event)
        appearance_menu.grid(row=0, column=3, padx=10)
        
    def crear_frame_cat(self):
        self.cat_frame = CTkFrame(self.ventana, corner_radius=50)
        self.cat_frame.grid(row=7, columnspan=2)
        
        self.cat_label = CTkLabel(self.cat_frame, text=self.get_cat_fact())
        self.cat_label.grid(row=0, columnspan=2, padx=5)
        
    def setup_bindings(self):
        self.ventana.bind('<Return>', self.calcular)
        self.ventana.bind('<Escape>', lambda e: self.ventana.focus_set())
        
    def get_cat_fact(self):
        numero = random.randint(30, 100)
        os.system('cls' if os.name == 'nt' else 'clear')
        r = requests.get(f'https://catfact.ninja/fact?max_length={numero}')
        return f"{r.json()['fact']} 🐾"
        
    def calcular(self, event=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            sueldo1 = float(self.reemplazar_punto_y_coma(self.cajauno))
            sueldo2 = float(self.reemplazar_punto_y_coma(self.cajados))
            total_a_pagar = float(self.reemplazar_punto_y_coma(self.cajatres))
        except ValueError:
            messagebox.showerror(message="Por favor, ingrese únicamente valores numéricos", 
                               title="Error de Entrada")
            return
            
        suma_sueldos = sueldo1 + sueldo2
        if suma_sueldos < total_a_pagar:
            messagebox.showerror(message="El monto total a pagar no puede superar la suma de los sueldos", 
                               title="Error")
            self.limpiar()
            return
            
        primer_porcentaje = (sueldo1 * 100) / suma_sueldos
        segundo_porcentaje = (sueldo2 * 100) / suma_sueldos
        
        primer_pago = round((total_a_pagar * primer_porcentaje) / 100, 2)
        segundo_pago = round((total_a_pagar * segundo_porcentaje) / 100, 2)
        
        self.mostrar_resultados(primer_pago, segundo_pago)
        
    def mostrar_resultados(self, primer_pago, segundo_pago):
        # Limpiar etiquetas de resultados anteriores    
        self.limpiar_etiquetas()

        self.etcuatro = CTkLabel(self.ventana, text="Sueldo 1:")
        self.etcuatro.grid(row=4, column=0, pady=10)
        
        self.etcinco = CTkLabel(self.ventana, text="Sueldo 2:")
        self.etcinco.grid(row=5, column=0, pady=10)
        
        self.etseis = CTkLabel(self.ventana, text=f"${str(primer_pago).replace('.',',')}", 
                              font=("Arial", 15), text_color="red")
        self.etseis.grid(row=4, column=1)
        
        self.etsiete = CTkLabel(self.ventana, text=f"${str(segundo_pago).replace('.',',')}", 
                               font=("Arial", 15), text_color="green")
        self.etsiete.grid(row=5, column=1)
        
    def reemplazar_punto_y_coma(self, entrada):
        result = entrada.get()
        result = result.replace(',', '.')
        result = result.replace('.', '')
        return result
        
    def limpiar(self):
        self.limpiar_campos()
        self.limpiar_etiquetas()
    
    def limpiar_campos(self):
        # Vaciar campos de entrada
        for entrada in [self.cajauno, self.cajados, self.cajatres]:
            entrada.delete(0, 'end')
            
    def limpiar_etiquetas(self):
        # Destruir etiquetas de resultados si existen
        etiquetas = ['etseis', 'etsiete', 'etcinco', 'etcuatro']
        for etiqueta in etiquetas:
            if hasattr(self, etiqueta):
                getattr(self, etiqueta).destroy()
                delattr(self, etiqueta)
            
    def change_appearance_mode_event(self, new_appearance_mode):
        set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "Light":
            if hasattr(self, 'etseis'):
                self.etseis.configure(text_color="white")
                self.etsiete.configure(text_color="white")
                self.etcuatro.configure(text_color="white")
                self.etcinco.configure(text_color="white")  
            for entrada in [self.cajauno, self.cajados, self.cajatres]:
                entrada.configure(text_color="black")
                
    @staticmethod
    def solo_numeros(char):
        return char.isdigit() or char in {'.', ','}
        
    def run(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = CuentasClaras()
    app.run()

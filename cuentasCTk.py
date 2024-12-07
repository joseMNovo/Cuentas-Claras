# pyinstaller --onefile --windowed --noconsole --icon=icon.ico cuentasCTk.py
from customtkinter import CTk, set_default_color_theme, set_appearance_mode, CTkLabel, CTkEntry, CTkFrame, CTkButton, CTkOptionMenu, CTkTabview
from tkinter import messagebox, ttk
from tkinter.font import BOLD, Font
import math
import requests
import random
import os
import json
from datetime import datetime

#pyinstaller --onefile --windowed --noconsole --icon=money.ico cuentasCTk.py

class CuentasClaras:
    def __init__(self):
        self.ventana = CTk()
        self.ventana.config(width=500, height=150)
        self.ventana.title("By Giuseppe")
        
        self.is_dark_mode = True
        self.historial_file = "historial_cuentas.json"
        self.cargar_historial()
        
        self.setup_ui()
        self.setup_bindings()
        set_default_color_theme("dark-blue")
        
    def setup_ui(self):
        # Crear TabView
        self.tabview = CTkTabview(self.ventana)
        self.tabview.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        # Crear pestañas
        self.tab_calculadora = self.tabview.add("Calculadora")
        self.tab_historial = self.tabview.add("Historial")
        
        # Configurar pestaña calculadora
        self.setup_calculadora_tab()
        
        # Configurar pestaña historial
        self.setup_historial_tab()
        
    def setup_calculadora_tab(self):
        # Título
        self.ettitulo = CTkLabel(self.tab_calculadora, text="------------- Cuentas Claras -------------")
        self.ettitulo.grid(row=0, columnspan=2)
        
        # Entradas
        vcmd = (self.ventana.register(self.solo_numeros), '%S')
        self.cajauno = self.crear_entrada(1, "Sueldo 1", "red", vcmd, self.tab_calculadora)
        self.cajados = self.crear_entrada(2, "Sueldo 2", "green", vcmd, self.tab_calculadora) 
        self.cajatres = self.crear_entrada(3, "A pagar", "blue", vcmd, self.tab_calculadora)
        
        # Frame de botones
        self.crear_frame_botones()
        
        # Frame de datos de gato
        self.crear_frame_cat()

    def setup_historial_tab(self):
        # Crear Treeview
        columns = ("ID", "Fecha", "Sueldo 1", "Sueldo 2", "Total", "Pago 1", "Pago 2")
        self.tree = ttk.Treeview(self.tab_historial, columns=columns, show="headings")
        
        # Configurar estilo del Treeview
        style = ttk.Style()
        style.theme_use('default')
        
        # Configurar colores y fuentes para el encabezado
        if self.is_dark_mode:
            heading_bg = "#2B2B2B"
            tree_bg = "#333333"
            odd_row_bg = "#404040"
            even_row_bg = "#333333"
            fg_color = "white"
        else:
            heading_bg = "#F0F0F0"
            tree_bg = "#FFFFFF"
            odd_row_bg = "#F5F5F5"
            even_row_bg = "#FFFFFF"
            fg_color = "black"
            
        style.configure("Treeview.Heading",
            background=heading_bg,
            foreground=fg_color,
            relief="flat",
            font=('Arial', 10, 'bold'))
            
        # Configurar colores y fuentes para el contenido
        style.configure("Treeview",
            background=tree_bg,
            foreground=fg_color,
            fieldbackground=tree_bg,
            font=('Arial', 9),
            rowheight=25)
            
        # Configurar selección
        style.map('Treeview',
            background=[('selected', '#1A83FF')],
            foreground=[('selected', 'white')])
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=50)
            else:
                self.tree.column(col, width=120)
            
        # Configurar colores alternados para las filas
        self.tree.tag_configure('oddrow', background=odd_row_bg)
        self.tree.tag_configure('evenrow', background=even_row_bg)
            
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Agregar scrollbar con estilo
        style.configure("Vertical.TScrollbar",
            background=heading_bg,
            troughcolor=tree_bg,
            arrowcolor=fg_color)
            
        scrollbar = ttk.Scrollbar(self.tab_historial, orient="vertical", 
            command=self.tree.yview, style="Vertical.TScrollbar")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botón para eliminar registro (inicialmente deshabilitado)
        self.delete_button = CTkButton(self.tab_historial, text="Eliminar registro", 
                                     command=self.eliminar_registro_seleccionado,
                                     state="disabled",
                                     fg_color="gray")
        self.delete_button.grid(row=1, column=0, pady=10)
        
        # Vincular evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
      
        # Cargar datos existentes
        self.actualizar_historial_tabla()
        
    def on_select(self, event):
        if self.tree.selection():
            self.delete_button.configure(state="normal", fg_color=["#3B8ED0", "#1F6AA5"])
        else:
            self.delete_button.configure(state="disabled", fg_color="gray")
        
    def eliminar_registro_seleccionado(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)['values']
            if item_values:
                id_registro = item_values[0]
                # Encontrar y eliminar el registro con el ID correspondiente
                for i, registro in enumerate(self.historial):
                    if registro["id"] == str(id_registro):
                        self.historial.pop(i)
                        break
                self.guardar_historial()
                self.actualizar_historial_tabla()
                self.delete_button.configure(state="disabled", fg_color="gray")
        
    def cargar_historial(self):
        if os.path.exists(self.historial_file):
            with open(self.historial_file, 'r') as f:
                self.historial = json.load(f)
        else:
            self.historial = []
            
    def guardar_historial(self):
        with open(self.historial_file, 'w') as f:
            json.dump(self.historial, f)
            
    def borrar_registro(self, index):
        self.historial.pop(index)
        self.guardar_historial()
        self.actualizar_historial_tabla()
            
    def actualizar_historial_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insertar datos
        for i, registro in enumerate(self.historial):
            item = self.tree.insert("", "end", values=(
                registro["id"],
                registro["fecha"],
                f"$ {registro['sueldo1']}",
                f"$ {registro['sueldo2']}",
                f"$ {registro['total']}",
                f"$ {registro['pago1']}",
                f"$ {registro['pago2']}"
            ))
            
    def crear_entrada(self, row, label_text, color, vcmd, parent):
        # Label
        label = CTkLabel(parent, text=label_text, fg_color=color, corner_radius=8)
        label.grid(row=row, column=0, pady=10)
        
        # Entry
        entry = CTkEntry(parent, width=300, height=40, text_color="silver", 
                        font=("Arial", 15), validate='key', validatecommand=vcmd)
        entry.grid(row=row, column=1, pady=10, padx=10)
        
        return entry
        
    def crear_frame_botones(self):
        frame = CTkFrame(self.tab_calculadora, corner_radius=10)
        frame.grid(row=6, columnspan=2)
        
        bcalcular = CTkButton(frame, text="Calcular", command=self.calcular)
        bcalcular.grid(row=0, column=0, pady=10, padx=10)
        
        blimpiar = CTkButton(frame, text="Limpiar", command=self.limpiar)
        blimpiar.grid(row=0, column=1, pady=10, padx=10)
        
        appearance_menu = CTkOptionMenu(frame, values=["Dark", "Light"], 
                                      command=self.change_appearance_mode_event)
        appearance_menu.grid(row=0, column=3, padx=10)
        
    def crear_frame_cat(self):
        self.cat_frame = CTkFrame(self.tab_calculadora, corner_radius=50)
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
        
        # Obtener el último ID
        ultimo_id = 0
        if self.historial:
            ultimo_id = max(int(registro["id"]) for registro in self.historial)
        
        # Guardar en historial
        registro = {
            "id": str(ultimo_id + 1),
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "sueldo1": str(sueldo1),
            "sueldo2": str(sueldo2),
            "total": str(total_a_pagar),
            "pago1": str(primer_pago),
            "pago2": str(segundo_pago)
        }
        self.historial.append(registro)
        self.guardar_historial()
        self.actualizar_historial_tabla()
        
        self.mostrar_resultados(primer_pago, segundo_pago)
        
    def mostrar_resultados(self, primer_pago, segundo_pago):
        # Limpiar etiquetas de resultados anteriores    
        self.limpiar_etiquetas()

        self.etcuatro = CTkLabel(self.tab_calculadora, text="Sueldo 1:")
        self.etcuatro.grid(row=4, column=0, pady=10)
        
        self.etcinco = CTkLabel(self.tab_calculadora, text="Sueldo 2:")
        self.etcinco.grid(row=5, column=0, pady=10)
        
        self.etseis = CTkLabel(self.tab_calculadora, text=f"${str(primer_pago).replace('.',',')}", 
                              font=("Arial", 15), text_color="red")
        self.etseis.grid(row=4, column=1)
        
        self.etsiete = CTkLabel(self.tab_calculadora, text=f"${str(segundo_pago).replace('.',',')}", 
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
        self.is_dark_mode = new_appearance_mode == "Dark"
        self.setup_historial_tab()
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

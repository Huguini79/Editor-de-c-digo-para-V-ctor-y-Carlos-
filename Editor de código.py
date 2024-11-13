import tkinter as tk
from tkinter import messagebox, simpledialog
import sys
import io
import os

root = tk.Tk()
root.configure(bg='white')
root.title('Editor de código')
root.geometry('1500x880')

global hecho
hecho = False

# Variables globales para manejar la ventana de salida y el área de texto de salida
output_window = None
output_text = None

def cierre_ventana():
    entrada = messagebox.askyesno('Advertencia', '¿Estás seguro de cerrar este programa?', icon='warning')
    if entrada:
        sys.exit(1)
    else:
        messagebox.showinfo('Ok', 'Puedes continuar con el programa.')

def python_lg():
    global hecho
    hecho = True
    pregunta_entrada = messagebox.askyesno('Pregunta', '¿Estás seguro de guardar todo el código fuente en un archivo .py?', icon='warning')
    if pregunta_entrada:
        archivo_python = 'script1.py'
        with open(archivo_python, 'w', encoding='utf-8') as write_python:
            write_python.write('# Código fuente escrito de Editor de código.exe\n\n')
            write_python.write(campo_de_texto.get('1.0', 'end-1c'))

# Función para insertar el carácter de cierre automáticamente
def auto_complete(event):
    char = event.char  # El carácter presionado
    cursor_index = campo_de_texto.index(tk.INSERT)  # Obtener la posición del cursor

    # Si es un carácter de apertura, insertar el cierre correspondiente
    if char == '(':
        campo_de_texto.insert(cursor_index, ')')
        campo_de_texto.mark_set(tk.INSERT, cursor_index)  # Mover el cursor dentro de los paréntesis
    elif char == '{':
        campo_de_texto.insert(cursor_index, '}')
        campo_de_texto.mark_set(tk.INSERT, cursor_index)  # Mover el cursor dentro de las llaves
    elif char == '[':
        campo_de_texto.insert(cursor_index, ']')
        campo_de_texto.mark_set(tk.INSERT, cursor_index)  # Mover el cursor dentro de los corchetes
    elif char == '"':
        campo_de_texto.insert(cursor_index, '"')
        campo_de_texto.mark_set(tk.INSERT, cursor_index)  # Mover el cursor entre las comillas
    elif char == "'":
        campo_de_texto.insert(cursor_index, "'")
        campo_de_texto.mark_set(tk.INSERT, cursor_index)  # Mover el cursor entre las comillas simples

# Función para manejar la ejecución del código y mostrar salidas
def python_ejecutar():
    global output_window, output_text

    # Cerrar la ventana de salida anterior si todavía existe
    if output_window is not None and tk.Toplevel.winfo_exists(output_window):
        output_window.destroy()
    
    # Crear una nueva ventana de salida
    output_window = tk.Toplevel(root)
    output_window.title("Salida del programa")
    output_text = tk.Text(output_window, height=20, width=80, wrap='word', bg='black', fg='white')
    output_text.pack(padx=10, pady=10)

    # Redirigir stdout a un buffer para capturar `print()`
    stdout_buffer = io.StringIO()
    sys.stdout = stdout_buffer

    # Redirigir input para capturar `input()`
    def custom_input(prompt=''):
        if prompt:
            output_text.insert(tk.END, prompt)
            output_text.see(tk.END)
        return simpledialog.askstring("Entrada", prompt)

    # Guardar la referencia original de input y reemplazarla temporalmente
    original_input = __builtins__.input
    __builtins__.input = custom_input

    # Ejecutar el código del campo de texto
    try:
        exec(campo_de_texto.get('1.0', 'end-1c'))
    except Exception as e:
        output_text.insert(tk.END, f"ERROR: {e}\n")
        output_window.configure(bg='red')
    finally:
        # Restaurar `input` y `stdout`
        __builtins__.input = original_input
        sys.stdout = sys.__stdout__

    # Obtener el contenido del buffer y mostrarlo en la ventana de salida
    output_content = stdout_buffer.getvalue()
    output_text.insert(tk.END, output_content)
    output_text.see(tk.END)

def compilar():
    if hecho == True:
        try:
            pregunta_compi = messagebox.askyesno('Pregunta', '¿Quieres que el .exe tenga el cmd o no(--noconsole)?')
            if pregunta_compi:
                os.system('pyinstaller --onefile script1.py')
            else:
                os.system('pyinstaller --onefile --noconsole script1.py')

        except Exception as e:
            messagebox.showerror('Error de compilación', f'Hubo un error al intentar compilar: {e}')
    else:
        messagebox.showerror('Error', 'Necesitar guardar el archivo de python')

campo_de_texto = tk.Text(root, height='80', width='200')
campo_de_texto.bind("<KeyRelease>", auto_complete)  # Asocia el evento de tecla con la función
tk.Button(root, text='Guardar archivo de Python', height='2', width='45', command=python_lg).grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text='Compilar a .exe', height='2', width='25', command=compilar).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text='Ejecutar script de python', width=40, height=2, command=python_ejecutar).grid(row=0, column=2, padx=10, pady=10)
campo_de_texto.grid(row=1, column=0, padx=200, pady=10, columnspan=3)
root.protocol('WM_DELETE_WINDOW', cierre_ventana)
root.mainloop()
import tkinter as tk
import ply.lex as lex

# Definición de tokens
tokens = (
    'VARIABLE',
    'FUNCION',
    'ITERAR',
    'SI',
    'PRINCIPAL',
    'ID',
    'NUMERO',
    'ASIGNACION',
    'OPERADOR',
    'IMPRIMIR',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'LLAVE_IZQ',
    'LLAVE_DER',
    'PUNTO_Y_COMA',
)

# Expresiones regulares para los tokens
t_VARIABLE = r'variable'
t_FUNCION = r'funcion'
t_ITERAR = r'iterar\s+[a-zA-Z]+\s*>>'
t_SI = r'si'
t_PRINCIPAL = r'correr'
t_ID = r'[a-zA-Z]+'
t_NUMERO = r'\d+'
t_ASIGNACION = r'='
t_OPERADOR = r'>>|[\+\-\/*]'
t_IMPRIMIR = r'imprimir'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_LLAVE_IZQ = r'{'
t_LLAVE_DER = r'}'
t_PUNTO_Y_COMA = r';'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Definición de la regla para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    error_char = t.value[0]
    print(f"Error: '{error_char}' en la posición {t.lexpos}")
    t.lexer.skip(1)

# Creación del lexer
lexer = lex.lex()

class IDESimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("AESCRIPT")
        self.text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=50)
        self.text_widget.pack(expand=tk.YES, fill=tk.BOTH)
        self.validation_button = tk.Button(root, text="Validar", command=self.validate_code)
        self.validation_button.pack()
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def validate_code(self):
        code = self.text_widget.get("1.0", tk.END)
        tokens_info = self.get_tokens_info(code)

        # Verificar si hay algún error en la información de tokens
        error_detected = any(token_info['token'] == 'error' for token_info in tokens_info)

        if error_detected:
            self.result_label.config(text="Código inválido")
        else:
            self.result_label.config(text="Código válido")

        # Crear una nueva ventana para mostrar la información de los tokens
        tokens_window = tk.Toplevel(self.root)
        tokens_window.title("Información de Tokens")

        # Crear un widget de texto para mostrar la información
        tokens_text = tk.Text(tokens_window, wrap=tk.WORD, height=15, width=50)
        tokens_text.pack(expand=tk.YES, fill=tk.BOTH)

        # Imprimir la información de los tokens en la nueva ventana
        tokens_text.insert(tk.END, "Información de Tokens:\n\n")
        for token_info in tokens_info:
            tokens_text.insert(tk.END, f"Token: {token_info['token']}\n")
            tokens_text.insert(tk.END, f"Valor: {token_info['value']}\n")
            if token_info['token'] == 'OPERADOR':
                tokens_text.insert(tk.END, f"Tipo: Operador\n")
            tokens_text.insert(tk.END, "\n")

    def get_tokens_info(self, code):
        # Analizar el código utilizando el lexer
        lexer.input(code)

        # Almacenar la información de los tokens en una lista de diccionarios
        tokens_info = []
        while True:
            tok = lexer.token()
            if not tok:
                break  # No hay más tokens
            tokens_info.append({'token': tok.type, 'value': tok.value})

        return tokens_info

if __name__ == "__main__":
    root = tk.Tk()
    ide_simulator = IDESimulator(root)
    root.mainloop()

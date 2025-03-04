import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import json
from fpdf import FPDF

class TuringMachine:
    def __init__(self, tape, transitions, start_state, accept_state):
        self.tape = list(tape) + ['B'] * 10  # Declaramos espacios vacios en la cinta
        self.head = 0
        self.state = start_state
        self.transitions = transitions
        self.accept_state = accept_state
        self.input_length = len(tape)  # longitud de la entrada

    def step(self):
        symbol = self.tape[self.head]
        if (self.state, symbol) in self.transitions:
            new_symbol, move, new_state = self.transitions[(self.state, symbol)]
            print(f"Transition: ({self.state}, {symbol}) → ({new_state}, {new_symbol}, {move})")
            self.tape[self.head] = new_symbol
            self.head += 1 if move == 'R' else -1 if move == 'L' else 0
            self.state = new_state
            self.display_tape()
            return True  # Indica que la máquina sigue en ejecución
        return False  # No hay transición, STOP MANO

    def run(self):
        print("\n=== Inicio de la Máquina de Turing ===\n")
        while self.state != self.accept_state and self.step():
            pass
        print("\n=== Fin de la Máquina de Turing ===\n")
        result_unary = ''.join(self.tape).strip('B')
        result_decimal = len(result_unary)  # UNARIO a DECIMAL
        print(f"\nResultado en unario: {result_unary}")
        print(f"Resultado en decimal (Fibonacci de {self.input_length}): {result_decimal}\n")
        return result_decimal
    
    def display_tape(self):
        tape_display = ''.join(
            [f"\033[91m{self.tape[i]}\033[0m" if i == self.head else self.tape[i] for i in range(len(self.tape))]
        )
        print(f"State: {self.state}\nTape: [{tape_display}]\n")

# Cargar transiciones desde un archivo JSON
def load_transitions_from_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return {(entry["state"], entry["symbol"]): (entry["new_symbol"], entry["move"], entry["new_state"]) for entry in data}

# Cargar transiciones
transitions = load_transitions_from_json("turing_fibonacci_transitions.json")

# Medir tiempos de ejecución
def measure_execution_time(n):
    tape_input = "1" * n
    tm = TuringMachine(tape_input, transitions, 'q0', 'HALT')
    start_time = time.time()
    result = tm.run()
    end_time = time.time()
    return n, end_time - start_time, result

# Probar la máquina con diferentes valores de N
test_values = [1, 2, 3,4,5,6,7,8,9,10]
results = [measure_execution_time(n) for n in test_values]
df = pd.DataFrame(results, columns=["N", "Execution Time (s)", "Fibonacci(N)"])

# Guardar tabla de tiempos
df.to_csv("turing_fibonacci_execution_times.csv", index=False)

# Crear PDF de reporte
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, "Reporte de Análisis Empírico - Máquina de Turing para Fibonacci", ln=True, align='C')
pdf.ln(10)

# Graficar dispersión de tiempos
plt.figure(figsize=(8,5))
plt.scatter(df["N"], df["Execution Time (s)"], label="Tiempos de ejecución")
plt.xlabel("N (Tamaño de Entrada)")
plt.ylabel("Tiempo de Ejecución (s)")
plt.title("Tiempo de Ejecución de la Máquina de Turing de Fibonacci")
plt.legend()
plt.savefig("turing_fibonacci_scatter.png")
pdf.cell(0, 10, "La siguiente gráfica muestra la dispersión de tiempos de ejecución en función del tamaño de la entrada.", ln=True)
pdf.image("turing_fibonacci_scatter.png", x=10, w=180)
pdf.ln(10)

# Ajuste de regresión polinómica
x = np.array(df["N"])
y = np.array(df["Execution Time (s)"])
poly_coeffs = np.polyfit(x, y, 2)  # Ajuste polinómico de grado 2
x_fit = np.linspace(min(x), max(x), 100)
y_fit = np.polyval(poly_coeffs, x_fit)

# Calcular R^2
y_pred = np.polyval(poly_coeffs, x)  # Valores predichos en los puntos originales
ss_tot = np.sum((y - np.mean(y))**2)  # Suma de cuadrados total
ss_res = np.sum((y - y_pred)**2)     # Suma de cuadrados residual
r2 = 1 - (ss_res / ss_tot)           # Coeficiente de determinación R^2

# Mostrar R^2 en pantalla
print(f"Coeficiente de determinación (R^2): {r2:.4f}")

# Graficar con R^2 en el título
plt.figure(figsize=(8,5))
plt.scatter(df["N"], df["Execution Time (s)"], label="Tiempos de ejecución")
plt.plot(x_fit, y_fit, color="red", label="Regresión Polinómica")
plt.xlabel("N (Tamaño de Entrada)")
plt.ylabel("Tiempo de Ejecución (s)")
plt.title(f"Ajuste de Regresión Polinómica (R² = {r2:.4f})")
plt.legend()
plt.savefig("turing_fibonacci_regression.png")
pdf.cell(0, 10, "La siguiente gráfica representa el ajuste de regresión polinómica para los tiempos de ejecución.", ln=True)
pdf.image("turing_fibonacci_regression.png", x=10, w=180)
pdf.ln(10)

pdf.output("turing_fibonacci_report.pdf")

print("\nAnálisis empírico completado. Resultados guardados:")
print("- Tabla de tiempos: turing_fibonacci_execution_times.csv")
print("- Diagrama de dispersión: turing_fibonacci_scatter.png")
print("- Gráfico de regresión: turing_fibonacci_regression.png")
print("- Reporte PDF: turing_fibonacci_report.pdf")

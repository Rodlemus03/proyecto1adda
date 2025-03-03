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

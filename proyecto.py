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

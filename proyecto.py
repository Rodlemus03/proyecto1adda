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

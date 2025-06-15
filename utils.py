import streamlit as st
import os
import pickle
import random


BASE_DIR = os.getenv("BASE_DIR", "/root")
LETTERS = ["A", "B", "C"]

@st.cache_data
def load_data(what):
    # Sostituisci con il tuo percorso
    return pickle.load(
        open(os.path.join(BASE_DIR, f"quesiti_{what}.pk"), "rb")
    )


def load_question(state):
    state.dataset = load_data(state.dataset_name.lower())
    # state.current_index = random.randint(0, len(state.dataset) - 1)
    state.options = None
    state.answered = False
    state.correct = None

    if state.materia_scelta != "Tutte le materie":
        state.dataset = state.dataset[
            state.dataset["MATERIA"] == state.materia_scelta
        ]
    row = state.dataset.iloc[state.current_index]
    options = LETTERS.copy()
    random.shuffle(options)
    state.domanda = row["DOMANDA"]
    state.numero = row["NUMERO"]
    state.materia = row["MATERIA"]
    state.A = row.A
    state.B = row.B
    state.C = row.C
    state.answer = row.A
    state.options = options

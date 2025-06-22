import streamlit as st
import os
import json
import pickle
import random


BASE_DIR = os.getenv("BASE_DIR", "/root")
LETTERS = ["A", "B", "C"]

ITEMS = {
    "current_index": 0,
    "answered": False,
    "correct": None,
    "options": LETTERS.copy(),
    "number_of_questions": 0,
    "number_of_corrects": 0,
    "subject": "Tutte le materie",
}

@st.cache_data
def load_data(what):
    # Sostituisci con il tuo percorso
    return pickle.load(open(os.path.join(BASE_DIR, f"quesiti_{what}.pk"), "rb"))


def dump_session_state(session_state):
    session_dict = {}
    for key in ITEMS:
        session_dict[key] = getattr(session_state, key, ITEMS[key])
    with open(os.path.join(BASE_DIR, "session_state.pkl"), "w") as f:
        json.dump(session_dict, f)


def load_session_state(session_state, reset=False):
    if os.path.exists(os.path.join(BASE_DIR, "session_state.pkl")) and reset is False:
        with open(os.path.join(BASE_DIR, "session_state.pkl"), "rb") as f:
            new_session_state = json.load(f)
            for key, value in new_session_state.items():
                setattr(session_state, key, value)
    else:
        for key, value in ITEMS.items():
            setattr(session_state, key, value)


def load_question(state):
    state.dataset = load_data(state.dataset_name.lower())
    # state.current_index = random.randint(0, len(state.dataset) - 1)
    state.options = None
    state.answered = False
    state.correct = None

    if state.materia_scelta != "Tutte le materie":
        state.dataset = state.dataset[state.dataset["MATERIA"] == state.materia_scelta]
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

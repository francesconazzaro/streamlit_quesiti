import os
import pickle
import random

import pandas as pd
import streamlit as st


BASE_DIR = os.getenv("BASE_DIR", "/root")


@st.cache_data
def load_data(what):
    # Sostituisci con il tuo percorso
    return pickle.load(
        open(os.path.join(BASE_DIR, f"quesiti_{what}.pk"), "rb")
    )


def load_question():
    st.session_state.dataset = load_data(st.session_state.dataset_name.lower())
    # st.session_state.current_index = random.randint(0, len(st.session_state.dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None

    if st.session_state.materia_scelta != "Tutte le materie":
        st.session_state.dataset = st.session_state.dataset[
            st.session_state.dataset["MATERIA"] == st.session_state.materia_scelta
        ]
    row = st.session_state.dataset.iloc[st.session_state.current_index]
    options = letters.copy()
    random.shuffle(options)
    st.session_state.domanda = row["DOMANDA"]
    st.session_state.numero = row["NUMERO"]
    st.session_state.materia = row["MATERIA"]
    st.session_state.A = row.A
    st.session_state.B = row.B
    st.session_state.C = row.C
    st.session_state.answer = row.A
    st.session_state.options = options


def back_question():
    st.session_state.current_index = st.session_state.current_index - 1
    load_question()
    st.rerun()


def next_question():
    st.session_state.current_index = st.session_state.current_index + 1
    load_question()
    st.rerun()


def update_index():
    st.session_state.current_index = int(st.session_state.index_input) - 2


istruttori = load_data("istruttori")
funzionari = load_data("funzionari")

left, right = st.columns(2)
st.session_state.dataset_name = left.segmented_control(
    "Seleziona il tipo Concorso",
    options=["Istruttori", "Funzionari"],
    default="Istruttori",
    on_change=load_question,
)

dataset = load_data(st.session_state.dataset_name.lower())
materia_options = dataset["MATERIA"].unique().tolist()
st.session_state.materia_scelta = right.selectbox(
    "Seleziona la materia",
    options=["Tutte le materie"] + materia_options,
    index=0,
)

index = st.select_slider(
    "Da quale domanda vuoi iniziare?",
    options=range(1, 2500),
    value=1,
    on_change=update_index,
    key="index_input",
)
letters = ["A", "B", "C"]
if st.button("🔄 Ricarica domande"):
    st.session_state.current_index = index - 1
    load_question()

if "current_index" not in st.session_state:
    st.session_state.current_index = index - 1
# if st.button("🔄 Ricarica domande"):
# dataset = load_data(dataset_name.lower())

if "options" not in st.session_state:
    st.session_state.dataset = load_data(st.session_state.dataset_name.lower())
    # st.session_state.current_index = random.randint(0, len(st.session_state.dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None


if st.session_state.options is None:
    next_question()

st.markdown(f"## Concorso: {st.session_state.dataset_name}")
st.markdown(f"### Materia: {st.session_state.materia}")
st.markdown(f"**Domanda {st.session_state.numero}:**")
st.text(f"{st.session_state.domanda}")

labels = {
    letter: st.session_state.get(option)
    for letter, option in zip(letters, st.session_state.options)
}
selected = st.radio(
    "Scegli una risposta:",
    options=[f"{k}: {v}" for k, v in labels.items()],
    index=None,
    disabled=st.session_state.answered,
)

if selected and not st.session_state.answered:
    answer = selected.split(":")[1]
    st.session_state.answered = True
    if answer.strip().lower() == st.session_state.answer.strip().lower():
        st.session_state.correct = True
        st.success("✅ Risposta corretta!")
    else:
        st.session_state.correct = False
        st.error(
            f"❌ Risposta sbagliata. Quella corretta era: **{letters[st.session_state.options.index('A')]}**: {st.session_state.answer}"
        )
else:
    st.text(" ")
    st.text(" ")

left, right = st.columns(2)
if left.button("⬅️ Domanda precedente"):
    back_question()
if right.button("➡️ Prossima domanda"):
    next_question()

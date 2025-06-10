import streamlit as st
import pandas as pd
import random

import pickle


# Carica il file CSV o qualsiasi altra fonte
@st.cache_data
def load_data(what):
    # Sostituisci con il tuo percorso
    return pickle.load(
        open(f"/root/quesiti_{what}.pk", "rb")
    )


def load_question():
    st.session_state.dataset = load_data(st.session_state.dataset_name.lower())
    # st.session_state.current_index = random.randint(0, len(st.session_state.dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None

    # Genera una nuova sequenza mescolata delle opzioni
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

def next_question():
    print("Indice precedente:", st.session_state.current_index)
    st.session_state.current_index = st.session_state.current_index + 1
    print("Indice corrente:", st.session_state.current_index)
    load_question()
    st.rerun()


def update_index():
    st.session_state.current_index = int(st.session_state.index_input) - 2


istruttori = load_data("istruttori")
funzionari = load_data("funzionari")

st.session_state.dataset_name = st.segmented_control(
    "Seleziona il tipo di domanda",
    options=["Istruttori", "Funzionari"],
    default="Istruttori",
    on_change=load_question,
)
index = st.select_slider("Da dove vuoi iniziare?", options=range(1, 2500), value=1, on_change=update_index, key="index_input")

if "current_index" not in st.session_state:
    st.session_state.current_index = index - 2
# if st.button("🔄 Ricarica domande"):
# dataset = load_data(dataset_name.lower())

letters = ["A", "B", "C"]
# Inizializza lo stato della sessione
if "options" not in st.session_state:
    st.session_state.dataset = load_data(st.session_state.dataset_name.lower())
    # st.session_state.current_index = random.randint(0, len(st.session_state.dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None


# Imposta le opzioni mescolate solo se non sono già state impostate per questa domanda
if st.session_state.options is None:
    next_question()

# Interfaccia utente
st.markdown(f"## Concorso: {st.session_state.dataset_name}")
st.markdown(f"### Materia: {st.session_state.materia}")
st.markdown(f"**Domanda {st.session_state.numero}:**")
st.text(f"{st.session_state.domanda}")

# Mostra le opzioni
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
print("Hai selezionato:", selected)
# Valutazione della risposta
if selected and not st.session_state.answered:
    answer = selected.split(":")[1]
    st.session_state.answered = True
    if answer.strip() == st.session_state.answer.strip():
        st.session_state.correct = True
        st.success("✅ Risposta corretta!")
    else:
        st.session_state.correct = False
        st.error(
            f"❌ Risposta sbagliata. Quella corretta era: **{letters[st.session_state.options.index('A')]}**: {st.session_state.answer}"
        )

# Bottone per la prossima domanda
if st.button("➡️ Prossima domanda"):
    next_question()

import streamlit as st
import pandas as pd
import random

import pickle


# Carica il file CSV o qualsiasi altra fonte
@st.cache_data
def load_data(what):
    # Sostituisci con il tuo percorso
    return pickle.load(
        open(f"/Users/francesconazzaro/Downloads/quesiti_{what}.pk", "rb")
    )


istruttori = load_data("istruttori")
funzionari = load_data("funzionari")

dataset_name = st.selectbox(
    "Seleziona il tipo di domanda",
    options=["Istruttori", "Funzionari"],
)

if st.button("🔄 Ricarica domande"):
    dataset = load_data("istruttori" if dataset_name == "Istruttori" else "funzionari")
    st.session_state.current_index = random.randint(0, len(dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None


letters = ["A", "B", "C"]
# Inizializza lo stato della sessione
if "current_index" not in st.session_state:
    st.session_state.current_index = random.randint(0, len(dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None


def next_question():
    st.session_state.current_index = random.randint(0, len(dataset) - 1)
    st.session_state.options = None
    st.session_state.answered = False
    st.session_state.correct = None

    # Genera una nuova sequenza mescolata delle opzioni
    row = dataset.iloc[st.session_state.current_index]
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
    st.rerun()


# Imposta le opzioni mescolate solo se non sono già state impostate per questa domanda
if st.session_state.options is None:
    next_question()

# Interfaccia utente
st.markdown(f"### Materia: {st.session_state.materia}")
st.markdown(f"**{st.session_state.numero} Domanda:** {st.session_state.domanda}")

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

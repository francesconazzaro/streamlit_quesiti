import streamlit as st
import pickle

import utils
import study


def update_index():
    st.session_state.current_index = int(st.session_state.index_input) - 2


istruttori = utils.load_data("istruttori")
funzionari = utils.load_data("funzionari")

mode = st.sidebar.segmented_control(
    "Modalità", options=["Studio", "Esame"], default="Studio"
)
randomize = st.sidebar.checkbox("Randomizza le domande")

if st.session_state.get("current_index") is None:
    print("Initializing session state")
    utils.load_session_state(st.session_state)

left, right = st.columns(2)
st.session_state.dataset_name = left.segmented_control(
    "Seleziona il tipo Concorso",
    options=["Istruttori", "Funzionari"],
    default="Istruttori",
)

if st.session_state.dataset_name == "Istruttori":
    data = study.Exam(
        dataset=istruttori,
        dataset_name=st.session_state.dataset_name,
        current_index=st.session_state.current_index,
    )
elif st.session_state.dataset_name == "Funzionari":
    data = study.Exam(
        dataset=funzionari,
        dataset_name=st.session_state.dataset_name,
        current_index=st.session_state.current_index,
    )

options = ["Tutte le materie"] + data.get_list_of_subjects()

st.session_state.subject = st.session_state.materia_scelta = right.selectbox(
    "Seleziona la materia",
    options=options,
    index=options.index(st.session_state.subject),
)

exam = study.Exam(
    dataset=data.dataset,
    dataset_name=data.dataset_name,
    current_index=st.session_state.current_index,
    subject=st.session_state.subject,
    randomize=randomize,
)

index = st.select_slider(
    "Da quale domanda vuoi iniziare?",
    options=range(1, 2500),
    value=1,
    on_change=update_index,
    key="index_input",
)

letters = ["A", "B", "C"]

if mode == "Esame" and st.session_state.number_of_questions:
    if st.session_state.number_of_corrects / st.session_state.number_of_questions > 0.7:
        color = "green"
    else:
        color = "red"
    result = f":{color}[{st.session_state.number_of_corrects} / {st.session_state.number_of_questions}  —  {(st.session_state.number_of_corrects / st.session_state.number_of_questions * 100):.1f} %]"
else:
    result = ""

left, right = st.columns(2)
left.markdown(f"## Concorso: {exam.dataset_name}")
right.markdown(f"## {result}")
st.markdown(f"### Materia: {exam.materia}")
st.markdown(f"**Domanda {exam.numero}:**")
st.text(f"{exam.domanda}")

labels = {
    letter: getattr(exam, option)
    for letter, option in zip(letters, st.session_state.options)
}
selected = st.radio(
    "Scegli una risposta:",
    options=[f"{k}: {v}" for k, v in labels.items()],
    index=None,
    disabled=st.session_state.answered,
)

print(selected)

if selected and not st.session_state.answered:
    answer = selected.split(":")[1]
    st.session_state.answered = True
    print(f"Selected answer: {answer}, {st.session_state.answered}")
    if answer.strip().lower() == exam.answer.strip().lower():
        exam.correct(st.session_state)
        st.success("✅ Risposta corretta!")
    else:
        exam.wrong(st.session_state)
        st.error(
            f"❌ Risposta sbagliata. Quella corretta era: **{letters[st.session_state.options.index('A')]}**: {exam.answer}"
        )
else:
    st.text(" ")
    st.text(" ")


left, right = st.columns(2)
if left.button("⬅️ Domanda precedente"):
    exam.back_question(st.session_state)
    st.rerun()
if right.button("➡️ Prossima domanda"):
    exam.next_question(st.session_state)
    st.rerun()

if st.button("🔄 Ricarica domanda"):
    exam.reload_questions(st.session_state)
    st.rerun()
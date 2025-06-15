import streamlit as st

import utils
import study


def update_index():
    st.session_state.current_index = int(st.session_state.index_input) - 2


istruttori = utils.load_data("istruttori")
funzionari = utils.load_data("funzionari")

mode = st.sidebar.segmented_control("Modalità", options=["Studio", "Esame"], default="Studio")
randomize = st.sidebar.checkbox("Randomizza le domande")

if st.session_state.get("current_index") is None:
    print("Initializing session state")
    st.session_state.current_index = 0
    st.session_state.answered = False
    st.session_state.correct = None
    st.session_state.options = utils.LETTERS.copy()
    st.session_state.number_of_questions = 0
    st.session_state.number_of_corrects = 0

left, right = st.columns(2)
dataset_name = left.segmented_control(
    "Seleziona il tipo Concorso",
    options=["Istruttori", "Funzionari"],
    default="Istruttori",
)

if dataset_name == "Istruttori":
    subjects = study.Exam(
        dataset=istruttori,
        dataset_name=dataset_name,
        current_index=st.session_state.current_index,
    )
elif dataset_name == "Funzionari":
    subjects = study.Exam(
        dataset=funzionari,
        dataset_name=dataset_name,
        current_index=st.session_state.current_index,
    )

subject = st.session_state.materia_scelta = right.selectbox(
    "Seleziona la materia",
    options=["Tutte le materie"] + subjects.get_list_of_subjects(),
    index=0,
)

print(subject)

exam = study.Exam(
    dataset=subjects.dataset,
    dataset_name=subjects.dataset_name,
    current_index=st.session_state.current_index,
    subject=subject,
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
# if st.button("🔄 Ricarica domande"):
#     st.session_state.current_index = index - 1
#     exam.reload_questions(st.session_state)

if mode == "Esame":
    if (
        st.session_state.number_of_questions
        and st.session_state.number_of_corrects / st.session_state.number_of_questions
        > 0.7
    ):
        color = "green"
    else:
        color = "red"
    result = f":{color}[{st.session_state.number_of_corrects} / {st.session_state.number_of_questions}]"
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
if mode == "Esame":
    if left.button("⬅️ Domanda precedente"):
        exam.back_question(st.session_state)
        st.rerun()
if right.button("➡️ Prossima domanda"):
    exam.next_question(st.session_state)
    st.rerun()

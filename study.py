from dataclasses import dataclass
import os.path
import pandas as pd
import random
import utils


@dataclass
class Question:
    text: str
    options: list[str]
    correct_option: str
    correct_answer: bool


@dataclass
class Subject:
    name: str
    questions: list[Question]


@dataclass
class Exam:
    dataset: pd.DataFrame
    dataset_name: str
    current_index: int
    user: str
    subject: str = "Tutte le materie"
    answered: bool = False
    randomize: bool = False

    def __post_init__(self):
        if self.subject != "Tutte le materie":
            self.dataset = self.dataset[self.dataset["MATERIA"] == self.subject]

        if self.current_index <= self.length():
            row = self.dataset.iloc[self.current_index - 1]
        else:
            row = self.dataset.iloc[random.randint(0, self.length() - 1)]
        options = utils.LETTERS.copy()
        random.shuffle(options)
        self.domanda = row["DOMANDA"]
        self.numero = row["NUMERO"]
        self.materia = row["MATERIA"]
        self.A = row.A
        self.B = row.B
        self.C = row.C
        self.answer = row.A

    def length(self):
        return len(self.dataset)

    def load_question(self, session_state):
        session_state.answered = False
        session_state.correct = None

        row = self.dataset.iloc[self.current_index - 1]
        options = utils.LETTERS.copy()
        random.shuffle(options)
        self.domanda = row["DOMANDA"]
        self.numero = row["NUMERO"]
        self.materia = row["MATERIA"]
        self.A = row.A
        self.B = row.B
        self.C = row.C
        self.answer = row.A
        session_state.options = options

    def next_question(self, session_state):
        if self.randomize:
            session_state.current_index = random.randint(0, len(self.dataset) - 1)
        else:
            session_state.current_index = (session_state.current_index + 1) % self.length()
        self.load_question(session_state)
        utils.dump_session_state(session_state)

    def back_question(self, session_state):
        session_state.current_index = max(1, session_state.current_index - 1)
        self.load_question(session_state)
        utils.dump_session_state(session_state)

    def reload_questions(self, session_state):
        utils.load_session_state(session_state, reset=True)
        self.load_question(session_state)

    def get_list_of_subjects(self):
        return self.dataset["MATERIA"].unique().tolist()

    def correct(self, session_state):
        session_state.correct = True
        session_state.number_of_corrects += 1
        session_state.number_of_questions += 1

    def wrong(self, session_state, answer):
        session_state.correct = False
        session_state.number_of_questions += 1
        try:
            wrong_answer = utils.load_wrong(session_state.user)
        except Exception:
            wrong_answer = pd.DataFrame(columns=["DOMANDA", "NUMERO", "MATERIA", "RISPOSTA", "given_answer", "A", "B", "C"])
        # Fill the DataFrame with the wrong answer details
        if self.numero not in list(wrong_answer["NUMERO"]):
            wrong_answer.loc[len(wrong_answer)] = {
                "DOMANDA": self.domanda,
                "NUMERO": self.numero,
                "MATERIA": self.materia,
                "RISPOSTA": self.answer,
                "given_answer": answer,
                "A": self.A,
                "B": self.B,
                "C": self.C
            }
            utils.dump_wrong_answers(session_state.user, wrong_answer)

import pandas as pd
import os


class ChatBot:
    def __init__(self, filename="conversatie.xlsx"):
        self.filename = filename
        self.history = []
        self.questions = [
            "Salut! Cum te numești?",
            "Cu ce te ocupi?",
            "Ce te interesează cel mai mult acum?"
        ]
        self.answers = []
        self.current_question = 0

    def add_to_history(self, sender, message):
        self.history.append({"from": sender, "message": message})
        self.save()

    def save(self):
        df = pd.DataFrame(self.history)
        df.to_excel(self.filename, index=False)

    def reset(self):
        self.history = []
        self.answers = []
        self.current_question = 0
        self.save()

    def get_next_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.current_question += 1
            return question
        return None

    def process_input(self, user_input):
        self.add_to_history("User", user_input)
        if self.current_question <= len(self.questions):
            self.answers.append(user_input)
        next_questions = self.get_next_question()
        if next_questions:
            self.add_to_history("Bot", next_questions)
            return next_questions
        response = self.generate_response()
        self.add_to_history("Bot", response)
        return response

    def generate_response(self):
        if len(self.answers) >= 3:
            name, occupation, interest = self.answers[:3]
            return (f"Îți mulțumesc, {name}! E grozav că ești implicat în {occupation} și te interesează {interest}. "
                    f"Sper să-ți fiu de folos!")
        return "Mulțumesc pentru răspunsuri!"

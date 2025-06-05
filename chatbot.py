import pandas as pd

from CONSTANTS import USER_QUESTIONS, QUESTIONS


class ChatBot:
    def __init__(self, filename="conversatie.xlsx"):
        self.filename = filename
        self.history = []
        self.questions = QUESTIONS
        self.answers = []
        self.current_question = 0
        self.user_questions = USER_QUESTIONS

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

    def check_for_known_question(self, user_input):
        user_input = user_input.lower()
        for key, value in self.user_questions.items():
            if key in user_input:
                return value
        return None

    def process_input(self, user_input):
        self.add_to_history("User", user_input)

        known_answer = self.check_for_known_question(user_input)
        if known_answer:
            self.add_to_history("Bot", known_answer)
            return known_answer

        if self.current_question <= len(self.questions):
            self.answers.append(user_input)

        next_question = self.get_next_question()
        if next_question:
            self.add_to_history("Bot", next_question)
            return next_question

        response = self.generate_response()
        self.add_to_history("Bot", response)
        return response

    def generate_response(self):
        if len(self.answers) >= 3:
            name, occupation, interest = self.answers[:3]
            return (f"Îți mulțumesc, {name}! E grozav că ești implicat în {occupation} și te interesează {interest}. "
                    f"Sper să-ți fiu de folos!")
        return "Mulțumesc pentru răspunsuri!"

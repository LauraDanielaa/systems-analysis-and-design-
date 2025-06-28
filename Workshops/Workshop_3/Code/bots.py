import random
import numpy as np

class QuestionerBot:
    """Bot que genera preguntas estratégicas"""

    def __init__(self, strategy="adaptive", bot_id=None):
        self.strategy = strategy
        self.bot_id = bot_id or f"Q_{random.randint(1000, 9999)}"
        self.skill_mu = 600 + random.uniform(-50, 50)
        self.skill_sigma = 100
        self.question_history = []
        self.performance_history = []

    def generate_question(self, game_state):
        """Genera pregunta basada en la estrategia del bot"""
        round_num = game_state.get('round', 0)
        category = game_state.get('category', 'unknown')

        if self.strategy == "adaptive":
            if round_num == 0:
                general_questions = [
                    "is it a living thing",
                    "is it something you can hold",
                    "is it man-made",
                    "is it larger than a person",
                    "is it found indoors"
                ]
                question = random.choice(general_questions)
            elif round_num < 5:
                category_questions = [
                    "is it used daily",
                    "is it made of metal",
                    "can you eat it",
                    "is it electronic",
                    "does it have moving parts"
                ]
                question = random.choice(category_questions)
            else:
                specific_questions = [
                    "is it found in a kitchen",
                    "is it used for transportation",
                    "is it decorative",
                    "can it be worn",
                    "does it require electricity"
                ]
                question = random.choice(specific_questions)
        else:
            # Estrategia aleatoria
            all_questions = [
                "is it alive", "is it big", "is it small", "is it useful",
                "is it expensive", "is it common", "is it rare", "is it old"
            ]
            question = random.choice(all_questions)

        self.question_history.append(question)
        return question

class AnswererBot:
    """Bot que responde preguntas basado en la palabra clave"""

    def __init__(self, consistency=0.8, bot_id=None):
        self.consistency = consistency
        self.bot_id = bot_id or f"A_{random.randint(1000, 9999)}"
        self.skill_mu = 600 + random.uniform(-50, 50)
        self.skill_sigma = 100
        self.response_history = []

    def answer_question(self, question, keyword, category):
        """Responde a una pregunta basada en la palabra clave"""
        question = question.lower()
        keyword = keyword.lower()

        # Lógica de respuesta basada en contenido
        if "living" in question or "alive" in question:
            if category == "animal" or any(word in keyword for word in ["plant", "tree", "flower"]):
                correct_answer = 1
            else:
                correct_answer = 0
        elif "electronic" in question:
            electronic_words = ["computer", "phone", "television", "radio", "camera", "microphone"]
            if any(word in keyword for word in electronic_words):
                correct_answer = 1
            else:
                correct_answer = 0
        elif "hold" in question:
            if category == "things" and random.random() > 0.4:
                correct_answer = 1
            else:
                correct_answer = 0
        elif "big" in question or "large" in question:
            large_items = ["truck", "house", "building", "car", "tree"]
            if any(word in keyword for word in large_items):
                correct_answer = 1
            else:
                correct_answer = 0
        else:
            # Respuesta aleatoria ponderada
            correct_answer = random.choices([0, 1], weights=[0.6, 0.4])[0]

        # Aplicar consistencia del bot
        if random.random() < self.consistency:
            final_answer = correct_answer
        else:
            # Respuesta inconsistente
            final_answer = 0.5 if random.random() < 0.3 else (1 - correct_answer)

        self.response_history.append(final_answer)
        return final_answer

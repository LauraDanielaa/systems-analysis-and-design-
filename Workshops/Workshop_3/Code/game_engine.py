import time
import random

class GameEngine:
    """Motor principal del juego"""

    def __init__(self, max_rounds=20, time_limit=60):
        self.max_rounds = max_rounds
        self.time_limit = time_limit
        self.games_played = 0

    def run_game(self, questioner, answerer, keyword, category):
        """Ejecuta una partida completa"""
        game_state = {
            'keyword': keyword,
            'category': category,
            'round': 0,
            'guessed': False,
            'history': [],
            'start_time': time.time(),
            'questioner_id': questioner.bot_id,
            'answerer_id': answerer.bot_id
        }

        # Determinar número de rondas (variable para realismo)
        max_rounds = random.randint(5, self.max_rounds)

        for round_num in range(max_rounds):
            game_state['round'] = round_num

            # Generar pregunta
            question = questioner.generate_question(game_state)

            # Simular tiempo de procesamiento
            processing_time = random.uniform(0.5, 3.0)

            # Verificar timeout
            if processing_time > self.time_limit:
                return {
                    'status': 'timeout',
                    'rounds': round_num + 1,
                    'history': game_state['history'],
                    'winner': 'answerer'
                }

            # Obtener respuesta
            answer = answerer.answer_question(question, keyword, category)
            game_state['history'].append((question, answer, processing_time))

            # Simular probabilidad de acierto (aumenta con las rondas)
            base_probability = 0.05
            round_bonus = 0.03 * round_num
            skill_bonus = (questioner.skill_mu - 600) / 1000

            guess_probability = base_probability + round_bonus + skill_bonus
            guess_probability = max(0.01, min(0.8, guess_probability))

            if random.random() < guess_probability:
                game_state['guessed'] = True
                break

        # Determinar resultado
        if game_state['guessed']:
            status = 'success'
            winner = 'questioner'
        else:
            status = 'failure'
            winner = 'answerer'

        self.games_played += 1

        return {
            'status': status,
            'rounds': game_state['round'] + 1,
            'history': game_state['history'],
            'winner': winner,
            'total_time': sum([h[2] for h in game_state['history']])
        }

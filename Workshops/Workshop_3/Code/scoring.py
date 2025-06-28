class ScoringSystem:
    """Sistema de puntuación basado en ELO"""

    def __init__(self, k_factor=32):
        self.k_factor = k_factor
        self.history = []

    def update_skills(self, questioner, answerer, game_result):
        """Actualiza habilidades usando sistema ELO modificado"""

        # Determinar resultado desde perspectiva del questioner
        if game_result['winner'] == 'questioner':
            q_score = 1.0
        elif game_result['status'] == 'timeout':
            q_score = 0.0  # Penalizar timeout
        else:
            q_score = 0.0

        # Calcular expectativas
        q_expected = 1 / (1 + 10**((answerer.skill_mu - questioner.skill_mu) / 400))
        a_expected = 1 - q_expected

        # Actualizar habilidades
        questioner.skill_mu += self.k_factor * (q_score - q_expected)
        answerer.skill_mu += self.k_factor * ((1 - q_score) - a_expected)

        # Reducir incertidumbre gradualmente
        questioner.skill_sigma = max(50, questioner.skill_sigma * 0.98)
        answerer.skill_sigma = max(50, answerer.skill_sigma * 0.98)

        # Registrar en historial
        self.history.append({
            'questioner_id': questioner.bot_id,
            'answerer_id': answerer.bot_id,
            'q_mu_before': questioner.skill_mu - self.k_factor * (q_score - q_expected),
            'a_mu_before': answerer.skill_mu - self.k_factor * ((1 - q_score) - a_expected),
            'q_mu_after': questioner.skill_mu,
            'a_mu_after': answerer.skill_mu,
            'result': game_result['winner'],
            'rounds': game_result['rounds']
        })

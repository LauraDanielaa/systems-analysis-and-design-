import random

class Matchmaker:
    """Sistema de emparejamiento por habilidad"""

    def __init__(self, skill_tolerance=100):
        self.skill_tolerance = skill_tolerance

    def find_match(self, questioner_pool, answerer_pool):
        """Encuentra emparejamiento basado en habilidad similar"""

        if not questioner_pool or not answerer_pool:
            return None, None

        # Seleccionar questioner aleatorio
        questioner = random.choice(questioner_pool)

        # Encontrar answerer con habilidad similar
        compatible_answerers = [
            a for a in answerer_pool
            if abs(a.skill_mu - questioner.skill_mu) <= self.skill_tolerance
        ]

        if compatible_answerers:
            answerer = random.choice(compatible_answerers)
        else:
            # Si no hay compatible, tomar el más cercano
            answerer = min(answerer_pool, key=lambda a: abs(a.skill_mu - questioner.skill_mu))

        return questioner, answerer

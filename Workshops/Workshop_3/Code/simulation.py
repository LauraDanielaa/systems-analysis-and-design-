import pandas as pd
import numpy as np
from bots import QuestionerBot, AnswererBot
from game_engine import GameEngine
from scoring import ScoringSystem
from matchmaking import Matchmaker

def run_simulation(data, keyword_dict, config):
    """Ejecuta simulación completa con múltiples escenarios"""

    print("\n" + "="*60)
    print("INICIANDO SIMULACIÓN PRINCIPAL")
    print("="*60)

    # Configuración por defecto
    default_config = {
        'num_games': 100,
        'num_questioners': 10,
        'num_answerers': 10,
        'scenarios': ['balanced', 'chaotic', 'skilled']
    }
    config = {**default_config, **config}

    all_results = []

    for scenario in config['scenarios']:
        print(f"\n{'-'*40}")
        print(f"EJECUTANDO ESCENARIO: {scenario.upper()}")
        print(f"{'-'*40}")

        # Configurar bots según escenario
        if scenario == 'balanced':
            questioners = [QuestionerBot(strategy="adaptive") for _ in range(config['num_questioners'])]
            answerers = [AnswererBot(consistency=0.8) for _ in range(config['num_answerers'])]
        elif scenario == 'chaotic':
            questioners = [QuestionerBot(strategy="random") for _ in range(config['num_questioners'])]
            answerers = [AnswererBot(consistency=0.5) for _ in range(config['num_answerers'])]
        else:  # skilled
            questioners = [QuestionerBot(strategy="adaptive") for _ in range(config['num_questioners'])]
            for q in questioners:
                q.skill_mu += random.uniform(0, 200)  # Bots más hábiles
            answerers = [AnswererBot(consistency=0.9) for _ in range(config['num_answerers'])]

        # Inicializar sistemas
        engine = GameEngine()
        scoring = ScoringSystem()
        matchmaker = Matchmaker()

        # Ejecutar juegos
        scenario_results = []

        # Seleccionar subset de datos
        game_data = data.sample(n=min(config['num_games'], len(data)), random_state=42)

        for i, (_, row) in enumerate(game_data.iterrows()):
            if i % 20 == 0:
                print(f"Progreso: {i+1}/{len(game_data)}")

            # Obtener palabra clave
            keyword = row.get('keyword_clean', row.get('keyword', 'unknown'))
            category = keyword_dict.get(keyword, 'unknown')

            # Hacer emparejamiento
            questioner, answerer = matchmaker.find_match(questioners, answerers)

            if questioner and answerer:
                # Ejecutar juego
                game_result = engine.run_game(questioner, answerer, keyword, category)

                # Actualizar habilidades
                scoring.update_skills(questioner, answerer, game_result)

                # Registrar resultado
                scenario_results.append({
                    'scenario': scenario,
                    'game_id': i,
                    'keyword': keyword,
                    'category': category,
                    'rounds': game_result['rounds'],
                    'status': game_result['status'],
                    'winner': game_result['winner'],
                    'total_time': game_result.get('total_time', 0),
                    'q_id': questioner.bot_id,
                    'a_id': answerer.bot_id,
                    'q_mu': questioner.skill_mu,
                    'q_sigma': questioner.skill_sigma,
                    'a_mu': answerer.skill_mu,
                    'a_sigma': answerer.skill_sigma,
                    'questions_asked': len(game_result['history'])
                })

        all_results.extend(scenario_results)
        print(f"Completado escenario {scenario}: {len(scenario_results)} juegos")

    return pd.DataFrame(all_results)

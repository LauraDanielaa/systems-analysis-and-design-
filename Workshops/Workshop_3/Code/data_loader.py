import pandas as pd
import os

def load_csv_robust(file_path, max_attempts=5):
    """Carga CSV con múltiples estrategias para manejar errores de formato"""

    strategies = [
        {'engine': 'python'},
        {'engine': 'python', 'on_bad_lines': 'skip'},
        {'engine': 'python', 'on_bad_lines': 'skip', 'quoting': 3},
        {'engine': 'python', 'on_bad_lines': 'skip', 'quoting': 3, 'escapechar': '\\'},
        {'engine': 'c', 'on_bad_lines': 'skip', 'error_bad_lines': False}
    ]

    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"Intentando estrategia {i} para cargar {os.path.basename(file_path)}...")
            df = pd.read_csv(file_path, **strategy)
            print(f"✅ Éxito con estrategia {i}: {df.shape}")
            return df
        except Exception as e:
            print(f"❌ Estrategia {i} falló: {str(e)[:100]}...")
            if i == max_attempts:
                raise Exception(f"No se pudo cargar {file_path} con ninguna estrategia")
            continue

    raise Exception("Todas las estrategias fallaron")

def load_games_data(file_path):
    """Carga el dataset de juegos"""
    return load_csv_robust(file_path)

def load_keywords_data(file_path):
    """Carga el dataset de palabras clave"""
    return pd.read_csv(file_path)

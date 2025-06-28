import pandas as pd
import numpy as np
import re
import ast
import random
def process_answers(answer_sequence):
    """Convierte secuencia de respuestas a formato binario"""
    if pd.isna(answer_sequence):
        return [], 0

    # Limpiar formato de lista
    answers_str = str(answer_sequence).replace("'", "").replace("[", "").replace("]", "")
    answer_list = [ans.strip().lower() for ans in answers_str.split(',') if ans.strip()]

    # Mapeo a binario
    binary_map = {
        'yes': 1, 'y': 1, 'true': 1,
        'no': 0, 'n': 0, 'false': 0,
        'maybe': 0.5, 'possibly': 0.5, 'perhaps': 0.5
    }

    binary_answers = [binary_map.get(ans, 0) for ans in answer_list]
    avg_certainty = np.mean([abs(ans - 0.5) for ans in binary_answers]) if binary_answers else 0

    return binary_answers, avg_certainty

def process_questions(question_sequence):
    """Procesa y limpia secuencia de preguntas"""
    if pd.isna(question_sequence):
        return [], 0

    # Extraer preguntas
    questions_str = str(question_sequence).replace("'", "").replace("[", "").replace("]", "")
    question_list = [q.strip() for q in questions_str.split(',') if q.strip()]

    cleaned_questions = []
    for question in question_list:
        # Normalización
        q_clean = question.lower()
        q_clean = re.sub(r'[^\w\s\?]', '', q_clean)
        q_clean = re.sub(r'\s+', ' ', q_clean)
        q_clean = q_clean.strip()

        # Filtros de calidad
        if len(q_clean) >= 5 and len(q_clean.split()) >= 2:
            cleaned_questions.append(q_clean)

    avg_length = np.mean([len(q.split()) for q in cleaned_questions]) if cleaned_questions else 0
    return cleaned_questions, avg_length

def clean_games_data(games_df, keywords_df):
    """Limpieza completa del dataset de juegos"""

    print(f"Dataset original: {games_df.shape}")

    # Crear diccionario de palabras clave
    keyword_dict = dict(zip(keywords_df['keyword'], keywords_df['category']))

    # Limpiar datos básicos
    critical_columns = ['keyword', 'answers', 'questions']
    available_columns = [col for col in critical_columns if col in games_df.columns]

    initial_rows = len(games_df)
    games_df = games_df.dropna(subset=available_columns)
    print(f"Después de eliminar nulos: {len(games_df)} filas (-{initial_rows - len(games_df)})")

    # Procesar respuestas
    games_df[['answers_binary', 'answer_certainty']] = games_df['answers'].apply(
        lambda x: pd.Series(process_answers(x))
    )

    # Procesar preguntas
    games_df[['questions_clean', 'avg_question_length']] = games_df['questions'].apply(
        lambda x: pd.Series(process_questions(x))
    )

    # Métricas adicionales
    games_df['num_answers'] = games_df['answers_binary'].apply(len)
    games_df['num_questions'] = games_df['questions_clean'].apply(len)
    games_df['qa_ratio'] = games_df['num_answers'] / (games_df['num_questions'] + 1)

    # Normalizar palabras clave y agregar categorías
    games_df['keyword_clean'] = games_df['keyword'].str.lower().str.strip()
    games_df['category'] = games_df['keyword_clean'].map(keyword_dict).fillna('unknown')

    # Métricas de éxito
    if 'guessed' in games_df.columns:
        games_df['success'] = games_df['guessed'].astype(int)
    else:
        games_df['success'] = (games_df['num_questions'] <= 15).astype(int)

    # Filtros de calidad (menos restrictivos)
    quality_filter = (
        (games_df['num_answers'] >= 1) &
        (games_df['num_questions'] >= 1) &
        (games_df['num_answers'] <= 30)
    )

    games_df = games_df[quality_filter]
    print(f"Dataset final limpio: {games_df.shape}")

    return games_df, keyword_dict

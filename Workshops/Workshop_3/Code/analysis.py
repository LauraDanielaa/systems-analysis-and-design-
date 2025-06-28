import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analyze_results(results_df, save_plots=True):
    """Análisis completo de resultados con visualizaciones"""

    print("\n" + "="*60)
    print("ANÁLISIS DE RESULTADOS")
    print("="*60)

    if len(results_df) == 0:
        print("❌ No hay datos para analizar")
        return

    # Estadísticas generales
    total_games = len(results_df)
    success_rate = (results_df['status'] == 'success').mean()
    timeout_rate = (results_df['status'] == 'timeout').mean()
    avg_rounds = results_df['rounds'].mean()

    print(f"📊 ESTADÍSTICAS GENERALES:")
    print(f"   Total de juegos: {total_games}")
    print(f"   Tasa de éxito: {success_rate:.2%}")
    print(f"   Tasa de timeout: {timeout_rate:.2%}")
    print(f"   Rondas promedio: {avg_rounds:.2f}")

    # Análisis por escenario
    if 'scenario' in results_df.columns:
        scenario_stats = results_df.groupby('scenario').agg({
            'status': lambda x: (x == 'success').mean(),
            'rounds': 'mean',
            'total_time': 'mean'
        }).round(3)
        scenario_stats.columns = ['Tasa_Éxito', 'Rondas_Promedio', 'Tiempo_Promedio']
        print(f"\n📈 ANÁLISIS POR ESCENARIO:")
        print(scenario_stats)

    # Análisis por categoría
    if 'category' in results_df.columns:
        category_stats = results_df.groupby('category').agg({
            'status': lambda x: (x == 'success').mean(),
            'rounds': 'mean'
        }).sort_values('status', ascending=False).head(10)
        category_stats.columns = ['Tasa_Éxito', 'Rondas_Promedio']
        print(f"\n🎯 TOP 10 CATEGORÍAS (por tasa de éxito):")
        print(category_stats.round(3))

    # Detección de comportamiento caótico
    rounds_std = results_df['rounds'].std()
    skill_variation_q = results_df['q_mu'].std()
    skill_variation_a = results_df['a_mu'].std()

    print(f"\n🌪️  ANÁLISIS DE CAOS:")
    print(f"   Variabilidad en rondas: {rounds_std:.2f}")
    print(f"   Variación habilidad Q: {skill_variation_q:.2f}")
    print(f"   Variación habilidad A: {skill_variation_a:.2f}")

    if rounds_std > 5:
        print("   ⚠️  Alta variabilidad en duración de partidas")
    if skill_variation_q > 100 or skill_variation_a > 100:
        print("   ⚠️  Comportamiento caótico en evolución de habilidades")

    # Crear visualizaciones
    if save_plots:
        create_plots(results_df)

    return {
        'total_games': total_games,
        'success_rate': success_rate,
        'avg_rounds': avg_rounds,
        'chaos_indicators': {
            'rounds_std': rounds_std,
            'skill_variation_q': skill_variation_q,
            'skill_variation_a': skill_variation_a
        }
    }

def create_plots(results_df):
    """Crea visualizaciones completas"""

    # Configurar estilo
    plt.style.use('default')
    sns.set_palette("husl")

    # Figura principal con múltiples subplots
    fig = plt.figure(figsize=(16, 12))

    # 1. Evolución de habilidades
    plt.subplot(2, 3, 1)
    if len(results_df) > 1:
        plt.plot(results_df['q_mu'].values, label='Questioner (μ)', alpha=0.7, linewidth=2)
        plt.plot(results_df['a_mu'].values, label='Answerer (μ)', alpha=0.7, linewidth=2)
        plt.fill_between(range(len(results_df)),
                         results_df['q_mu'] - results_df['q_sigma'],
                         results_df['q_mu'] + results_df['q_sigma'],
                         alpha=0.2)
    plt.title('Evolución de Habilidades', fontsize=12, fontweight='bold')
    plt.xlabel('Número de Juego')
    plt.ylabel('Puntuación de Habilidad')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 2. Distribución de resultados
    plt.subplot(2, 3, 2)
    if 'status' in results_df.columns:
        status_counts = results_df['status'].value_counts()
        colors = ['#2ecc71', '#e74c3c', '#f39c12'][:len(status_counts)]
        plt.bar(status_counts.index, status_counts.values, color=colors)
        plt.title('Distribución de Resultados', fontsize=12, fontweight='bold')
        plt.ylabel('Cantidad de Juegos')
        for i, v in enumerate(status_counts.values):
            plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    # 3. Comportamiento caótico
    plt.subplot(2, 3, 3)
    if len(results_df) > 10:
        scatter = plt.scatter(results_df['rounds'], results_df['q_mu'],
                              c=range(len(results_df)), cmap='viridis', alpha=0.6, s=30)
        plt.colorbar(scatter, label='Número de Juego')
    plt.title('Comportamiento Caótico', fontsize=12, fontweight='bold')
    plt.xlabel('Rondas Jugadas')
    plt.ylabel('Habilidad Questioner (μ)')
    plt.grid(True, alpha=0.3)

    # 4. Distribución de rondas
    plt.subplot(2, 3, 4)
    plt.hist(results_df['rounds'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(results_df['rounds'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Media: {results_df["rounds"].mean():.1f}')
    plt.title('Distribución de Rondas por Juego', fontsize=12, fontweight='bold')
    plt.xlabel('Número de Rondas')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # 5. Rendimiento por escenario
    plt.subplot(2, 3, 5)
    if 'scenario' in results_df.columns and len(results_df['scenario'].unique()) > 1:
        scenario_success = results_df.groupby('scenario')['status'].apply(
            lambda x: (x == 'success').mean()
        ).sort_values(ascending=False)

        bars = plt.bar(range(len(scenario_success)), scenario_success.values,
                       color=['#3498db', '#e67e22', '#9b59b6'][:len(scenario_success)])
        plt.title('Tasa de Éxito por Escenario', fontsize=12, fontweight='bold')
        plt.ylabel('Tasa de Aciertos')
        plt.xticks(range(len(scenario_success)), scenario_success.index, rotation=45)

        for i, v in enumerate(scenario_success.values):
            plt.text(i, v + 0.01, f'{v:.2%}', ha='center', fontweight='bold')

    # 6. Heatmap de correlaciones
    plt.subplot(2, 3, 6)
    numeric_cols = ['rounds', 'total_time', 'q_mu', 'a_mu', 'questions_asked']
    available_cols = [col for col in numeric_cols if col in results_df.columns]

    if len(available_cols) > 2:
        corr_matrix = results_df[available_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
    plt.title('Correlaciones entre Variables', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig('simulation_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("📈 Visualizaciones guardadas como 'simulation_comprehensive_analysis.png'")

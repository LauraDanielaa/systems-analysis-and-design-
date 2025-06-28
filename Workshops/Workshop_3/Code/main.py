import os
import sys

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import load_games_data, load_keywords_data
from preprocessing import clean_games_data
from simulation import run_simulation
from analysis import analyze_results

def main():
    """Función principal que ejecuta toda la simulación"""

    print("🚀 INICIANDO SIMULACIÓN DEL SISTEMA '20 QUESTIONS'")
    print("="*80)

    # Configuración de archivos
    GAMES_FILE = '../games_data.csv'
    KEYWORDS_FILE = '../keywords.csv'

    try:
        # 1. Cargar datos
        print("📁 Paso 1: Cargando datos...")
        games_df = load_games_data(GAMES_FILE)
        keywords_df = load_keywords_data(KEYWORDS_FILE)

        # 2. Limpiar datos
        print("🧹 Paso 2: Limpiando datos...")
        df_clean, keyword_dict = clean_games_data(games_df, keywords_df)

        if len(df_clean) == 0:
            print("❌ Error: No hay datos válidos para simular")
            return

        # 3. Configurar simulación
        simulation_config = {
            'num_games': min(150, len(df_clean)),
            'num_questioners': 8,
            'num_answerers': 8,
            'scenarios': ['balanced', 'chaotic', 'skilled']
        }

        print(f"⚙️  Configuración de simulación:")
        for key, value in simulation_config.items():
            print(f"   {key}: {value}")

        # 4. Ejecutar simulación
        print("\n🎮 Paso 3: Ejecutando simulación...")
        results = run_simulation(df_clean, keyword_dict, simulation_config)

        if len(results) == 0:
            print("❌ Error: No se generaron resultados")
            return

        # 5. Analizar resultados
        print("\n📊 Paso 4: Analizando resultados...")
        analysis_summary = analyze_results(results, save_plots=True)

        # 6. Guardar resultados
        results.to_csv('simulation_results_complete.csv', index=False)
        print(f"\n💾 Resultados guardados en 'simulation_results_complete.csv'")

        # 7. Resumen final
        print("\n" + "="*80)
        print("🎉 SIMULACIÓN COMPLETADA EXITOSAMENTE")
        print("="*80)
        print("📋 Archivos generados:")
        print("   📊 simulation_comprehensive_analysis.png - Gráficos de análisis")
        print("   📄 simulation_results_complete.csv - Resultados detallados")

        print(f"\n🏆 RESUMEN EJECUTIVO:")
        print(f"   🎮 Juegos simulados: {analysis_summary['total_games']}")
        print(f"   ✅ Tasa de éxito: {analysis_summary['success_rate']:.2%}")
        print(f"   🎯 Rondas promedio: {analysis_summary['avg_rounds']:.1f}")

        chaos = analysis_summary['chaos_indicators']
        print(f"   🌪️  Indicadores de caos:")
        print(f"      - Variabilidad rondas: {chaos['rounds_std']:.2f}")
        print(f"      - Volatilidad habilidades: {chaos['skill_variation_q']:.1f}")

        return results, analysis_summary

    except Exception as e:
        print(f"❌ Error durante la simulación: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    results, summary = main()

    if results is not None:
        print("\n🔍 Análisis adicional disponible:")
        print("   - results: DataFrame con todos los resultados")
        print("   - summary: Diccionario con métricas clave")
    else:
        print("\n❌ La simulación no se completó correctamente")

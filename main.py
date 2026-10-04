import os
import numpy as np

from engine.api_client import FootballDataClient
from engine.processor import DataProcessor
from engine.model import PredictionModel
from engine.betting_markets import BettingMarkets
from engine.ml_models import (
    GradientBoostingPredictor,
    LSTMMomentumAnalyzer,
    BivariatePoissionModel,
)


def _history_to_metric_series(history, team_id, processor):
    """Convierte historial bruto del cliente a serie de métricas de partido."""
    series = []
    for item in history or []:
        if not item:
            continue
        matched = item.get("match") or {}
        stats = item.get("stats") or {}
        metrics = processor._extract_stats(matched, stats, team_id)
        series.append({
            "goals": metrics.get("goals", 0),
            "shots_on_target": metrics.get("shots_on_target", 0),
            "total_shots": metrics.get("total_shots", 0),
            "corners": metrics.get("corners", 0),
        })
    return series


def _format_percentage(value):
    """Formatea valores decimales a porcentajes."""
    if isinstance(value, (int, float)):
        return f"{value * 100:.2f}%" if 0 <= value <= 1 else f"{value:.2f}%"
    return str(value)


def _print_section_header(title):
    """Imprime un encabezado de sección bien formateado."""
    print(f"\n{'═' * 80}")
    print(f"  {title.upper()}")
    print(f"{'═' * 80}")


def _print_subsection(title):
    """Imprime un subtítulo de subsección."""
    print(f"\n  ▶ {title}")
    print(f"  {'-' * 76}")


def run_pipeline(match_id):
    print(f"\n{'█' * 80}")
    print(f"  🏆 SISTEMA DE PROYECCIÓN AUTOMÁTICA DE FÚTBOL")
    print(f"  Iniciando análisis para Match ID: {match_id}")
    print(f"{'█' * 80}")

    client = FootballDataClient()
    processor = DataProcessor()
    model = PredictionModel()
    betting = BettingMarkets()

    # 1. Obtener detalles del partido
    print("\n  📊 Obteniendo detalles del partido...")
    response = client.get_match_details(match_id)
    if not response:
        print("  ❌ Error: No se pudo obtener la respuesta de la API.")
        return

    match_data = response.get('data', response)

    team_a_id = match_data.get('home_team', {}).get('id')
    team_b_id = match_data.get('away_team', {}).get('id')
    team_a_name = match_data.get('home_team', {}).get('name', 'Local')
    team_b_name = match_data.get('away_team', {}).get('name', 'Visitante')
    match_date = match_data.get('utc_date', '').split('T')[0]

    if not team_a_id or not team_b_id:
        print("  ❌ Error: No se pudieron identificar los IDs de los equipos.")
        return

    print(f"  ✅ Partido: {team_a_name} vs {team_b_name}")
    print(f"  📅 Fecha: {match_date}")

    # 2. Obtener historial
    print("\n  📈 Recopilando estadísticas históricas detalladas...")
    hist_a = client.get_historical_team_data(team_a_id, match_date)
    hist_b = client.get_historical_team_data(team_b_id, match_date)

    # 3. Calcular promedios de métricas
    print(f"  🔍 Procesando {len(hist_a)} partidos de {team_a_name}")
    print(f"  🔍 Procesando {len(hist_b)} partidos de {team_b_name}...")
    avg_a = processor.calculate_averages(hist_a, team_a_id)
    avg_b = processor.calculate_averages(hist_b, team_b_id)

    if not avg_a or not avg_b:
        print("  ❌ Error: No se pudieron calcular promedios suficientes.")
        return

    # 4. Proyección base del modelo existente
    print("  ⚙️  Ejecutando modelo base...")
    features = processor.prepare_features(avg_a, avg_b)
    predictions = model.predict_market(features)

    # 5. Gradient Boosting para ajustar la línea final
    print("  🚀 Ejecutando Gradient Boosting...")
    goal_signal = float(predictions.get('goals', {}).get('safe_over_line', 1.5))
    corner_signal = float(predictions.get('corners', {}).get('safe_over_line', 7.5))
    shot_signal = float(predictions.get('shots_on_target', {}).get('safe_over_line', 6.0))

    gb_features = np.array([
        [
            avg_a.get('goals', 0),
            avg_b.get('goals', 0),
            avg_a.get('corners', 0),
            avg_b.get('corners', 0),
            avg_a.get('shots_on_target', 0),
            avg_b.get('shots_on_target', 0),
            avg_a.get('total_shots', 0),
            avg_b.get('total_shots', 0),
        ]
    ], dtype=float)
    gb_targets = np.array([goal_signal + corner_signal / 4 + shot_signal / 3], dtype=float)

    gb_model = GradientBoostingPredictor()
    gb_model.fit(gb_features, gb_targets)
    gb_prediction = float(gb_model.predict(gb_features)[0])

    # 6. Momentum por equipo con serie histórica
    print("  🔄 Analizando momentum y forma reciente...")
    history_a = _history_to_metric_series(hist_a, team_a_id, processor)
    history_b = _history_to_metric_series(hist_b, team_b_id, processor)

    momentum_a = LSTMMomentumAnalyzer().analyze_momentum(history_a)
    momentum_b = LSTMMomentumAnalyzer().analyze_momentum(history_b)

    # 7. Poisson Bivariada para score exacto
    print("  🎯 Calculando matriz de resultados exactos...")
    poisson = BivariatePoissionModel()
    exact_score = poisson.predict_exact_score(
        team_a_goals=avg_a.get('goals', 1.2),
        team_b_goals=avg_b.get('goals', 1.1),
        max_goals=4,
    )

    # 8. Mercados de apuestas deportivos
    print("  💰 Generando mercados BTTS, remates al arco y corners...")
    team_a_conceded = avg_b.get('goals', 0)
    team_b_conceded = avg_a.get('goals', 0)

    btts = betting.calculate_btts_probability(
        team_a_goals_avg=avg_a.get('goals', 0),
        team_b_goals_avg=avg_b.get('goals', 0),
        team_a_conceded_avg=team_a_conceded,
        team_b_conceded_avg=team_b_conceded,
    )

    shots = betting.calculate_shots_on_target_market(
        team_a_sot=avg_a.get('shots_on_target', 0),
        team_b_sot=avg_b.get('shots_on_target', 0),
    )

    corners = betting.calculate_corners_market(
        team_a_corners=avg_a.get('corners', 0),
        team_b_corners=avg_b.get('corners', 0),
    )

    combined = betting.combine_markets(shots, corners, btts)

    # ============= SALIDA FORMATEADA =============
    _print_section_header("📋 RESUMEN EJECUTIVO")
    
    result_score = exact_score.get('most_likely_score', 'N/A')
    print(f"\n  Resultado más probable:        {result_score}")
    print(f"  Proyección total de goles:     {predictions.get('goals', {}).get('projection_total', 'N/A'):.2f}")
    print(f"  Probabilidad BTTS:             {_format_percentage(btts.get('btts_yes', 0))}")
    print(f"  Mercado fuerte:                {combined.get('strongest_market', 'N/A')}")
    print(f"  Nivel de riesgo:               {combined.get('risk_level', 'N/A')}")
    print(f"  Recomendación BTTS:            {btts.get('btts_recommendation', 'N/A')}")

    # ============= PREDICCIÓN PRINCIPAL =============
    _print_section_header("🎯 PREDICCIÓN PRINCIPAL - GOLES")
    
    goals_data = predictions.get('goals', {})
    print(f"\n  Campo                          │ Valor")
    print(f"  {'─' * 76}")
    print(f"  Proyección total               │ {goals_data.get('projection_total', 'N/A'):.2f} goles")
    print(f"  Máximo por equipo              │ {goals_data.get('projection_max', 'N/A'):.2f} goles")
    print(f"  Línea segura UNDER             │ < {goals_data.get('safe_under_line', 'N/A'):.2f}")
    print(f"  Línea segura OVER              │ > {goals_data.get('safe_over_line', 'N/A'):.2f}")

    # ============= TOP 3 RESULTADOS =============
    _print_section_header("🏆 TOP 3 RESULTADOS MÁS PROBABLES")
    
    top_scores = exact_score.get('top_3_scores', [])
    print(f"\n  Posición │ Resultado │ Probabilidad")
    print(f"  {'─' * 76}")
    for idx, score_data in enumerate(top_scores, 1):
        score = score_data.get('score', 'N/A')
        prob = score_data.get('probability', 0)
        print(f"      {idx}    │    {score:^7}   │ {_format_percentage(prob)}")

    # ============= MERCADO DE REMATES =============
    _print_section_header("🎾 MERCADO DE REMATES AL ARCO (SHOTS ON TARGET)")
    
    shots_data = shots
    print(f"\n  Métrica                        │ Valor")
    print(f"  {'─' * 76}")
    print(f"  Total proyectado               │ {shots_data.get('shots_on_target_total', 'N/A'):.2f}")
    print(f"  Máximo por equipo              │ {shots_data.get('shots_on_target_max', 'N/A'):.2f}")
    print(f"  Remates {team_a_name:<17}       │ {shots_data.get('team_a_shots', 'N/A'):.2f}")
    print(f"  Remates {team_b_name:<17}       │ {shots_data.get('team_b_shots', 'N/A'):.2f}")
    print(f"  Línea principal                │ {shots_data.get('main_line', 'N/A'):.2f}")
    print(f"  Línea segura UNDER             │ {shots_data.get('safe_under_line', 'N/A'):.2f}")
    print(f"  Línea segura OVER              │ {shots_data.get('safe_over_line', 'N/A'):.2f}")

    # ============= MERCADO DE CORNERS =============
    _print_section_header("⚽ MERCADO DE CORNERS")
    
    corners_data = corners
    print(f"\n  Métrica                        │ Valor")
    print(f"  {'─' * 76}")
    print(f"  Total proyectado               │ {corners_data.get('corners_total', 'N/A'):.2f}")
    print(f"  Máximo por equipo              │ {corners_data.get('corners_max', 'N/A'):.2f}")
    print(f"  Corners {team_a_name:<17}       │ {corners_data.get('team_a_corners', 'N/A'):.2f}")
    print(f"  Corners {team_b_name:<17}       │ {corners_data.get('team_b_corners', 'N/A'):.2f}")
    print(f"  Línea principal                │ {corners_data.get('total_main_line', 'N/A'):.2f}")
    print(f"  Línea segura UNDER             │ {corners_data.get('total_safe_under', 'N/A'):.2f}")
    print(f"  Línea segura OVER              │ {corners_data.get('total_safe_over', 'N/A'):.2f}")
    print(f"  Tendencia                      │ {corners_data.get('corners_trend', 'Moderado')}")

    # ============= BTTS (AMBOS EQUIPOS ANOTAN) =============
    _print_section_header("🔄 BTTS - AMBOS EQUIPOS ANOTAN")
    
    print(f"\n  Métrica                        │ Valor")
    print(f"  {'─' * 76}")
    print(f"  BTTS YES                       │ {_format_percentage(btts.get('btts_yes', 0))}")
    print(f"  BTTS NO                        │ {_format_percentage(btts.get('btts_no', 0))}")
    print(f"  Recomendación                  │ {btts.get('btts_recommendation', 'N/A')}")
    print(f"  Confianza                      │ {btts.get('btts_confidence', 'N/A')}/10")
    print(f"  Probabilidad {team_a_name:<14} │ {_format_percentage(btts.get('team_a_score_prob', 0))}")
    print(f"  Probabilidad {team_b_name:<14} │ {_format_percentage(btts.get('team_b_score_prob', 0))}")

    # ============= MOMENTUM Y FORMA =============
    _print_section_header("📊 MOMENTUM Y FORMA RECIENTE")
    
    _print_subsection(f"{team_a_name}")
    if isinstance(momentum_a, dict):
        print(f"    Momentum Score:        {momentum_a.get('momentum_score', 'N/A')}")
        print(f"    Tendencia:             {momentum_a.get('momentum_direction', 'N/A')}")
        print(f"    Forma Reciente:        {momentum_a.get('recent_form', 'N/A')}")
        print(f"    Recomendación:         {momentum_a.get('recommendation', 'N/A')}")
        print(f"    Trend Goles:           {momentum_a.get('goals_trend', 'N/A')}")
        print(f"    Trend Remates:         {momentum_a.get('sot_trend', 'N/A')}")
        print(f"    Trend Corners:         {momentum_a.get('corners_trend', 'N/A')}")
        print(f"    Volatilidad:           {momentum_a.get('goals_volatility', 'N/A'):.3f}")
    else:
        print(f"    {momentum_a}")

    _print_subsection(f"{team_b_name}")
    if isinstance(momentum_b, dict):
        print(f"    Momentum Score:        {momentum_b.get('momentum_score', 'N/A')}")
        print(f"    Tendencia:             {momentum_b.get('momentum_direction', 'N/A')}")
        print(f"    Forma Reciente:        {momentum_b.get('recent_form', 'N/A')}")
        print(f"    Recomendación:         {momentum_b.get('recommendation', 'N/A')}")
        print(f"    Trend Goles:           {momentum_b.get('goals_trend', 'N/A')}")
        print(f"    Trend Remates:         {momentum_b.get('sot_trend', 'N/A')}")
        print(f"    Trend Corners:         {momentum_b.get('corners_trend', 'N/A')}")
        print(f"    Volatilidad:           {momentum_b.get('goals_volatility', 'N/A'):.3f}")
    else:
        print(f"    {momentum_b}")

    # ============= MODELO GRADIENT BOOSTING =============
    _print_section_header("🤖 MODELO GRADIENT BOOSTING AJUSTADO")
    print(f"\n  Predicción GB:                 {gb_prediction:.2f}")

    # ============= EVALUACIÓN DE RIESGO =============
    _print_section_header("⚠️  EVALUACIÓN DE RIESGO")
    print(f"\n  Nivel de Riesgo:               {combined.get('risk_level', 'N/A')}")
    print(f"  Motivo:                        Líneas {'precisas' if 'precisas' in str(combined.get('risk_level', '')) else 'imprecisas'}")
    print(f"  Mercado Fuerte:                {combined.get('strongest_market', 'N/A')}")

    # ============= CONCLUSIÓN FINAL =============
    _print_section_header("✅ CONCLUSIÓN FINAL")
    print(f"\n  Resultado más probable:        {result_score}")
    print(f"  Proyección total de goles:     {predictions.get('goals', {}).get('projection_total', 'N/A'):.2f}")
    print(f"  BTTS Recomendación:            {btts.get('btts_recommendation', 'N/A')}")
    print(f"  Mercado fuerte:                {combined.get('strongest_market', 'N/A')}")
    print(f"  Riesgo:                        {combined.get('risk_level', 'N/A')}")
    
    print(f"\n{'█' * 80}\n")

    return {
        "match": {
            "home_team": team_a_name,
            "away_team": team_b_name,
            "date": match_date,
        },
        "base_predictions": predictions,
        "gb_prediction": round(gb_prediction, 2),
        "momentum": {
            team_a_name: momentum_a,
            team_b_name: momentum_b,
        },
        "markets": combined,
        "exact_score": exact_score,
    }


if __name__ == "__main__":
    M_ID = os.getenv('MATCH_ID')
    if not M_ID or M_ID == '0':
        print("Error: Debes proporcionar un MATCH_ID.")
    else:
        run_pipeline(M_ID)

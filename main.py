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


def run_pipeline(match_id):
    print(f"--- Iniciando Proyección Automática para Match ID: {match_id} ---")

    client = FootballDataClient()
    processor = DataProcessor()
    model = PredictionModel()
    betting = BettingMarkets()

    # 1. Obtener detalles del partido
    print("Obteniendo detalles del partido...")
    response = client.get_match_details(match_id)
    if not response:
        print("Error: No se pudo obtener la respuesta de la API.")
        return

    match_data = response.get('data', response)

    team_a_id = match_data.get('home_team', {}).get('id')
    team_b_id = match_data.get('away_team', {}).get('id')
    team_a_name = match_data.get('home_team', {}).get('name', 'Local')
    team_b_name = match_data.get('away_team', {}).get('name', 'Visitante')
    match_date = match_data.get('utc_date', '').split('T')[0]

    if not team_a_id or not team_b_id:
        print("❌ Error: No se pudieron identificar los IDs de los equipos.")
        return

    print(f"✅ Partido: {team_a_name} vs {team_b_name} ({match_date})")

    # 2. Obtener historial
    print("\nRecopilando estadísticas históricas detalladas...")
    hist_a = client.get_historical_team_data(team_a_id, match_date)
    hist_b = client.get_historical_team_data(team_b_id, match_date)

    # 3. Calcular promedios de métricas
    print(f"Procesando {len(hist_a)} partidos de {team_a_name} y {len(hist_b)} de {team_b_name}...")
    avg_a = processor.calculate_averages(hist_a, team_a_id)
    avg_b = processor.calculate_averages(hist_b, team_b_id)

    if not avg_a or not avg_b:
        print("❌ Error: No se pudieron calcular promedios suficientes.")
        return

    # 4. Proyección base del modelo existente
    print("Ejecutando modelo base...")
    features = processor.prepare_features(avg_a, avg_b)
    predictions = model.predict_market(features)

    # 5. Gradient Boosting para ajustar la línea final
    print("Ejecutando Gradient Boosting...")
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
    print("Analizando momentum y forma reciente...")
    history_a = _history_to_metric_series(hist_a, team_a_id, processor)
    history_b = _history_to_metric_series(hist_b, team_b_id, processor)

    momentum_a = LSTMMomentumAnalyzer().analyze_momentum(history_a)
    momentum_b = LSTMMomentumAnalyzer().analyze_momentum(history_b)

    # 7. Poisson Bivariada para score exacto
    print("Calculando matriz de resultados exactos...")
    poisson = BivariatePoissionModel()
    exact_score = poisson.predict_exact_score(
        team_a_goals=avg_a.get('goals', 1.2),
        team_b_goals=avg_b.get('goals', 1.1),
        max_goals=4,
    )

    # 8. Mercados de apuestas deportivos
    print("Generando mercados BTTS, remates al arco y corners...")
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

    print(f"\n{'=' * 60}")
    print(f" PROYECCIÓN FINAL: {team_a_name} vs {team_b_name}")
    print(f"{'=' * 60}")

    for market, data in predictions.items():
        print(f"\nMercado: {market.upper()}")
        print(f"  - Proyección Total: {data['projection_total']}")
        print(f"  - Proyección Máximo Equipo: {data['projection_max']}")
        print(f"  - Línea segura (UNDER): < {data['safe_under_line']}")
        print(f"  - Línea segura (OVER): > {data['safe_over_line']}")

    print(f"\nGradient Boosting ajustado: {gb_prediction:.2f}")
    print(f"Momentum {team_a_name}: {momentum_a}")
    print(f"Momentum {team_b_name}: {momentum_b}")
    print(f"\nBTTS: {btts}")
    print(f"Remates al arco: {shots}")
    print(f"Corners: {corners}")
    print(f"Mercado fuerte: {combined['strongest_market']}")
    print(f"Riesgo: {combined['risk_level']}")
    print(f"\nScore exacto más probable: {exact_score['most_likely_score']}")
    print(f"Top scores: {exact_score['top_3_scores']}")

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

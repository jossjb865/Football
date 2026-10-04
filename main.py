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


def _build_final_markets(predictions, shots, corners, exact_score, gb_prediction, momentum_a, momentum_b):
    """Combina evidencia de los modelos y entrega solo 2 mercados finales."""
    goals_data = predictions.get('goals', {})
    corners_data = corners

    momentum_score_a = momentum_a.get('momentum_score', 50)
    momentum_score_b = momentum_b.get('momentum_score', 50)
    avg_momentum = (momentum_score_a + momentum_score_b) / 2.0

    total_expected_goals = exact_score.get('total_expected_goals', 0)
    draw_prob = exact_score.get('draw_prob', 0)

    goals_market = {
        "market": "GOALS",
        "projection_total": round(float(goals_data.get('projection_total', 0.0)), 2),
        "projection_max": round(float(goals_data.get('projection_max', 0.0)), 2),
        "safe_under_line": round(float(goals_data.get('safe_under_line', 0.0)), 2),
        "safe_over_line": round(float(goals_data.get('safe_over_line', 0.0)), 2),
        "confidence": "Alta" if gb_prediction > 1.0 else "Media",
        "evidence": [
            f"GB ajustado: {gb_prediction:.2f}",
            f"Poisson total esperado: {total_expected_goals:.2f}",
            f"Empate más probable: {draw_prob:.2%}",
            f"Momentum promedio: {avg_momentum:.0f}",
        ],
    }

    corners_market = {
        "market": "CORNERS",
        "projection_total": round(float(corners_data.get('corners_total', 0.0)), 2),
        "projection_max": round(float(corners_data.get('corners_max', 0.0)), 2),
        "safe_under_line": round(float(corners_data.get('total_safe_under', 0.0)), 2),
        "safe_over_line": round(float(corners_data.get('total_safe_over', 0.0)), 2),
        "confidence": "Alta" if corners_data.get('corners_total', 0) >= 7 else "Media",
        "evidence": [
            f"Ajuste de mercado: {corners_data.get('corners_trend', 'Moderado')}",
            f"Momentum equipo A: {momentum_score_a}",
            f"Momentum equipo B: {momentum_score_b}",
            f"Remates al arco total: {shots.get('shots_on_target_total', 0.0):.2f}",
        ],
    }

    return [goals_market, corners_market]


def run_pipeline(match_id):
    print(f"\n{'=' * 80}")
    print(f" PROYECCIÓN AUTOMÁTICA - MATCH ID: {match_id}")
    print(f"{'=' * 80}")

    client = FootballDataClient()
    processor = DataProcessor()
    model = PredictionModel()
    betting = BettingMarkets()

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
        print("Error: No se pudieron identificar los IDs de los equipos.")
        return

    print(f"Partido: {team_a_name} vs {team_b_name} ({match_date})")

    print("Recopilando historial...")
    hist_a = client.get_historical_team_data(team_a_id, match_date)
    hist_b = client.get_historical_team_data(team_b_id, match_date)

    avg_a = processor.calculate_averages(hist_a, team_a_id)
    avg_b = processor.calculate_averages(hist_b, team_b_id)

    if not avg_a or not avg_b:
        print("Error: No se pudieron calcular promedios suficientes.")
        return

    features = processor.prepare_features(avg_a, avg_b)
    predictions = model.predict_market(features)

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

    print("Analizando momentum...")
    history_a = _history_to_metric_series(hist_a, team_a_id, processor)
    history_b = _history_to_metric_series(hist_b, team_b_id, processor)
    momentum_a = LSTMMomentumAnalyzer().analyze_momentum(history_a)
    momentum_b = LSTMMomentumAnalyzer().analyze_momentum(history_b)

    print("Calculando score exacto...")
    poisson = BivariatePoissionModel()
    exact_score = poisson.predict_exact_score(
        team_a_goals=avg_a.get('goals', 1.2),
        team_b_goals=avg_b.get('goals', 1.1),
        max_goals=4,
    )

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

    final_markets = _build_final_markets(
        predictions=predictions,
        shots=shots,
        corners=corners,
        exact_score=exact_score,
        gb_prediction=gb_prediction,
        momentum_a=momentum_a,
        momentum_b=momentum_b,
    )

    print(f"\n{'=' * 60}")
    print(" MERCADOS FINALES (2)")
    print(f"{'=' * 60}")
    for market in final_markets:
        print(f"\nMercado: {market['market']}")
        print(f"  - Proyección Total: {market['projection_total']}")
        print(f"  - Proyección Máximo Equipo: {market['projection_max']}")
        print(f"  - Línea segura (UNDER): < {market['safe_under_line']}")
        print(f"  - Línea segura (OVER): > {market['safe_over_line']}")
        print(f"  - Confianza: {market['confidence']}")
        print(f"  - Evidencia: {', '.join(market['evidence'])}")

    print(f"\nResultado más probable: {exact_score['most_likely_score']}")
    print(f"BTTS: {btts.get('btts_recommendation')} | {btts.get('btts_yes')} / {btts.get('btts_no')}")
    print(f"Mercado fuerte: {combined['strongest_market']}")
    print(f"Riesgo: {combined['risk_level']}")

    return {
        "match": {
            "home_team": team_a_name,
            "away_team": team_b_name,
            "date": match_date,
        },
        "final_markets": final_markets,
        "exact_score": exact_score,
        "btts": btts,
        "strongest_market": combined['strongest_market'],
        "risk_level": combined['risk_level'],
    }


if __name__ == "__main__":
    M_ID = os.getenv('MATCH_ID')
    if not M_ID or M_ID == '0':
        print("Error: Debes proporcionar un MATCH_ID.")
    else:
        run_pipeline(M_ID)

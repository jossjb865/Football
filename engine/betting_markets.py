"""
Módulo especializado para mercados de apuestas deportivas.
Calcula probabilidades basadas en historial de partidos para:
- BTTS (Both Teams To Score / Ambos Equipos Anotan)
- Remates al Arco (Shots On Target)
- Corners (Total y por equipo)
"""

import math
from typing import Dict, List, Optional, Tuple

class BettingMarkets:
    """Calcula líneas de apuesta profesionales con probabilidades."""
    
    def __init__(self):
        # Factores de ajuste basados en patrones históricos
        self.btts_confidence_threshold = 0.55  # 55% para marcar apuesta segura
        self.shot_variance_factor = 0.15  # Factor de variación para remates
        self.corner_stability_factor = 1.2  # Multiplicador para estabilidad de corners
    
    def calculate_btts_probability(self, team_a_goals_avg: float, 
                                   team_b_goals_avg: float,
                                   team_a_conceded_avg: Optional[float] = None,
                                   team_b_conceded_avg: Optional[float] = None) -> Dict:
        """
        Calcula probabilidad de BTTS (ambos equipos anotan).
        
        Args:
            team_a_goals_avg: Promedio de goles marcados por equipo A
            team_b_goals_avg: Promedio de goles marcados por equipo B
            team_a_conceded_avg: Promedio de goles recibidos por equipo A (opcional)
            team_b_conceded_avg: Promedio de goles recibidos por equipo B (opcional)
            
        Returns:
            Dict con probabilidad BTTS y línea de apuesta recomendada
        """
        # Probabilidad simple: ambos anotan al menos 1 gol
        prob_a_scores = min(1.0, max(0.0, team_a_goals_avg / 1.5))
        prob_b_scores = min(1.0, max(0.0, team_b_goals_avg / 1.5))
        
        # Ajuste defensivo si hay datos de goles recibidos
        if team_a_conceded_avg is not None:
            prob_b_scores *= (team_a_conceded_avg / 1.2)  # Más defensivos = menos goles en contra
            prob_b_scores = min(1.0, prob_b_scores)
            
        if team_b_conceded_avg is not None:
            prob_a_scores *= (team_b_conceded_avg / 1.2)
            prob_a_scores = min(1.0, prob_a_scores)
        
        # Probabilidad conjunta (multiplicativa)
        btts_probability = prob_a_scores * prob_b_scores
        
        return {
            "btts_yes": round(btts_probability, 3),
            "btts_no": round(1.0 - btts_probability, 3),
            "btts_recommendation": "SI" if btts_probability >= self.btts_confidence_threshold else "NO",
            "btts_confidence": round(abs(btts_probability - 0.5) * 2 * 100, 1),  # 0-100%
            "team_a_score_prob": round(prob_a_scores, 3),
            "team_b_score_prob": round(prob_b_scores, 3)
        }
    
    def calculate_shots_on_target_market(self, team_a_sot: float, 
                                        team_b_sot: float,
                                        team_a_accuracy: Optional[float] = None,
                                        team_b_accuracy: Optional[float] = None) -> Dict:
        """
        Calcula líneas de apuesta para remates al arco.
        
        Args:
            team_a_sot: Promedio de remates al arco equipo A
            team_b_sot: Promedio de remates al arco equipo B
            team_a_accuracy: Precisión de remates (%), opcional
            team_b_accuracy: Precisión de remates (%), opcional
            
        Returns:
            Dict con proyecciones y líneas seguras para remates
        """
        total_shots = team_a_sot + team_b_sot
        max_shots = max(team_a_sot, team_b_sot)
        
        # Variación en remates al arco
        variance = total_shots * self.shot_variance_factor
        
        # Líneas conservadoras
        safe_under = math.floor((total_shots - variance) * 2) / 2
        safe_over = math.ceil((total_shots + variance) * 2) / 2
        
        # Línea principal (sin varianza)
        main_line = round(total_shots, 1)
        
        return {
            "shots_on_target_total": round(total_shots, 2),
            "shots_on_target_max": round(max_shots, 2),
            "team_a_shots": round(team_a_sot, 2),
            "team_b_shots": round(team_b_sot, 2),
            "main_line": main_line,
            "safe_under_line": max(0.0, safe_under),
            "safe_over_line": safe_over,
            "line_spread": round(safe_over - safe_under, 1),
            "accuracy_edge": self._calculate_accuracy_edge(team_a_accuracy, team_b_accuracy) if team_a_accuracy else None
        }
    
    def calculate_corners_market(self, team_a_corners: float,
                                team_b_corners: float) -> Dict:
        """
        Calcula líneas de apuesta profesionales para corners.
        Ofrece líneas totales y por equipo.
        
        Args:
            team_a_corners: Promedio de corners equipo A
            team_b_corners: Promedio de corners equipo B
            
        Returns:
            Dict con líneas de apuesta para corners
        """
        total_corners = team_a_corners + team_b_corners
        max_corners = max(team_a_corners, team_b_corners)
        
        # Corners tienen menos variabilidad que otros mercados
        variance = total_corners * 0.08  # 8% variance para corners
        
        # Líneas de apuesta profesionales
        safe_under = math.floor((total_corners - variance) * 2) / 2
        safe_over = math.ceil((total_corners + variance) * 2) / 2
        main_line = round(total_corners, 1)
        
        # Líneas individuales por equipo
        team_a_main = round(team_a_corners, 1)
        team_b_main = round(team_b_corners, 1)
        
        return {
            "corners_total": round(total_corners, 2),
            "corners_max": round(max_corners, 2),
            "team_a_corners": round(team_a_corners, 2),
            "team_b_corners": round(team_b_corners, 2),
            "total_main_line": main_line,
            "total_safe_under": max(0.0, safe_under),
            "total_safe_over": safe_over,
            "team_a_main_line": team_a_main,
            "team_b_main_line": team_b_main,
            "corners_trend": self._analyze_corners_trend(total_corners)
        }
    
    def combine_markets(self, shots_data: Dict, corners_data: Dict, 
                       btts_data: Dict) -> Dict:
        """
        Combina todos los mercados en un resumen integrado.
        
        Returns:
            Dict consolidado con todos los mercados y recomendaciones
        """
        return {
            "btts_market": btts_data,
            "shots_on_target_market": shots_data,
            "corners_market": corners_data,
            "strongest_market": self._identify_strongest_market(shots_data, corners_data, btts_data),
            "risk_level": self._calculate_risk_level(shots_data, corners_data, btts_data)
        }
    
    @staticmethod
    def _calculate_accuracy_edge(team_a_acc: Optional[float], 
                                 team_b_acc: Optional[float]) -> Optional[str]:
        """Determina ventaja de precisión entre equipos."""
        if not (team_a_acc and team_b_acc):
            return None
        
        diff = abs(team_a_acc - team_b_acc)
        if diff > 10:
            winner = "A" if team_a_acc > team_b_acc else "B"
            return f"Equipo {winner} con +{diff:.1f}% precisión"
        return "Precisión equilibrada"
    
    @staticmethod
    def _analyze_corners_trend(total_corners: float) -> str:
        """Analiza tendencia de corners según volumen."""
        if total_corners < 5:
            return "Muy bajo (< 5)"
        elif total_corners < 8:
            return "Bajo (5-8)"
        elif total_corners < 11:
            return "Moderado (8-11)"
        elif total_corners < 15:
            return "Alto (11-15)"
        else:
            return "Muy alto (> 15)"
    
    @staticmethod
    def _identify_strongest_market(shots_data: Dict, corners_data: Dict, 
                                   btts_data: Dict) -> str:
        """Identifica el mercado con mayor claridad de línea."""
        # Mercado más confiable es el que tiene menor spread
        shots_spread = shots_data.get("line_spread", float('inf'))
        corners_spread = corners_data["total_safe_over"] - corners_data["total_safe_under"]
        btts_confidence = btts_data.get("btts_confidence", 0)
        
        if btts_confidence > 70:
            return "BTTS"
        elif shots_spread < corners_spread:
            return "Remates al Arco"
        else:
            return "Corners"
    
    @staticmethod
    def _calculate_risk_level(shots_data: Dict, corners_data: Dict, 
                             btts_data: Dict) -> str:
        """Calcula nivel de riesgo general del partido."""
        shots_spread = shots_data.get("line_spread", 0)
        corners_spread = corners_data["total_safe_over"] - corners_data["total_safe_under"]
        btts_confidence = btts_data.get("btts_confidence", 50)
        
        avg_spread = (shots_spread + corners_spread) / 2
        
        if avg_spread > 3 or btts_confidence < 40:
            return "ALTO - Líneas imprecisas"
        elif avg_spread > 1.5 or btts_confidence < 55:
            return "MODERADO - Patrón mixto"
        else:
            return "BAJO - Líneas claras"

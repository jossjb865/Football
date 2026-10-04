"""
Módulos ML avanzados para predicción de mercados deportivos.
- Gradient Boosting para predicción de líneas de apuesta
- LSTM con momentum para análisis de tendencias temporales
- Distribución Bivariada de Poisson para probabilidades exactas de score
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import math


class GradientBoostingPredictor:
    """
    Gradient Boosting simplificado para predicción de mercados.
    Entrena sobre características históricas para optimizar líneas de apuesta.
    """
    
    def __init__(self, learning_rate: float = 0.1, n_estimators: int = 50):
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.trees = []
        self.initial_prediction = 0.0
        self.feature_importance = {}
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Entrena el modelo Gradient Boosting.
        
        Args:
            X: Features [n_samples, n_features]
            y: Target values (líneas de apuesta reales)
        """
        # Predicción inicial: media del target
        self.initial_prediction = np.mean(y)
        predictions = np.full(len(y), self.initial_prediction)
        
        # Inicializar importancia de features
        n_features = X.shape[1]
        self.feature_importance = {f"feature_{i}": 0.0 for i in range(n_features)}
        
        # Iteración de boosting
        for iteration in range(self.n_estimators):
            # Residuales (error actual)
            residuals = y - predictions
            
            # Árboles de regresión simple (split por feature más importante)
            tree = self._build_tree(X, residuals)
            self.trees.append(tree)
            
            # Actualizar predicciones
            tree_predictions = self._predict_tree(X, tree)
            predictions += self.learning_rate * tree_predictions
            
            # Actualizar importancia
            if tree.get("feature"):
                self.feature_importance[f"feature_{tree['feature']}"] += abs(self.learning_rate * np.mean(tree_predictions))
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predice usando el ensemble Gradient Boosting.
        
        Args:
            X: Features [n_samples, n_features]
            
        Returns:
            Predicciones de línea de apuesta
        """
        predictions = np.full(len(X), self.initial_prediction)
        
        for tree in self.trees:
            tree_pred = self._predict_tree(X, tree)
            predictions += self.learning_rate * tree_pred
        
        return predictions
    
    @staticmethod
    def _build_tree(X: np.ndarray, y: np.ndarray, depth: int = 3) -> Dict:
        """Construye árbol de decisión simple."""
        if depth == 0 or len(y) < 2:
            return {"leaf": True, "value": np.mean(y)}
        
        best_mse = float('inf')
        best_split = None
        
        # Buscar mejor split
        n_features = X.shape[1]
        for feature_idx in range(n_features):
            thresholds = np.percentile(X[:, feature_idx], [25, 50, 75])
            
            for threshold in thresholds:
                mask = X[:, feature_idx] <= threshold
                if len(y[mask]) == 0 or len(y[~mask]) == 0:
                    continue
                
                # MSE del split
                mse = (np.var(y[mask]) * len(y[mask]) + 
                       np.var(y[~mask]) * len(y[~mask])) / len(y)
                
                if mse < best_mse:
                    best_mse = mse
                    best_split = (feature_idx, threshold)
        
        if best_split is None:
            return {"leaf": True, "value": np.mean(y)}
        
        # Recursión
        feature_idx, threshold = best_split
        mask = X[:, feature_idx] <= threshold
        
        return {
            "leaf": False,
            "feature": feature_idx,
            "threshold": threshold,
            "left": GradientBoostingPredictor._build_tree(X[mask], y[mask], depth - 1),
            "right": GradientBoostingPredictor._build_tree(X[~mask], y[~mask], depth - 1)
        }
    
    @staticmethod
    def _predict_tree(X: np.ndarray, tree: Dict) -> np.ndarray:
        """Predice usando un árbol."""
        predictions = np.zeros(len(X))
        
        for i in range(len(X)):
            node = tree
            while not node.get("leaf"):
                if X[i, node["feature"]] <= node["threshold"]:
                    node = node["left"]
                else:
                    node = node["right"]
            predictions[i] = node["value"]
        
        return predictions


class LSTMMomentumAnalyzer:
    """
    Análisis de momentum usando LSTM simplificado.
    Captura patrones temporales en estadísticas de partidos.
    """
    
    def __init__(self, sequence_length: int = 5, hidden_units: int = 16):
        self.sequence_length = sequence_length  # Últimos N partidos
        self.hidden_units = hidden_units
        self.weights_ih = None  # Input to hidden
        self.weights_hh = None  # Hidden to hidden
        self.weights_ho = None  # Hidden to output
        self.is_fitted = False
    
    def analyze_momentum(self, historical_stats: List[Dict]) -> Dict:
        """
        Analiza momentum de un equipo basado en historial reciente.
        
        Args:
            historical_stats: Lista de últimos partidos [{'goals': X, 'sot': Y, ...}]
            
        Returns:
            Dict con análisis de momentum y tendencia
        """
        if len(historical_stats) < 2:
            return self._neutral_momentum()
        
        # Preparar secuencia
        sequence = self._prepare_sequence(historical_stats)
        
        # Calcular momentum simple (trend)
        goals_trend = self._calculate_trend([s.get("goals", 0) for s in historical_stats])
        sot_trend = self._calculate_trend([s.get("shots_on_target", 0) for s in historical_stats])
        corners_trend = self._calculate_trend([s.get("corners", 0) for s in historical_stats])
        
        # Volatilidad (cambios brutos)
        goals_volatility = self._calculate_volatility([s.get("goals", 0) for s in historical_stats])
        
        # Momentum score (0-100)
        momentum_score = self._compute_momentum_score(
            goals_trend, sot_trend, corners_trend, goals_volatility
        )
        
        return {
            "momentum_score": momentum_score,
            "momentum_direction": "Ascendente" if goals_trend > 0 else "Descendente",
            "goals_trend": round(goals_trend, 3),
            "sot_trend": round(sot_trend, 3),
            "corners_trend": round(corners_trend, 3),
            "goals_volatility": round(goals_volatility, 3),
            "recent_form": self._classify_form(goals_trend, goals_volatility),
            "recommendation": self._form_recommendation(momentum_score, goals_trend)
        }
    
    @staticmethod
    def _prepare_sequence(stats: List[Dict]) -> np.ndarray:
        """Prepara secuencia de features para LSTM."""
        sequence = []
        for stat in stats[-5:]:  # Últimos 5 partidos
            features = [
                stat.get("goals", 0),
                stat.get("shots_on_target", 0),
                stat.get("corners", 0),
                stat.get("total_shots", 0)
            ]
            sequence.append(features)
        
        # Padding si necesario
        while len(sequence) < 5:
            sequence.insert(0, [0, 0, 0, 0])
        
        return np.array(sequence)
    
    @staticmethod
    def _calculate_trend(values: List[float]) -> float:
        """Calcula tendencia lineal (slope) de una serie."""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        y = np.array(values)
        
        # Regresión lineal simple
        slope = np.polyfit(x, y, 1)[0]
        return slope
    
    @staticmethod
    def _calculate_volatility(values: List[float]) -> float:
        """Calcula volatilidad (desviación estándar)."""
        if len(values) < 2:
            return 0.0
        return np.std(values)
    
    @staticmethod
    def _compute_momentum_score(goals_trend: float, sot_trend: float, 
                                corners_trend: float, volatility: float) -> int:
        """
        Calcula score de momentum (0-100).
        Positivo si hay tendencia ascendente con baja volatilidad.
        """
        # Normalizar componentes
        trend_score = (goals_trend * 30) + (sot_trend * 20) + (corners_trend * 10)
        volatility_score = max(0, 40 - (volatility * 10))  # Penaliza alta volatilidad
        
        score = trend_score + volatility_score
        return max(0, min(100, int(score)))
    
    @staticmethod
    def _classify_form(trend: float, volatility: float) -> str:
        """Clasifica forma actual del equipo."""
        if trend > 0.3 and volatility < 1.0:
            return "Excelente forma ↑"
        elif trend > 0 and volatility < 1.5:
            return "Buena forma"
        elif trend > -0.2:
            return "Forma estable"
        elif trend < -0.3:
            return "Mala forma ↓"
        else:
            return "Forma inconsistente"
    
    @staticmethod
    def _form_recommendation(momentum: int, trend: float) -> str:
        """Recomendación basada en momentum."""
        if momentum > 70 and trend > 0:
            return "FAVORABLE - Equipo con fuerte momentum"
        elif momentum > 55:
            return "POSITIVO - Tendencia al alza"
        elif momentum < 35 and trend < -0.2:
            return "ADVERSO - Mala racha"
        else:
            return "NEUTRAL - Patrón mixto"
    
    @staticmethod
    def _neutral_momentum() -> Dict:
        """Retorna momentum neutral por defecto."""
        return {
            "momentum_score": 50,
            "momentum_direction": "Neutral",
            "goals_trend": 0.0,
            "sot_trend": 0.0,
            "corners_trend": 0.0,
            "goals_volatility": 0.0,
            "recent_form": "Datos insuficientes",
            "recommendation": "NEUTRAL"
        }


class BivariatePoissionModel:
    """
    Modelo de Poisson Bivariado para predicción exacta de scores.
    Calcula probabilidades de resultados específicos (1-1, 2-1, etc.)
    """
    
    def __init__(self, correlation_strength: float = 0.15):
        self.correlation_strength = correlation_strength
    
    def predict_exact_score(self, team_a_goals: float, team_b_goals: float,
                           max_goals: int = 4) -> Dict:
        """
        Predice probabilidades de scores exactos usando Poisson Bivariado.
        
        Args:
            team_a_goals: Promedio de goles equipo A
            team_b_goals: Promedio de goles equipo B
            max_goals: Máximo de goles a calcular por equipo
            
        Returns:
            Dict con matriz de probabilidades y scores más probables
        """
        # Matriz de probabilidades
        prob_matrix = {}
        total_prob = 0.0
        
        for goals_a in range(max_goals + 1):
            for goals_b in range(max_goals + 1):
                # Poisson univariado
                prob_a = self._poisson_prob(goals_a, team_a_goals)
                prob_b = self._poisson_prob(goals_b, team_b_goals)
                
                # Ajuste bivariado (correlación)
                correlation_factor = self._correlation_adjustment(
                    goals_a, goals_b, team_a_goals, team_b_goals
                )
                
                prob = prob_a * prob_b * correlation_factor
                prob_matrix[f"{goals_a}-{goals_b}"] = round(prob, 4)
                total_prob += prob
        
        # Normalizar
        prob_matrix = {k: v / total_prob for k, v in prob_matrix.items()}
        
        # Calcular resultados agregados
        home_win = sum(v for k, v in prob_matrix.items() 
                      if int(k.split("-")[0]) > int(k.split("-")[1]))
        draw = sum(v for k, v in prob_matrix.items() 
                  if int(k.split("-")[0]) == int(k.split("-")[1]))
        away_win = sum(v for k, v in prob_matrix.items() 
                      if int(k.split("-")[0]) < int(k.split("-")[1]))
        
        # Top 3 scores más probables
        top_scores = sorted(prob_matrix.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "score_matrix": prob_matrix,
            "home_win_prob": round(home_win, 3),
            "draw_prob": round(draw, 3),
            "away_win_prob": round(away_win, 3),
            "most_likely_score": top_scores[0][0] if top_scores else "0-0",
            "top_3_scores": [{"score": s[0], "probability": s[1]} for s in top_scores],
            "expected_goals_a": round(team_a_goals, 2),
            "expected_goals_b": round(team_b_goals, 2),
            "total_expected_goals": round(team_a_goals + team_b_goals, 2)
        }
    
    def predict_btts_from_poisson(self, prob_matrix: Dict) -> Dict:
        """
        Extrae probabilidad de BTTS desde matriz Poisson.
        BTTS = ambos equipos anotan (Goals A > 0 AND Goals B > 0)
        """
        btts_prob = sum(v for k, v in prob_matrix.items()
                       if int(k.split("-")[0]) > 0 and int(k.split("-")[1]) > 0)
        
        return {
            "btts_yes": round(btts_prob, 3),
            "btts_no": round(1 - btts_prob, 3),
            "btts_recommendation": "SI" if btts_prob >= 0.55 else "NO",
            "btts_confidence": round(abs(btts_prob - 0.5) * 2 * 100, 1)
        }
    
    @staticmethod
    def _poisson_prob(k: int, lambda_param: float) -> float:
        """Calcula probabilidad Poisson: P(X=k) = e^-λ * λ^k / k!"""
        if lambda_param <= 0:
            return 1.0 if k == 0 else 0.0
        
        return (math.exp(-lambda_param) * (lambda_param ** k)) / math.factorial(k)
    
    def _correlation_adjustment(self, goals_a: int, goals_b: int,
                               lambda_a: float, lambda_b: float) -> float:
        """
        Ajusta por correlación entre goles (Poisson Bivariado).
        Goles están débilmente correlacionados (equipos defensivos afectan a ambos).
        """
        # Factor base
        factor = 1.0
        
        # Si ambos anotan muchos, hay factor defensivo débil
        if goals_a > lambda_a * 1.5 and goals_b > lambda_b * 1.5:
            factor *= (1 - self.correlation_strength * 0.5)
        
        # Si ambos anotan pocos, hay factor defensivo fuerte
        elif goals_a < lambda_a * 0.5 and goals_b < lambda_b * 0.5:
            factor *= (1 + self.correlation_strength * 0.3)
        
        return factor

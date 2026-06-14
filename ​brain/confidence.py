# ==========================================================
# FSE CONFIDENCE ENGINE (CORE)
# ==========================================================

class ConfidenceEngine:
    """
    Calculates how reliable a signal is.
    Output: 0.0 → 1.0
    """

    def evaluate(self, analysis, ml_score=0.5, history_score=0.5):
        volatility = analysis.get("volatility", 100)
        liquidity = analysis.get("liquidity", "LOW")
        structure = analysis.get("structure", "BEARISH")

        score = 0.5  # base confidence

        # --------------------------
        # VOLATILITY PENALTY
        # --------------------------
        if volatility < 10:
            score -= 0.2
        elif volatility > 15:
            score += 0.2

        # --------------------------
        # LIQUIDITY BOOST
        # --------------------------
        if liquidity == "HIGH":
            score += 0.2
        elif liquidity == "LOW":
            score -= 0.2

        # --------------------------
        # STRUCTURE ALIGNMENT
        # --------------------------
        if structure == "BULLISH":
            score += 0.1
        else:
            score += 0.05

        # --------------------------
        # ML + HISTORY FACTOR
        # --------------------------
        score += (ml_score * 0.2)
        score += (history_score * 0.2)

        # clamp 0–1
        if score > 1:
            score = 1
        if score < 0:
            score = 0

        return round(score, 3)

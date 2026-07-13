class DrowsinessAnalyzer:

    def __init__(self):

        self.score = 0

    def analyze(
        self,
        eyes_closed,
        closed_duration,
        blink_count,
        head_direction,
        is_yawning,
        yawn_count
    ):

        score = 0

        # -----------------------------
        # Eye state
        # -----------------------------

        if eyes_closed:
            score += 25

        if closed_duration > 1.0:
            score += 30

        if closed_duration > 2.5:
            score += 35

        # -----------------------------
        # Head direction
        # -----------------------------

        if head_direction in ["LEFT", "RIGHT"]:
            score += 35

        elif head_direction == "DOWN":
            score += 40

        elif head_direction == "UP":
            score += 25

        # -----------------------------
        # Yawning
        # -----------------------------

        if is_yawning:
            score += 40

        if yawn_count >= 2:
            score += 10

        # -----------------------------
        # Limit score
        # -----------------------------

        score = min(
            score,
            100
        )

        # -----------------------------
        # Instant status
        # -----------------------------

        if score >= 70:
            status = "DROWSY"

        elif score >= 40:
            status = "WARNING"

        else:
            status = "NORMAL"

        self.score = score

        return status, score
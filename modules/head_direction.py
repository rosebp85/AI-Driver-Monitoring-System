class HeadDirectionClassifier:

    def classify(
        self,
        yaw,
        pitch
    ):

        if yaw > 20:
            return "LEFT"

        elif yaw < -20:
            return "RIGHT"

        elif pitch > 15:
            return "DOWN"

        elif pitch < -15:
            return "UP"

        else:
            return "CENTER"
import time
import winsound


class AlertManager:

    def __init__(self):

        self.history = []

        self.WINDOW_SECONDS = 3.0

        self.WARNING_AVG_THRESHOLD = 25
        self.DROWSY_AVG_THRESHOLD = 55

        self.active_alert = None
        self.alarm_playing = False

        self.ALARM_PATH = "assets/beep.wav"

    def update(
        self,
        score
    ):

        current_time = time.time()

        self.history.append(
            (
                current_time,
                score
            )
        )

        self.history = [
            item for item in self.history
            if current_time - item[0] <= self.WINDOW_SECONDS
        ]

        if len(self.history) == 0:

            average_score = 0

        else:

            total_score = sum(
                item[1] for item in self.history
            )

            average_score = total_score / len(self.history)

        if average_score >= self.DROWSY_AVG_THRESHOLD:

            self.active_alert = "DROWSY ALERT"

            if not self.alarm_playing:

                winsound.PlaySound(
                    self.ALARM_PATH,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )

                self.alarm_playing = True

        elif average_score >= self.WARNING_AVG_THRESHOLD:

            self.active_alert = "WARNING ALERT"

            if self.alarm_playing:

                winsound.PlaySound(
                    None,
                    winsound.SND_PURGE
                )

                self.alarm_playing = False

        else:

            self.active_alert = None

            if self.alarm_playing:

                winsound.PlaySound(
                    None,
                    winsound.SND_PURGE
                )

                self.alarm_playing = False

        return (
            self.active_alert,
            average_score
        )
import time
import winsound


class DriverBehavior:

    def __init__(self):

        self.history = []

        self.WINDOW_SECONDS = 10.0

        self.HEAD_WARNING_SECONDS = 3.0
        self.EYES_DROWSY_SECONDS = 2.0
        self.YAWN_WARNING_COUNT = 2

        self.active_alert = None
        self.status = "NORMAL"

        self.alarm_playing = False
        self.ALARM_PATH = "assets/beep.wav"

    def update(
        self,
        eyes_closed,
        head_direction,
        is_yawning
    ):

        current_time = time.time()

        self.history.append(
            {
                "time": current_time,
                "eyes_closed": eyes_closed,
                "head_direction": head_direction,
                "is_yawning": is_yawning
            }
        )

        self.history = [
            item for item in self.history
            if current_time - item["time"] <= self.WINDOW_SECONDS
        ]

        eye_closed_time = 0
        head_off_road_time = 0
        yawn_count = 0

        for i in range(1, len(self.history)):

            prev = self.history[i - 1]
            curr = self.history[i]

            dt = curr["time"] - prev["time"]

            if prev["eyes_closed"]:
                eye_closed_time += dt

            if prev["head_direction"] != "CENTER":
                head_off_road_time += dt

            if curr["is_yawning"] and not prev["is_yawning"]:
                yawn_count += 1

        if eye_closed_time >= self.EYES_DROWSY_SECONDS:

            self.status = "DROWSY"
            self.active_alert = "DROWSY ALERT"

            if not self.alarm_playing:

                winsound.PlaySound(
                    self.ALARM_PATH,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )

                self.alarm_playing = True

        elif (
            head_off_road_time >= self.HEAD_WARNING_SECONDS
            or yawn_count >= self.YAWN_WARNING_COUNT
        ):

            self.status = "WARNING"
            self.active_alert = "WARNING ALERT"

            if self.alarm_playing:

                winsound.PlaySound(
                    None,
                    winsound.SND_PURGE
                )

                self.alarm_playing = False

        else:

            self.status = "NORMAL"
            self.active_alert = None

            if self.alarm_playing:

                winsound.PlaySound(
                    None,
                    winsound.SND_PURGE
                )

                self.alarm_playing = False

        return {
            "status": self.status,
            "alert": self.active_alert,
            "eye_closed_time": eye_closed_time,
            "head_off_road_time": head_off_road_time,
            "yawn_count": yawn_count
        }
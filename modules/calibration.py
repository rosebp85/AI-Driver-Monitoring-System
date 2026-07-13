class HeadCalibration:

    def __init__(self):

        self.yaw_values = []
        self.pitch_values = []

        self.center_yaw = 0
        self.center_pitch = 0

        self.max_frames = 60
        self.finished = False

    def update(
        self,
        yaw,
        pitch
    ):

        if self.finished:
            return

        self.yaw_values.append(yaw)
        self.pitch_values.append(pitch)

        if len(self.yaw_values) >= self.max_frames:

            self.center_yaw = sum(
                self.yaw_values
            ) / len(self.yaw_values)

            self.center_pitch = sum(
                self.pitch_values
            ) / len(self.pitch_values)

            self.finished = True

    def normalize(
        self,
        yaw,
        pitch
    ):

        yaw -= self.center_yaw
        pitch -= self.center_pitch

        return yaw, pitch
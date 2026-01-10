import math
import random

import glfw
from simple_pid import PID

from viewer import Viewer

MJCF_PATH = "assets/inverted_pendulum.xml"

CAMERA_CONFIG = {
    "distance": 1.0,
    "azimuth": 180.0,
    "elevation": -30.0,
    "lookat": [0.0, 0.0, 0.1],
}


class InvertedPendulumViewer(Viewer):
    RF_DISTANCE = 0.01
    WHEEL_RADIUS = 0.02
    DT = 0.005
    VELOCITY = 1.0

    def __init__(self, *args, **kwargs):
        super().__init__(mjcf_path=MJCF_PATH, camera_config=CAMERA_CONFIG, title="InvertedPendulum", *args, **kwargs)
        self.attitude_controller = PID(5, 1, 1, setpoint=0, sample_time=self.DT)
        self.position_controller = PID(20, 0, 5, setpoint=0, sample_time=self.DT)
        self.target_pos = 0.0

    def get_attitude(self):
        f = self.data.sensor("front").data[0]
        b = self.data.sensor("back").data[0]
        if f == -1:
            th = -0.5 * math.pi
        elif b == -1:
            th = 0.5 * math.pi
        else:
            th = math.atan2(b - f, self.RF_DISTANCE)
        return th

    def get_position(self):
        enc = -self.data.sensor("encoder").data[0]
        return 2 * enc * self.WHEEL_RADIUS

    def _key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_RIGHT:
            self.target_pos += self.VELOCITY * self.DT
        elif key == glfw.KEY_LEFT:
            self.target_pos -= self.VELOCITY * self.DT
        else:
            super()._key_callback(window, key, scancode, action, mods)

        self.position_controller.setpoint = self.target_pos

    def _callback(self):
        th = self.get_attitude()
        torque_at = self.attitude_controller(th)

        x = self.get_position()
        torque_pos = self.position_controller(x)

        self.data.ctrl[0] = torque_at + torque_pos

        self.data.ctrl[1] = random.uniform(-0.1, 0.1)

    def _create_overlay(self):
        super()._create_overlay()

        self.add_overlay(self.TOPLEFT, "Move Inverted Pendulum", "[Right] / [Left] Arrow")


if __name__ == "__main__":
    viewer = InvertedPendulumViewer()
    viewer()

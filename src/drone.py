import glfw
import numpy as np
from simple_pid import PID

from viewer import Viewer

MJCF_PATH = "assets/drone.xml"

CAMERA_CONFIG = {
    "distance": 5.0,
    "azimuth": 180.0,
    "elevation": -30.0,
    "lookat": [0, 0.0, 0.75],
}

GRAVITY = 9.8


class DroneViewer(Viewer):
    MASS = 1.0
    NUM_THRUST = 4
    STABLE_FORCE = MASS * GRAVITY / NUM_THRUST
    TARGET_ACC = 4.0

    hovering = True

    def __init__(self, *args, **kwargs):
        super().__init__(mjcf_path=MJCF_PATH, camera_config=CAMERA_CONFIG, title="Drone", *args, **kwargs)
        self.force = np.full(self.NUM_THRUST, self.STABLE_FORCE)
        self.target_pos = np.array([0.0, 0.0, 0.0])
        dt = 0.005
        self.controller = PID(10, 0.1, 0.05, setpoint=0, sample_time=dt)

    def set_force(self, force):
        for i in range(4):
            self.data.ctrl[i] = force[i]

    def _key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_UP and action != glfw.RELEASE:
            self.hovering = False
            force = self.STABLE_FORCE + self.TARGET_ACC * self.MASS / self.NUM_THRUST
            self.force = np.full(self.NUM_THRUST, force)
        elif key == glfw.KEY_DOWN and action != glfw.RELEASE:
            self.hovering = False
            force = self.STABLE_FORCE - self.TARGET_ACC * self.MASS / self.NUM_THRUST
            self.force = np.full(self.NUM_THRUST, force)
        else:
            self.hovering = True
            super()._key_callback(window, key, scancode, action, mods)

    def _callback(self):
        if self.hovering:
            z_vel = self.data.sensor("body_vel").data[2]
            force = self.controller(z_vel)
            self.force = np.full(self.NUM_THRUST, force + self.STABLE_FORCE)
        else:
            self.controller.reset()

        self.set_force(self.force)

    def _create_overlay(self):
        super()._create_overlay()

        self.add_overlay(self.TOPLEFT, "[Up] / [Down]", "")


if __name__ == "__main__":
    viewer = DroneViewer()
    viewer()

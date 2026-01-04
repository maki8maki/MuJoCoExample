import glfw
import numpy as np
from simple_pid import PID

from viewer import Viewer

MJCF_PATH = "assets/omni.xml"

CAMERA_CONFIG = {
    "distance": 5.0,
    "azimuth": 180.0,
    "elevation": -30.0,
    "lookat": [0, 0.0, 0.75],
}


class OmniViewer(Viewer):
    DT = 0.005

    def __init__(self, *args, **kwargs):
        super().__init__(mjcf_path=MJCF_PATH, camera_config=CAMERA_CONFIG, title="Omni", *args, **kwargs)
        self.th = 0.0
        self.forces = np.zeros((4,))
        self.vel_controllers = [PID(10, 0, 1, setpoint=0, sample_time=self.DT) for _ in range(4)]

    def update_state(self):
        self.th += self.DT * self.data.sensor("gyro").data[2]

    def calc_force(self, force, global_dir):
        local_dir = global_dir - self.th
        force_x = force * np.cos(local_dir)
        force_y = force * np.sin(local_dir)
        self.forces = np.array([force_x, force_y, -force_x, -force_y]).reshape(4)

    def set_force(self):
        for i in range(4):
            if abs(self.forces[i]) < 1e-9:
                self.data.ctrl[i] = self.vel_controllers[i](self.data.sensor(f"wheel_{i}").data[0])
            else:
                self.data.ctrl[i] = self.forces[i]

    def _key_callback(self, window, key, scancode, action, mods):
        if action in [glfw.PRESS, glfw.REPEAT]:
            FORCE = 2.0
        else:
            FORCE = 0.0
        if key == glfw.KEY_UP:
            # 前進
            self.calc_force(FORCE, 0.0)
        elif key == glfw.KEY_DOWN:
            # 後退
            self.calc_force(FORCE, np.pi)
        elif key == glfw.KEY_LEFT:
            # 左移動
            self.calc_force(FORCE, np.pi / 2)
        elif key == glfw.KEY_RIGHT:
            # 右移動
            self.calc_force(FORCE, -np.pi / 2)
        elif key == glfw.KEY_A:
            # 左回転
            self.forces = np.full_like(self.forces, FORCE)
        elif key == glfw.KEY_S:
            # 右回転
            self.forces = np.full_like(self.forces, -FORCE)
        else:
            super()._key_callback(window, key, scancode, action, mods)

    def _callback(self):
        self.update_state()
        self.set_force()

    def _create_overlay(self):
        super()._create_overlay()

        self.add_overlay(self.TOPLEFT, "Go Forward / Backword", "[Up] / [Down] Arrow")
        self.add_overlay(self.TOPLEFT, "Go Left / Right", "[Left] / [Right] Arrow")
        self.add_overlay(self.TOPLEFT, "Rotate Counterclockwise / Clockwise", "[A] / [S]")


if __name__ == "__main__":
    viewer = OmniViewer()
    viewer()

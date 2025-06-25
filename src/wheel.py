import glfw

from viewer import Viewer

MJCF_PATH = "assets/wheel.xml"

CAMERA_CONFIG = {
    "distance": 5.0,
    "azimuth": 180.0,
    "elevation": -30.0,
    "lookat": [0, 0.0, 0.75],
}


class WheelViewer(Viewer):
    def __init__(self, *args, **kwargs):
        super().__init__(mjcf_path=MJCF_PATH, camera_config=CAMERA_CONFIG, title="Wheel", *args, **kwargs)

    def _key_callback(self, window, key, scancode, action, mods):
        if action in [glfw.PRESS, glfw.REPEAT]:
            FORCE = 1.0
        else:
            FORCE = 0.0
        if key == glfw.KEY_UP:
            # 前進
            self.data.ctrl[0] = FORCE
            self.data.ctrl[1] = FORCE
        elif key == glfw.KEY_DOWN:
            # 後退
            self.data.ctrl[0] = -FORCE
            self.data.ctrl[1] = -FORCE
        elif key == glfw.KEY_LEFT:
            # 左回転
            self.data.ctrl[0] = -FORCE
            self.data.ctrl[1] = FORCE
        elif key == glfw.KEY_RIGHT:
            # 右回転
            self.data.ctrl[0] = FORCE
            self.data.ctrl[1] = -FORCE
        else:
            super()._key_callback(window, key, scancode, action, mods)

    def _create_overlay(self):
        super()._create_overlay()

        self.add_overlay(self.TOPLEFT, "Forward ([Up]) / Backword ([Down])", "")
        self.add_overlay(self.TOPLEFT, "[Left] / [Right] Rotation", "")


if __name__ == "__main__":
    viewer = WheelViewer()
    viewer()

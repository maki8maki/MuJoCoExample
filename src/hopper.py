import glfw

from viewer import Viewer

MJCF_PATH = "assets/hopper.xml"

CAMERA_CONFIG = {
    "distance": 2.5,
    "azimuth": 180.0,
    "elevation": -30.0,
    "lookat": [0, 0.0, 0.75],
}


class HopperViewer(Viewer):
    def __init__(self, *args, **kwargs):
        super().__init__(mjcf_path=MJCF_PATH, camera_config=CAMERA_CONFIG, title="Hopper", *args, **kwargs)

    def _key_callback(self, window, key, scancode, action, mods):
        FORCE = 100
        if key == glfw.KEY_UP:
            self.data.ctrl[0] = FORCE
        elif key == glfw.KEY_DOWN:
            self.data.ctrl[0] = -FORCE
        else:
            super()._key_callback(window, key, scancode, action, mods)

    def _create_overlay(self):
        super()._create_overlay()

        self.add_overlay(self.TOPLEFT, "[Up] / [Down] arrow", "")


viewer = HopperViewer()

viewer()

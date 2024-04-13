import sys

from engine import *

from scenes.test_scene import TestScene


def main() -> int:
    Game.init(name="LD55", version="v1")
    Engine.init_default()
    Window.init_default()
    Renderer.init_default()
    Input.init_default()
    scene = TestScene()
    Engine.start(scene)
    return 0


if __name__ == "__main__":
    with papp.crash_handler():
        sys.exit(main())

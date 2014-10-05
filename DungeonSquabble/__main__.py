from core import control

from consts import WINDOW_SIZE, DISPLAY_SIZE, FPS
from scenes import GameScene
import resources


def on_init():
    resources.init()


def main():
    gs = GameScene()
    control.run(gs, WINDOW_SIZE, DISPLAY_SIZE, fps=FPS, on_init=on_init)


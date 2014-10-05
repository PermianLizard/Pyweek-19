from core import control

from consts import WINDOW_SIZE, DISPLAY_SIZE
from scenes import GameScene


def main():
    gs = GameScene()
    control.run(gs, WINDOW_SIZE, DISPLAY_SIZE)


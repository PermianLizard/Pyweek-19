from core import control

from consts import DISPLAY_SIZE, DISPLAY_RESOLUTION
from scenes import GameScene


def main():
    gs = GameScene()
    control.run(gs, DISPLAY_SIZE, DISPLAY_RESOLUTION)


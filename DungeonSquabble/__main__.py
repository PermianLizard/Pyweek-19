from core import control

from DungeonSquabble.consts import TITLE, WINDOW_SIZE, DISPLAY_SIZE, FPS
from DungeonSquabble.scenes import GameScene
from DungeonSquabble import resources


def on_init():
    resources.init()


def main():
    gs = GameScene()
    control.run(gs, TITLE, WINDOW_SIZE, DISPLAY_SIZE, fps=FPS, on_init=on_init)


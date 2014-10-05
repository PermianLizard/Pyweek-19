from core import control
from core import director

from consts import DISPLAY_SIZE, DISPLAY_RESOLUTION
from scenes import GameScene

def main():
    """ your app starts here
    """

    gs = GameScene()

    control.run(gs, DISPLAY_SIZE, DISPLAY_RESOLUTION)

    #controller = Controller(DISPLAY_SIZE, DISPLAY_RESOLUTION)
    #controller.run(None)


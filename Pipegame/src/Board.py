import pygame
from src.constant import *
from src.Spritesheet import Spritesheet
from src.PipeManager import PipeManager
from src.PipeTile import PipeTile


class Board(pygame.sprite.Group):
    def __init__(self, hsize, vsize):
        pygame.sprite.Group.__init__(self)
        self.hsize, self.vsize = hsize, vsize
        self.tileSize = 64
        self.PipeManager = PipeManager()
        self.load()

    def load(self):
        self.pipeSpriteSheet = Spritesheet(os.path.join(IMAGES_PATH, "tileset_64.png"))

    def newGame(self):
        self.PipeManager.generate(self.hsize, self.vsize)
        self.PipeManager.scramble()
        self.PipeManager.light()
        pieces = self.PipeManager.pieces
        self.empty()
        for x in range(self.hsize):
            for y in range(self.vsize):
                self.add(PipeTile(x, y, pieces[x][y], self.pipeSpriteSheet))

    def update(self):
        pygame.sprite.Group.update(
            self, self.PipeManager.pieces, self.PipeManager.states
        )

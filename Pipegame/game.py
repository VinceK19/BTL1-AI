import pygame
from src.constant import *
from src.Spritesheet import Spritesheet
from src.Board import Board
from src.Button import Button


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 18)
        self.canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
        self.window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))

        self.newGameButton = Button(
            DISPLAY_W - 100, 20, 100, 30, "NEW GAME", self.font, (255, 255, 255)
        )
        self.load()
        self.running = True

    def load(self):
        self.board = Board(5, 5)

    def run(self):
        while self.running:
            self.handleEvent()
            self.update()
            self.draw()

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if self.newGameButton.checkPressed():
            self.board.newGame()

    def update(self):
        self.board.update()

    def draw(self):
        self.window.blit(self.canvas, (0, 0))
        self.board.draw(self.window)
        self.newGameButton.draw(self.window)
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

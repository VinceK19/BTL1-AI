import pygame


class Button:
    def __init__(self, x, y, w, h, text, font: pygame.font.Font, color):
        self.font = font
        self.surface = pygame.Surface((w, h))
        self.surface.fill(color)
        self.textSurf = self.font.render(text, 1, (0, 0, 0))
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = (w // 2, h // 2)
        self.surface.blit(self.textSurf, self.textRect)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)

        self.clicked = False

    def draw(self, surface):
        surface.blit(self.surface, (self.rect.x, self.rect.y))

    def checkPressed(self):
        action = False
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        if self.rect.collidepoint(pos) and pressed[0] == 1 and self.clicked == False:
            self.clicked = True
            action = True
        if pressed[0] == 0:
            self.clicked = False

        return action

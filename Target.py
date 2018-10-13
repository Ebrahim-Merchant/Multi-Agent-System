import pygame
k=5
class Target:
    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.name = name
        self.color = color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    # draw the target
    def draw(self, screen):
        pygame.draw.rect(
            screen, self.color,
            [self.x - k * 1, self.y - k * 1, 2 * k * 1, 2 * k * 1])

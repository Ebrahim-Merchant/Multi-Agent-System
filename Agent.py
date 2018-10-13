import pygame

k=5
class Agent:
    def __init__(self, x, y, name, color,count_iter=0):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.count_iter = count_iter
        self.target_list = []

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def put_x(self, x):
        self.x = self.x + x

    def put_y(self, y):
        self.y = self.y + y

    def set_target(self, target):

        if target in self.target_list:
            return
        else:
            self.target_list.append(target)

    def get_target(self):
        

        if not self.target_list:
            return None
        else:
            return self.target_list[0]

    def get_target_2(self):
        
        return self.target_list

    def remove_target(self, target):
        
        if target in self.target_list:
            self.target_list.remove(target)
            return True
        else:
            return False


    # the function depicts the agent on the screen along with the flashing radar
    def draw(self, screen, radar):
        if radar:
            # draw the radar
            pygame.draw.ellipse(screen, self.color, [self.x - k * 10, self.y - k * 10, 2 * k * 10, 2 * k * 10], 1)
        # draw the agent
        pygame.draw.rect(screen, self.color, [self.x - k * 1, self.y - k * 1, 2 * k * 1, 2 * k * 1])
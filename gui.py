import pygame
from typing import Union

# Colors
white = (255, 255, 255)
red = (255, 114, 118)
orange = "#FFAB6E"
background = "#262626"
green = "#93bf85"


class GraphicElement(pygame.sprite.Sprite):
    def __init__(self, position: tuple, group: pygame.sprite.Group):
        super().__init__(group)
        self.position = pygame.math.Vector2(position)
        self.image: pygame.Surface
        self.rect: pygame.Rect

    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class RGBText(GraphicElement):
    def __init__(self, position: tuple, text, group: pygame.sprite.Group, font_size=50, font_path="monogram.ttf"):
        super().__init__(position, group)
        self.text = text
        self.font = pygame.font.Font(font_path, font_size)
        self.color = [120, 120, 240]
        self.colorDir = [-1, 1, 1]
        self.speed = 0.3

        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def change_color(self, color: list, direction: list):
        for i in range(3):
            color[i] += self.speed * direction[i]
            if color[i] >= 255 or color[i] <= 0:
                direction[i] *= -1

    def update(self):
        self.image = self.font.render(self.text, False, self.color)
        self.change_color(self.color, self.colorDir)


class SimpleText(GraphicElement):
    def __init__(self, position: tuple, text, group: pygame.sprite.Group, text_color=white, font_size=50,
                 font_path="monogram.ttf"):
        super().__init__(position, group)
        self.text = text
        self.color = text_color
        self.font = pygame.font.Font(font_path, font_size)
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def update(self):
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))


class InputBox(GraphicElement):
    def __init__(self, position: tuple, width: Union[int, float], height: Union[int, float],
                 group: pygame.sprite.Group, text="", text_color=white, font_size=50, font_path="monogram.ttf"):
        super().__init__(position, group)
        self.width = width
        self.height = height
        # Colors
        self.passive_color = white
        self.active_color = orange
        self.hover_color = red
        # Attributes
        self.text = text
        self.actual_color = self.passive_color

        self.font = pygame.font.Font(font_path, font_size)
        self.text_surface = self.font.render(text, False, text_color)
        self.active = False

        self.color_rect = pygame.Rect(0, 0, width, height)

        self.image = pygame.Surface((width, height))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, self.actual_color, self.color_rect, 2, 10)
        self.image.blit(self.text_surface, (13, 0))
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))

    def is_empty(self):
        return True if self.text == "" else False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if self.active:
            self.actual_color = self.active_color
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 4:
                    if event.unicode in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                        self.text += event.unicode
        else:
            self.actual_color = self.passive_color
        self.text_surface = self.font.render(self.text, True, self.passive_color)

    def update(self):
        if self.hover() and not self.active:
            self.actual_color = self.hover_color
        elif not self.hover() and not self.active:
            self.actual_color = self.passive_color
        # self.rect.w = max(260, self.text_surface.get_width() + 10)
        # self.rect.x = self.position.x - self.rect.w / 2

        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, self.actual_color, self.color_rect, 2, 10)
        text_rect = self.text_surface.get_rect(center=(self.rect.w / 2, self.rect.h / 2 - 3))
        self.image.blit(self.text_surface, text_rect)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))


class Button(GraphicElement):
    def __init__(self, position: tuple, group: pygame.sprite.Group):
        super().__init__(position, group)
        self.pressed = False


class TextButton(Button):
    def __init__(self, text: str, position: tuple, group: pygame.sprite.Group, colour=white, antialiasing=False,
                 background_color=None, font_path="monogram.ttf", font_size=50, hover_colour=red):
        super().__init__(position, group)
        # font
        self.font = pygame.font.Font(font_path, font_size)
        # text
        self.text = text
        self.image = self.font.render(text, antialiasing, colour, background_color)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.background = background_color
        self.text_aa = antialiasing

        self.text_colour = colour
        self.hover_colour = hover_colour
        self.actual_color = colour

    def update(self):
        if self.hover():
            self.actual_color = self.hover_colour
        else:
            self.actual_color = self.text_colour
        self.image = self.font.render(self.text, self.text_aa, self.actual_color, self.background)

    def check_click(self):
        action = False
        if self.hover():
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.pressed = True
                action = True

            if not pygame.mouse.get_pressed()[0]:
                self.pressed = False
        else:
            self.pressed = False
        return action


class Notification(GraphicElement):
    def __init__(self, pos: tuple, text: str, time: int, group: pygame.sprite.Group, text_color=green,
                 font_size=30, font_path="monogram.ttf"):
        super().__init__(pos, group)
        self.text = text
        self.font = pygame.font.Font(font_path, font_size)
        self.color = text_color
        self.image = self.font.render(self.text, False, self.color)
        self.rect = self.image.get_rect(center=(self.position.x, self.position.y))
        self.createTime = time
        self.duration = 3000

    def update(self):
        if pygame.time.get_ticks() - self.createTime > self.duration:
            self.kill()

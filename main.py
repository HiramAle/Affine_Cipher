import pygame
import ctypes
from gui import SimpleText, InputBox, TextButton, Notification, RGBText
from Affine import validate_alpha, extended_euclidean_algorithm

ctypes.windll.user32.SetProcessDPIAware()


class Window:
    def __init__(self):
        pygame.init()
        self.width = 720
        self.height = 720
        self.display = pygame.display.set_mode((self.width, self.height))
        self.mainPanel = pygame.Surface((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption("Affine")
        pygame.display.set_icon(pygame.image.load("player_icon.png").convert_alpha())
        # ---------- Graphic Elements ----------
        self.components = pygame.sprite.Group()
        self.notifications = pygame.sprite.Group()

        self.title = RGBText((self.mainPanel.get_width() / 2, 100), "Affine cipher", self.components, font_size=60)
        SimpleText((self.mainPanel.get_width() / 2 - 200, 200), "Alpha", self.components)
        SimpleText((self.mainPanel.get_width() / 2, 200), "Beta", self.components)
        SimpleText((self.mainPanel.get_width() / 2 + 200, 200), "n", self.components)

        self.equation = SimpleText((self.mainPanel.get_width() / 2, 450), "", self.components)
        self.inverse = SimpleText((self.mainPanel.get_width() / 2, 550), "", self.components)

        self.ibAlpha = InputBox((self.mainPanel.get_width() / 2 - 200, 250), 100, 50, self.components)
        self.ibBeta = InputBox((self.mainPanel.get_width() / 2, 250), 100, 50, self.components)
        self.ibN = InputBox((self.mainPanel.get_width() / 2 + 200, 250), 100, 50, self.components)

        self.btnCalculate = TextButton("Calculate", (self.mainPanel.get_width() / 2, 350), self.components)

        self.colors = [[120, 120, 240]]
        self.colorDir = [[-1, 1, 1]]

        self.font = pygame.font.Font("monogram.ttf", 60)

    def draw(self):
        # Background
        self.mainPanel.fill("#262626")
        self.components.draw(self.mainPanel)
        self.notifications.draw(self.mainPanel)
        self.display.blit(self.mainPanel, (0, 0))
        pygame.display.update()

    def update(self):
        self.components.update()
        self.notifications.update()

        if self.btnCalculate.check_click():
            if self.ibAlpha.is_empty() or self.ibN.is_empty() or self.ibBeta.is_empty():
                Notification((self.width - 100, (len(self.notifications) * 30) + 50), "> Fill al boxes",
                             pygame.time.get_ticks(), self.notifications)
                self.equation.text = ""
                self.inverse.text = ""
                return

            a = int(self.ibAlpha.text)
            b = int(self.ibBeta.text)
            n = int(self.ibN.text)

            if not validate_alpha(a, n):
                Notification((self.width - 100, (len(self.notifications) * 30) + 50), "> Alpha not valid",
                             pygame.time.get_ticks(), self.notifications)
                self.equation.text = ""
                self.inverse.text = ""
                return

            inverse = extended_euclidean_algorithm(a, n)[1] % n

            self.equation.text = f"{a}x + {b} mod {n}"
            self.inverse.text = f"Inverse of {a} mod {n} = {inverse}"

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()

            self.ibAlpha.handle_event(event)
            self.ibBeta.handle_event(event)
            self.ibN.handle_event(event)

    def run(self):
        while self.running:
            self.event_loop()
            self.update()
            self.draw()


if __name__ == '__main__':
    Window().run()

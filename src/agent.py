import random
import pygame
import config as cfg

class Agent:
    def __init__(self, state = 'S'):
        self.state = state
        self.x = random.randint(0, cfg.SCREEN_WIDTH)
        self.y = random.randint(0, cfg.SCREEN_HEIGHT)
        self.vx = random.uniform(-cfg.AGENT_SPEED, cfg.AGENT_SPEED)
        self.vy = random.uniform(-cfg.AGENT_SPEED, cfg.AGENT_SPEED)
        self.infection_time = 0
        self.pulse = 0


    def update_infection(self):
        if self.state == 'I':
            self.infection_time += 1
            if self.infection_time > 300:
                self.state = 'R'

    def move(self):
        self.x += self.vx 
        self.y += self.vy

        # Odbicie od ścian (granice ekranu)
        if self.x - cfg.AGENT_RADIUS < 0:  # Lewa ściana
            self.x = cfg.AGENT_RADIUS  # Ustaw pozycję na granicy
            self.vx = -self.vx + random.uniform(
                -1, 1
            )  # Zmień kierunek na przeciwny
        elif self.x + cfg.AGENT_RADIUS > cfg.SCREEN_WIDTH:  # Prawa ściana
            self.x = cfg.SCREEN_WIDTH - cfg.AGENT_RADIUS
            self.vx = -self.vx + random.uniform(-1, 1)

        if self.y - cfg.AGENT_RADIUS < 0:  # Górna ściana
            self.y = cfg.AGENT_RADIUS
            self.vy = -self.vy + random.uniform(-1, 1)
        elif self.y + cfg.AGENT_RADIUS > cfg.SCREEN_HEIGHT:  # Dolna ściana
            self.y = cfg.SCREEN_HEIGHT - cfg.AGENT_RADIUS
            self.vy = -self.vy + random.uniform(-1, 1)

    def draw(self, screen):
        color = (0, 255, 0) if self.state == 'S' else (255, 0, 0) if self.state == 'I' else (0, 0, 255)
        pygame.draw.circle(screen, color, (self.x, self.y), cfg.AGENT_RADIUS)

        if self.state == "I":
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (int(self.x), int(self.y)),
                cfg.INFECTION_RADIUS,
                1,
            )

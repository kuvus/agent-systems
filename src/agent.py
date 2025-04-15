import random
import pygame
import config as cfg

class Agent:
    def __init__(self, sim_width: int, sim_height: int, state: str = "S"):
        self.sim_width = sim_width
        self.sim_height = sim_height
        self.state = state
        self.x = random.randint(cfg.AGENT_RADIUS, self.sim_width - cfg.AGENT_RADIUS)
        self.y = random.randint(cfg.AGENT_RADIUS, self.sim_height - cfg.AGENT_RADIUS)
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

        if self.x - cfg.AGENT_RADIUS < 0:
            self.x = cfg.AGENT_RADIUS 
            self.vx = -self.vx + random.uniform(
                -1, 1
            ) 
        elif self.x + cfg.AGENT_RADIUS > cfg.SCREEN_WIDTH: 
            self.x = cfg.SCREEN_WIDTH - cfg.AGENT_RADIUS
            self.vx = -self.vx + random.uniform(-1, 1)

        if self.y - cfg.AGENT_RADIUS < 0:
            self.y = cfg.AGENT_RADIUS
            self.vy = -self.vy + random.uniform(-1, 1)
        elif self.y + cfg.AGENT_RADIUS > cfg.SCREEN_HEIGHT:
            self.y = cfg.SCREEN_HEIGHT - cfg.AGENT_RADIUS
            self.vy = -self.vy + random.uniform(-1, 1)

    def draw(self, sim_surface: pygame.Surface):
        color = (0, 255, 0) if self.state == 'S' else (255, 0, 0) if self.state == 'I' else (0, 0, 255)
        pygame.draw.circle(sim_surface, color, (self.x, self.y), cfg.AGENT_RADIUS)

        if self.state == "I":
            pygame.draw.circle(
                sim_surface,
                (255, 0, 0),
                (int(self.x), int(self.y)),
                cfg.INFECTION_RADIUS,
                1,
            )

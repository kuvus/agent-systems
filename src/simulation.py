import random
from agent import Agent
from sir import SIRModel
import config as cfg

class Simulation:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.agents = [Agent(width, height, state="I" if i < cfg.INITIAL_INFECTED else "S") for i in range(cfg.POPULATION_SIZE)]
        self.sir_model = SIRModel(cfg.POPULATION_SIZE, cfg.BETA, cfg.GAMMA, cfg.INITIAL_INFECTED)

    def update(self):
        self.sir_model.update()

        S, I, R = self.sir_model.get_counts()

        for agent in self.agents:
            agent.move()

            if agent.state == 'S' and I > 0:
                for other in self.agents:
                    if other.state == 'I' and self.is_in_infection_radius(agent, other):
                        if random.random() < cfg.BETA:
                            agent.state = 'I'
                            break

            # agent.update_infection()

            elif agent.state == 'I' and R > 0:
                if random.random() < cfg.GAMMA:
                    agent.state = 'R'

    def is_in_infection_radius(self, agent1: Agent, agent2: Agent):
        distance = (
            (agent1.x - agent2.x) ** 2 + (agent1.y - agent2.y) ** 2
        ) ** 0.5
        return distance < cfg.INFECTION_RADIUS

    def count_states(self):
        S = sum(1 for agent in self.agents if agent.state == "S")
        I = sum(1 for agent in self.agents if agent.state == "I")
        R = sum(1 for agent in self.agents if agent.state == "R")
        return S, I, R

    def draw(self, screen):
        for agent in self.agents:
            agent.draw(screen)

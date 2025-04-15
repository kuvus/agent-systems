class SIRModel:
    def __init__(self, population_size: int, beta: float, gamma: float, initial_infected: int):
        self.population_size = population_size
        self.beta = beta
        self.gamma = gamma
        self.S = population_size - initial_infected
        self.I = initial_infected
        self.R = 0

    def update(self, dt=1):
        dS = -self.beta * self.S * self.I / self.population_size
        dI = self.beta * self.S * self.I / self.population_size - self.gamma * self.I
        dR = self.gamma * self.I

        self.S += dS * dt
        self.I += dI * dt
        self.R += dR * dt

        self.S = max(0, self.S)
        self.I = max(0, self.I)
        self.R = max(0, self.R)

    def get_counts(self):
        return int(self.S), int(self.I), int(self.R)
        
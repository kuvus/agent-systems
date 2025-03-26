import pygame
import config as cfg
from simulation import Simulation
from sir import SIRModel
import matplotlib.pyplot as plt

def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    simulation = Simulation()

    plt.ion()
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    time_steps = []
    S_data_sim, I_data_sim, R_data_sim = [], [], []
    S_data_sir, I_data_sir, R_data_sir = [], [], []

    running = True
    t = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulation.update()



        S_sim, I_sim, R_sim = simulation.count_states()
        time_steps.append(t)
        S_data_sim.append(S_sim)
        I_data_sim.append(I_sim)
        R_data_sim.append(R_sim)

        # Pobieranie danych z globalnego modelu SIR
        S_sir, I_sir, R_sir = simulation.sir_model.get_counts()
        S_data_sir.append(S_sir)
        I_data_sir.append(I_sir)
        R_data_sir.append(R_sir)

        if t % 30 == 0:

            axes[0].clear()
            axes[1].clear()

            # # Wykres dla symulacji agentowej
            axes[0].plot(time_steps, S_data_sim, label="Zdrowi (Symulacja)", color="green")
            axes[0].plot(time_steps, I_data_sim, label="Chorzy (Symulacja)", color="red")
            axes[0].plot(time_steps, R_data_sim, label="Odporni (Symulacja)", color="blue")
            axes[0].set_title("Symulacja Agentowa")
            axes[0].set_xlabel("Czas")
            axes[0].set_ylabel("Liczba osób")
            axes[0].legend(loc="upper right")

            # # Wykres dla globalnego modelu SIR
            axes[1].plot(time_steps, S_data_sir, label="Zdrowi (Model SIR)", color="green", linestyle="--")
            axes[1].plot(time_steps, I_data_sir, label="Chorzy (Model SIR)", color="red", linestyle="--")
            axes[1].plot(time_steps, R_data_sir, label="Odporni (Model SIR)", color="blue", linestyle="--")
            axes[1].set_title("Model SIR")
            axes[1].set_xlabel("Czas")
            axes[1].set_ylabel("Liczba osób")
            axes[1].legend(loc="upper right")

            # Wyświetlenie wykresów
            # plt.tight_layout()
            plt.pause(0.01)

        screen.fill((0, 0, 0))
        simulation.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        t += 1

    pygame.quit()
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()

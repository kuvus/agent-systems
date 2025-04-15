import pygame
import config as cfg
from simulation import Simulation
from sir import SIRModel
import matplotlib.pyplot as plt
import os
import config as cfg


def draw_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    text: str,
    font: pygame.font.Font,
    button_color: tuple[int, int, int],
    text_color: tuple[int, int, int],
):
    pygame.draw.rect(screen, button_color, rect, border_radius=5)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    pygame.display.set_caption("Symulacja epidemii")
    clock = pygame.time.Clock()

    sim_surface = pygame.Surface((cfg.SIM_AREA_WIDTH, cfg.SIM_AREA_HEIGHT))

    simulation = Simulation(cfg.SIM_AREA_WIDTH, cfg.SIM_AREA_HEIGHT)

    simulation_state = "idle"

    button_font = pygame.font.Font(None, 24)
    total_button_width = 2 * cfg.BUTTON_WIDTH + cfg.BUTTON_PADDING
    start_button_x = (cfg.SCREEN_WIDTH - total_button_width) // 2
    reset_button_x = start_button_x + cfg.BUTTON_WIDTH + cfg.BUTTON_PADDING

    start_button_rect = pygame.Rect(
        start_button_x, cfg.BUTTON_Y, cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT
    )
    reset_button_rect = pygame.Rect(
        reset_button_x, cfg.BUTTON_Y, cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT
    )

    time_steps = []
    S_data_sim, I_data_sim, R_data_sim = [], [], []
    S_data_sir, I_data_sir, R_data_sir = [], [], []

    running = True
    t = 0
    while running:
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        start_hover = start_button_rect.collidepoint(mouse_pos)
        reset_hover = reset_button_rect.collidepoint(mouse_pos)

        if clicked:
            if start_hover and simulation_state == "idle":
                simulation_state = "running"
                print("Simulation started")
            elif reset_hover:
                simulation_state = "idle"
                simulation = Simulation(cfg.SIM_AREA_WIDTH, cfg.SIM_AREA_HEIGHT)
                time_steps = []
                S_data_sim, I_data_sim, R_data_sim = [], [], []
                S_data_sir, I_data_sir, R_data_sir = [], [], []
                t = 0
                print("Simulation reset")

        if simulation_state == "running":

            simulation.update()

            S_sim, I_sim, R_sim = simulation.count_states()
            time_steps.append(t)
            S_data_sim.append(S_sim)
            I_data_sim.append(I_sim)
            R_data_sim.append(R_sim)

            if hasattr(simulation, "sir_model"):
                S_sir, I_sir, R_sir = simulation.sir_model.get_counts()
                S_data_sir.append(S_sir)
                I_data_sir.append(I_sir)
                R_data_sir.append(R_sir)
            else:
                S_data_sir.append(0)
                I_data_sir.append(0)
                R_data_sir.append(0)

            if cfg.SHOW_PLOTS:
                print("Generowanie wykresów...")

                plt.ion()
                fig, axes = plt.subplots(1, 2, figsize=(12, 6))

                if t % 30 == 0:

                    axes[0].clear()
                    axes[1].clear()

                    axes[0].plot(
                        time_steps,
                        S_data_sim,
                        label="Zdrowi (Symulacja)",
                        color="green",
                    )
                    axes[0].plot(
                        time_steps,
                        I_data_sim,
                        label="Chorzy (Symulacja)",
                        color="red",
                    )
                    axes[0].plot(
                        time_steps,
                        R_data_sim,
                        label="Odporni (Symulacja)",
                        color="blue",
                    )
                    axes[0].set_title("Symulacja Agentowa")
                    axes[0].set_xlabel("Czas")
                    axes[0].set_ylabel("Liczba osób")
                    axes[0].legend(loc="upper right")

                    if S_data_sir:
                        axes[1].plot(
                            time_steps,
                            S_data_sir,
                            label="Zdrowi (Model SIR)",
                            color="green",
                            linestyle="--",
                        )
                        axes[1].plot(
                            time_steps,
                            I_data_sir,
                            label="Chorzy (Model SIR)",
                            color="red",
                            linestyle="--",
                        )
                        axes[1].plot(
                            time_steps,
                            R_data_sir,
                            label="Odporni (Model SIR)",
                            color="blue",
                            linestyle="--",
                        )
                        axes[1].set_title("Model SIR")
                        axes[1].set_xlabel("Czas")
                        axes[1].set_ylabel("Liczba osób")
                        axes[1].legend(loc="upper right")
                    else:
                        axes[1].set_title("Model SIR (brak danych)")

                    plt.pause(0.01)

        screen.fill(cfg.BACKGROUND_COLOR)

        sim_surface.fill(cfg.SIM_AREA_COLOR)
        simulation.draw(sim_surface)
        screen.blit(sim_surface, (cfg.SIM_AREA_X, cfg.SIM_AREA_Y))

        sim_area_rect = pygame.Rect(
            cfg.SIM_AREA_X,
            cfg.SIM_AREA_Y,
            cfg.SIM_AREA_WIDTH,
            cfg.SIM_AREA_HEIGHT,
        )
        pygame.draw.rect(screen, (0, 0, 0), sim_area_rect, 2)

        start_color = (
            cfg.BUTTON_HOVER_COLOR if start_hover else cfg.BUTTON_COLOR
        )
        reset_color = (
            cfg.BUTTON_HOVER_COLOR if reset_hover else cfg.BUTTON_COLOR
        )
        draw_button(
            screen,
            start_button_rect,
            "Start",
            button_font,
            start_color,
            cfg.TEXT_COLOR,
        )
        draw_button(
            screen,
            reset_button_rect,
            "Reset",
            button_font,
            reset_color,
            cfg.TEXT_COLOR,
        )

        pygame.display.flip()
        clock.tick(60)
        t += 1

    pygame.quit()
    # plt.ioff()
    # plt.show()


if __name__ == "__main__":
    main()

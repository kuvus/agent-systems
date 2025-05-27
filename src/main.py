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

    # Initialize matplotlib figure once outside the loop
    fig, axes = None, None
    lines_sim = {}
    lines_sir = {}
    if cfg.SHOW_PLOTS:
        plt.ion()
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        # Initialize simulation plot lines
        (lines_sim["S"],) = axes[0].plot([], [], label="Zdrowi (Symulacja)", color="green")
        (lines_sim["I"],) = axes[0].plot([], [], label="Chorzy (Symulacja)", color="red")
        (lines_sim["R"],) = axes[0].plot([], [], label="Odporni (Symulacja)", color="blue")
        axes[0].set_title("Symulacja Agentowa")
        axes[0].set_xlabel("Czas")
        axes[0].set_ylabel("Liczba osób")
        axes[0].legend(loc="upper right")

        # Initialize SIR model plot lines
        (lines_sir["S"],) = axes[1].plot([], [], label="Zdrowi (Model SIR)", color="green", linestyle="--")
        (lines_sir["I"],) = axes[1].plot([], [], label="Chorzy (Model SIR)", color="red", linestyle="--")
        (lines_sir["R"],) = axes[1].plot([], [], label="Odporni (Model SIR)", color="blue", linestyle="--")
        axes[1].set_title("Model SIR")
        axes[1].set_xlabel("Czas")
        axes[1].set_ylabel("Liczba osób")
        axes[1].legend(loc="upper right")

        plt.show(block=False)

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
            if start_hover:
                if simulation_state == "idle":
                    simulation_state = "running"
                    print("Simulation started")
                elif simulation_state == "running":
                    simulation_state = "paused"
                    print("Simulation paused")
                elif simulation_state == "paused":
                    simulation_state = "running"
                    print("Simulation resumed")
            elif reset_hover:
                simulation_state = "idle"
                simulation = Simulation(cfg.SIM_AREA_WIDTH, cfg.SIM_AREA_HEIGHT)
                time_steps = []
                S_data_sim, I_data_sim, R_data_sim = [], [], []
                S_data_sir, I_data_sir, R_data_sir = [], [], []
                t = 0
                if cfg.SHOW_PLOTS and fig is not None:
                    lines_sim["S"].set_data([], [])
                    lines_sim["I"].set_data([], [])
                    lines_sim["R"].set_data([], [])
                    lines_sir["S"].set_data([], [])
                    lines_sir["I"].set_data([], [])
                    lines_sir["R"].set_data([], [])
                    axes[0].relim()
                    axes[0].autoscale_view()
                    axes[1].relim()
                    axes[1].autoscale_view()
                    fig.canvas.draw_idle() # Use draw_idle for efficiency
                    fig.canvas.flush_events()
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

            # Update plots only every 30 frames and only if plots are enabled
            if cfg.SHOW_PLOTS and t % 60 == 0 and fig is not None:
                # Update simulation data
                lines_sim["S"].set_data(time_steps, S_data_sim)
                lines_sim["I"].set_data(time_steps, I_data_sim)
                lines_sim["R"].set_data(time_steps, R_data_sim)
                axes[0].relim()
                axes[0].autoscale_view()

                # Update SIR model data if available
                if S_data_sir and any(S_data_sir):
                    lines_sir["S"].set_data(time_steps, S_data_sir)
                    lines_sir["I"].set_data(time_steps, I_data_sir)
                    lines_sir["R"].set_data(time_steps, R_data_sir)
                    axes[1].set_title("Model SIR") # Keep title update in case it changes
                else:
                    lines_sir["S"].set_data([], []) # Clear data if not available
                    lines_sir["I"].set_data([], [])
                    lines_sir["R"].set_data([], [])
                    axes[1].set_title("Model SIR (brak danych)")
                
                axes[1].relim()
                axes[1].autoscale_view()

                # Update the figure
                fig.canvas.draw_idle() # Use draw_idle for efficiency
                fig.canvas.flush_events()

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

        # Dynamic button text based on simulation state
        if simulation_state == "idle":
            start_button_text = "Start"
        elif simulation_state == "running":
            start_button_text = "Pause"
        else:  # paused
            start_button_text = "Resume"

        start_color = (
            cfg.BUTTON_HOVER_COLOR if start_hover else cfg.BUTTON_COLOR
        )
        reset_color = (
            cfg.BUTTON_HOVER_COLOR if reset_hover else cfg.BUTTON_COLOR
        )
        draw_button(
            screen,
            start_button_rect,
            start_button_text,
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
        
        # Only increment time when running
        if simulation_state == "running":
            t += 1

    pygame.quit()
    if cfg.SHOW_PLOTS and fig is not None:
        plt.ioff()
        plt.close(fig)


if __name__ == "__main__":
    main()

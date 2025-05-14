import asyncio

import pygame

from pyfalldown.command import (
    Command,
    add,
    add_collectible,
    check_over,
    collect_collectibles,
    move_ball,
    scroll,
    wrap,
)
from pyfalldown.state import Ball, Collectible, Platform, State, Velocity

from .config import Config


def init_state() -> State:
    ball = Ball(15, 15, 15)
    platforms = [Platform(100, 200, 100, 10)]
    collectibles: list[Collectible] = []
    return State(ball, platforms, collectibles)


class UI:
    def __init__(self) -> None:
        self.__render_width = 480
        self.__render_height = 640

        self.__window = pygame.display.set_mode(
            (self.__render_width, self.__render_height),
            pygame.DOUBLEBUF | pygame.RESIZABLE,
        )
        pygame.display.set_caption("pyfalldown")
        self.__config = Config()

        self.__state: State = init_state()
        self.__commands: list[Command] = []
        self.__ball_velocity = Velocity(0, self.__config.gravity)

        self.__clock = pygame.time.Clock()
        self.__running = True

    def process_events(self) -> None:
        self.__commands.append(wrap(check_over, self.__render_height))
        self.__commands.append(wrap(scroll, self.__config.scroll_speed))
        self.__commands.append(
            wrap(
                add,
                10,
                50,
                160,
                self.__render_width,
                80,
                wrap(add_collectible, self.__render_width, self.__config.max_collectible_value),
            )
        )

        vx, vy = self.__ball_velocity.vx, self.__ball_velocity.vy
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    vx = 5
                elif event.key == pygame.K_LEFT:
                    vx = -5
            elif event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                vx = 0
        self.__ball_velocity = Velocity(vx, vy)
        self.__commands.append(wrap(move_ball, Velocity(vx, vy), self.__render_width))
        self.__commands.append(wrap(collect_collectibles))

    def update(self) -> None:
        for command in self.__commands:
            if not self.__state.over:
                self.__state = command(self.__state)
        self.__commands.clear()

    def render(self) -> None:
        state = self.__state
        config = self.__config
        self.__window.fill(config.theme.background_color)
        for p in state.platforms:
            if p.y - p.half_height >= self.__render_height:
                continue
            pygame.draw.rect(
                self.__window,
                config.theme.platform_color,
                pygame.Rect(p.x - p.half_width, p.y - p.half_height, p.half_width * 2, p.half_height * 2),
            )
        pygame.draw.circle(self.__window, config.theme.ball_color, (state.ball.x, state.ball.y), state.ball.radius)

        for c in state.collectibles:
            if len(c.points) == 3:
                pygame.draw.polygon(self.__window, config.theme.triangle_color, c.points)
            elif len(c.points) == 4:
                pygame.draw.polygon(self.__window, config.theme.square_color, c.points)

        score_text = config.theme.score_font.render(f"Score: {state.score}", True, config.theme.score_color)
        score_text_width = score_text.get_width()
        self.__window.blit(score_text, (self.__render_width - score_text_width - 10, 10))

        if state.over:
            game_over_text = config.theme.game_over_font.render(
                "Game Over! Please restart.", True, config.theme.game_over_color
            )
            game_over_text_width, game_over_text_height = game_over_text.get_width(), game_over_text.get_height()
            x = self.__render_width // 2 - game_over_text_width // 2
            y = self.__render_height // 2 - game_over_text_height // 2
            self.__window.blit(game_over_text, (x, y))

        pygame.display.flip()

    async def run(self) -> None:
        while self.__running:
            self.process_events()
            self.update()
            self.render()
            self.__clock.tick(60)
            await asyncio.sleep(0)

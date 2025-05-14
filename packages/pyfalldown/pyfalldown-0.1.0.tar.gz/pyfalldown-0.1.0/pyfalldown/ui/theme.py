from dataclasses import dataclass, field

import pygame


def create_default_game_over_font() -> pygame.font.Font:
    return pygame.font.SysFont("Verdana", 16)


def create_default_score_font() -> pygame.font.Font:
    return pygame.font.SysFont("Verdana", 18)


@dataclass
class Theme:
    background_color: tuple[int, int, int] = (0, 0, 0)
    ball_color: tuple[int, int, int] = (50, 100, 255)
    platform_color: tuple[int, int, int] = (255, 255, 255)
    game_over_font: pygame.font.Font = field(default_factory=create_default_game_over_font)
    game_over_color: tuple[int, int, int] = (255, 10, 10)
    score_font: pygame.font.Font = field(default_factory=create_default_score_font)
    score_color: tuple[int, int, int] = (255, 255, 0)
    triangle_color: tuple[int, int, int] = (80, 200, 80)
    square_color: tuple[int, int, int] = (200, 80, 80)

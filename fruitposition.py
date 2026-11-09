import pygame
import random

def fruit_position(
    grid_width: int,
    grid_height: int,
    snake_body: list[pygame.Vector2]
    ) -> pygame.Vector2 | None:
    """
    needs to guess the positions not occupied by the snake body.
    takes many attempts when the grid is almost full.
    """

    if len(snake_body) >= grid_width * grid_height:
        return None

    while True:
        x = random.randrange(grid_width)
        y = random.randrange(grid_height)

        fruit = pygame.Vector2(x, y)

        if fruit not in snake_body:
            return fruit

def generate_fruit_position(
    grid_width: int,
    grid_height: int,
    snake_body: list[pygame.Vector2]
) -> pygame.Vector2 | None:
    """
    It only gives the aviable options and choise randompy selects one.
    But it checks each candidate against a list, so the cost grows with Snake's length.
    """

    # It's a list comprehension, a compact way to create a list using loops and conditions.
    available_positions = [
        pygame.Vector2(x, y)
        for y in range(grid_height)
        for x in range(grid_width)
        if pygame.Vector2(x,y) not in snake_body
    ]

    if not available_positions:
        return None

    return random.choice(available_positions)
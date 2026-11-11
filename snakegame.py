from enum import Enum
import pygame
import config
import random


def initialize_snake_body(
    grid_width: int,
    grid_height: int,
    initial_lenght: int,
) -> pygame.Vector2:
    """
        Creates Snake's initial body extending left from its head.
    """
    head = _initialize_snake_position(grid_width, grid_height)

    body = []

    for i in range(initial_lenght):
        segment = pygame.Vector2(head.x - i, head.y)
        body.append(segment)

    return body

def fruit_position(
    grid_width: int,
    grid_height: int,
    snake_body: list[pygame.Vector2]
    ) -> pygame.Vector2 | None:
    """
    Evaluates the available positions where the fruit can appear.
    Returns None when theres no space left for fruit
    """
    occupied_positions = {
        (int(segment.x), int(segment.y))
        for segment in snake_body
    }

    available_positions = [
        pygame.Vector2(x, y)
        for x in range(grid_width)
        for y in range(grid_height)
        if (x, y) not in occupied_positions
    ]

    if not available_positions:
        return None

    return random.choice(available_positions)

def _initialize_snake_position(
    grid_width: int,
    grid_height: int
) -> pygame.Vector2:
    """
    Calculates Snake's starting position in grid position.
    """
    x = grid_width // config.SNAKE_START_X_DIVISOR

    y = grid_height // config.SNAKE_START_Y_DIVISOR

    return pygame.Vector2(x, y)

class Direction(Enum): 
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN =(0, 1)

def next_snake_position(
    position: pygame.Vector2,
    direction: Direction
) -> pygame.Vector2:
    """
    Calculates Snake's next grid position.
    """
    movement = pygame.Vector2(direction.value)
    return position + movement

def move_snake_body(
    snake_body: list[pygame.Vector2],
    direction: Direction,
    grow: bool
) -> list[pygame.Vector2]:
    """
    Calculates Snake's updated body positions.
    Adds a square on the snakes direction and pops its tail.
    """

    head = snake_body[0]
    new_head =  next_snake_position(head, direction)
    new_body = snake_body.copy()

    new_body.insert(0, new_head)
    if not grow:
        new_body.pop()
    return new_body
    
def get_direction_from_key(
        key: int,
    ) -> Direction | None:
    if key == pygame.K_RIGHT:
        return Direction.RIGHT

    elif key == pygame.K_LEFT:
        return Direction.LEFT

    elif key == pygame.K_UP:
        return Direction.UP

    elif key == pygame.K_DOWN:
        return Direction.DOWN
    else:
        return None
    
def is_valid_direction(
        current_direction: Direction,
        new_direction: Direction
) -> bool:

    """
    Checks whether the proposed direction is allowed.

    Args:
        current_direction: Snake's current movement direction.
        new_direction: The requested movement direction.

    Returns:
        True if the direction isn't the opposite of
        the current direction.
    """
    current_vector = pygame.Vector2(current_direction.value)
    new_vector = pygame.Vector2(new_direction.value)

    return current_vector + new_vector != pygame.Vector2(0, 0)

def wall_collision( 
    grid_width: int,
    grid_height: int,
    snake_position: pygame.Vector2
    ) -> bool:
    """
    Checks if the snake collided 
    with the grid's limits.
    """
    return (snake_position.x < 0
            or snake_position.x >= grid_width
            or snake_position.y < 0
            or snake_position.y >= grid_height)

def fruit_collision(
    fruit_position: pygame.Vector2 | None,
    snake_head: pygame.Vector2
    ) -> bool:
    """
    Returns True if the snake is on a square containing a fruit.
    """
    return fruit_position is not None and  fruit_position == snake_head

def body_colission(
        snake_body: list[pygame.Vector2]
)-> bool:
    """
    Returns True if the head want to be on a square occupied by its body.
    """
    snake_head = snake_body[0] 
    body =  snake_body[1:]
    
    if snake_head in body:
        return True
    
    return False
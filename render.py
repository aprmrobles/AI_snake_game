import pygame
import color
import config
from snakegame import Direction


# Public functions


def calculate_window_size(
    grid_width: int,
    grid_height: int,
    cell_size: int
) -> tuple[int, int]:
    """
    Calculates the game window dimensions in pixels.

    Args:
        grid_width: Number of columns.

        grid_height: Number of rows.

        cell_size: Dimensions of each square cell in pixels.

    Returns:
        Window dimensions (width, height) in pixels.
    """
    width = grid_width * cell_size
    height = grid_height * cell_size

    return width, height


def initialize_game(
    window_size: tuple[int, int]
) -> tuple[pygame.Surface, pygame.time.Clock, bool]:
    """
    Initializes Pygame and creates the game window.

    Args:
        Window dimensions (width, height) in pixels.

    Returns:
        - screen: Surface used to draw the game.
        - clock: Controls the game loop's frame rate.
        - running: Initial game loop state (True).
    """
    pygame.init()

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()
    running = True

    return screen, clock, running


def background(
    screen: pygame.Surface,
    grid_width: int,
    grid_height: int,
    cell_size: int
) -> pygame.Surface:
    """
        A surface containing the completed checkerboard.
    """

    background_surface = _create_surface(screen)

    _draw_grid(
    background_surface,
    grid_width,
    grid_height,
    cell_size)

    return background_surface


def render_frame(
    screen: pygame.Surface,
    background: pygame.Surface,
    snake_body: list[pygame.Vector2],
    fruit_position: pygame.Vector2 | None,
    cell_size: int,
    direction: Direction,
    ) -> None:
    """
    Draws the background and Snake's head.
    """
    screen.blit(background, (0, 0))

    if fruit_position is not None:
        draw_fruit(
            screen,
            fruit_position,
            cell_size
        )

    _draw_snake_body(screen, snake_body, cell_size)
    _draw_snake_eyes(screen, snake_body, cell_size, direction)


# Helper functions for grid rendering

def _create_surface(
    screen: pygame.Surface
) -> pygame.Surface:
    """
    Creates a new surface with the screen dimensions.
    """
    surface = pygame.Surface(screen.get_size())
    return surface.convert()


def _draw_grid(
    surface: pygame.Surface,
    grid_width: int,
    grid_height: int,
    cell_size: int
) -> None:
    """
    Draws an alternating-color grid onto a surface.

    Args:
        surface: Surface on which the grid is drawn.
        grid_width: Number of columns.
        grid_height: Number of rows.
        cell_size: Size of each cell in pixels.

    Returns:
        None. Modifies the provided surface directly.
    """

    for row in range(grid_height):
        for column in range(grid_width):

            grid_position = pygame.Vector2(column, row)

            pixel_position = _grid_to_pixel(
                grid_position,
                cell_size
                )

            square_color = _get_cell_color(grid_position)

            _draw_square(surface, 
                        square_color, 
                        pixel_position,
                        cell_size
                        )


def _grid_to_pixel(
    coordinate: pygame.Vector2,
    cell_size: int
) -> pygame.Vector2:
    """
    Converts grid coordinates into pixel coordinates.
    """

    x = coordinate.x * cell_size
    y = coordinate.y * cell_size

    return pygame.Vector2(x, y)


def _draw_snake_body(
    surface: pygame.Surface,
    snake_body: list[pygame.Vector2],
    cell_size: int
) -> None:

    for segment in snake_body:
        pixel_position =_grid_to_pixel(segment, cell_size)
        
        _draw_square(
                surface,
                color.SNAKE,
                pixel_position,
                cell_size
            )

    
def _draw_snake_eyes(
    surface: pygame.Surface,
    snake_body: list[pygame.Vector2],
    cell_size: int,
    direction: Direction
) -> None:
    """
    Draws Snake's eyes at their head.
    """
    head_position = snake_body[0]
    head_pixel_position =_grid_to_pixel(
        head_position, 
        cell_size)

    eye1_position, eye2_position =_get_eyes_positions(
        head_pixel_position, 
        cell_size,
         direction )

    _draw_eye_circle(
            surface,
            eye1_position,
            cell_size)
    
    _draw_eye_circle(
            surface,
            eye2_position,
            cell_size)
    

def _get_eyes_positions(
    head_pixel_position: pygame.Vector2,
    cell_size: int,
    direction: Direction,
) -> tuple[pygame.Vector2, pygame.Vector2]:
    """Calculates both eye positions in pixel coordinates."""

    # Points in the direction Snake is facing.
    forward = pygame.Vector2(direction.value)
    forward_distance = cell_size * config.EYE_FORWARD_OFFSET_RATIO

    # Points perpendicular to Snake's direction.
    sideways = pygame.Vector2(-forward.y, forward.x)
    side_distance = cell_size * config.EYE_SIDE_OFFSET_RATIO

    get_middle = 2
    head_center = head_pixel_position + pygame.Vector2(
    cell_size / get_middle,
    cell_size / get_middle
    )

    forward_offset = forward * forward_distance
    side_offset = sideways * side_distance

    eye1 = head_center + forward_offset + side_offset
    eye2 = head_center + forward_offset - side_offset

    return eye1, eye2


def _get_cell_color(
    coordinate: pygame.Vector2 
) -> tuple[int, int, int]:
    """
    Returns a checkerboard style color (RGB).

    """
    if (coordinate.x + coordinate.y) % 2 == 0:
        return color.BACKGROUND1
    else:
        return color.BACKGROUND2


def _draw_square(
    surface: pygame.Surface,
    square_color: tuple[int, int, int],
    coordinate: pygame.Vector2,
    cell_size: int
) -> pygame.Rect:
    """
    Draws a pixel square on the Pygame surface.
    """
    pygame.draw.rect(
    surface,
    square_color,
    pygame.Rect(coordinate.x, 
                coordinate.y,  
                cell_size, 
                cell_size)
    )


def _draw_eye_circle(
        surface: pygame.Surface,
        eye_position: pygame.Vector2,
        cell_size: int
):
    eye_radius = cell_size // config.EYE_RADIUS_DIVISOR

    pygame.draw.circle(
        surface, 
        color.EYE, 
        eye_position,
        eye_radius)


def draw_fruit(surface: pygame.Surface,
        fruit_position: pygame.Vector2,
        cell_size: int
        ):

    fruit_radius = cell_size * config.FRUIT_RADIUS_RATIO

    pixel_position = _grid_to_pixel(fruit_position, cell_size)

    get_middle = 2
    center = pixel_position + pygame.Vector2(
        cell_size // get_middle,
        cell_size // get_middle
        )
    
    pygame.draw.circle(
            surface, 
            color.FRUIT, 
            center,
            fruit_radius)
    
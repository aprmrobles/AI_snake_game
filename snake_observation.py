import pygame
from snakegame import Direction
import snakegame

def observation_vector(
    snake_body: list[pygame.Vector2],
    snake_direction: Direction,
    fruit: pygame.Vector2,
    grid_width: int,
    grid_height: int
) -> tuple[int, int , int, int, int, int]:
    """
    Combines danger and fruit information into six numerical inputs for the neural network.
    """
    dangers = get_danger_inputs(
          snake_body, 
          snake_direction, 
          fruit, grid_width, 
          grid_height)
     
    fruits =  fruit_direction_inputs(
    snake_body[0],
    fruit,
    snake_direction)

    observation = dangers + fruits
    observation_int = tuple(int(i) for i in observation)

    return observation_int
   
def get_danger_inputs(
    snake_body: list[pygame.Vector2],
    snake_direction: Direction,
    fruit: pygame.Vector2,
    grid_width: int,
    grid_height: int
) -> tuple[bool, bool, bool]:
    """
    Returns collision risks for left, straight, and right movements.
    """
    
    left, straight, right = possible_directions(snake_direction)
    directions = [left, straight, right]

    dangers = []

    for direction in directions:
        dangers.append(danger_colission(
    snake_body,
    direction,
    fruit,
    grid_width,
    grid_height
         ))

    return tuple(dangers)     
    
def possible_directions(
    current_direction: Direction
) ->tuple[Direction, Direction, Direction]:
    """
    Calculates left, straight, and right directions relative to Snake's heading.
    """

    directions = [
         Direction.UP,
         Direction.LEFT,
         Direction.DOWN,
         Direction.RIGHT
    ]
    index = directions.index(current_direction)

    left = directions[(index + 1) % 4] 
    straight = current_direction
    right = directions[(index - 1) % 4]

    return left, straight, right
     
def danger_colission(
    snake_body: list[pygame.Vector2],
    snake_direction: Direction,
    fruit: pygame.Vector2,
    grid_width: int,
    grid_height: int
) -> bool:
     """
     Checks whether a movement would cause a wall or body collision.
     """
     wall_ahead = is_wall_ahead(
          snake_body[0], 
          snake_direction,
          grid_width,
          grid_height
          )
     body_ahead = is_body_ahead(
          snake_body,
          snake_direction,
          fruit
          )  
     return (wall_ahead or body_ahead)

def is_wall_ahead(
        snake_head: pygame.Vector2, 
        snake_direction: Direction,
        grid_width: int,
        grid_height: int
        ) -> bool:
    """
    Determines whether the next movement would hit a wall.
    """
    next_postion = snakegame.next_snake_position(snake_head, snake_direction)
    if next_postion.x < 0 or next_postion.x >= grid_width:
         return True 
    
    if next_postion.y < 0 or next_postion.y >= grid_height:
        return True

    return False
          
def is_body_ahead(
        snake_body:list[pygame.Vector2], 
        snake_direction: Direction,
        fruit: pygame.Vector2,
        ) -> bool:
     
     """
     Determines whether the next movement would
    collide with Snake's body, takes into account growth.
     """
     head = snake_body[0]
     body = snake_body[1: -1]
     next_position = snakegame.next_snake_position(head, snake_direction)

     if fruit == next_position:
        body = snake_body[1:]

     return next_position in body

def fruit_direction_inputs(
    snake_head: pygame.Vector2,
    fruit_position: pygame.Vector2,
    snake_direction: Direction,
    ) -> tuple[bool, bool, bool]:
    """
    Returns three Booleans describing the fruit's relative direction.
    """
    friuit_LR = is_fruit_LR(snake_head,
            fruit_position, 
            snake_direction)

    fruit_left = friuit_LR == Direction.LEFT
    
    fruit_straight = is_fruit_ahead(
         snake_head,
        fruit_position, 
        snake_direction)

    fruit_right = friuit_LR == Direction.RIGHT

    return fruit_left, fruit_straight, fruit_right

def is_fruit_ahead(
          snake_head: pygame.Vector2,
          fruit_position: pygame.Vector2,
          snake_direction: Direction
          ) -> bool:
    """
    Uses the dot product to determine whether the fruit is ahead.
    """
    dist_fruit = dist_to_fruit(snake_head, fruit_position)
    direction = pygame.Vector2(snake_direction.value)

    dot_product = direction.dot(dist_fruit)

    return dot_product > 0

def is_fruit_LR(
          snake_head: pygame.Vector2,
          fruit_position: pygame.Vector2,
          snake_direction: Direction
          ) -> Direction | None:
    """
    Uses the cross product to determine whether the fruit is left or right.
    """
    
    dist_fruit = dist_to_fruit(snake_head, fruit_position)
    direction = pygame.Vector2(snake_direction.value)

    cross_product = direction.cross(dist_fruit)

    if cross_product > 0: 
         return Direction.RIGHT

    if cross_product < 0:
         return Direction.LEFT
    
    return None

def dist_to_fruit(
        snake_head: pygame.Vector2, 
        fruit_position: pygame.Vector2
        ) -> pygame.Vector2:
    """
    Calculates the displacement vector from Snake's head to the fruit.
    """
    return fruit_position - snake_head 

def set_direction(
        vector: pygame.Vector2
        ) -> tuple[Direction | None, Direction | None]:
    """
    Converts a displacement vector into horizontal and vertical directions.
    """
    if vector.x > 0:
        direct_x = Direction.RIGHT
    elif vector.x < 0:
        direct_x = Direction.LEFT
    else:
         direct_x = None

    if vector.y > 0:
            direct_y = Direction.DOWN
    elif vector.y < 0:
            direct_y = Direction.UP
    else:
            direct_y = None
    return (direct_x, direct_y)




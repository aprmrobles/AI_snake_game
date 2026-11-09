import pygame
import config
import render
import snakegame

window_size = render.calculate_window_size(
    config.GRID_WIDTH,
    config.GRID_HEIGHT,
    config.CELL_SIZE
)

screen, clock, running = render.initialize_game(window_size)

board_surface = render.background(
    screen,
    config.GRID_WIDTH,
    config.GRID_HEIGHT,
    config.CELL_SIZE
)


snake_body = snakegame.initialize_snake_body(
        config.GRID_WIDTH,
        config.GRID_HEIGHT,
        config.SNAKE_INITIAL_LENGTH
    )

fruit_position = snakegame.fruit_position(
    config.GRID_WIDTH,
    config.GRID_HEIGHT,
    snake_body
    )

current_direction = snakegame.Direction.RIGHT
next_direction = current_direction
last_move_time = pygame.time.get_ticks()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            requested_direction = snakegame.get_direction_from_key(event.key)

            if requested_direction is not None:
                if snakegame.is_valid_direction(
                    current_direction,
                    requested_direction):

                    next_direction = requested_direction

    current_time = pygame.time.get_ticks()

    if current_time - last_move_time >= config.MOVE_INTERVAL:

        current_direction = next_direction

        next_head = snakegame.next_snake_position(snake_body[0], current_direction)

        ate_fruit = False
        if next_head == fruit_position:
            ate_fruit = True

        next_body = snakegame.move_snake_body(snake_body, current_direction, grow= ate_fruit)

        
        
        if (snakegame.wall_collision(
        config.GRID_WIDTH,
        config.GRID_HEIGHT,
        next_body[0]) 
        or 
        snakegame.body_colission(next_body)):
            running = False

        else:
            snake_body = next_body


        if ate_fruit:
            fruit_position = snakegame.fruit_position(
                config.GRID_WIDTH,
                config.GRID_HEIGHT,
                snake_body
            )
        last_move_time = current_time


    render.render_frame(
        screen, 
        board_surface, 
        snake_body,
        fruit_position, 
        config.CELL_SIZE,
        current_direction
        )

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()

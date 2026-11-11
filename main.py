import pygame
import config
import render
import snakegame
import snake_observation as obs
import neural_network as ANN
# ANN stands for Artificial Neural Network

# SElect GAME_MODE: "manual", "ai"
#----------------
GAME_MODE = "ai" 
#----------------

grid_settings = (
        config.GRID_WIDTH,
        config.GRID_HEIGHT,
        config.CELL_SIZE
    )

window_size = render.calculate_window_size(*grid_settings)

screen, clock, running = render.initialize_game(window_size)

board_surface = render.background(screen, *grid_settings)

snake_body = snakegame.initialize_snake_body(
        *grid_settings[:2],
        config.SNAKE_INITIAL_LENGTH
    )

fruit_position = snakegame.fruit_position(*grid_settings[:2], snake_body)

current_direction = snakegame.Direction.RIGHT
next_direction = current_direction
last_move_time = pygame.time.get_ticks()

# used if AI is playing
hidden_layer = ANN.initialize_hidden_layer()
output_layer = ANN.initialize_output_layer()
   

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and GAME_MODE == "manual":
            requested_direction = snakegame.get_direction_from_key(event.key)

            if requested_direction is not None:
                if snakegame.is_valid_direction(
                    current_direction,
                    requested_direction):

                    next_direction = requested_direction

    current_time = pygame.time.get_ticks()

    if current_time - last_move_time >= config.MOVE_INTERVAL:

        if GAME_MODE == "ai":
            observation = obs.observation_vector(
                snake_body, 
                current_direction, 
                fruit_position, 
                *grid_settings[:2])
            
            scores = ANN.forward(observation, hidden_layer, output_layer)
            action = ANN.select_action(scores)
            next_direction = obs.action_to_direction(action, current_direction)

        current_direction = next_direction
        
        snake_body, fruit_position, collision = snakegame.step(
            snake_body, current_direction, fruit_position, *grid_settings[:2])

        if collision:
            running = False

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

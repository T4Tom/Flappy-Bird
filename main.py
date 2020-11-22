import pygame, sys, random

pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512) # Initiates the sound mixer
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450)) # Second layer to make it continuous

def create_pipe():
    random_pipe_pos = random.choice(pipe_height) # Chooses a random height from the set pipe height list
    bottom_pipe = pipe_surface.get_rect(midtop = (350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512: # If the bottom reaches a certain point (top pipes can't reach this point)
            if pipe.right >= 0: # If the pipe is on the screen
                screen.blit(pipe_surface, pipe)
        else:
            if pipe.right >= 0: # If the pipe is on the screen
                flip_pipe = pygame.transform.flip(pipe_surface, False, True) # Rotates the top pipe
                screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # If the bird collided with a pipe
            death_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 450: # If the bird went too high or too low
        death_sound.play()
        return False
    return True # Else return true

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3, 1) # Rotozoom rotates the bird (surface, amount, rescale)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index] # New bird surface
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery)) # New bird rect using old bird centery
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render("Score: {0}".format(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
    elif game_state == "game_over":
        score_surface = game_font.render("High Score: {0}".format(int(high_score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 425))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("Score: {0}".format(int(score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (144, 50))
        screen.blit(high_score_surface, high_score_rect)

game_font = pygame.font.Font("04B_19__.TTF", 20) # You can choose the ttf font by downloading it from the internet

def update_score(score, high_score):
    if score > high_score:
        high_score_file = open("highscore.txt", "w")
        high_score_file.write(str(score))
        high_score_file.close()
        high_score = score
    return high_score

# Game variables

gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score_file = open("highscore.txt", "r")
high_score = float(high_score_file.read())
high_score_file.close()


bg_surface = pygame.image.load("assets/background-day.png").convert() # Convert makes images load better
floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha() # Convert alpha makes it a png for the transformation
bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap] # List of frames for the animation
bird_index = 2
bird_surface = bird_frames[bird_index] # Determines what frame shows
bird_rect = bird_surface.get_rect(center = (100, 200))

BIRDFLAP = pygame.USEREVENT + 1 # Plus 1 because it needs to be a new userevent
pygame.time.set_timer(BIRDFLAP, 200) # 2 seconds timer


pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_list = [] # Loaded pipes
SPAWNPIPE = pygame.USEREVENT # Making the timer
pygame.time.set_timer(SPAWNPIPE, 1200) # Making the timer
pipe_height = [200, 300, 400] # These are the possible pipe heights

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))


# Sound effects

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # Exit without errors
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active:
            bird_movement = 0 # Resetting speed
            bird_movement -= 6 # Jump
            flap_sound.play() # Play the sound effect
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_active == False:
            game_active = True # Restart game
            pipe_list = [] # Unload pipes
            bird_rect.center = (50, 200) # Reset position
            bird_movement = 0 # Reset speed
            score = 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            bird_movement = 0
            bird_movement -= 6
            flap_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN and game_active == False:
            game_active = True
            pipe_list = []
            bird_rect.center = (50, 200)
            bird_movement = 0
            score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # Every 1.2 secods a new pipe spawns
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1 # Changes the bird frame
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation() # New bird surface and new bird rect

    

    screen.blit(bg_surface, (0, 0))

    if game_active:

        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface) # Rotates the bird
        bird_rect.centery += bird_movement # Moves the bird down
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list) # Checks if the game is still running

        # Pipes

        pipe_list = move_pipes(pipe_list) # Moves the pipes
        draw_pipes(pipe_list) # Draws the pipes from the list onto the screen
        
        score += 0.01
        score_display("main_game")

    else:
        high_score = update_score(score, high_score) # Updates the high score
        score_display("game_over")
        screen.blit(game_over_surface, game_over_rect)

    # Floor

    floor_x_pos -= 0.5 # Continuously moving
    draw_floor()
    if floor_x_pos <= -288: # If the floor runs out of space
        floor_x_pos = 0 # Start from the beginning



    screen.blit(floor_surface, (floor_x_pos, 450))

    pygame.display.update()
    clock.tick(120)

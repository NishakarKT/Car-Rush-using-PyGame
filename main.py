import pygame

pygame.init()

# >>> Game Variables
# General
shake_var = 1
crash_impact = [50, 20]
clock = pygame.time.Clock()
fps = 600

# Screen
width = 840
height = 640
cars_width = 80
cars_length = 150
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Crash")

# Background
road_pos = [[0, 0], [0, -height]]
right_road_limit = width - cars_width - 30
left_road_limit = 15
grass_patch_width = 60

# Player Car
player_pos = [width/2 - 50, height - 200]
player_vel = [5,0]
player_vel_max = 70
player_vel_max_grass = 20
accl_y = 0.5
player_nav = "car"

# Enemy cars
enemy_count = 5
enemy_pos = []
enemy_vel = []
enemy_accl = []
enemy_vel_max = []
enemy_nav = []
for i in range(enemy_count):
    enemy_pos.append([100*(i+1), height - 2.5*cars_length])
for i in range(enemy_count):
    enemy_vel.append([player_vel[0],2*(i+1)])
for i in range(enemy_count):
    enemy_accl.append((i+8)*0.1)
for i in range(enemy_count):
    enemy_vel_max.append(5*(i+8))
for i in range(enemy_count):
    enemy_nav.append("car")

# Image Dictionaries
player_car_images = {
    "car": pygame.image.load("images\\car_0.png").convert_alpha(),
    "car_right": pygame.image.load("images\\car_0_right.png").convert_alpha(),
    "car_left": pygame.image.load("images\\car_0_left.png").convert_alpha()
}
enemy_cars_images = {}
for i in range(enemy_count):
    enemy_cars_images[i] = {
    "car": pygame.image.load(f"images\\car_{1}.png").convert_alpha(),
    "car_right": pygame.image.load(f"images\\car_{1}_right.png").convert_alpha(),
    "car_left": pygame.image.load(f"images\\car_{1}_left.png").convert_alpha()
    }

# Music
pygame.mixer.Channel(0).play(pygame.mixer.Sound(
    "audio\\normal_engine.mp3"), loops=-1)

# Main Game Loop
while True:
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Navigation
    # Player car X
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player_vel[1] > 1:
        player_pos[0] += player_vel[0]
        player_nav = "car_right"
    elif keys[pygame.K_LEFT] and player_vel[1] > 1:
        player_pos[0] -= player_vel[0]
        player_nav = "car_left"

    # Player car Y
    if keys[pygame.K_UP]:
        if player_vel[1] <= player_vel_max:
            player_vel[1] += accl_y
        road_pos[0][1] += player_vel[1]
        road_pos[1][1] += player_vel[1]
        if road_pos[0][1] >= height:
            road_pos[0][1] = -height
        elif road_pos[1][1] >= height:
            road_pos[1][1] = -height
        for i in range(enemy_count):
            enemy_pos[i][1] += player_vel[1]
    elif not keys[pygame.K_UP]:
        if player_vel[1] >= accl_y/2:
            player_vel[1] -= accl_y/2
        road_pos[0][1] += player_vel[1]
        road_pos[1][1] += player_vel[1]
        if road_pos[0][1] >= height:
            road_pos[0][1] = -height
        elif road_pos[1][1] >= height:
            road_pos[1][1] = -height
        for i in range(enemy_count):
            enemy_pos[i][1] += player_vel[1]

    # side road slow down and boundary check
    if player_pos[0] > right_road_limit - grass_patch_width or player_pos[0] < left_road_limit + grass_patch_width:
        if player_vel[1] >= player_vel_max_grass:
            player_vel[1] -= 1.5*accl_y
    if player_pos[0] >= right_road_limit:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("audio\\crash.mp3"))
        game_window.blit(pygame.image.load("images\\bang.png").convert_alpha(
        ), ((player_pos[0] + right_road_limit)/2 + 100, (player_pos[1] + height)/2 - 100))
        pygame.display.update()
        player_pos[0] -= crash_impact[0]
    elif player_pos[0] <= left_road_limit:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("audio\\crash.mp3"))
        game_window.blit(pygame.image.load("images\\bang.png").convert_alpha(
        ), ((player_pos[0] - 100)/2, (player_pos[1] + height)/2 - 100))
        pygame.display.update()
        player_pos[0] += crash_impact[0]

    # Blocking behaviour of the enemy cars
    for i in range(enemy_count):
        if enemy_pos[i][0] <= right_road_limit and enemy_pos[i][0] >= left_road_limit:
            if player_pos[0] < enemy_pos[i][0]:
                enemy_pos[i][0] -= enemy_vel[i][0]
                enemy_nav[i] = "car_left"
            if player_pos[0] > enemy_pos[i][0]:
                enemy_pos[i][0] += enemy_vel[i][0]
                enemy_nav[i] = "car_right"
        else:
            game_window.blit(pygame.image.load("images\\bang.png").convert_alpha(), ((player_pos[0] + enemy_pos[0][0])/2 - 30, (player_pos[1] + enemy_pos[0][1])/2))
            pygame.display.update()
            if enemy_pos[i][0] < left_road_limit:
                enemy_pos[i][0] = left_road_limit
            if enemy_pos[i][0] > right_road_limit:
                enemy_pos[i][0] = right_road_limit

    # Crash Test for enemy cars
    for i in range(enemy_count):
        if abs(player_pos[0] - enemy_pos[i][0]) <= cars_width and abs(player_pos[1] - enemy_pos[i][1]) <= cars_length:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("audio\\crash.mp3"))
            game_window.blit(pygame.image.load("images\\bang.png").convert_alpha(), (player_pos[0], player_pos[1]))
            pygame.display.update()
            if player_pos[0] > enemy_pos[i][0]:
                player_pos[0] += crash_impact[0]
                enemy_pos[i][0] -= crash_impact[0]
                player_nav = "car_right"
                enemy_nav[i] = "car_left"
            if player_pos[0] <= enemy_pos[i][0]:
                player_pos[0] -= crash_impact[0]
                enemy_pos[i][0] += crash_impact[0]
                player_nav = "car_left"
                enemy_nav[i] = "car_right"
            if player_pos[1] < enemy_pos[i][1]:
                player_vel[1] += crash_impact[1]
            if player_pos[1] > enemy_pos[i][1]:
                player_vel[1] -= crash_impact[1]

    # Enemy Cars motion
    for i in range(enemy_count):
        enemy_pos[i][1] -= enemy_vel[i][1]
        if enemy_vel[i][1] < enemy_vel_max[i]:
            enemy_vel[i][1] += enemy_accl[i]

    # Display
    game_window.blit(pygame.image.load(
        "images\\road.png").convert_alpha(), (road_pos[0][0], road_pos[0][1]))
    game_window.blit(pygame.image.load(
        "images\\road.png").convert_alpha(), (road_pos[1][0], road_pos[1][1]))

    for i in range(enemy_count):
        if shake_var % 2 == 0:
            game_window.blit(player_car_images[player_nav], (player_pos[0], player_pos[1]))
            game_window.blit(enemy_cars_images[i][enemy_nav[i]],
                            (enemy_pos[i][0], enemy_pos[i][1]))
        else:
            game_window.blit(player_car_images[player_nav], (player_pos[0] - 1, player_pos[1]))
            game_window.blit(enemy_cars_images[i][enemy_nav[i]],
                            (enemy_pos[i][0] - 2, enemy_pos[i][1]))

    # Update
    pygame.display.update()

    # Resets
    player_nav = "car"
    for i in range(enemy_count):
        enemy_nav[i] = "car"
    shake_var += 1
    clock.tick(fps)

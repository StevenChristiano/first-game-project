import pygame,sys 
from pygame.locals import * # import all component from pygames
pygame.init() #initiate pygame

clock = pygame.time.Clock() # set up the clock

pygame.display.set_caption("Tabbids Adventure") # set window name

WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) #initiate the window
display = pygame.Surface((300, 200)) #create another blank surface(basically black)

# game_map[y][x]
# game_map =[['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'], 
#            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
#            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
#            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
#            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

grass_image= pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load('dirt.png')

player_image = pygame.image.load('bunny3.png')
player_image.set_colorkey((1, 1, 1)) # set the color in parentheses to transparant 
                                     # (i don't want to use it, so i set to color i don't use)

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height()) # making players' rectangle
test_rect = pygame.Rect(100,100,100,50)

background_objects = [[0.25, [120,10,70,400]] , # make sure the smaller value is written first
                      [0.25, [280,30,40,400]] , # it means the closest the object to us, the fastest the camera move
                      [0.50, [30,40,40, 400]] , # would be weird if the front move slower than the back
                      [0.5, [130,90,100,400]], 
                      [0.5, [300,80,120,400]]
                    ]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile): # if rect collide with tile
            hit_list.append(tile)
    return hit_list #return list of collision
        
        # things moving, how it's moving, things that potentially can be run into)
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom' : False, 'right': False, 'left' : False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True  

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


moving_right = False
moving_left = False
# player_location = [50,50] # not needed in the code
player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]

while True: #game loop
    display.fill((146,244,255))

    true_scroll[0] += (player_rect.x - true_scroll[0] - 134)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 84)/20
    scroll = true_scroll.copy()
    scroll[0] = int (scroll[0])
    scroll[1] = int (scroll[1])
                               # color               # position & size
    pygame.draw.rect(display, (7,80,65), pygame.Rect(0, 120, 300, 80)) # 1st object horizontal rect
    for background_object in background_objects:
        # parallex effect
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], background_object[1][1] - scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14,222,150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 100, 105), obj_rect)

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)) #(x_pos, y_pos, width, height)
            x += 1
        y += 1

    # display.blit(player_image, player_location) #position (x, y)
    
    # setting gravity(kalo char sampe bates bawah window )
    # if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
    #     player_y_momentum = -player_y_momentum
    # else:
        # player_y_momentum += 0.2
    # player_location[1] += player_y_momentum

    player_movement = [0, 0] #velocity of movement not position
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
    
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    
    if collisions['bottom']:
        player_y_momentum = 1
        air_timer = 0
    else:
        air_timer +=1    
    if collisions['top']:
        player_y_momentum = 1
        air_timer = 0

    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    # if moving_right == True: #also not needed
    #     player_location[0] += 4
    # if moving_left == True:
    #     player_location[0] -= 4

    # player_rect.x = player_location[0]
    # player_rect.y = player_location[1]

    # if player_rect.colliderect(test_rect):
    #     pygame.draw.rect(screen, (255, 0, 0), test_rect)
    # else:
    #     pygame.draw.rect(screen, (0,0,0), test_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if air_timer < 20:
                    player_y_momentum = -4.5
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
    surf = pygame.transform.scale(display, WINDOW_SIZE) # change the size of image (old size, new size)
    screen.blit(surf, (0, 0)) # (0, 0) means top left
    pygame.display.update()
    clock.tick(60) #various thing (to keep the game running at 60 fps)
    


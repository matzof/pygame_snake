import random
import pygame
pygame.init()

# SCREEN GENERATION
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Snake")

# CONFIGURATION VARIABLES
clock = pygame.time.Clock()

# VARIABLES
fps = 50
cell_pixels = int(1.3*screen_height/20)
max_num_cols = round(screen_height/cell_pixels-2)
max_num_rows = round(screen_width/cell_pixels-2)
x_field = 298
y_field = 34
num_cols = 10
num_rows = 10
sound = True
snake = []
fruits = []
obstacles  = []
animals = []
walls = []
sliders = []

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
brown = (169, 89, 30)
red = (255, 0, 0)
light_green = (153, 255, 51)
dark_green = (0, 150, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# LOAD MEDIA
background_image = pygame.image.load('media/grass.jpg')
field_image = pygame.image.load('media/ground.jpg')
walls_image = pygame.image.load('media/walls.png')
back_image = pygame.image.load('media/back.png')
sound_on = pygame.image.load('media/sound_on.png')
sound_off = pygame.image.load('media/sound_off.png')

green_slider = pygame.image.load('media/green_slider.png')

music = pygame.mixer.music.load('media/music.mp3')
pygame.mixer.music.play(-1)

head_left = pygame.transform.scale(pygame.image.load('media/head_left.png'), (cell_pixels, cell_pixels))
head_right = pygame.transform.scale(pygame.image.load('media/head_right.png'), (cell_pixels, cell_pixels))
head_up = pygame.transform.scale(pygame.image.load('media/head_up.png'), (cell_pixels, cell_pixels))
head_down = pygame.transform.scale(pygame.image.load('media/head_down.png'), (cell_pixels, cell_pixels))
straight_vertical = pygame.transform.scale(pygame.image.load('media/straight_vertical.png'), (cell_pixels, cell_pixels))
straight_horizontal = pygame.transform.scale(pygame.image.load('media/straight_horizontal.png'), (cell_pixels, cell_pixels))
tail_left = pygame.transform.scale(pygame.image.load('media/tail_left.png'), (cell_pixels, cell_pixels))
tail_right = pygame.transform.scale(pygame.image.load('media/tail_right.png'), (cell_pixels, cell_pixels))
tail_up = pygame.transform.scale(pygame.image.load('media/tail_up.png'), (cell_pixels, cell_pixels))
tail_down = pygame.transform.scale(pygame.image.load('media/tail_down.png'), (cell_pixels, cell_pixels))
turn_down_left = pygame.transform.scale(pygame.image.load('media/turn_down_left.png'), (cell_pixels, cell_pixels))
turn_down_right = pygame.transform.scale(pygame.image.load('media/turn_down_right.png'), (cell_pixels, cell_pixels))
turn_up_left = pygame.transform.scale(pygame.image.load('media/turn_up_left.png'), (cell_pixels, cell_pixels))
turn_up_right = pygame.transform.scale(pygame.image.load('media/turn_up_right.png'), (cell_pixels, cell_pixels))

apple = pygame.transform.scale(pygame.image.load('media/apple.png'), (cell_pixels, cell_pixels))

rock = pygame.transform.scale(pygame.image.load('media/rock.png'), (cell_pixels, cell_pixels))
rocks = pygame.transform.scale(pygame.image.load('media/rocks.png'), (cell_pixels, cell_pixels))
lake = pygame.transform.scale(pygame.image.load('media/lake.png'), (cell_pixels, cell_pixels))
trap = pygame.transform.scale(pygame.image.load('media/trap.png'), (cell_pixels, cell_pixels))

eagle_right = pygame.transform.scale(pygame.image.load('media/eagle_right.png'), (cell_pixels, cell_pixels))
eagle_left = pygame.transform.scale(pygame.image.load('media/eagle_left.png'), (cell_pixels, cell_pixels))
mongoose_right = pygame.transform.scale(pygame.image.load('media/mongoose_right.png'), (cell_pixels, cell_pixels))
mongoose_left = pygame.transform.scale(pygame.image.load('media/mongoose_left.png'), (cell_pixels, cell_pixels))


#%%
def resume():
    global run_pause
    run_pause = False
    
def quit_game():
    pygame.quit()
    quit()

def quit_confirm():
    global run_pause
    run_pause = True
    while run_pause:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
        pygame.draw.circle(screen, white, (int(10*screen_width/20), 
                           int(10*screen_height/20)), int(13*screen_height/20))
        print_message('Do you really want to quit?', black, screen_width/2, 300, 90)
        button('Yes', 60, black, 8*screen_width/20, 11*screen_height/20, light_green, green, quit_game)
        button('No', 60, black, 12*screen_width/20, 11*screen_height/20, light_green, green, resume)
        pygame.display.update()

#%%
def redraw_display():
    screen.blit(background_image, (0, 0))
    screen.blit(walls_image, (x_field-cell_pixels, y_field-cell_pixels))
    screen.blit(field_image, (x_field, y_field))
    for part in snake:
        part.draw_part(screen)
    for fruit in fruits:
        fruit.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for animal in animals:
        animal.draw(screen)
    pygame.display.update()   

#%%
def print_message(message, color, x, y, font_size):
    font = pygame.font.SysFont("comicsans", font_size, False, False)
    text = font.render(message, 1, color)
    textRect = text.get_rect(center=(x, y))
    screen.blit(text, textRect)

# PRINT BUTTON AND CHECK IF CLICKED
def button(text, text_size, text_color, x_center, y_center, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()    
    font = pygame.font.SysFont("comicsansms",text_size, False, False)
    textSurf = font.render(text, True, text_color)
    textRect = textSurf.get_rect( center=(x_center, y_center) ) 
    if (textRect.collidepoint(mouse[0], mouse[1])):
        pygame.draw.rect(screen, active_color, textRect)
        if click[0] and action != None:
            pygame.time.wait(200)
            action()         
    else:
        pygame.draw.rect(screen, inactive_color, textRect)
    screen.blit(textSurf, textRect)
    
def game_button(text, text_size, text_color, x_center, y_center, inactive_color, active_color, 
                move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()    
    font = pygame.font.SysFont("comicsansms",text_size, False, False)
    textSurf = font.render(text, True, text_color)
    textRect = textSurf.get_rect( center=(x_center, y_center) ) 
    if (textRect.collidepoint(mouse[0], mouse[1])):
        pygame.draw.rect(screen, active_color, textRect)
        if click[0]:
            pygame.time.wait(200)
            start_game(move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows)         
    else:
        pygame.draw.rect(screen, inactive_color, textRect)
    screen.blit(textSurf, textRect)

def back_button(x_center, y_center, width):
    run = True
    height = width
    image = pygame.transform.scale(back_image, (width, height))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    screen.blit(image, (x_center - width/2, y_center - height/2))
    if (image.get_rect(center = (x_center, y_center)).collidepoint(mouse[0], mouse[1])):
        image = pygame.transform.scale(image, (int(width*1.1), int(height*1.05)))
        pygame.draw.rect(screen, white, image.get_rect(center = (x_center, y_center)))
        screen.blit(image, (x_center - width/2, y_center - height/2))
        if click[0]:
            pygame.time.wait(200)
            run = False      
    return run 

def music_button(x_center, y_center, width):
    global sound
    height = width
    if sound == False:
        pygame.mixer.music.pause()
        image = pygame.transform.scale(sound_off, (width, height))
    if sound == True:
        pygame.mixer.music.unpause()
        image = pygame.transform.scale(sound_on, (width, height))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    screen.blit(image, (x_center - width/2, y_center - height/2))
    if (image.get_rect(center = (x_center, y_center)).collidepoint(mouse[0], mouse[1])):
        image = pygame.transform.scale(image, (int(width*1.1), int(height*1.05)))
        pygame.draw.rect(screen, white, image.get_rect(center = (x_center, y_center)))
        screen.blit(image, (x_center - width/2, y_center - height/2))
        if click[0] and sound == True:
            sound = False 
            pygame.time.wait(300)
        elif click[0] and sound == False:
            sound = True
            pygame.time.wait(300)

class create_slider(object):
    def __init__(self, init_val, min_val, max_val, x_center, y_center, width, height):
        self.min_val = min_val
        self.max_val = max_val
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.radius = int(height/2)
        self.min_pos = int(x_center - width/2 + self.radius)
        self.max_pos = int(x_center + width/2 - self.radius)
        self.current_val = init_val
        self.current_pos = int(((self.max_pos - self.min_pos)/(max_val-min_val))*
                                (self.current_val-self.min_val) + self.min_pos)
    
    def draw(self, screen):
        self.update_slider(screen)
        # DISPLAY BAR
        self.green_slider = pygame.transform.scale(green_slider, (self.width, self.height))
        screen.blit(self.green_slider, (self.x_center - self.width/2, self.y_center - self.radius))
        # DISPLAY SLIDER VALUES
        unit_pixels = (self.max_pos - self.min_pos)/(self.max_val-self.min_val)
        for i in range(self.max_val - self.min_val + 1):
            interval = int((self.max_val - self.min_val)/((self.max_pos - self.min_pos)/55))
            if interval == 0:
                interval = 1
            if i%interval == 0:
                print_message(str(i+self.min_val), black, self.min_pos + i*unit_pixels, 
                              self.y_center - self.radius + int(1.3*screen_height/20), 25)
#            pygame.draw.line(screen, black, (self.min_pos + i*unit_pixels, self.y_center - self.radius), 
#                                            (self.min_pos + i*unit_pixels, self.y_center - self.radius + 50))
        # DISPLAY SLIDER
        pygame.draw.circle(screen, dark_green, (self.current_pos, self.y_center), self.radius)
        pygame.draw.circle(screen, white, (self.current_pos, self.y_center), self.radius-3)
        
        
    def update_slider(self, screen):
        rect = pygame.Rect(self.x_center - self.width/2, self.y_center - self.height/2,
                           self.width, self.height)
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]) and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.current_pos = mouse_pos[0]
            self.current_val = (((self.max_val-self.min_val)/(self.max_pos - self.min_pos))*
                                    (self.current_pos-self.min_pos) + self.min_val)
            if self.current_pos < self.min_pos:
                self.current_val = self.min_val
                self.current_pos = self.min_pos
            if self.current_pos > self.max_pos:
                self.current_val = self.max_val
                self.current_pos = self.max_pos
        else:
            self.current_val = round(((self.max_val-self.min_val)/(self.max_pos - self.min_pos))*
                                      (self.current_pos-self.min_pos) + self.min_val)
            self.current_pos = round(((self.max_pos - self.min_pos)/(self.max_val-self.min_val))*
                                      (self.current_val-self.min_val) + self.min_pos) 

#%%
def main_menu():
    pygame.time.wait(200)
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, white, (int(10*screen_width/20), 
                           int(10*screen_height/20)), int(13*screen_height/20))
        print_message('Classic Snake', black, screen_width/2, 5*screen_height/20, 120)
        game_button('Quick game', 60, black, int(screen_width/2), int(7.9*screen_height/20), light_green, green, 300, 3, 6, 3, 13, 13)
        button('Custom Game', 60, black, int(screen_width/2), int(11.1*screen_height/20), light_green, green, custom_game_menu)
        button('Instructions', 60, black, int(screen_width/2), int(14.3*screen_height/20), light_green, green, instructions)
        button('Quit', 60, black, int(screen_width/2), int(17.5*screen_height/20), light_green, green, quit_game)
        music_button(int(13*screen_width/20), int(1.8*screen_height/20), int(2.5*screen_height/20))
        pygame.display.update()

#%%
def instructions():
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, white, (int(10*screen_width/20), 
                           int(10*screen_height/20)), int(13*screen_height/20))
        print_message('Instructions', black, screen_width/2, 5*screen_height/20, 120)
        print_message('Use your mouse to navigate the menu', dark_green, screen_width/2, 8*screen_height/20, 60)
        print_message('Use [Up], [Down], [Left], [Right] to turn', dark_green, screen_width/2, 11*screen_height/20, 60)
        print_message('Press [P] to pause', dark_green, screen_width/2, 14*screen_height/20, 60)
        print_message('Press [Esc] to quit', dark_green, screen_width/2, 17*screen_height/20, 60)
        
        run = back_button(int(7*screen_width/20), int(2*screen_height/20), int(2.5*screen_height/20))
        music_button(int(13*screen_width/20), int(1.8*screen_height/20), int(2.5*screen_height/20))
        pygame.display.update()
           
#%%

class create_wall(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row

class create_fruit(object):    
    def __init__(self, fruit_type):
        self.col = random.randint(1, num_cols)
        self.row = random.randint(1, num_rows)
        self.fruit_type = fruit_type
        
    def draw(self, screen):
        if self.fruit_type == 'apple':
            screen.blit(apple, (cell_position(self.col, self.row)))

class create_obstacle(object):
    def __init__(self):
        self.col = random.randint(1, num_cols)
        self.row = random.randint(1, num_rows)
        self.obstacle_type = random.randint(1, 4)
        
    def draw(self, screen):
        if self.obstacle_type == 1: # ROCK
            screen.blit(rock, (cell_position(self.col, self.row)))
        elif self.obstacle_type == 2: # ROCKS
            screen.blit(rocks, (cell_position(self.col, self.row)))
        elif self.obstacle_type == 3: # TRAP
            screen.blit(trap, (cell_position(self.col, self.row)))
        elif self.obstacle_type == 4: # LAKE
            screen.blit(lake, (cell_position(self.col, self.row)))

class create_animal(object):
    def __init__(self):
        self.col = random.randint(1, num_cols)
        self.row = random.randint(1, num_rows)
        self.animal_type = random.randint(1, 2)
        self.dir = random.randint(1,4)
        
    def draw(self, screen):
        if self.animal_type == 1 and (self.dir == 1 or self.dir == 2): # MONGOOSE RIGHT
            screen.blit(mongoose_right, (cell_position(self.col, self.row)))
        elif self.animal_type == 1 and (self.dir == 3 or self.dir == 4): # MONGOOSE LEFT
            screen.blit(mongoose_left, (cell_position(self.col, self.row)))
        elif self.animal_type == 2 and (self.dir == 1 or self.dir == 4): # EAGLE RIGHT
            screen.blit(eagle_right, (cell_position(self.col, self.row)))
        elif self.animal_type == 2 and (self.dir == 2 or self.dir == 3): # EAGLE LEFT
            screen.blit(eagle_left, (cell_position(self.col, self.row)))   

def cell_position(col, row):
    x = x_field + cell_pixels * (col-1)
    y = y_field + cell_pixels * (row-1)
    return x, y

class snake_part(object): 
    def __init__(self, col_init, row_init):
        self.col = col_init # col corresponds to x axis 
        self.row = row_init # row corresponds to y axis
        self.present_dir = 'right'
        self.future_dir = 'right'
        self.forbidden_direction = 'left'
        self.part_type = 'head_right'
    
    def determine_direction(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LEFT] and not (self.forbidden_direction == 'left'):
            self.future_dir = 'left'
        elif self.keys[pygame.K_RIGHT] and not (self.forbidden_direction == 'right'):
            self.future_dir = 'right'
        elif self.keys[pygame.K_UP] and not (self.forbidden_direction == 'up'):
            self.future_dir = 'up'
        elif self.keys[pygame.K_DOWN] and not (self.forbidden_direction == 'down'):
            self.future_dir = 'down'
    
    def move(self):
        if self.present_dir == 'left':
            self.col -= 1
        elif self.present_dir == 'right':
            self.col += 1
        elif self.present_dir == 'up':
            self.row -= 1
        elif self.present_dir == 'down':
            self.row += 1
                   
    def draw_part(self, screen):
        # head
        if self.part_type == 'head_left':
            screen.blit(head_left, (cell_position(self.col, self.row)))
        elif self.part_type == 'head_right':
            screen.blit(head_right, (cell_position(self.col, self.row)))
        elif self.part_type == 'head_up':
            screen.blit(head_up, (cell_position(self.col, self.row)))
        elif self.part_type == 'head_down':
            screen.blit(head_down, (cell_position(self.col, self.row)))
        
        # straight body
        if self.part_type == 'straight_horizontal':
            screen.blit(straight_horizontal, (cell_position(self.col, self.row)))
        elif self.part_type == 'straight_vertical':
            screen.blit(straight_vertical, (cell_position(self.col, self.row)))
        # turning body
        elif self.part_type == 'turn_up_right':
            screen.blit(turn_up_right, (cell_position(self.col, self.row)))
        elif self.part_type == 'turn_up_left':
            screen.blit(turn_up_left, (cell_position(self.col, self.row)))
        elif self.part_type == 'turn_down_right':
            screen.blit(turn_down_right, (cell_position(self.col, self.row)))
        elif self.part_type == 'turn_down_left':
            screen.blit(turn_down_left, (cell_position(self.col, self.row)))
        # tail
        elif self.part_type == 'tail_left':
            screen.blit(tail_left, (cell_position(self.col, self.row)))
        elif self.part_type == 'tail_right':
            screen.blit(tail_right, (cell_position(self.col, self.row)))
        elif self.part_type == 'tail_up':
            screen.blit(tail_up, (cell_position(self.col, self.row)))
        elif self.part_type == 'tail_down':
            screen.blit(tail_down, (cell_position(self.col, self.row)))

def head_update(part):
    if part.present_dir == 'left':
        part.part_type = 'head_left'
    elif part.present_dir == 'right':
        part.part_type = 'head_right'
    elif part.present_dir == 'up':
        part.part_type = 'head_up'
    elif part.present_dir == 'down':
        part.part_type = 'head_down'

def body_update(part):
    # straight movement
    if (part.present_dir == 'right' and part.future_dir == 'right' or
        part.present_dir == 'left' and part.future_dir == 'left'):
        part.part_type = 'straight_horizontal'
    if (part.present_dir == 'down' and part.future_dir == 'down' or
        part.present_dir == 'up' and part.future_dir == 'up'):
        part.part_type = 'straight_vertical'
    # turn movement
    if (part.present_dir == 'left' and part.future_dir == 'down' or
        part.present_dir == 'up' and part.future_dir == 'right'):
        part.part_type = 'turn_down_right'
    elif (part.present_dir == 'right' and part.future_dir == 'down' or
          part.present_dir == 'up' and part.future_dir == 'left'):
        part.part_type = 'turn_down_left'
    elif (part.present_dir == 'right' and part.future_dir == 'up' or
          part.present_dir == 'down' and part.future_dir == 'left'):
        part.part_type = 'turn_up_left'
    elif (part.present_dir == 'left' and part.future_dir == 'up' or
          part.present_dir == 'down' and part.future_dir == 'right'):
        part.part_type = 'turn_up_right'

def tail_update(snake, part):
    horizontal_movement = snake[len(snake)-2].col - part.col
    vertical_movement = snake[len(snake)-2].row - part.row
    if horizontal_movement == 1:
       part.part_type = 'tail_right' 
    if horizontal_movement == -1:
       part.part_type = 'tail_left' 
    if vertical_movement == 1:
       part.part_type = 'tail_down' 
    if vertical_movement == -1:
       part.part_type = 'tail_up'

def move_snake(new_part):
    if new_part == True:
        snake.append(snake_part(snake[len(snake)-1].col, snake[len(snake)-1].row))
    # determine movement direction
    for index in reversed(range(1, len(snake))):
        snake[index].present_dir = snake[index-1].present_dir
        snake[index].future_dir = snake[index-1].future_dir
    snake[0].present_dir = snake[0].future_dir
    # move all parts of the snake body
    for index, part in enumerate(snake):
        if new_part == False:
            part.move()
        elif not (index == len(snake)-1):
            part.move()
    new_part = False
    # update part_type of all parts of the snake         
    for index, part in enumerate(snake):
        # HEAD PART UPDATE        
        if index == 0:
            head_update(part)         
        # MAIN BODY UPDATE
        if 0 < index < len(snake):
            body_update(part)
        # SUBSTITUTE LAST PIECE WITH TAIL OR ADD A NEW PIECE
        if index == len(snake)-1:
            tail_update(snake, part)
            
    # determine the forbidden moving direction for the future (position of the second part of the snake)
    if len(snake) > 1:
        if snake[0].present_dir == 'right':
           snake[0].forbidden_direction = 'left' 
        if snake[0].present_dir == 'left':
           snake[0].forbidden_direction = 'right' 
        if snake[0].present_dir == 'down':
           snake[0].forbidden_direction = 'up' 
        if snake[0].present_dir == 'up':
           snake[0].forbidden_direction = 'down' 
    return new_part

def move_animals():
    for animal in animals:
        invalid_dir = 1
        correct_dir = False
        possible_dir = [i for i in range(1,5)]
        random.shuffle(possible_dir)
        for direction in possible_dir:
            invalid_dir = 0
            new_animal = create_animal()
            new_animal.col, new_animal.row = animal.col, animal.row
            if direction == 1: # RIGHT
                new_animal.col = animal.col + 1
            elif direction == 2: # DOWN
                new_animal.row = animal.row + 1
            elif direction == 3: # LEFT
                new_animal.col = animal.col - 1
            elif direction == 4: # UP
                new_animal.row = animal.row - 1
            invalid_dir += check_superposition(new_animal, snake)
            invalid_dir += check_superposition(new_animal, fruits)
            invalid_dir += check_superposition(new_animal, obstacles)
            invalid_dir += check_superposition(new_animal, animals)
            invalid_dir += check_superposition(new_animal, walls)
            if invalid_dir == 0:
                correct_dir = True
                correct_col = new_animal.col
                correct_row = new_animal.row
        if correct_dir == True:
            animal.col, animal.row = correct_col, correct_row
            
def check_superposition(element, group):
    invalid_position = 0
    for member in group:
        if member.col == element.col and member.row == element.row:
            invalid_position = 1
    return invalid_position

def generate_walls():
    for col in range(0, num_cols + 1):
        walls.append(create_wall(col, 0))
        walls.append(create_wall(col, num_rows + 1))
    for row in range(1, num_rows):
        walls.append(create_wall(0, row))
        walls.append(create_wall(num_cols + 1, row))
    

# create new fruits only outside of the snake's body
def generate_fruit(fruit_num):
    for i in range(fruit_num):
        invalid_position = 1
        while invalid_position > 0:
            invalid_position = 0
            fruits.append(create_fruit('apple'))
            index = len(fruits)-1
            fruit = fruits[index]
            invalid_position += check_superposition(fruit, snake)
            invalid_position += check_superposition(fruit, obstacles)
            invalid_position += check_superposition(fruit, animals)
            invalid_position += check_superposition(fruit, [x for i,x in enumerate(fruits) if i!=index])
            if invalid_position > 0:
                fruits.pop()

def generate_obstacles(obst_num):
    for i in range(obst_num):
        invalid_position = 1
        while invalid_position > 0:
            invalid_position = 0
            obstacles.append(create_obstacle())
            index = len(obstacles)-1
            obstacle = obstacles[index]
            invalid_position += check_superposition(obstacle, snake)
            invalid_position += check_superposition(obstacle, fruits)
            invalid_position += check_superposition(obstacle, animals)
            invalid_position += check_superposition(obstacle, [x for i,x in enumerate(obstacles) if i!=index])
            if invalid_position > 0:
                obstacles.pop()

def generate_animals(animals_num):
    for i in range(animals_num):
        invalid_position = 1
        while invalid_position > 0:
            invalid_position = 0
            animals.append(create_animal())
            index = len(animals)-1
            animal = animals[index]
            invalid_position += check_superposition(animal, snake)
            invalid_position += check_superposition(animal, fruits)
            invalid_position += check_superposition(animal, obstacles)
            invalid_position += check_superposition(animal, [x for i,x in enumerate(animals) if i!=index])
            if invalid_position > 0:
                animals.pop(index)

# check if the fruit is being eaten and adds a new fruit everytime one is eaten    
def eat_fruit(fruits, snake):
    eaten = False
    for index, fruit in enumerate(fruits):
        if fruit.col == snake[0].col and fruit.row == snake[0].row:
            fruits.pop(index)
            generate_fruit(1)
            eaten = True
    return eaten

def generate_snake(start_col, start_row, end_col, end_row):
    if start_col < end_col:
        start_col, end_col = end_col, start_col
    if start_row < end_row:
        start_row, end_row = end_row, start_row
    col = start_col
    row = start_row
    # generate horizontal parts
    while col > end_col:
        snake.append(snake_part(col, row))
        col -= 1
    # generate vertical parts
    snake.append(snake_part(col, row))
    snake[len(snake)-1].present_dir = 'down'
    snake[len(snake)-1].future_dir = 'right'
    snake[len(snake)-1].part_type = 'turn_up_right'
    while row > end_row:
        row -= 1
        snake.append(snake_part(col, row))
        snake[len(snake)-1].present_dir = 'down'
        snake[len(snake)-1].future_dir = 'down'
        snake[len(snake)-1].part_type = 'straight_vertical' 

def crash_popup(move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows):
    global run_pause
    run_pause = True
    while run_pause:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
        pygame.draw.rect(screen, white, (0, int(screen_height/2 - 230), screen_width, 460))
        print_message('You crashed!', black, screen_width/2, 270, 200)
        print_message('Your body was ' + str(len(snake)) + ' units long!', black, screen_width/2, 400, 80)
        button('Back to menu', 60, black, 400, 520, light_green, green, main_menu)
        game_button('Try Again', 60, black, 900, 520, light_green, green, 
               move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows)
        pygame.display.update()    
    
def check_if_crash(move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows):
    invalid_position = 0
    invalid_position += check_superposition(snake[0], walls)
    invalid_position += check_superposition(snake[0], obstacles)
    invalid_position += check_superposition(snake[0], animals)
    invalid_position += check_superposition(snake[0], [x for i,x in enumerate(snake) if i!=0])
    if invalid_position > 0:
        crash_popup(move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows)
            
def start_countdown(delay): # delay is the total number of seconds it will last
    for i in reversed(range(4)):
        if i == 0:
            count = 'Go!'
        else:
            count = str(i)
        font = pygame.font.SysFont("comicsans", 300, True, False)
        countdown_text = font.render(count, 1, white)
        textRect = countdown_text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(countdown_text, textRect)
        pygame.display.update() 
        pygame.time.wait(delay*250)
        redraw_display()

def initialize_time():
    redraw_display()
    start_countdown(2)
    move_counter = 1
    start_game = pygame.time.get_ticks()
    return move_counter, start_game
            
def clear_field():
    snake.clear()
    fruits.clear()
    walls.clear()
    obstacles.clear()
    animals.clear()
    
def pause_menu():
    global run_pause
    run_pause = True
    while run_pause:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, white, (int(screen_width/2), int(screen_height/2)), 500)
        print_message('Pause', black, int(screen_width/2), int(5*screen_height/20), 120)
        button('Resume', 60, black, int(screen_width/2), int(8*screen_height/20), light_green, green, resume)
        button('Back to menu', 60, black, int(screen_width/2), int(11*screen_height/20), light_green, green, main_menu)
        button('Quit', 60, black, int(screen_width/2), int(14*screen_height/20), light_green, green, quit_confirm)
        pygame.display.update()

def adapt_field(num_cols_1, num_rows_1):
    global field_image, walls_image
    global x_field, y_field, num_cols, num_rows
    num_cols, num_rows = num_cols_1, num_rows_1
    field_image = pygame.transform.scale(field_image, (num_cols*cell_pixels, num_rows*cell_pixels))
    walls_image = pygame.transform.scale(walls_image, ((num_cols+2)*cell_pixels, (num_rows+2)*cell_pixels))
    field_width, field_height = field_image.get_size()
    x_field = int((screen_width - field_width)/2)
    y_field = int((screen_height - field_height)/2)
    return num_cols, num_rows

def start_game(move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows):
    run = True
    new_part = False
    clear_field()
    num_cols, num_rows = adapt_field(num_cols, num_rows)
    generate_snake(random.randint(1,num_cols-1), random.randint(1,num_rows-1), 
                   random.randint(1,num_cols-1), random.randint(1,num_rows-1))
    new_part = move_snake(new_part)
    generate_fruit(fruit_num)
    generate_obstacles(obst_num)
    generate_animals(animal_num)
    generate_walls()
    move_counter, start_game = initialize_time()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            # check for exit event
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
            elif keys_pressed[pygame.K_p]:
                pause_menu()
                move_counter, start_game = initialize_time()
        # move all parts of the snake with regular delay
        snake[0].determine_direction()
        if (pygame.time.get_ticks() - start_game)/move_delay > move_counter:
            move_counter += 1
            move_animals()
            new_part = move_snake(new_part)
            new_part = eat_fruit(fruits, snake)
            
        check_if_crash(move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows)
        redraw_display()
    snake.clear()
    fruits.clear()
    

#%%
def custom_game_menu():
    run = True
    fruit_num = random.randint(1,15)
    obst_num = random.randint(0, 15)
    animal_num = random.randint(0,15)
    speed = random.randint(7,15)
    global num_cols, num_rows
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_ESCAPE]:
                quit_confirm()
        screen.blit(background_image, (0, 0))
        pygame.draw.circle(screen, white, (int(10*screen_width/20), 
                           int(10*screen_height/20)), int(13*screen_height/20))
        print_message('Choose game parameters', black, int(screen_width/2), int(4.5*screen_height/20), 95)
        # VELOCITY SLIDER
        print_message('Movement speed', black, int(6.6*screen_width/20), int(6.5*screen_height/20), 65)
        velocity_slider = create_slider(speed, 1, 15, int(6.6*screen_width/20), int(7.7*screen_height/20), 
                                        int(6.2*screen_width/20), int(0.8*screen_height/20))
        velocity_slider.draw(screen)
        speed = velocity_slider.current_val
        if speed < 8:
            move_delay = 1100 - speed*100
        elif speed < 11:
            move_delay = 700 - speed*50
        else:
            move_delay = 450 - speed*25
        # NUMBER OF FRUITS SLIDER
        print_message('Fruit', black, int(6.6*screen_width/20), int(10*screen_height/20), 65)
        fruit_slider = create_slider(fruit_num, 1, 15, int(6.6*screen_width/20), int(11.2*screen_height/20), 
                                     int(6.2*screen_width/20), int(0.8*screen_height/20))
        fruit_slider.draw(screen)
        fruit_num = fruit_slider.current_val
        # NUMBER OF OBSTACLES SLIDER
        print_message('Obstacles', black, int(6.6*screen_width/20), int(13.5*screen_height/20), 65)
        obstacle_slider = create_slider(obst_num, 0, 15, int(6.6*screen_width/20), int(14.7*screen_height/20), 
                                        int(6.2*screen_width/20), int(0.8*screen_height/20))
        obstacle_slider.draw(screen)
        obst_num = obstacle_slider.current_val
        # NUMBER OF WILD ANIMALS SLIDER
        print_message('Wild animals', black, int(13.4*screen_width/20), int(6.5*screen_height/20), 65)
        animal_slider = create_slider(animal_num, 0, 15, int(13.4*screen_width/20), int(7.7*screen_height/20), 
                                      int(6.2*screen_width/20), int(0.8*screen_height/20))
        animal_slider.draw(screen)
        animal_num = animal_slider.current_val
        # WIDTH OF FIELD SLIDER
        print_message('Field width', black, int(13.4*screen_width/20), int(10*screen_height/20), 65)
        width_slider = create_slider(num_cols, 5, max_num_rows, int(13.4*screen_width/20), int(11.2*screen_height/20), 
                                      int(6.2*screen_width/20), int(0.8*screen_height/20))
        width_slider.draw(screen)
        num_cols = width_slider.current_val
        # HEIGHT OF FIELD SLIDER
        print_message('Field height', black, int(13.4*screen_width/20), int(13.5*screen_height/20), 65)
        height_slider = create_slider(num_rows, 5, max_num_cols, int(13.4*screen_width/20), int(14.7*screen_height/20), 
                                      int(6.2*screen_width/20), int(0.8*screen_height/20))
        height_slider.draw(screen)
        num_rows = height_slider.current_val
        
        game_button('Start game', 50, black, int(screen_width/2), int(18.5*screen_height/20), light_green, green, 
                    move_delay, fruit_num, obst_num, animal_num, num_cols, num_rows)
        
        run = back_button(int(7*screen_width/20), int(2*screen_height/20), int(2.5*screen_height/20))
        music_button(int(13*screen_width/20), int(1.8*screen_height/20), int(2.5*screen_height/20))
        pygame.display.update()

 #%% 
def story_mode():
    pass

#%%       
def main():
    main_menu()
    quit_game()

if __name__ == "__main__":
    main()











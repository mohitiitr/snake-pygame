import pygame
import random
 


 
pygame.font.init()
 
# GLOBALS VARS
s_width = 900 #screen width
s_height = 700 #screen height
play_width = 600  # meaning 600 // 30 = 20 width per block
play_height = 600  # meaning 600 // 30 = 20 height per blo ck
block_size = 20 # block size
 
top_left_x = 50 # top left x of play area
top_left_y = s_height - play_height # top left y of play area
 

 ## GLOBAL SCORE VARS
score = [0,0,0]

# snake details
snake = [(top_left_x + play_width/2 , top_left_y+ play_height/2)]
direction = 1
 
#colors of food that will be generated 
food_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# snake color
snake_color = (11,102,35)#forest green


def draw_text_atXY(text, size, color, surface ,x = play_width/2 ,  y = play_height/2 , isbold = True):
    font = pygame.font.SysFont('comicsans', size, bold=isbold)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x  + x - (label.get_width() / 2), (top_left_y + y- label.get_height()/2)  ))
 

#this takes the y parameter as input to display contents at given y but x is the middle of the screen
def draw_text_atY(text, size, color, surface , y = play_height/2 , isbold = True):
    font = pygame.font.SysFont('comicsans', size, bold=isbold)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), (top_left_y + y- label.get_height()/2)  ))
 


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
 






# this draws the grey coloured lines  
def draw_mesh(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*block_size), (sx + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))  # vertical lines
 
 
 





def draw_window(surface):
    surface.fill((0,0,0))
    # Snake Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('SNAKE', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))# 30 here denotes distance from the top
 
    # for i in range(len(grid)):
    #     for j in range(len(grid[i])):
    #         pygame.draw.rect(surface, grid[i][j], (top_left_x + j* block_size, top_left_y + i * block_size, block_size, block_size), 0)
 
    # draw mesh 
    # IF YOU WANT TO DISABLE / DRAW THE MESH JUST COMMENT / UNCOMMENT THE LINE OF CODE BELOW
    # draw_mesh(surface, 30, 30)
    #border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()
 


def is_next_move_valid(x , y):
    global snake

    if len(snake)>0:
        for index in range(len(snake)-1):
            item = snake[index]
            if x == item[0] and y == item[1]:
                return False

    if ( x >= top_left_x+play_width + 3* block_size )   or (x <= top_left_x + 1 * block_size   ) :
        return False
    if (y >= top_left_y+play_height  - 2* block_size) or (y <= top_left_y - 4 *block_size) :
        return False

    return True              



def make_snake_move(surface):
    global snake
    global direction
    
    # draw_text_middle('make snake move', 50, (255,255,255), win)
    # pygame.display.update()
    # pygame.time.delay(2000)
    # draw_text_middle('make snake move' ,50, (0,0,0), win)

    pygame.display.update()
    #remove last snake block
    item = snake[-1]
    x = item[0]
    y = item[1]
    #enter next snake's loaction
    try :
        item = snake[0]
        x_new = item[0]
        y_new = item[1]
    except :
        x_new = x
        y_new = y
    if direction == 0: # move right
        y_new += block_size
    elif direction == 1: # move up
        x_new -= block_size   
    elif direction == 2 : #move l
        y_new -= block_size
    elif direction == 3 :
        x_new += block_size
    else :# some weired thing happend and we need to check
        x_new+=1
        draw_text_atXY('WARNING', 30, (255, 255, 255), surface ,play_width + 70 ,play_height/2 +70, False)
        draw_text_atXY('direction is '+str(direction), 10, (255, 255, 255), surface ,play_width + 70,play_height/2 +70, False)
    
    
    if is_next_move_valid(x_new , y_new) :


        # draw_text_middle(''+str(x_new) + " " + str(y_new), 50, (255,255,255), win)
        # pygame.display.update()
        # pygame.time.delay(2000)
        # draw_text_middle(''+str(x_new) + " " + str(y_new), 50, (0,0,0), win)

        # add new point to the snake
        snake.insert(0,(x_new , y_new))
        #remove last element in snake
        snake.pop()
        # draw the new snake block on the screen
        pygame.draw.rect(surface, snake_color, ( y_new, x_new, block_size, block_size), 0)     

        # delete the last snake block 
        pygame.draw.rect(surface, (0,0,0), ( y,  x, block_size, block_size), 0)
        
        return True

    return False        




 
def main():
    
    # global score
     # snake this is list which contains the coordinates where snake currently is 
    global snake
    # if direction is 0 (right) , 1(up) , 2(left ) or 3 (down)
    global direction 

   

    # to run the game  
    run = True
    
    # clock variable to render the game
    clock = pygame.time.Clock()

    # time to make snake move
    move_time = 0

    # snakes's speed 
    move_speed = 0.27

    draw_window(win)
    # pygame.draw.rect(win, snake_color, ( top_left_x + 10, top_left_y +10* block_size, block_size, block_size), 0)
    valid = make_snake_move(win)
    # draw_text_middle("valid is " +str(valid), 50, (255,255,255), win)
    # pygame.display.update()
    # pygame.time.delay(2000)
    # draw_text_middle("valid is " +str(valid), 50, (0,0,0), win)

    while run and valid:
        
 
        move_time += clock.get_rawtime()
        clock.tick()
 
        # SNAKE MOVING CODE
        if move_time/1000 >= move_speed:
            move_time = 0
            valid = make_snake_move(win)
            
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 2 # 2 is left
                    

                elif event.key == pygame.K_RIGHT:
                    direction = 0 # 0 is right
                    

                elif event.key == pygame.K_UP:
                    direction = 1 # 1 is up
                    

                if event.key == pygame.K_DOWN:
                    direction = 3 # 3 is down
                    
                valid = make_snake_move(win)
                
 
        
        
        
        
        # draw_text_atXY('Current Score : '+str(score[0]), 35, (255, 255, 255), win ,play_width + 120,play_height/2 +70, False)
        # draw_text_atXY('Best Score : '+str(score[2]), 25, (255, 255, 255), win ,play_width + 120,play_height/2 +90, False)
        # draw_text_atXY('2nd Best Score : '+str(score[1]), 20, (255, 255, 255), win ,play_width + 118,play_height/2 +110, False)
        pygame.display.update()
 
        
 
    
    # score.sort()
    # score[0]=0
    draw_text_middle("You Lost !!", 50, (255,255,255), win)
    snake = [(top_left_x + play_width/2 , top_left_y+ play_height/2)]
    direction = 1
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_atY('Press any key to begin.', 60, (255, 255, 255), win , 100)
        draw_text_atY('Instructions.', 30, (255, 255, 255), win , 150 ,True)
        draw_text_atY('(up arrow key )== change of the shape', 20, (255, 255, 255), win , 180, False)
        draw_text_atY('(left arrow key) == move block left by one unit', 20, (255, 255, 255), win , 200, False)
        draw_text_atY('(right arrow key) == move block right by one unit', 20, (255, 255, 255), win , 220, False)
        draw_text_atY('(down arrow key) == move block down by one unit', 20, (255, 255, 255), win , 240, False)
        draw_text_atY('Version 2.5.3', 15, (255, 255, 255), win , 300, False)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main()
    #testing for this option 
    #pygame.quit()
 
 
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Snake')
 
main_menu()  
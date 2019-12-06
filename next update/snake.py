import pygame
from random import randint
 


 
pygame.font.init()
 
# GLOBALS VARS
s_width = 900 #screen width
s_height = 700 #screen height
play_width = 600  # meaning 600 // 30 = 20 width per block
play_height = 600  # meaning 600 // 30 = 20 height per blo ck
block_size = 20 # block size
 
top_left_x = 60 # top left x of play area
top_left_y = s_height - play_height # top left y of play area
 

 ## GLOBAL SCORE VARS
score = [0,0,0]

# snake details
snake = [(top_left_x + play_width/2 , top_left_y+ play_height/2)]
direction = 1
 
#colors of food that will be generated 
food_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

food = (-1,-1)
is_food_not_there = True

# snake color
snake_color = (11,102,35)#forest green

def is_food_eaten(x,y,surface):
    global food
    global is_food_not_there

    # if (x>= food[0]-block_size and x<= food[0] + block_size) and (y>= food[1]-block_size and y<= food[1] + block_size):
    if x ==food[0] and y == food[1]:
        pygame.draw.rect(surface, (0,0,0), ( food[0], food[1], block_size, block_size), 0) 
        is_food_not_there = True
        return True
    return False    


def check_food_loc_valid(x,y):
    global snake
    for item in snake:
        if x== item[0] and y == item[1]:
            return False
    return True        


def generate_food(surface):
    global is_food_not_there

    x = top_left_x +block_size * randint(1 , 29)
    y = top_left_y +block_size * randint(1 , 29)
    if check_food_loc_valid(x,y) :
        #true means return this food value else generatenew one
        is_food_not_there = False
        pygame.draw.rect(surface, snake_color, ( x, y, block_size, block_size), 0) 
        return (x,y)

    else : 
        return generate_food(surface)  


    



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

    if (  (x >= top_left_x + play_width )  or (x<=top_left_x - 1*block_size)  ) :
        return False
    if ( y >= top_left_y+play_height  ) or (y <= top_left_y - 1*block_size) :
        return False

    return True              

def draw_snake(surface):
	global snake
	for item in snake:
		pygame.draw.rect(surface, snake_color, ( item[0], item[1], block_size, block_size), 0)

		


def make_snake_move(surface):
    global snake
    global direction

    
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
        x_new += block_size
    elif direction == 1: # move up
        y_new -= block_size   
    elif direction == 2 : #move l
        x_new -= block_size
    elif direction == 3 :
        y_new += block_size
    else :# some weired thing happend and we need to check
        x_new+=1
        draw_text_atXY('WARNING', 30, (255, 255, 255), surface ,play_width + 70 ,play_height/2 +70, False)
        draw_text_atXY('direction is '+str(direction), 10, (255, 255, 255), surface ,play_width + 70,play_height/2 +70, False)
    
    
    if is_next_move_valid(x_new , y_new) :


        if  not is_food_eaten(x_new,y_new,surface):
        #     one = 1 # random stuff to make work go
        # else :
            #remove last element in snake
            snake.pop()
            # delete the last snake block 
            pygame.draw.rect(surface, (0,0,0), ( x,  y, block_size, block_size), 0)


        # add new point to the snake
        snake.insert(0,(x_new , y_new))

        
        
        return True

    return False        




 
def main():
    
    # global score
     # snake this is list which contains the coordinates where snake currently is 
    global snake
    # if direction is 0 (right) , 1(up) , 2(left ) or 3 (down)
    global direction 

    global food
    global is_food_not_there

    # to run the game  
    run = True
    
    # clock variable to render the game
    clock = pygame.time.Clock()

    # time to make snake move
    move_time = 0

    # snakes's speed 
    move_speed = 0.27


    is_food_not_there = True
    food_time =0
    food_speed = 1.5 # food will appear after 0.5 seconds after being consumed

    draw_window(win)
    # pygame.draw.rect(win, snake_color, ( top_left_x + 10, top_left_y +10* block_size, block_size, block_size), 0)
    valid = make_snake_move(win)
    # draw_text_middle("valid is " +str(valid), 50, (255,255,255), win)
    # pygame.display.update()
    # pygame.time.delay(2000)
    # draw_text_middle("valid is " +str(valid), 50, (0,0,0), win)


    # pygame.draw.rect(win, snake_color, ( top_left_x + 10*block_size, top_left_y +20* block_size, block_size, block_size), 0)
    # pygame.draw.rect(win, (255,0,0), ( top_left_x + 11*block_size, top_left_y +20* block_size, block_size, block_size), 0)
    


    while run and valid:
        
 		
        move_time += clock.get_rawtime()
        food_time += clock.get_rawtime()
        clock.tick()
        
        # FOOD APPEARING CODE
        if food_time/1000 >= food_speed:
            food_time =0
            if is_food_not_there :
                food = generate_food(win)
                is_food_not_there = False



        # SNAKE MOVING CODE
        if move_time/1000 >= move_speed:
            move_time = 0
            valid = make_snake_move(win)
            draw_snake(win)
            
    
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
                draw_snake(win)
 
        # draw_mesh(win , 30 ,30)
        
        
        
        # draw_text_atXY('Current Score : '+str(score[0]), 35, (255, 255, 255), win ,play_width + 120,play_height/2 +70, False)
        # draw_text_atXY('Best Score : '+str(score[2]), 25, (255, 255, 255), win ,play_width + 120,play_height/2 +90, False)
        # draw_text_atXY('2nd Best Score : '+str(score[1]), 20, (255, 255, 255), win ,play_width + 118,play_height/2 +110, False)
        pygame.display.update()
 
        
 
    
    # score.sort()
    # score[0]=0
    draw_text_middle("You Lost !!", 50, (255,255,255), win)
    snake = [(top_left_x + play_width/2 , top_left_y+ play_height/2)]
    direction = 1
    food = (-1,-1)
    is_food_not_there = True
    pygame.display.update()
    pygame.time.delay(2000)
 
 
# def main_menu():
#     run = True
#     while run:
#         win.fill((0,0,0))
#         draw_text_atY('Press any key to begin.', 60, (255, 255, 255), win , 100)
#         draw_text_atY('Instructions.', 30, (255, 255, 255), win , 150 ,True)
#         draw_text_atY('(up arrow key )== move up', 20, (255, 255, 255), win , 180, False)
#         draw_text_atY('(left arrow key) == move left', 20, (255, 255, 255), win , 200, False)
#         draw_text_atY('(right arrow key) == move right', 20, (255, 255, 255), win , 220, False)
#         draw_text_atY('(down arrow key) == move down', 20, (255, 255, 255), win , 240, False)
#         draw_text_atY('Version 2.5.3', 15, (255, 255, 255), win , 300, False)
        
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
 
#             if event.type == pygame.KEYDOWN:
#                 main()
#     #testing for this option 
#     #pygame.quit()



def display_instructions(win):
    win.fill( (0,0,0)  )
    draw_text_atY('Instructions.', 40, (255, 255, 255), win , 120 ,True)
    draw_text_atY('(up arrow key )== move up', 30, (255, 255, 255), win , 160, False)
    draw_text_atY('(left arrow key) == move left', 30, (255, 255, 255), win, 200, False)
    draw_text_atY('(right arrow key) == move right', 30, (255, 255, 255), win , 240, False)
    draw_text_atY('(down arrow key) == move down', 30, (255, 255, 255), win , 280, False)
    pygame.display.update()




def display_about(win):
    win.fill( (0,0,0) )
    draw_text_atY('Version 2.7.4', 15, (255, 255, 255), win , 300, False)
    draw_text_atY("Designed with love by Mohit Kumar ",30 , (255,255,255) , win , 160 ,False)
    draw_text_atY("For young developers so that they can :",20 , (255,255,255) , win , 190 ,False)
    draw_text_atY("learn from examples",20 , (255,255,255) , win , 210 ,False)
    draw_text_atY("and even play too",20 , (255,255,255) , win , 230 ,False)   
    draw_text_atY('my github handle @mohitiitr', 30 ,(255,255,255) , win , 270,False) 
    pygame.display.update()

    



def display_menu(win , index ):
    win.fill((0,0,0))
    if index == 0:
        draw_text_atY('Start Game', 60, (21,239,232), win , 100)
        draw_text_atY('Instructions', 50, (255, 255, 255), win , 200)
        draw_text_atY('About Game', 50, (255, 255, 255), win , 300)
    elif index == 1:
        draw_text_atY('Start Game', 50, (255, 255, 255), win , 100)
        draw_text_atY('Instructions', 60,(21,239,232), win , 200)
        draw_text_atY('About Game', 50, (255, 255, 255), win , 300)      
    elif index == 2 :    
        draw_text_atY('Start Game', 50, (255, 255, 255), win , 100)
        draw_text_atY('Instructions', 50, (255, 255, 255), win , 200)
        draw_text_atY('About Game', 60 ,(21,239,232), win , 300)
    else :
        draw_text_atY('Index error index is ' + str(index), 50, (255, 255, 255), win , 100)    
    pygame.display.update()
     




def main_menu():
    global win
    run = True
    index = 0
    display_menu(win,index)
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    index = (index-1 )%3
                    if (index<0):
                        index+=3
                    display_menu(win,index)

                elif event.key == pygame.K_DOWN:
                    index = (index+1 )%3
                    display_menu(win,index)

                elif event.key == pygame.K_RETURN:  
                    if index == 0 :
                        main()
                    elif index == 1:
                        display_instructions(win)
                        pygame.time.delay(5000)
                        index = 0
                    elif index == 2:
                        display_about(win)
                        pygame.time.delay(5000)
                        index = 0    
                    display_menu(win,index)    
                            

    #testing for this option 
    #pygame.quit()
 

 
 
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Snake')
 
main_menu()  
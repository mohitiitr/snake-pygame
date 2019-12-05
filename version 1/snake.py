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
    # IF YOU WANT TO DISABLE THE MESH JUST COMMENT THE LINE OF CODE BELOW
    draw_mesh(surface, 30, 30)
    #border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()
 
 
def main():
    global grid
    global score
    
    # if direction is 0 (right) , 1(up) , 2(left ) or 3 (down)
    direction = 1

    # snake this is list which contains the coordinates where snake currently is 
    snake = [(top_left_x + play_width/2 , top_left_y+ play_height/2)]
    

    # to run the game  
    run = True
    
    # clock variable to render the game
    clock = pygame.time.Clock()

    # time to make snake move
    move_time = 0
    
    # snakes's speed 
    move_speed = 0.27

    while run:
        
 
        move_time += clock.get_rawtime()
        clock.tick()
 
        # PIECE moveING CODE
        if move_time/1000 >= move_speed:
            move_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
 
                '''if event.key == pygame.K_SPACE:
                   while valid_space(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
                   print(convert_shape_format(current_piece))'''  # todo fix
 
        shape_pos = convert_shape_format(current_piece)
 
        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                snake[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
 
            # call four times to check for multiple clear rows
            score[0] +=  clear_rows(grid, snake)*10
        
        draw_window(win)
        draw_next_shape(next_piece, win)
        draw_text_atXY('Current Score : '+str(score[0]), 35, (255, 255, 255), win ,play_width + 120,play_height/2 +70, False)
        draw_text_atXY('Best Score : '+str(score[2]), 25, (255, 255, 255), win ,play_width + 120,play_height/2 +90, False)
        draw_text_atXY('2nd Best Score : '+str(score[1]), 20, (255, 255, 255), win ,play_width + 118,play_height/2 +110, False)
        pygame.display.update()
 
        # Check if user lost
        if check_lost(snake):
            run = False
 
    draw_text_middle("You Lost !!", 50, (255,255,255), win)
    score.sort()
    score[0]=0
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
pygame.display.set_caption('Tetris')
 
main_menu()  
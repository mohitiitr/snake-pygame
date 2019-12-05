import pygame
import random
 


 
pygame.font.init()
 
# GLOBALS VARS
s_width = 900
s_height = 700
play_width = 600  # meaning 600 // 30 = 20 width per block
play_height = 600  # meaning 600 // 30 = 20 height per blo ck
block_size = 20
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 

 ## GLOBAL SCORE VARS
score = [0,0,0]
 

snake_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
 
# class Piece(object):
#     rows = 20  # y
#     columns = 10  # x
 
#     def __init__(self, column, row, shape):
#         self.x = column
#         self.y = row
#         self.shape = shape
#         self.color = shape_colors[shapes.index(shape)]
#         self.rotation = 0  # number from 0-3
 
 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 

 
 
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True


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
 
 
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*block_size), (sx + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))  # vertical lines
 

 
# def draw_next_shape(shape, surface):
#     font = pygame.font.SysFont('comicsans', 30)
#     label = font.render('Next Shape', 1, (255,255,255))
 
#     sx = top_left_x + play_width + 50
#     sy = top_left_y + play_height/2 - 100
#     format = shape.shape[shape.rotation % len(shape.shape)]
 
#     for i, line in enumerate(format):
#         row = list(line)
#         for j, column in enumerate(row):
#             if column == '0':
#                 pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
#     surface.blit(label, (sx + 10, sy- 30))
 
 
def draw_window(surface):
    surface.fill((0,0,0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('SNAKE', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()
 
 
def main():
    global grid
    global score
 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
 
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
 
    while run:
        fall_speed = 0.27
 
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
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
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
 
            # call four times to check for multiple clear rows
            score[0] +=  clear_rows(grid, locked_positions)*10
        
        draw_window(win)
        draw_next_shape(next_piece, win)
        draw_text_atXY('Current Score : '+str(score[0]), 35, (255, 255, 255), win ,play_width + 120,play_height/2 +70, False)
        draw_text_atXY('Best Score : '+str(score[2]), 25, (255, 255, 255), win ,play_width + 120,play_height/2 +90, False)
        draw_text_atXY('2nd Best Score : '+str(score[1]), 20, (255, 255, 255), win ,play_width + 118,play_height/2 +110, False)
        pygame.display.update()
 
        # Check if user lost
        if check_lost(locked_positions):
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
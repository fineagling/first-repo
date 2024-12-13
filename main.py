import pygame, sys, time
from engine import Button
from random import choice
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator and Solver")
menu_backGround = pygame.image.load("assets/backgroundv2.png")
game_backGround = pygame.image.load("assets/play_background.png")
red = pygame.Color(255,0,0)
black = pygame.Color(0,0,0)
green = pygame.Color(0,255,0)
white = pygame.Color(255,255,255)
colour_input_active = pygame.Color("lightskyblue3")
colour_input_passive = pygame.Color("black")
colour = colour_input_passive
active = False
run = True
RES = SCREEN_WIDTH, SCREEN_HEIGHT
TILE = 60
collums = 900 // TILE
rows = 700 // TILE
clock = pygame.time.Clock()
distance_from_corner_x = 300
distance_from_corner_y = 10
global visited_origin
visited_origin = 0
maze_complete = False
TILE_number_x = 0
TILE_number_y = 0
user_text = ""
input_size_rect = pygame.Rect(30,430,140,50)
is_text_inputted = False
is_input_full = False
TILE_changed_value = 0
start_coordinate = []
end_coordinate = []
maze_clicked_number = 0
def TILE_change(TILE, user_text, collums, rows):
    TILE = (1901/99) + ((79/99) * (int(user_text)))
    collums = 900 // TILE
    rows = 700 // TILE
    return TILE_changed_value

def get_font(size):
    return pygame.font.Font("assets/GamePlayed.ttf", size)

def one_player(run):
    class Cell:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {"top": True, "right": True, "bottom": True, "left": True}
            self.visited = False
            self.thickness = 1
    
        def draw_current_cell(self, visited_origin):
            x, y = self.x * TILE, self.y * TILE
            if x == 0 and y == 0:
                visited_origin = visited_origin + 1            
            
            if visited_origin == 0:
                pygame.draw.rect(screen, pygame.Color("yellow"), (x + self.thickness + distance_from_corner_x, y + self.thickness + distance_from_corner_y, TILE - self.thickness, TILE - self.thickness)) 
           

        def draw(self):
            x, y = (self.x * TILE) + distance_from_corner_x, (self.y * TILE) + distance_from_corner_y
            tile_number_pos = [(TILE_number_x - 1), (TILE_number_y - 1)]
            coordinates_pos = [self.x, self.y]
            
            global maze_clicked_number, start_coordinate, end_coordinate
            if self.visited and (tile_number_pos != coordinates_pos):
                pygame.draw.rect(screen, pygame.Color("black"), (x, y, TILE, TILE))
            else:
                if maze_clicked_number == 1:                  
                    pygame.draw.rect(screen, pygame.Color("green"), (distance_from_corner_x + ((TILE_number_x - 1) * TILE), distance_from_corner_y + ((TILE_number_y-1) * TILE), TILE, TILE) )
                    start_coordinate = coordinates_pos
                if maze_clicked_number == 2:
                    pygame.draw.rect(screen, pygame.Color("green"), (distance_from_corner_x + ((TILE_number_x - 1) * TILE), distance_from_corner_y + ((TILE_number_y-1) * TILE), TILE, TILE) )
                    end_coordinate = coordinates_pos
                if maze_clicked_number >= 3:
                    pygame.draw.rect(screen, pygame.Color("black"), (x, y, TILE, TILE))

            if self.walls["top"]:
                pygame.draw.line(screen, pygame.Color("red"), (x, y), (x + TILE, y), self.thickness)
            if self.walls["bottom"]:
                pygame.draw.line(screen, pygame.Color("red"), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
            if self.walls["left"]:
                pygame.draw.line(screen, pygame.Color("red"), (x, y + TILE), (x, y), self.thickness)
            if self.walls["right"]:
                pygame.draw.line(screen, pygame.Color("red"), (x + TILE, y), (x + TILE, y + TILE), self.thickness)

        def check_cell(self, x, y):
            find_index = lambda x, y: x + y * collums
            if x < 0 or x > collums - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cells[find_index(x, y)]
         
        def check_neighbours(self):
            neighbours = []
            top = self.check_cell(self.x, self.y - 1)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)
            right = self.check_cell(self.x + 1, self.y)
            if top and not top.visited:
                neighbours.append(top)
            if bottom and not bottom.visited:
                neighbours.append(bottom)
            if left and not left.visited:
                neighbours.append(left)
            if right and not right.visited:
                neighbours.append(right)
            return choice(neighbours) if neighbours else False

        def make_array_of_dictionaries(self):
            dictionaries_array = []
            for i in range(rows):
                array_per_row = []
                for j in range(collums):
                    array_per_row.append(self.walls)
                dictionaries_array.append(array_per_row)
            return dictionaries_array
            #doesnt quite work but getting there need to make 2d array instead
            #intead need to do something like dictionaries_aray = [[0 for i in range(colums)] for j in range(rows)]
            #then try the rest of the code but addapt it, use the i loop to hold data for each row using the array[][0] part and the j loop to alter the array[0][] part 
            #use self.x and self.y to add each dictionary to the position that is specified by the statement at the start of BFS, don't need to make an i and j loop
            #use dictionaries_array[self.x][self.y] = self.walls
            

    
       
    def check_if_mouse_in_maze(position):
        if position[0] in range(distance_from_corner_x, (collums * TILE) + distance_from_corner_x) and position[1] in range(distance_from_corner_y, (rows * TILE) + distance_from_corner_y):  
            return True
        
    def gather_tile_number(position):
        global TILE_number_x
        TILE_number_x = (position[0] - (distance_from_corner_x - TILE))//TILE
        global TILE_number_y
        TILE_number_y = (position[1]-(distance_from_corner_y - TILE))//TILE
    
    def remove_walls(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls["left"] = False
            next.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next.walls["left"] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls["top"] = False
            next.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next.walls["top"] = False

    grid_cells = [Cell(col, row) for row in range(rows) for col in range(collums)]
    current_cell = grid_cells[0]
    stack = []
    
    def breadth_first_search(start_coordinate, end_coordinate):
        array_of_possible_cells = [Cell.make_array_of_dictionaries() for Cell in grid_cells] 
        print(array_of_possible_cells)
        #semi working
        
   
   
   
   
    while run:
        screen.fill("#2a0807")
        one_play_mouse_pos = pygame.mouse.get_pos()
        ONE_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(50), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
        global maze_complete, active, user_text, colour, is_text_inputted, is_input_full, maze_clicked_number

        for button in [ONE_PLAY_BACK]:
            button.changecolour(one_play_mouse_pos)
            button.text_update(screen)

        pygame.draw.rect(screen, colour, input_size_rect)
        input_text_surface = get_font(32).render(user_text, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_size_rect.x + 5, input_size_rect.y + 5))
        input_size_rect.w = max(100, input_text_surface.get_width() + 10)        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONE_PLAY_BACK.checkforinput(one_play_mouse_pos):
                    main_menu()
                if maze_complete and check_if_mouse_in_maze(one_play_mouse_pos) and maze_clicked_number <= 2:
                    gather_tile_number(one_play_mouse_pos)
                    maze_clicked_number = maze_clicked_number + 1
                    breadth_first_search(start_coordinate, end_coordinate)
                if input_size_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN and event.unicode.isdigit():               
                is_text_inputted = True
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif len(user_text) <= 1:
                    user_text += event.unicode
                else:
                    TILE_change(TILE, user_text, collums, rows)
                    #if TILE == TILE_changed_value:
                    is_input_full = True
                    
                     
        
        if is_text_inputted and is_input_full:
            [Cell.draw() for Cell in grid_cells]
            current_cell.visited = True
            current_cell.draw_current_cell(visited_origin)

            next_cell = current_cell.check_neighbours()
            if next_cell:
                next_cell.visited = True
                stack.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()
            elif next_cell == False:
                maze_complete = True
            
        if active:
            colour = colour_input_active
        else:
            colour = colour_input_passive

        pygame.draw.rect(screen, colour, input_size_rect)
        input_text_surface = get_font(32).render(user_text, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_size_rect.x + 5, input_size_rect.y + 5))
        input_size_rect.w = max(140, input_text_surface.get_width() + 10)     
        
        clock.tick(200000)
        pygame.display.update()
        
def two_player(run):  
    while run:
        screen.fill("#2a0807")
        two_play_mouse_pos = pygame.mouse.get_pos()
        TWO_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(50), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
        for button in [TWO_PLAY_BACK]:
            button.changecolour(two_play_mouse_pos)
            button.text_update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TWO_PLAY_BACK.checkforinput(two_play_mouse_pos):
                    main_menu()
    
        pygame.display.update()

def main_menu():
    while run == True:
        screen.blit(menu_backGround, (0,0))
        menu_mouse_pos = pygame.mouse.get_pos()
        heading_main_menu_text = get_font(180).render("MAZE", True, "#b68f40")
        menu_rect = heading_main_menu_text.get_rect(center=(640,100))
        ONE_PLAYER_BUTTON = Button(pos=(640,250), button_font=get_font(60), base_colour= white, hovering_colour="#d7fcd4", input_text="1 PLAYER", image=None, x_start=475, y_start=200, x_end=780, y_end=300)
        TWO_PLAYER_BUTTOM = Button(pos=(640,400), button_font=get_font(60), base_colour=white, hovering_colour="#d7fcd4", input_text="2 PLAYER", image=None, x_start=475, y_start=350, x_end=780, y_end=450) 
        QUIT_BUTTON = Button(pos=(640,550), button_font=get_font(60), base_colour=white, hovering_colour="#d7fcd4", input_text="QUIT", image=None, x_start=475, y_start=500, x_end=780, y_end=600) 
        screen.blit(heading_main_menu_text, menu_rect)
        for button in [ONE_PLAYER_BUTTON, TWO_PLAYER_BUTTOM, QUIT_BUTTON]:
            button.changecolour(menu_mouse_pos)
            button.text_update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONE_PLAYER_BUTTON.checkforinput(menu_mouse_pos):
                    one_player(run)
                if TWO_PLAYER_BUTTOM.checkforinput(menu_mouse_pos):
                    two_player(run)
                if QUIT_BUTTON.checkforinput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
main_menu()


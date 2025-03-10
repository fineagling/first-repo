import pygame, sys
from engine import Button
from random import choice
from collections import deque
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
run = True
RES = SCREEN_WIDTH, SCREEN_HEIGHT
cell_size = 40
collums = 900 // cell_size
rows = 700 // cell_size
clock = pygame.time.Clock()
distance_from_corner_x = 300
distance_from_corner_y = 10
global visited_origin
visited_origin = 0
active = False
maze_complete = False
cell_size_number_x = 0
cell_size_number_y = 0
user_text = ""
input_size_rect = pygame.Rect(30,430,140,50)
colour_input_active = pygame.Color("lightskyblue3")
colour_input_passive = pygame.Color("black")
colour = colour_input_passive
is_text_inputted = False
is_input_full = False
cell_size_changed_value = 0
start_coordinate = []
end_coordinate = []
maze_clicked_number = 0
dictionaries_array = [[0 for i in range(rows)] for j in range(collums)]
breadth_first_search_complete = False
global queue
queue = deque()
global cycles
cycles = 0
global path_list
path_list = []
def cell_size_change(cell_size, user_text, collums, rows):
    cell_size_changed_value = (1901/99) + ((79/99) * (int(user_text)))
    cell_size = cell_size_changed_value   
    collums = 900 // cell_size
    rows = 700 // cell_size

def get_font(size):
    return pygame.font.Font("assets/GamePlayed.ttf", size)

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"north": True, "east": True, "south": True, "west": True}
        self.visited = False
        self.thickness = 1
    
    def draw_current_cell(self, visited_origin):
        x, y = self.x * cell_size, self.y * cell_size
        if x == 0 and y == 0:
            visited_origin = visited_origin + 1            
            
        if visited_origin == 0:
            pygame.draw.rect(screen, pygame.Color("yellow"), (x + self.thickness + distance_from_corner_x, y + self.thickness + distance_from_corner_y, cell_size - self.thickness, cell_size - self.thickness)) 
           
    def draw(self):
        x, y = (self.x * cell_size) + distance_from_corner_x, (self.y * cell_size) + distance_from_corner_y
        cell_number_pos = [(cell_size_number_x - 1), (cell_size_number_y - 1)]
        coordinates_pos = [self.x, self.y]
            
        global maze_clicked_number, start_coordinate, end_coordinate
        if self.visited and (cell_number_pos != coordinates_pos):
            pygame.draw.rect(screen, pygame.Color("black"), (x, y, cell_size, cell_size))
        else:
            if maze_clicked_number == 1:                  
                pygame.draw.rect(screen, pygame.Color("green"), (distance_from_corner_x + ((cell_size_number_x - 1) * cell_size), distance_from_corner_y + ((cell_size_number_y - 1) * cell_size), cell_size, cell_size) )
                start_coordinate = coordinates_pos
            if maze_clicked_number == 2:
                pygame.draw.rect(screen, pygame.Color("green"), (distance_from_corner_x + ((cell_size_number_x - 1) * cell_size), distance_from_corner_y + ((cell_size_number_y - 1) * cell_size), cell_size, cell_size) )
                end_coordinate = coordinates_pos
            if maze_clicked_number >= 3:
                pygame.draw.rect(screen, pygame.Color("black"), (x, y, cell_size, cell_size))

        if self.walls["north"]:
            pygame.draw.line(screen, pygame.Color("red"), (x, y), (x + cell_size, y), self.thickness)
        if self.walls["south"]:
            pygame.draw.line(screen, pygame.Color("red"), (x + cell_size, y + cell_size), (x, y + cell_size), self.thickness)
        if self.walls["west"]:
            pygame.draw.line(screen, pygame.Color("red"), (x, y + cell_size), (x, y), self.thickness)
        if self.walls["east"]:
            pygame.draw.line(screen, pygame.Color("red"), (x + cell_size, y), (x + cell_size, y + cell_size), self.thickness)

    def check_cell(self, x, y):
        find_position_in_list = lambda x, y: x + y * collums
        if x < 0 or x > collums - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_position_in_list(x, y)]
         
    def check_neighbours(self):
        neighbours = []
        north = self.check_cell(self.x, self.y - 1)
        south = self.check_cell(self.x, self.y + 1)
        west = self.check_cell(self.x - 1, self.y)
        east = self.check_cell(self.x + 1, self.y)
        if north and not north.visited:
            neighbours.append(north)
        if south and not south.visited:
            neighbours.append(south)
        if west and not west.visited:
            neighbours.append(west)
        if east and not east.visited:
            neighbours.append(east)
        return choice(neighbours) if neighbours else False

    def make_array_of_dictionaries(self):
        self.walls["x"] = self.x
        self.walls["y"] = self.y
        self.walls["prev_x"] = 0
        self.walls["prev_y"] = 0
        return self.walls

    def reset(self):
        self.visited = False  
        self.walls["north"] = True
        self.walls["south"] = True
        self.walls["east"] = True
        self.walls["west"] = True
        
def check_if_mouse_in_maze(position):
    if position[0] in range(distance_from_corner_x, (collums * cell_size) + distance_from_corner_x) and position[1] in range(distance_from_corner_y, (rows * cell_size) + distance_from_corner_y):  
        return True
        
def gather_cell_number(position):
    global cell_size_number_x
    cell_size_number_x = (position[0] - (distance_from_corner_x - cell_size))//cell_size
    global cell_size_number_y
    cell_size_number_y = (position[1]-(distance_from_corner_y - cell_size))//cell_size
    
def remove_walls(current, next):
    change_in_x = current.x - next.x
    if change_in_x == 1:
        current.walls["west"] = False
        next.walls["east"] = False
    elif change_in_x == -1:
        current.walls["east"] = False
        next.walls["west"] = False
    change_in_y = current.y - next.y
    if change_in_y == 1:
        current.walls["north"] = False
        next.walls["south"] = False
    elif change_in_y == -1:
        current.walls["south"] = False
        next.walls["north"] = False

grid_cells = [Cell(col, row) for row in range(rows) for col in range(collums)]
current_cell = grid_cells[0]
stack = []

def breadth_first_search_variables(start_coordinate, end_coordinate):
    global array_of_possible_cells
    array_of_possible_cells = deque()
    array_of_possible_cells = [Cell.make_array_of_dictionaries() for Cell in grid_cells]
    global start_walls
    start_walls = (array_of_possible_cells[(start_coordinate[0] + (start_coordinate[1] * collums))])
    global end_walls
    end_walls = (array_of_possible_cells[(end_coordinate[0] + (end_coordinate[1] * collums))])
    global visited
    visited = deque()

def BFS_check_neighbours(breadth_current_cell):
        if breadth_current_cell['north'] == False:
            x_temp_1 = breadth_current_cell['x']
            y_temp_1 = breadth_current_cell['y']
            child_cell_1 = array_of_possible_cells[((y_temp_1 * collums) + (x_temp_1)) - collums]
            if child_cell_1 not in visited:
                child_cell_1["prev_x"] = child_cell_1["x"]
                child_cell_1["prev_y"] = child_cell_1["y"] + 1
                queue.append(child_cell_1)
        if breadth_current_cell['south'] == False:
            x_temp_2 = breadth_current_cell['x']
            y_temp_2 = breadth_current_cell['y']                
            child_cell_2 = array_of_possible_cells[((y_temp_2 * collums) + (x_temp_2)) + collums]
            if child_cell_2 not in visited:
                child_cell_2["prev_x"] = child_cell_2["x"]
                child_cell_2["prev_y"] = child_cell_2["y"] - 1
                queue.append(child_cell_2)
        if breadth_current_cell['east'] == False:
            x_temp_3 = breadth_current_cell['x']
            y_temp_3 = breadth_current_cell['y']                
            child_cell_3 = array_of_possible_cells[((y_temp_3 * collums) + (x_temp_3)) + 1]
            if child_cell_3 not in visited:
                child_cell_3["prev_x"] = child_cell_3["x"] - 1
                child_cell_3["prev_y"] = child_cell_3["y"]
                queue.append(child_cell_3)
        if breadth_current_cell['west'] == False:
            x_temp_4 = breadth_current_cell['x']
            y_temp_4 = breadth_current_cell['y']                
            child_cell_4 = array_of_possible_cells[((y_temp_4 * collums) + (x_temp_4)) - 1]
            if child_cell_4 not in visited:
                child_cell_4["prev_x"] = child_cell_4["x"] + 1
                child_cell_4["prev_y"] = child_cell_4["y"]
                queue.append(child_cell_4)  

def display_default_image():
    default_maze = pygame.image.load("assets/default_maze.png")
    screen.blit(default_maze, (distance_from_corner_x, distance_from_corner_y))
    pygame.display.update()

def one_player(run, current_cell):
    number_of_run_loops = 0
    search_complete = False
    while run:
        screen.fill("#2a0807")
        one_play_mouse_pos = pygame.mouse.get_pos()
        ONE_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(50), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
        global maze_complete, active, user_text, colour, is_text_inputted, is_input_full, maze_clicked_number
        for button in [ONE_PLAY_BACK]:
            button.changecolour(one_play_mouse_pos)
            button.text_update(screen)
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ONE_PLAY_BACK.checkforinput(one_play_mouse_pos):
                    main_menu()
                if maze_complete and check_if_mouse_in_maze(one_play_mouse_pos) and maze_clicked_number <= 2:
                    gather_cell_number(one_play_mouse_pos)
                    maze_clicked_number = maze_clicked_number + 1
                if maze_clicked_number == 3:
                    breadth_first_search_variables(start_coordinate, end_coordinate)  
                    number_of_run_loops = number_of_run_loops + 1
                    if number_of_run_loops == 1:
                        queue.append(start_walls)
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
                    cell_size_change(cell_size, user_text, collums, rows)
                    is_input_full = True
            
        if is_input_full == False:
                display_default_image()    
        
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

        while len(queue) > 0 and search_complete != True:
            breadth_current_cell = queue.popleft()
            if breadth_current_cell == end_walls:
                pygame.draw.rect(screen, pygame.Color("blue"), ((cell_size * breadth_current_cell['x']) + 1 + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + 1 + distance_from_corner_y, cell_size - 1, cell_size - 1))
                search_complete = True
                [Cell.draw() for Cell in grid_cells]
                break
            BFS_check_neighbours(breadth_current_cell)
            visited.append(breadth_current_cell)
            pygame.draw.rect(screen, pygame.Color("blue"), ((cell_size * breadth_current_cell['x']) + 1 + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + 1 + distance_from_corner_y, cell_size - 1, cell_size - 1))
            pygame.display.update()

        if search_complete == True:
            while breadth_current_cell != start_walls:
                previous_temp_x = breadth_current_cell["prev_x"]
                previous_temp_y = breadth_current_cell["prev_y"]
                pygame.draw.rect(screen, pygame.Color("yellow"), ((cell_size * breadth_current_cell['x']) + (cell_size/4) + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + (cell_size/4) + distance_from_corner_y, cell_size - (cell_size//2), cell_size - (cell_size//2)))
                next_cell_check = array_of_possible_cells[((breadth_current_cell["y"] * collums) + (breadth_current_cell["x"])) + ((previous_temp_y - breadth_current_cell["y"]) * collums) + (previous_temp_x - breadth_current_cell["x"])]
                breadth_current_cell = next_cell_check        
                pygame.draw.rect(screen, pygame.Color("green"), ((cell_size * start_walls['x']) + ((2*cell_size)//10) + distance_from_corner_x, ( cell_size * start_walls['y']) + ((2*cell_size)//10) + distance_from_corner_y, cell_size - ((2*cell_size)//5), cell_size - ((2*cell_size)//5)))
            pygame.display.update() 
            pygame.time.wait(6000)
            [Cell.reset() for Cell in grid_cells]
            maze_clicked_number = 0
            maze_complete = False
            user_text = user_text[:-2]
            is_text_inputted = False
            is_input_full = False
            one_player(run, current_cell)

        pygame.draw.rect(screen, colour, input_size_rect)
        input_text_surface = get_font(32).render(user_text, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_size_rect.x + 5, input_size_rect.y + 5))
        input_size_rect.w = max(140, input_text_surface.get_width() + 10)     
        info_text_line_1 = get_font(13).render("input a maze size, and when the maze", True, "#b68f40")
        info_rect_line_1 = info_text_line_1.get_rect(center=(150,30))   
        info_text_line_2 = get_font(13).render("has generated, click two points on the", True, "#b68f40")
        info_rect_line_2 = info_text_line_2.get_rect(center=(150,50))
        info_text_line_3 = get_font(13).render("maze and watch the magic happen", True, "#b68f40")
        info_rect_line_3 = info_text_line_3.get_rect(center=(150,70))     
        input_box_text = get_font(11).render("input a number between 1-99", True, "#b68f40")
        input_box_rect = input_box_text.get_rect(center=(100,420)) 
        screen.blit(info_text_line_1, info_rect_line_1)
        screen.blit(info_text_line_2, info_rect_line_2)
        screen.blit(info_text_line_3, info_rect_line_3)
        screen.blit(input_box_text, input_box_rect)
        clock.tick(2000)
        pygame.display.update()
        
def two_player(run, current_cell): 
    number_of_run_loops = 0
    search_complete = False 
    while run:
        screen.fill("#2a0807")
        two_play_mouse_pos = pygame.mouse.get_pos()
        TWO_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(50), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
        global maze_complete, active, user_text, colour, is_text_inputted, is_input_full, maze_clicked_number
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
                if maze_complete and check_if_mouse_in_maze(two_play_mouse_pos) and maze_clicked_number <= 2:
                    gather_cell_number(two_play_mouse_pos)
                    maze_clicked_number = maze_clicked_number + 1
                if maze_clicked_number == 3:
                    breadth_first_search_variables(start_coordinate, end_coordinate)  
                    number_of_run_loops = number_of_run_loops + 1
                    if number_of_run_loops == 1:
                        queue.append(start_walls)
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
                    cell_size_change(cell_size, user_text, collums, rows)
                    is_input_full = True
            
        if is_input_full == False:
                display_default_image()    
        
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

        while len(queue) > 0 and search_complete != True:
            breadth_current_cell = queue.popleft()
            if breadth_current_cell == end_walls:
                pygame.draw.rect(screen, pygame.Color("blue"), ((cell_size * breadth_current_cell['x']) + 1 + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + 1 + distance_from_corner_y, cell_size - 1, cell_size - 1))
                search_complete = True
                [Cell.draw() for Cell in grid_cells]
                break
            BFS_check_neighbours(breadth_current_cell)
            visited.append(breadth_current_cell)
            pygame.draw.rect(screen, pygame.Color("blue"), ((cell_size * breadth_current_cell['x']) + 1 + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + 1 + distance_from_corner_y, cell_size - 1, cell_size - 1))
            pygame.display.update()

        if search_complete == True:
            while breadth_current_cell != start_walls:
                previous_temp_x = breadth_current_cell["prev_x"]
                previous_temp_y = breadth_current_cell["prev_y"]
                pygame.draw.rect(screen, pygame.Color("yellow"), ((cell_size * breadth_current_cell['x']) + (cell_size/4) + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + (cell_size/4) + distance_from_corner_y, cell_size - (cell_size//2), cell_size - (cell_size//2)))
                next_cell_check = array_of_possible_cells[((breadth_current_cell["y"] * collums) + (breadth_current_cell["x"])) + ((previous_temp_y - breadth_current_cell["y"]) * collums) + (previous_temp_x - breadth_current_cell["x"])]
                breadth_current_cell = next_cell_check        
                pygame.draw.rect(screen, pygame.Color("green"), ((cell_size * start_walls['x']) + ((2*cell_size)//10) + distance_from_corner_x, ( cell_size * start_walls['y']) + ((2*cell_size)//10) + distance_from_corner_y, cell_size - ((2*cell_size)//5), cell_size - ((2*cell_size)//5)))
            pygame.display.update() 
            pygame.time.wait(6000)
            [Cell.reset() for Cell in grid_cells]
            maze_clicked_number = 0
            maze_complete = False
            user_text = user_text[:-2]
            is_text_inputted = False
            is_input_full = False
            two_player(run, current_cell)

        pygame.draw.rect(screen, colour, input_size_rect)
        input_text_surface = get_font(32).render(user_text, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_size_rect.x + 5, input_size_rect.y + 5))
        input_size_rect.w = max(140, input_text_surface.get_width() + 10)     
        info_text_line_1 = get_font(13).render("input a maze size, and when the maze", True, "#b68f40")
        info_rect_line_1 = info_text_line_1.get_rect(center=(150,30))   
        info_text_line_2 = get_font(13).render("has generated, click two points on the", True, "#b68f40")
        info_rect_line_2 = info_text_line_2.get_rect(center=(150,50))
        info_text_line_3 = get_font(13).render("maze and watch the magic happen", True, "#b68f40")
        info_rect_line_3 = info_text_line_3.get_rect(center=(150,70))     
        input_box_text = get_font(11).render("input a number between 1-99", True, "#b68f40")
        input_box_rect = input_box_text.get_rect(center=(100,420)) 
        screen.blit(info_text_line_1, info_rect_line_1)
        screen.blit(info_text_line_2, info_rect_line_2)
        screen.blit(info_text_line_3, info_rect_line_3)
        screen.blit(input_box_text, input_box_rect)
        clock.tick(2000)
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
                    one_player(run, current_cell)
                if TWO_PLAYER_BUTTOM.checkforinput(menu_mouse_pos):
                    two_player(run, current_cell)
                if QUIT_BUTTON.checkforinput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
main_menu()


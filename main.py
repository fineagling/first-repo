import pygame, sys
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
run = True
RES = SCREEN_WIDTH, SCREEN_HEIGHT
TILE = 20
collums = 900 // TILE
rows = 700 // TILE
clock = pygame.time.Clock()
distance_from_corner_x = 300
distance_from_corner_y = 10
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def one_player(run):
    class Cell:
        def __init__(self, x, y):
            self.x, self.y = x, y
            #defines the coordinates of the cell
            self.walls = {"top": True, "right": True, "bottom": True, "left": True}
            #dictionary for which side a cell still has
            self.visited = False
            #if the cell is visited
            self.thickness = 2
            #thickness of the line of the cells
    
        def draw_current_cell(self):
            x, y = self.x * TILE, self.y * TILE
            pygame.draw.rect(screen, pygame.Color("yellow"), (x + self.thickness + distance_from_corner_x, y + self.thickness + distance_from_corner_y, TILE - self.thickness, TILE - self.thickness)) 

        def draw(self):
            x, y = (self.x * TILE) + distance_from_corner_x, (self.y * TILE) + distance_from_corner_y
            #defining x and y as the x and y coordinate multiplied by the TILE size, and adding on x and y values to draw the cells in the middle of the screen
            if self.visited:
                pygame.draw.rect(screen, pygame.Color("black"), (x, y, TILE, TILE))
                #if a cells is visted then draw a black background on it
            
            if self.walls["top"]:
                pygame.draw.line(screen, pygame.Color("red"), (x, y), (x + TILE, y), self.thickness)
            if self.walls["bottom"]:
                pygame.draw.line(screen, pygame.Color("red"), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
            if self.walls["left"]:
                pygame.draw.line(screen, pygame.Color("red"), (x, y + TILE), (x, y), self.thickness)
            if self.walls["right"]:
                pygame.draw.line(screen, pygame.Color("red"), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
                #each side of the cell that is true from the dictionary, the cell still has and therefore we draw that side

        

        def check_cell(self, x, y):
            find_index = lambda x, y: x + y * collums
            if x < 0 or x > collums - 1 or y < 0 or y > rows - 1:
                return False
            return grid_cells[find_index(x, y)]
         
        def check_neighbours(self):
            neighbours = []
            #defines empty list for possible neighbouring cells to be put in
            top = self.check_cell(self.x, self.y - 1)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)
            right = self.check_cell(self.x + 1, self.y)
            if top and not top.visited:
                neighbours.append(top)
                #if the cell is checked and is true, and is not visited it is added (appended) to the list of possible neighbours
            if bottom and not bottom.visited:
                neighbours.append(bottom)
                #if the cell is checked and is true, and is not visited it is added (appended) to the list of possible neighbours
            if left and not left.visited:
                neighbours.append(left)
                #if the cell is checked and is true, and is not visited it is added (appended) to the list of possible neighbours
            if right and not right.visited:
                neighbours.append(right)
                #if the cell is checked and is true, and is not visited it is added (appended) to the list of possible neighbours
            return choice(neighbours) if neighbours else False
            #return a random choice from the list of neighbours, if there is nothing in the list the return false
        
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
    #creating array of the instances created by the class Cell in the range of the number of collums and number of rows
    current_cell = grid_cells[0]
    #the current cell is the first of the array of grid_cells
    stack = []
    #define the stack
 
    while run:
        screen.fill("#2a0807")
        one_play_mouse_pos = pygame.mouse.get_pos()
        ONE_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(30), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
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
    
        [Cell.draw() for Cell in grid_cells]
        #carry out the draw sub-routine for each instance in the array of grid_cells
        current_cell.visited = True
        current_cell.draw_current_cell()

        next_cell = current_cell.check_neighbours()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        
        clock.tick(2000)
        #how fast the maze generates
        pygame.display.update()
        
def two_player(run):
    
    while run:
        screen.fill("#2a0807")
        two_play_mouse_pos = pygame.mouse.get_pos()
        TWO_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(30), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
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
        heading_main_menu_text = get_font(135).render("MAZE", True, "#b68f40")
        menu_rect = heading_main_menu_text.get_rect(center=(640,100))

        ONE_PLAYER_BUTTON = Button(pos=(640,250), button_font=get_font(40), base_colour= white, hovering_colour="#d7fcd4", input_text="1 PLAYER", image=None, x_start=475, y_start=200, x_end=780, y_end=300)
        TWO_PLAYER_BUTTOM = Button(pos=(640,400), button_font=get_font(40), base_colour=white, hovering_colour="#d7fcd4", input_text="2 PLAYER", image=None, x_start=475, y_start=350, x_end=780, y_end=450) 
        QUIT_BUTTON = Button(pos=(640,550), button_font=get_font(40), base_colour=white, hovering_colour="#d7fcd4", input_text="QUIT", image=None, x_start=475, y_start=500, x_end=780, y_end=600) 
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

import pygame, sys
from engine import Button
from random import choice
from collections import deque
#these lines import pygame, libraries that the program uses, and then the button class from the engine 
pygame.init()
#this line initialises pygame
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#these variables are the dimensions of the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#this line sets screen as a display using pygame
pygame.display.set_caption("Maze Generator and Solver")
#this line sets the caption of the window
menu_backGround = pygame.image.load("assets/backgroundv2.png")
game_backGround = pygame.image.load("assets/play_background.png")
#these are defining the menu and the game background images
red = pygame.Color(255,0,0)
black = pygame.Color(0,0,0)
green = pygame.Color(0,255,0)
white = pygame.Color(255,255,255)
#these lines set out colours to save time 
run = True
#This is the run variable for the run loop
cell_size = 80
#This is the variable that sets the size of each cell of the maze in pixels
collums = 900 // cell_size
rows = 700 // cell_size
#These variables use the cell size variable to calculate how many collums and rows the maze has
clock = pygame.time.Clock()
#This line sets the clock so that the tick speed of the program to speed it up or slow it down
distance_from_corner_x = 300
distance_from_corner_y = 10
#these variables define how far from the edge of the screen the maze is
global visited_origin
visited_origin = 0
#this line defines the variable that checks how many times the DFS has returned back to the origin
active = False
#This is a boolean value that represents if the input box is active or not
maze_complete = False
#this is a boolean value that checks if the maze has been generated
cell_size_number_x = 0
cell_size_number_y = 0
#These lines define the variables that hold the x and y positions of the clicked cells
user_text = ""
#this defines user text as a text variable so that it can be used for the input box
input_size_rect = pygame.Rect(30,430,140,50)
#this defines the rectangle for the input box 
colour_input_active = pygame.Color("lightskyblue3")
colour_input_passive = pygame.Color("black")
#these define the colours that the input ox will be when they are clicked or not 
colour = colour_input_passive
#sets the colour for the input box as a variabke called colour
is_text_inputted = False
is_input_full = False
#These are boolean variables for the text box
cell_size_changed_value = 0
#This defines the changed cell size value that cell size change function will use
start_coordinate = []
end_coordinate = []
#these are the actual coordinates for the start and the end cells that have been clicked
maze_clicked_number = 0
#this variable tracks how many times the maze has been clicked
breadth_first_search_complete = False
#this is a boolean value that checks if the search for the BFS is complete
global queue
queue = deque()
#this sets the queue data structure as a deque
number_of_maze_generations = 1
#this sets the number of maze generations that isn't zero indexed
length_of_path = 1
#this sets the length of the path  as 1 as it isn't zero indexed
player_1_score, player_2_score = 0, 0
#this sets the scores for player 1 and 2
def cell_size_change(cell_size, user_text, collums, rows):
    cell_size_changed_value = (1901/99) + ((79/99) * (int(user_text)))
    cell_size = cell_size_changed_value   
    collums = 900 // cell_size
    rows = 700 // cell_size
#This function changes the cell size based on the input in the inpit box, and then update the number of collums and rows 

def get_font(size):
    return pygame.font.Font("assets/GamePlayed.ttf", size)
#This function returns the correct font using an input of the size

class Cell:
#defines the start are the Cell class
    def __init__(self, x, y):
    #defining the initializer of the class
        self.x, self.y = x, y
        self.walls = {"north": True, "east": True, "south": True, "west": True}
        self.visited = False
        self.thickness = 1
        #these are defining the attributes of the class
        
    
    def draw_current_cell(self, visited_origin):
    #defines the draw current cell method
        x, y = self.x * cell_size, self.y * cell_size
        #this defines the position of the cell as an x and y coordinate
        if x == 0 and y == 0:
            visited_origin = visited_origin + 1     
        #these lines check if the cell that the loop is currently on then increase viited origin by 1
            
        if visited_origin == 0:
            pygame.draw.rect(screen, pygame.Color("yellow"), (x + self.thickness + distance_from_corner_x, y + self.thickness + distance_from_corner_y, cell_size - self.thickness, cell_size - self.thickness)) 
        #if the DFS has not been back to the origin, then draw the current cell as a yellow cell
           
    def draw(self):
    #defines the draw method that draws the grid of the maze out
        x, y = (self.x * cell_size) + distance_from_corner_x, (self.y * cell_size) + distance_from_corner_y
        #this defines x ad y posiitons of the cell in the grid but with distances from the edge of the screen as these will be used to draw the grid
        cell_number_pos = [(cell_size_number_x - 1), (cell_size_number_y - 1)]
        #create a position of cell based on the two cells that have been clicked by the user
        coordinates_pos = [self.x, self.y]
        #create a position of the cell that is currently being drawn
            
        global maze_clicked_number, start_coordinate, end_coordinate
        if self.visited and (cell_number_pos != coordinates_pos):
            pygame.draw.rect(screen, pygame.Color("black"), (x, y, cell_size, cell_size))
        #these lines check if the cell being drawn is visited and also not the same cell that has been clicked
        else:
        #if the cell is the same as the cell that has been clicked it enters this part of the program
            if maze_clicked_number == 1:                  
                pygame.draw.rect(screen, pygame.Color("green"), (distance_from_corner_x + ((cell_size_number_x - 1) * cell_size), distance_from_corner_y + ((cell_size_number_y - 1) * cell_size), cell_size, cell_size) )
            #If it is the first click from the user, draw a green cell
                start_coordinate = coordinates_pos
            if maze_clicked_number == 2:
                pygame.draw.rect(screen, pygame.Color("green"), (distance_from_corner_x + ((cell_size_number_x - 1) * cell_size), distance_from_corner_y + ((cell_size_number_y - 1) * cell_size), cell_size, cell_size) )
            #If it is the second click from the user, draw a green cell
                end_coordinate = coordinates_pos
            if maze_clicked_number >= 3:
                pygame.draw.rect(screen, pygame.Color("black"), (x, y, cell_size, cell_size))
            #after the user clicks again, then redraw the cell black like it was


        if self.walls["north"]:
            pygame.draw.line(screen, pygame.Color("red"), (x, y), (x + cell_size, y), self.thickness)
        #if the north or top wall of the cell that is being drawn by this method is true, then draw that line at the top of the cell
        if self.walls["south"]:
            pygame.draw.line(screen, pygame.Color("red"), (x + cell_size, y + cell_size), (x, y + cell_size), self.thickness)
        #if the south or bottom wall of the cell that is being drawn by this method is true, then draw that line at the bottom of the cell
        if self.walls["west"]:
            pygame.draw.line(screen, pygame.Color("red"), (x, y + cell_size), (x, y), self.thickness)
        #if the west or left wall of the cell that is being drawn by this method is true, then draw that line at the left of the cell
        if self.walls["east"]:
            pygame.draw.line(screen, pygame.Color("red"), (x + cell_size, y), (x + cell_size, y + cell_size), self.thickness)
        #if the east or right wall of the cell that is being drawn by this method is true, then draw that line at the right of the cell

    def check_cell(self, x, y):
    #This defines the check cell method of the class
        find_position_in_list = lambda x, y: x + y * collums
        #This line defines a lamba to find the position of an item in a 1d list as if it were in a 2d grid
        if x < 0 or x > collums - 1 or y < 0 or y > rows - 1:
            return False
        #This line checks if the cell is within the bounds of the maze, so that the program doesn't break
        return grid_cells[find_position_in_list(x, y)]
        #This returns the output of the lambda using the x and y cooridnates of the cell
         
    def check_neighbours(self):
    #This defines the check neighbours method
        neighbours = []
        defines a list of possible neighbours
        north = self.check_cell(self.x, self.y - 1)
        south = self.check_cell(self.x, self.y + 1)
        west = self.check_cell(self.x - 1, self.y)
        east = self.check_cell(self.x + 1, self.y)
        #These lines define the cells that are above, bellow, to the right of and to the left of the current cell using the check cell method
        if north and not north.visited:
            neighbours.append(north)
        #if there is a north neighbor that the current cell of the DFS could go to, and it is not visited, add that cell to the possible neighbours list
        if south and not south.visited:
            neighbours.append(south)
        #if there is a south neighbor that the current cell of the DFS could go to, and it is not visited, add that cell to the possible neighbours list
        if west and not west.visited:
            neighbours.append(west)
        #if there is a west neighbor that the current cell of the DFS could go to, and it is not visited, add that cell to the possible neighbours list
        if east and not east.visited:
            neighbours.append(east)
        #if there is a east neighbor that the current cell of the DFS could go to, and it is not visited, add that cell to the possible neighbours list
        return choice(neighbours) if neighbours else False
        #this method then returns a random choice of the possible neighbours in the neighbours list

    def make_array_of_dictionaries(self):
    #This line defines the method that adds the keys to the walls dictionary for the specified cell
        self.walls["x"] = self.x
        self.walls["y"] = self.y
        #These lines define 2 new keys to add to the dictionary of the specified cell, containing there x and y coordinates
        self.walls["prev_x"] = 0
        self.walls["prev_y"] = 0
        #These lines define 2 new keys to add to the dictionary of the specified cell that represent the x and y coordinates of the previous cell of the BFS, and sets them to 0 so that they can be altered later on
        return self.walls
        #this method then returns the walls dictionary for the cell specified

    def reset(self):
    #This defines the reset method of the class, used for when the program needs to reset itself after a go
        self.visited = False 
        #This line sets the cell specified as not visited
        self.walls["north"] = True
        self.walls["south"] = True
        self.walls["east"] = True
        self.walls["west"] = True
        #These lines set each wall of the cell specified to true
        
        
def check_if_mouse_in_maze(position):
#This defines the function that checks if the maze is in the bounds of the maze
    if position[0] in range(distance_from_corner_x, (collums * cell_size) + distance_from_corner_x) and position[1] in range(distance_from_corner_y, (rows * cell_size) + distance_from_corner_y):  
        return True
    #This if statement checks if the mouse position is in the bound of the maze, and if so it returns true
        
def gather_cell_number(position):
#This defines the function that creates the x and y cordinates of the tile the user has clicked
    global cell_size_number_x
    cell_size_number_x = (position[0] - (distance_from_corner_x - cell_size))//cell_size
    #This takes the x position of the click and calculates the x coordinate of the click based on the maze
    global cell_size_number_y
    cell_size_number_y = (position[1]-(distance_from_corner_y - cell_size))//cell_size
    #This takes the y position of the click and calculates the y coordinate of the click based on the maze
    
def remove_walls(current, next):
#This defines the remove walls function that removes the wall between the current and then next cell of the DFS 
    change_in_x = current.x - next.x
    #defines a change in x variable to see which way the next cell is in compared to the current cell
    if change_in_x == 1:
        current.walls["west"] = False
        next.walls["east"] = False
    #if the change in the x values is 1, then remove the west wall of the current cell and the east wall of the next cell
    elif change_in_x == -1:
        current.walls["east"] = False
        next.walls["west"] = False
    #if the change in the x values is -1, then remove the east wall of the current cell and the west wall of the next cell   
    change_in_y = current.y - next.y
    #defines a change in y variable to see which way the next cell is in compared to the current cell
    if change_in_y == 1:
        current.walls["north"] = False
        next.walls["south"] = False
    #if the change in the y values is 1, then remove the north wall of the current cell and the south wall of the next cell
    elif change_in_y == -1:
        current.walls["south"] = False
        next.walls["north"] = False
    #if the change in the y values is -1, then remove the south wall of the current cell and the north wall of the next cell

grid_cells = [Cell(col, row) for row in range(rows) for col in range(collums)]
#This defines a list of objects created for every cell in the maze
current_cell = grid_cells[0]
#set the current cell to the first object in the grid cells list
stack = []
#This defines the stack for the DFS

def breadth_first_search_variables(start_coordinate, end_coordinate):
#This defines the function that defines all of the neccessary variables that cannot be defined with all of the other variables as they cannot be accessed until the DFS is complete
    global array_of_possible_cells
    array_of_possible_cells = deque()
    #This defines the array of possible cells as a deque (two sided queue data structure)
    array_of_possible_cells = [Cell.make_array_of_dictionaries() for Cell in grid_cells]
    #This creates a list of the dictionary for each cell in the maze, as it carries out the make array of dictionaries method for every cell in the grid cells list
    global start_walls
    start_walls = (array_of_possible_cells[(start_coordinate[0] + (start_coordinate[1] * collums))])
    #asigns the dictinary of the cell that was clicked first using the start coordinate, to the start walls variable
    global end_walls
    end_walls = (array_of_possible_cells[(end_coordinate[0] + (end_coordinate[1] * collums))])
    #asigns the dictinary of the cell that was clicked second using the end coordinate, to the end walls variable
    global visited
    visited = deque()
    #defines visited as a deque (two sided queue data structure)

def BFS_check_neighbours(breadth_current_cell):
#This defines the BFS check neighbours function that checks all possible neighbours for the current cell of the search
        if breadth_current_cell['north'] == False:
        #If the top wall of the current cell in the BFS is false then enter this if statement
            x_temp_1 = breadth_current_cell['x']
            y_temp_1 = breadth_current_cell['y']
            #This line creates two temporary variables for values of the x and y keys for the dictionary that is represented by the breadth current cell variable
            child_cell_1 = array_of_possible_cells[((y_temp_1 * collums) + (x_temp_1)) - collums]
            #This line uses the fact the top wall is gone to create a variable child cell 1, and then assign the dictionary of the cell above the breadth current cell to it
            if child_cell_1 not in visited:
            #if the child cell dictionary is not in the visited list
                child_cell_1["prev_x"] = child_cell_1["x"]
                child_cell_1["prev_y"] = child_cell_1["y"] + 1
                #This line sets the prev x value to the same as the current cell, and then sets the prev y value to 1 greater than the child cell, as the previous cell in the search was bellow it
                queue.append(child_cell_1)
                #This adds the child cell to the queue
        if breadth_current_cell['south'] == False:
        #If the bottom wall of the current cell in the BFS is false then enter this if statement    
            x_temp_2 = breadth_current_cell['x']
            y_temp_2 = breadth_current_cell['y']
            #This line creates two temporary variables for values of the x and y keys for the dictionary that is represented by the breadth current cell variable
            child_cell_2 = array_of_possible_cells[((y_temp_2 * collums) + (x_temp_2)) + collums]
            #This line uses the fact the bottom wall is gone to create a variable child cell 2, and then assign the dictionary of the cell bellow the breadth current cell to it
            if child_cell_2 not in visited:
            #if the child cell dictionary is not in the visited list
                child_cell_2["prev_x"] = child_cell_2["x"]
                child_cell_2["prev_y"] = child_cell_2["y"] - 1
                #This line sets the prev x value to the same as the current cell, and then sets the prev y value to 1 less than the child cell, as the previous cell in the search was above it
                queue.append(child_cell_2)
                #This adds the child cell to the queue
        if breadth_current_cell['east'] == False:
        #If the right wall of the current cell in the BFS is false then enter this if statement     
            x_temp_3 = breadth_current_cell['x']
            y_temp_3 = breadth_current_cell['y']     
            #This line creates two temporary variables for values of the x and y keys for the dictionary that is represented by the breadth current cell variable
            child_cell_3 = array_of_possible_cells[((y_temp_3 * collums) + (x_temp_3)) + 1]
            #This line uses the fact the right wall is gone to create a variable child cell 3, and then assign the dictionary of the cell right of the breadth current cell to it
            if child_cell_3 not in visited:
            #if the child cell dictionary is not in the visited list    
                child_cell_3["prev_x"] = child_cell_3["x"] - 1
                child_cell_3["prev_y"] = child_cell_3["y"]
                #This line sets the prev y value to the same as the current cell, and then sets the prev x value to 1 less than the child cell, as the previous cell in the search was right of it
                queue.append(child_cell_3)
                #This adds the child cell to the queue
        if breadth_current_cell['west'] == False:
        #If the left wall of the current cell in the BFS is false then enter this if statement   
            x_temp_4 = breadth_current_cell['x']
            y_temp_4 = breadth_current_cell['y']  
            #This line creates two temporary variables for values of the x and y keys for the dictionary that is represented by the breadth current cell variable
            child_cell_4 = array_of_possible_cells[((y_temp_4 * collums) + (x_temp_4)) - 1]
            #This line uses the fact the left wall is gone to create a variable child cell 4, and then assign the dictionary of the cell left of the breadth current cell to it
            if child_cell_4 not in visited:
            #if the child cell dictionary is not in the visited list
                child_cell_4["prev_x"] = child_cell_4["x"] + 1
                child_cell_4["prev_y"] = child_cell_4["y"]
                #This line sets the prev y value to the same as the current cell, and then sets the prev x value to 1 more than the child cell, as the previous cell in the search was left of it
                queue.append(child_cell_4)  
                #This adds the child cell to the queue

def display_default_image():
#This defines the function to display the default maze image
    default_maze = pygame.image.load("assets/default_maze.png")
    #his defines the default maze imgae from the files
    screen.blit(default_maze, (distance_from_corner_x, distance_from_corner_y))
    #This draws the default image in the same position as the maze
    pygame.display.update()
    #This updates that part of the display


def one_player(run, current_cell):
#This line defines the one player part of the game
    number_of_run_loops = 0
    search_complete = False
    #These lines define 2 variables used only in the one player part, number of run loops and search complete
    while run:
    #This is the run loop
        screen.fill("#2a0807")
        #This fils the screen with a background colour
        one_play_mouse_pos = pygame.mouse.get_pos()
        #This defines a one player mouse position using the pygame get mouse position built in function
        ONE_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(50), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
        #This defines a one player back button from the button class that was created 
        global maze_complete, active, user_text, colour, is_text_inputted, is_input_full, maze_clicked_number
        for button in [ONE_PLAY_BACK]:
            button.changecolour(one_play_mouse_pos)
            button.text_update(screen)
        #This mini for loop runs the change colour and text update methods for the back button
      
        for event in pygame.event.get():
        #This is the start of the event handler
            if event.type == pygame.QUIT:
            #If the user clicks the x in the top right on the window
                pygame.quit()
                sys.exit()
                #stop the program and close the window
            if event.type == pygame.MOUSEBUTTONDOWN:
            #If there is a click then enter this if statement
                if ONE_PLAY_BACK.checkforinput(one_play_mouse_pos):
                #if when the program runs the check for input method for the back button, and an input is registered enter the if statement
                    [Cell.reset() for Cell in grid_cells]
                    #carry out the reset method from the cell class for every cell in the maze
                    maze_clicked_number = 0
                    maze_complete = False
                    user_text = user_text[:-2]
                    is_text_inputted = False
                    is_input_full = False
                    #These lines reset every variable needed to reset in order to start the DFS and BFS again
                    main_menu()
                    #Call the main menu function
                if maze_complete and check_if_mouse_in_maze(one_play_mouse_pos) and maze_clicked_number <= 2:
                #if the maze generation is complete and the mouse is in the maze and the maze clicked number is less than 2 then enter this if statement
                    gather_cell_number(one_play_mouse_pos)
                    #call the gather cell number function
                    maze_clicked_number = maze_clicked_number + 1
                    #add one to the maze clicked number
                if maze_clicked_number == 3:
                #if the maze clicked number is 3 then enter the if statement
                    breadth_first_search_variables(start_coordinate, end_coordinate)
                    #call the BFS variables function
                    number_of_run_loops = number_of_run_loops + 1
                    #add one to the number of run loops
                    if number_of_run_loops == 1:
                        queue.append(start_walls)
                        #if this is the first run loop, then add the start walls to the queue to start the BFS 
                if input_size_rect.collidepoint(event.pos):
                #if the input box has been clicked, then enter this part of the if  statement
                    active = True
                    #set active as true
                else:
                #if the input box hasn't been clicked, then enter this part of the statement
                    active = False
                    #set active to false
            if event.type == pygame.KEYDOWN and event.unicode.isdigit():       
            #if the event is a key has been pressed and it is a digit (number) enter this if statement
                is_text_inputted = True
                #set is text inputted to true
                if len(user_text) <= 1:
                #If the length of what has been inputted into the input box is less than 2 enter the if staement
                    user_text += event.unicode
                    #add the digit to the input box
                else:
                #If the length of what has been inputted into the input box is 2 digits long then enter the if staement
                    cell_size_change(cell_size, user_text, collums, rows)
                    #call the cell size change function to change the cell size of the maze
                    is_input_full = True
                    #set is input full to true
            if event.type == pygame.KEYDOWN and is_input_full == False:
                #if a key has been pressed and the input box isn't full then enter the if statement
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]           
                    #if the key pressed is the backspace, then delete the most recent digit inputted into the input box
            
        if is_input_full == False:
                display_default_image()    
                #if the inpt box is not full then call the display default image function
        
        if is_text_inputted and is_input_full:
        #if there has been text inputted into the input box, and the input box is full then start the DFS 
            [Cell.draw() for Cell in grid_cells]
            #carry out the draw method for every cell in the maze
            current_cell.visited = True
            #set the current cell's visited atribute to true
            current_cell.draw_current_cell(visited_origin)
            #carry out the draw current cell method on the current cell

            next_cell = current_cell.check_neighbours()
            #sets the next cell to the choice that is retund by the check neighbours function
            if next_cell:
            #if there is a next cell that the program can go to 
                next_cell.visited = True
                #sets the next cell to visited
                stack.append(current_cell)
                #add the current cell to the stack
                remove_walls(current_cell, next_cell)
                #remove the walls between the current and next cell
                current_cell = next_cell
                #set the current cell to the next cell
            elif stack:
            #if there are items in the stack
                current_cell = stack.pop()
                #pop the stack so that the DFS can backtrack
            elif next_cell == False:
            #if all of the cells have been visited
                maze_complete = True
                #set maze complete to true to signify that generation is complete
            
        if active:
            colour = colour_input_active
            #if active is true then set the colour to the active colour
        else:
            colour = colour_input_passive
            #if active is not true then set the colour to the passive colour

        while len(queue) > 0 and search_complete != True:
        #while the length of the queue is greater than zero and the search isn't complete
            breadth_current_cell = queue.popleft()
            #dequeue the queue and assign the deuqueue to breadth current cell
            if breadth_current_cell == end_walls:
            #if the current cell is the end walls
                pygame.draw.rect(screen, pygame.Color("blue"), ((cell_size * breadth_current_cell['x']) + 1 + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + 1 + distance_from_corner_y, cell_size - 1, cell_size - 1))
                #draw the end walls cell in blue
                search_complete = True
                #change search complete to true
                [Cell.draw() for Cell in grid_cells]
                #redraw the grid, so that all of the black backgrounds get drawn, and gets rid of the blue tiles
                break
                #break out of this while loop
            BFS_check_neighbours(breadth_current_cell)
            #call the BFS check neighbours function
            visited.append(breadth_current_cell)
            #add the current cell to the visited list
            pygame.draw.rect(screen, pygame.Color("blue"), ((cell_size * breadth_current_cell['x']) + 1 + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + 1 + distance_from_corner_y, cell_size - 1, cell_size - 1))
            #draw a blue tile in the position of the current cell
            pygame.display.update()
            #update the display

        if search_complete == True:
        #if the search is complete
            while breadth_current_cell != start_walls:
            #while the current cell is not equal to the start walls, as this loop follows the previous tiles after the search from the end walls to the start walls
                previous_temp_x = breadth_current_cell["prev_x"]
                previous_temp_y = breadth_current_cell["prev_y"]
                #create an x and a y temporary variable holding the values of the prev x and prev y keys of the current cell dictionary
                pygame.draw.rect(screen, pygame.Color("yellow"), ((cell_size * breadth_current_cell['x']) + (cell_size/4) + distance_from_corner_x, ( cell_size * breadth_current_cell['y']) + (cell_size/4) + distance_from_corner_y, cell_size - (cell_size//2), cell_size - (cell_size//2)))
                #This draws a small yellow square in the position of the current cell to show the path
                next_cell_check = array_of_possible_cells[((breadth_current_cell["y"] * collums) + (breadth_current_cell["x"])) + ((previous_temp_y - breadth_current_cell["y"]) * collums) + (previous_temp_x - breadth_current_cell["x"])]
                #This sets a placeholder variable equal to the previous cell of the current cell using the temporary variables that have just been defined and the array of possible cells that was defined earlier
                breadth_current_cell = next_cell_check     
                #this sets the placeholder variable equal to the current cell
                pygame.draw.rect(screen, pygame.Color("green"), ((cell_size * start_walls['x']) + ((2*cell_size)//10) + distance_from_corner_x, ( cell_size * start_walls['y']) + ((2*cell_size)//10) + distance_from_corner_y, cell_size - ((2*cell_size)//5), cell_size - ((2*cell_size)//5)))
                #this draws the start walls cell in green, as this cell wasn't being drawn 
            pygame.display.update() 
            pygame.time.wait(6000)
            #This line pauses the program for 6 seconds once it has broken out of the while loop and the path is complete so the user can see the path
            [Cell.reset() for Cell in grid_cells]
            maze_clicked_number = 0
            maze_complete = False
            user_text = user_text[:-2]
            is_text_inputted = False
            is_input_full = False
            #These lines reset the program once that the program has broken out of the while loop
            one_player(run, current_cell)
            #This calls the one player sub-routine

        pygame.draw.rect(screen, colour, input_size_rect)
        #This line darws the rectangle for the input box to be drawn onto
        input_text_surface = get_font(32).render(user_text, True, (255, 255, 255))
        #This defines the input box text surface
        screen.blit(input_text_surface, (input_size_rect.x + 5, input_size_rect.y + 5))
        #This draws the input box rectangle and text surface onto the screen
        input_size_rect.w = max(140, input_text_surface.get_width() + 10)     
        #This line sets where text actually gets drawn onto the box, and how far away the text can be from the sides
        info_text_line_1 = get_font(12).render("input a maze size, and when the maze has", True, "#b68f40")
        info_rect_line_1 = info_text_line_1.get_rect(center=(150,30))   
        info_text_line_2 = get_font(12).render("generated, click two points on the maze,", True, "#b68f40")
        info_rect_line_2 = info_text_line_2.get_rect(center=(150,50))
        info_text_line_3 = get_font(12).render("click again and watch the magic happen", True, "#b68f40")
        info_rect_line_3 = info_text_line_3.get_rect(center=(150,70))     
        #These lines define text surfaces and and rectangles for 3 lines of the explanation in the top left corner
        input_box_text = get_font(11).render("input a number between 1-99 for your maze complexity", True, "#b68f40")
        input_box_rect = input_box_text.get_rect(center=(100,420)) 
        #These lines define a text surface and rectange to draw onto for the text above the input box
        screen.blit(info_text_line_1, info_rect_line_1)
        screen.blit(info_text_line_2, info_rect_line_2)
        screen.blit(info_text_line_3, info_rect_line_3)
        screen.blit(input_box_text, input_box_rect)
        #These lines draw all of the text onto the screen
        clock.tick(2000)
        #This line affects the tick speed, which is how fast the DFS runs
        pygame.display.update()
        
def two_player(run, current_cell, length_of_path, number_of_maze_generations, player_1_score, player_2_score): 
#This line defines the two player part of the game
    number_of_run_loops = 0
    search_complete = False 
    #These lines define 2 variables used only in the one player part, number of run loops and search complete
    global path_complete
    path_complete = False
    #This line defines a path complete variable which is needed to calculate the score of both players
    while run:
    #This is the run loop
        screen.fill("#2a0807")
        #This fils the screen with a background colour
        two_play_mouse_pos = pygame.mouse.get_pos()
        #This defines a two player mouse position using the pygame get mouse position built in function
        TWO_PLAY_BACK = Button(pos=(100, 600), button_font= get_font(50), base_colour= white, hovering_colour= "#d7fcd4", input_text="BACK", image= "assets/back_rect.png", x_start=50, y_start= 550, x_end= 150, y_end=650)
        #This defines a two player back button from the button class that was created 
        global maze_complete, active, user_text, colour, is_text_inputted, is_input_full, maze_clicked_number
        for button in [TWO_PLAY_BACK]:
            button.changecolour(two_play_mouse_pos)
            button.text_update(screen)
        #This mini for loop runs the change colour and text update methods for the back button    

        for event in pygame.event.get():
        #This is the start of the event handler
            if event.type == pygame.QUIT:
            #If the user clicks the x in the top right on the window
                pygame.quit()
                sys.exit()
            #stop the program and close the window    
            if event.type == pygame.MOUSEBUTTONDOWN:
            #If there is a click then enter this if statement
                if TWO_PLAY_BACK.checkforinput(two_play_mouse_pos):
                #if when the program runs the check for input method for the back button, and an input is registered enter the if statement    
                    [Cell.reset() for Cell in grid_cells]
                    #carry out the reset method from the cell class for every cell in the maze
                    maze_clicked_number = 0
                    maze_complete = False
                    user_text = user_text[:-2]
                    is_text_inputted = False
                    is_input_full = False
                    #These lines reset every variable needed to reset in order to start the DFS and BFS again
                    main_menu()
                    #Call the main menu function
                if maze_complete and check_if_mouse_in_maze(two_play_mouse_pos) and maze_clicked_number <= 2:
                    #if the maze generation is complete and the mouse is in the maze and the maze clicked number is less than 2 then enter this if statement
                    gather_cell_number(two_play_mouse_pos)
                    #call the gather cell number function
                    maze_clicked_number = maze_clicked_number + 1
                    #add one to the maze clicked number
                #############################################################################################################################################
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
                if len(user_text) <= 1:
                    user_text += event.unicode
                else:
                    cell_size_change(cell_size, user_text, collums, rows)
                    is_input_full = True
            if event.type == pygame.KEYDOWN and is_input_full == False:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

            
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
                length_of_path = length_of_path + 1
            path_complete = True
            pygame.display.update() 
            pygame.time.wait(6000)
            [Cell.reset() for Cell in grid_cells]
            maze_clicked_number = 0
            maze_complete = False
            user_text = user_text[:-2]
            is_text_inputted = False
            is_input_full = False
            if number_of_maze_generations % 2 == 1 and path_complete == True:
                player_1_score = player_1_score + (length_of_path//(abs(start_walls["x"] - end_walls["x"]) + abs(start_walls["y"] - end_walls["y"])) * 2)
            elif number_of_maze_generations % 2 == 0 and path_complete == True:
                player_2_score = player_2_score + (length_of_path//(abs(start_walls["x"] - end_walls["x"]) + abs(start_walls["y"] - end_walls["y"])) * 2)
            number_of_maze_generations = number_of_maze_generations + 1
            two_player(run, current_cell, length_of_path, number_of_maze_generations, player_1_score, player_2_score)


        pygame.draw.rect(screen, colour, input_size_rect)
        input_text_surface = get_font(32).render(user_text, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_size_rect.x + 5, input_size_rect.y + 5))
        input_size_rect.w = max(140, input_text_surface.get_width() + 10)     
        info_text_line_1 = get_font(12).render("input a maze size, and when the maze has", True, "#b68f40")
        info_rect_line_1 = info_text_line_1.get_rect(center=(150,140))   
        info_text_line_2 = get_font(12).render("generated, click two points on the maze,", True, "#b68f40")
        info_rect_line_2 = info_text_line_2.get_rect(center=(150,160))
        info_text_line_3 = get_font(12).render("click again and watch the magic happen", True, "#b68f40")
        info_rect_line_3 = info_text_line_3.get_rect(center=(150,180))     
        input_box_text = get_font(11).render("input a number between 1-99", True, "#b68f40")
        input_box_rect = input_box_text.get_rect(center=(100,420)) 
        screen.blit(info_text_line_1, info_rect_line_1)
        screen.blit(info_text_line_2, info_rect_line_2)
        screen.blit(info_text_line_3, info_rect_line_3)
        screen.blit(input_box_text, input_box_rect)
        player_1_score_text = get_font(20).render(f"player 1 score: {player_1_score}", True, "#b68f40")
        player_1_score_rect = player_1_score_text.get_rect(center=(150,40))
        screen.blit(player_1_score_text, player_1_score_rect)
        player_2_score_text = get_font(20).render(f"player 2 score: {player_2_score}", True, "#b68f40")
        player_2_score_rect = player_2_score_text.get_rect(center=(150,80))
        screen.blit(player_2_score_text, player_2_score_rect)        
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
                    two_player(run, current_cell, length_of_path, number_of_maze_generations, player_1_score, player_2_score)
                if QUIT_BUTTON.checkforinput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
main_menu()


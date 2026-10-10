from tabulate import tabulate
from random import choice
from sys import exit

def check_wins(input_grid):#
    for row in input_grid:
        if row[0] == row[1] == row[2] != ' ':
            print(f'{row[0]} wins')
            return True
    for i in range(3):
        if input_grid[0][i] == input_grid[1][i] == input_grid[2][i] != ' ':
            print(f'{input_grid[0][i]} wins')
            return True
    if input_grid[0][0] == input_grid[1][1] == input_grid[2][2] != ' ':
        print(f'{input_grid[1][1]} wins')
        return True
    elif input_grid[0][2] == input_grid[1][1] == input_grid[2][0] != ' ':
        print(f'{input_grid[1][1]} wins')
        return True
    else:
        return False

def enter(x=int,y=int,type=str,grid=list):
    if grid[2-y][x] == "x" or grid[2-y][x] == "o":
        raise KeyError
    grid[2-y][x] = type
    return grid

def user_input(grid):
    cords = input("input cords to input: ").strip("()").split(",")
    cords = list(map(int, cords))
    if len(cords) != 2:
        raise IndexError
    if cords[0] != 1 and cords[0] != 2 and cords[0] != 3:
        raise ValueError
    if cords[1] != 1 and cords[1] != 2 and cords[1] != 3:
        raise ValueError
    return cords 
    
def output_table(grid):
    print(tabulate(grid,tablefmt="rounded_grid"))

def check_near_win(grid=list,player=str): 
    xnum = 0 
    index = 0
    #makes the columns into rows for a second grid so that I can iterate over it to check each column individually 
    columns = [[],[],[]]
    #checks for 2 xs in each row and fills the column grid 
    for row in grid:
        xnum = 0
        counter = 0
        for square in row:
            columns[counter].append(square)
            if square == player:
                xnum += 1
            else: 
                free = counter
            counter += 1
        if xnum == 2 and row[free] == ' ':
            return [True,"row",index, free]
        index += 1
    #does the same for the columns
    index = 0
    for column in columns:
        xnum = 0
        counter = 0
        for square in column:
            if square == player:
                xnum += 1
            else: 
                free = counter
            counter += 1
        if xnum == 2 and column[free] == ' ':
            return [True,"column",index, free]
        index += 1
    #checks the diagonals '-.
    if grid[0][0] == grid[1][1] == 'player' and grid[2][2] == ' ':
        return [True, "diagonal",2,2]
    if grid[0][0] == grid[2][2] == 'player' and grid[1][1] == ' ':
        return [True, "diagonal",1,1]
    if grid[2][2] == grid[1][1] == player and grid[0][0] == ' ':
        return [True, "diagonal",0,0]
    
    #checks the diagnoals .-'
    if grid[0][2] == grid[1][1] == player and grid[2][0] == ' ':
        return [True, "diagonal",2,0]
    if grid[0][2] == grid[2][0] == player and grid[1][1] == ' ':
        return [True, "diagonal",1,1] #doesn't need to differentiate between the two because they require the same action 
    if grid[2][0] == grid[1][1] == player and grid[0][2] == ' ':
        return [True, "diagonal",0,2]
    return [False]

def main():

    grid = [[' ',' ',' '],
            [' ',' ',' '],#x = cross, o = nought
            [' ',' ',' ']]  
    player_turn = True
    turn_num = 1 
    while not check_wins(grid):
        if player_turn:
            while True:
                try:
                    move= user_input(grid)
                    move = list(map(lambda s: s-1, move))
                    enter(*move,"x",grid)
                    print("You played:")
                    output_table(grid)
                    player_turn = False
                    break
                except IndexError:
                    print("enter two values for cords seperated by a comma")
                except ValueError:
                    print("enter cordinates from (1,1) to (3,3) in the form (x,y) or x,y")
                except KeyError:
                    print("the the position you entered is taken")
        else:    
            #NOTE always take the middle on first turn and if they play diagonal on both sides, go for a side move 

            offence = check_near_win(grid,'o')
            if offence[0]:
                match offence[1]:
                    case "row":
                        grid[offence[2]][offence[3]] = 'o'
                    case "column":
                        grid[offence[3]][offence[2]] = 'o'
                    case "diagonal":
                        grid[offence[2]][offence[3]] = 'o'
                    case _:
                        print(f"bruh: {offence}")
            else:
                defence = check_near_win(grid,'x')
                if defence[0]:
                    match defence[1]:
                        case "row":
                            grid[defence[2]][defence[3]] = 'o'
                        case "column":
                            grid[defence[3]][defence[2]] = 'o'
                        case "diagonal":
                            grid[defence[2]][defence[3]] = 'o'
                        case _:
                            print(f"bruh: {defence}")
                else:
                    if turn_num == 1 and grid[1][1] == " ":
                        grid[1][1] = "o"
                    elif turn_num == 2 and (grid[2][0] == 'x' == grid[0][2] or grid[0][0]== 'x' == grid[2][2]):
                        grid[0][1] = "o"
                    else:
                        
                        empty = []
                        y= 0
                        for row in grid:
                            x= 0
                            for square in row:
                                if square == " ":
                                    empty.append([x,y])
                                x += 1 
                            y += 1
                        if empty == []:
                            exit("draw")   
                        move = choice(empty)
                        grid[move[1]][move[0]] = 'o'
            turn_num += 1 
            print("I played:") 
            output_table(grid)
            player_turn = True

if __name__ == "__main__":
    main()
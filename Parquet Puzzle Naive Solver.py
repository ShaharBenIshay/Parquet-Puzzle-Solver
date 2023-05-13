import itertools
class Part:
    def __init__(self, id):
        """
        this is an part object that has a stick as a core.
        if there is 1 is the cell it mean that there is a block there, the place if the 1 is by binary order
        to the part id. for example if this is part 3 then a block of part 3 will be cell == "00000100"

        :param id: int
        """
        self.stick = []
        self.id = id
        for i in range(9):
            self.stick.append(["00000000","00000000","00000000"])

    def insert(self,cordinats):
        """
        insert to the clean stick the 1's - mean the block
        :param cordinats: list of tuples, every tuple is (row number,True if its on the left side,
        False for right side)
        :return: None
        """
        for i in range(len(cordinats)):
            row = cordinats[i][0]
            is_left = cordinats[i][1]
            idx = 0
            if is_left is False:
                idx = 2
            self.stick[row][idx] = ""
            for i in range(8):
                if i != 8 - self.id:
                    self.stick[row][idx] += "0"
                else:
                    self.stick[row][idx] += "1"

    def show_stick(self):
        """
        print the stick to screen
        :return: None
        """
        for row in range(len(self.stick)):
            print(self.stick[row])

    def show_stick_simple(self):
        simple_stick = []
        for row in range(len(self.stick)):
            new_row = []
            for col in range(len(self.stick[0])):
                if self.stick[row][col] == "00000000":
                    new_row.append(0)
                else:
                    new_row.append(1)
            simple_stick.append(new_row)
        for r in simple_stick:
            print(r)

    def rotate_right(self):
        """
        this function rotate the stick clock wise,every time by 90 degree
        :return: None
        """
        new_stick = []
        for col in range(len(self.stick[0])):
            new_row = []
            for row in range(len(self.stick)-1,-1,-1):
                new_row.append(self.stick[row][col])
            new_stick.append(new_row)
        self.stick = new_stick

    def rotate_left(self):
        new_stick = []
        for col in range(len(self.stick[0])):
            new_row = []
            for row in range(len(self.stick)):
                new_row.append(self.stick[row][col])
            new_stick.append(new_row)
        self.stick = new_stick


class Puzzle:
    def __init__(self):
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append("00000000")
            self.grid.append(row)

    def show_puzzle(self):
        """
        this function print the grid as follow:
        if the cell is "00000000" then it will represented by 0
        if the cell contain any 1 then it will represented by 1
        the validation will be by the insertion
        :return:
        """
        simple_grid = []
        for row in range(9):
            new_row = []
            for col in range(9):
                if self.grid[row][col] == "00000000":
                    new_row.append(0)
                else:
                    new_row.append(1)
            simple_grid.append(new_row)
        for r in simple_grid:
            print(r)

    def insert_part_vertical(self,part_to_insert,col_to_insert):
        """
        :param part_to_insert: part object
        :param col_to_insert: where the first column should start
        :return: True if successful to insert , else False
        """
        for row in range(len(part_to_insert.stick)):
            for col in range(3):
                if self.grid[row][col_to_insert + col] != "00000000":
                    if part_to_insert.stick[row][col] != "00000000":
                        return False   # check trying to insert to a place that already has 1
                else:
                    self.grid[row][col_to_insert + col] = part_to_insert.stick[row][col]
        return True


    def insert_part_horizontal(self,part_to_insert,row_to_insert):
        """
        :param part_to_insert: part object
        :param row_to_insert: where the first row should start
        :return: True if successful to insert , else False
        """
        for row in range(len(part_to_insert.stick)):
            for col in range(9):
                if self.grid[row+row_to_insert][col] != "00000000":
                    if part_to_insert.stick[row][col] != "00000000":
                        return False
                       # check trying to insert to a place that already has 1
                else:
                    self.grid[row+row_to_insert][col] = part_to_insert.stick[row][col]
        return True

    def clean_grid_from_part(self,part_id):
        """
        this function get the id of a part and clear the 1's of part_id from the grid
        :param part_id: int
        :return: remove the part from the grid
        """
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col][8-part_id] == "1":
                    temp = ""
                    for i in range(8):
                        if i == 8-part_id:
                            temp += "0"
                        else:
                            temp += self.grid[row][col][i]
                    self.grid[row][col] = temp

    def clean_grid_by_many_parts(self,parts):
        for part in parts:
            self.clean_grid_from_part(part.id)

    def check_solution(self):
        """
        check if the puzzle is correct - check even rows for 101010101 and odd rows for just 0's , execpt center
        :return: bool
        """
        for row in range(9):
            if row % 2 == 1:   # this should be only zero
                for col in range(9):
                    if self.grid[row][col] != "00000000":
                        return False
            else:  # mean row should be 101010101
                for col in range(9):
                    if col % 2 == 0 and self.grid[row][col] == "00000000":
                        # this cell should have 1
                        if col == 4 and row == 4:   # center case
                            pass
                        else:
                            return False
        return True

    def explain_how_to_solve(self,vertical_set,horizontal_set,orderA,orderB):
        print(" Let's solve this Puzzle ! ")
        print(f" You have 8 parts: vertical set {vertical_set} and horizontal set {horizontal_set}")
        print(" Take the horizontal set and rotate every part to the right - clockwise")
        vertical_by_order = list(zip(vertical_set,orderA))
        for item in vertical_by_order:  # item is tuple (part?,order?)
            print(f"Take Part{item[0]} and put its left column in column number:{item[1]}")
            temp_part = build_part(item[0])
            temp_part.show_stick_simple()
            print("----------------------------------------------------------------------")
        horizontal_by_order = list(zip(horizontal_set,orderB))
        for tup in horizontal_by_order:
            print(f"Take Part{tup[0]} and put its first row in row number:{tup[1]}")
            temp_part = build_part(tup[0])
            temp_part.rotate_right()
            temp_part.show_stick_simple()
            print("----------------------------------------------------------------------")
        print("FINISH , this is the final grid:")

def rotate_many_parts_to_left(parts):
    """
    rotate many parts to the left
    :param parts: list of parts
    :return: None
    """
    for part in parts:
        part.rotate_left()

def rotate_many_parts_to_right(parts):
    """
    rotate many parts to the right
    :param parts: list of parts
    :return: None
    """
    for part in parts:
        part.rotate_right()

def build_part(id):
    """
    this function get id and build the part accordingly to the id
    :param id: int
    :return: object part by the given id
    """
    part = Part(id)
    if id == 1:
        part.insert([(0,False),(4,True),(8,False)])
    elif id == 2:
        part.insert([(2, True), (2, False), (6, True)])
    elif id == 3:
        part.insert([(0, True), (4, False), (8, False)])
    elif id == 4:
        part.insert([(4, True), (6, False), (8, True)])
    elif id == 5:
        part.insert([(0, True), (8, False), (8, True)])
    elif id == 6:
        part.insert([(0, True), (2, False), (8, False)])
    elif id == 7:
        part.insert([(0, True), (2, False), (6, False)])
    else:
        part.insert([(0, True), (2, True), (8, False)])
    return part



""" now should find the solution"""
# step 1: get all combinations of [1,2,3,4,5,6,7,8] with 4 numbers
vertical_set = list(itertools.combinations([i for i in range(1,9)],4))
horizontal_set = list(itertools.combinations([i for i in range(1,9)],4))
# show the player the empty grid
empty_puzzle = Puzzle()
print(" # THIS IS MY SOLUTION - Written By Me And By Me Alone - No Other People or Internet Help #")
print(f"Hello this is your empty Puzzle grid:")
empty_puzzle.show_puzzle()
# step 2: try solve by choose vertical set of 4 parts
for ver_set in vertical_set:
    copy_puzzle = Puzzle()  # create empty puzzle
    # step 3: build 4 parts objects
    v1,v2,v3,v4 = map(lambda i:build_part(i),ver_set)
    # step 4: create all permutations for the order that those parts will be
    order_vertical = list(itertools.permutations([0,2,4,6]))
    # step 5: choose order for the vertical set of parts
    for orderA in order_vertical:
        # step 6: insert parts to the puzzle grid
        copy_puzzle.insert_part_vertical(v1,orderA[0])
        copy_puzzle.insert_part_vertical(v2, orderA[1])
        copy_puzzle.insert_part_vertical(v3, orderA[2])
        copy_puzzle.insert_part_vertical(v4, orderA[3])
        # step 7: choose horizontal set of 4 parts
        for hor_set in horizontal_set:
            # check if there is overlap -> if not then continue solving
            intersection_list = list(set.intersection(set(ver_set), set(hor_set)))
            if not intersection_list:   # if true mean that there is no overlap
                # step 8: build 4 parts objects
                h5,h6,h7,h8 = map(lambda i:build_part(i),hor_set)
                # step 9: change the parts to be horizontal,
                rotate_many_parts_to_right([h5,h6,h7,h8])
                # step 10: choose order for the horizontal set of parts
                order_horizontal = list(itertools.permutations([0,2,4,6]))
                for orderB in order_horizontal:
                    # step 11: try insert the horizontal parts to the grid
                    flag = []
                    flag.append(copy_puzzle.insert_part_horizontal(h5,orderB[0]))
                    flag.append(copy_puzzle.insert_part_horizontal(h6, orderB[1]))
                    flag.append(copy_puzzle.insert_part_horizontal(h7, orderB[2]))
                    flag.append(copy_puzzle.insert_part_horizontal(h8, orderB[3]))
                    # step 12A: if True then one or more insertions was not valid then i need to clean the grid
                    if False in flag:
                        copy_puzzle.clean_grid_by_many_parts([h5,h6,h7,h8])
                    # step 12B: if all insertions went well then check if its the solution
                    else:
                        if copy_puzzle.check_solution() is True:
                            # lets explain the player how to solve this puzzle !
                            copy_puzzle.explain_how_to_solve(ver_set,hor_set,orderA,orderB)
                            copy_puzzle.show_puzzle()
                            break  # no need to continue
                # if we didnt found solution then we should rotate the horizontal parts back the be vertical
                rotate_many_parts_to_left([h5,h6,h7,h8])
        # if this is not the right 4 vertical parts then clean the grid from them and continue searching
        copy_puzzle.clean_grid_by_many_parts([v1,v2,v3,v4])












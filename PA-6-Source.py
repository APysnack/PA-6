import Graph

'''
Alan Pysnack
CSC-332 Advanced Data Structs
10/28/2020
'''

class SequenceAlignment(object):

    # constructor for the sequence alignment object
    def __init__(self, x, y, match, mismatch, gap):
        # x and y are the input sequences
        self.x = x
        self.y = y

        # user designated values for match/gap/mismatch
        self.match_val = match
        self.mismatch_val = mismatch
        self.gap_val = gap

        # dictionaries to track the arrow locations on the graph
        self.cell_dict = {}
        self.solution = {}

    # part of the alignment calculation - returns match_val if the alignment is a match, mismatch_val if mismatch
    def delta(self, x, y, i, j):
        if x[i] == y[j]:
            return self.match_val
        else:
            return self.mismatch_val

    # finds the paths for completing the optimal solution
    def find_solution(self, OPT, m, n):

        # base case that returns if cell is 0,0 since it will be defaulted to a value of 0
        if m == 0 or n == 0:
            return

        # the cost of doing an insert, adds gap to the opt value from the left cell
        insert = OPT[m][n - 1] + self.gap_val

        # the value of alignment is the top left diagonal cell + the value of match/mismatch
        align = OPT[m - 1][n - 1] + self.delta(self.x, self.y, m - 1, n - 1)

        # the cost of deleting, adds gap to the opt value from the above cell
        delete = OPT[m - 1][n] + self.gap_val

        # determines the maximum value between the cost of inserting/aligning/deleting
        best_choice = max(insert, align, delete)

        # stores the path of the cell in the solution dictionary for that cell's location
        if best_choice == insert:
            self.solution[(m, n)] = 'right'
            return self.find_solution(OPT, m, n - 1)
        elif best_choice == align:
            self.solution[(m, n)] = 'diagonal'
            return self.find_solution(OPT, m - 1, n - 1)
        elif best_choice == delete:
            self.solution[(m, n)] = 'down'
            return self.find_solution(OPT, m - 1, n)


    # solves the location of all arrows for an individual cell
    def solve_cell(self, OPT, m, n):

        # base case for 0,0
        if m == 0 or n == 0:
            return

        # the cost of doing an insert, adds gap to the opt value from the left cell
        insert = OPT[m][n - 1] + self.gap_val

        # the value of alignment is the top left diagonal cell + the value of match/mismatch
        align = OPT[m - 1][n - 1] + self.delta(self.x, self.y, m - 1, n - 1)

        # the cost of deleting, adds gap to the opt value from the above cell
        delete = OPT[m - 1][n] + self.gap_val

        # if all 3 values are equal, stores info for all arrows
        if align == insert == delete:
            self.cell_dict[(m, n)] = ['down', 'right', 'diagonal']
            return

        # determines the best option from align/insert delete
        best_option = max(align, insert, delete)

        # if align and insert are both the best options, stores info for right and diagonal arrows
        if align == insert and align == best_option:
            self.cell_dict[(m, n)] = ['right', 'diagonal']
            return

        # if align and delete are both the best options, stores info for down and diagonal arrows
        if align == delete and align == best_option:
            self.cell_dict[(m, n)] = ['down', 'diagonal']
            return

        # if insert and delete are both the best options, stores info for right and diagonal arrows
        if insert == delete and insert == best_option:
            self.cell_dict[(m, n)] = ['right', 'down']
            return

        # otherwise only stores one arrow for align, insert, delete (diagonal, right, down, respectively)
        if align == best_option:
            self.cell_dict[(m, n)] = ['diagonal']
            return

        if insert == best_option:
            self.cell_dict[(m, n)] = ['right']
            return

        if delete == best_option:
            self.cell_dict[(m, n)] = ['down']
            return

    # primary function for getting sequence alignment data
    def alignment(self):
        # gets the row and col counts for the graph
        n = len(self.y)
        m = len(self.x)

        # graph initialized with all 0's
        OPT = [[0 for i in range(n + 1)] for j in range(m + 1)]

        # initializes first row (e.g. if gap val = -2, row is -2, -4, -6, etc.)
        for i in range(1, m + 1):
            OPT[i][0] = i * self.gap_val

        # initalizes first col (e.g. if gap val = -2, col is -2, -4, -6, etc.)
        for j in range(1, n + 1):
            OPT[0][j] = j * self.gap_val


        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # cycles through each cell and fills it with the max cost out of aligning/inserting/deleting
                OPT[i][j] = max(
                    # alignment cost
                    OPT[i - 1][j - 1] + self.delta(self.x, self.y, i - 1, j - 1),

                    # insertion cost
                    OPT[i - 1][j] + self.gap_val,

                    # deletion cost
                    OPT[i][j - 1] + self.gap_val,
                )

        # finds and stores an optimal path solution in the solution dict
        self.find_solution(OPT, m, n)

        # finds and stores each cell's arrow solutions in the cell dict
        for i in range(m+1):
            for j in range(n+1):
                self.solve_cell(OPT, i, j)

        return OPT, self.solution, self.cell_dict


# menu to prompt user for initial input values
def user_menu():
    match = ''
    mismatch = ''
    gap = ''

    # prompts the user to enter 2 strings. strips away any white spaces or numbers
    input_1 = input("Enter a sequence of letters (this will be displayed on the top row)\n").strip().replace(" ", "")
    seq_1 = ''.join([i for i in input_1 if not i.isdigit()]).upper()

    input_2 = input("Enter another sequence of letters (this will be displayed on the left column)\n").strip().replace(" ", "")
    seq_2 = ''.join([i for i in input_2 if not i.isdigit()]).upper()

    # prompts the user to enter values for match/mismatch/gap until integer is found
    while not is_digit(match):
        match = input("Please enter an integer for the Match value:\n")

    while not is_digit(mismatch):
        mismatch = input("Match value added successfully! Please enter an integer for the Mismatch value:\n")

    while not is_digit(gap):
        gap = input("Mismatch value added successfully! Please enter an integer for the Gap value:\n")


    match = int(match)
    mismatch = int(mismatch)
    gap = int(gap)

    return seq_1, seq_2, match, mismatch, gap

# function to check if the argumennt is a digit
def is_digit(n):
    is_digit = False

    try:
        a = int(n)
        is_digit = True
    except ValueError:
        is_digit = False

    return is_digit


# main function
if __name__ == '__main__':
    # gets initial input from user
    y, x, match, mismatch, gap = user_menu()

    # creates SequenceAlignment object with user's input as values
    sqalign = SequenceAlignment(x, y, match, mismatch, gap)

    # calls the alignment function and returns the matrix, the solution path, and arrow dictionary for each cell
    graph, solution, arrow_map = sqalign.alignment()

    # builds the visual graph using matplotlib
    Graph.build_graph(y, x, graph, arrow_map, solution)

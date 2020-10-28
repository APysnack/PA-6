import Graph

class SequenceAlignment(object):
    def __init__(self, x, y, match, mismatch, gap):
        self.x = x
        self.y = y
        self.solution = {}
        self.match_val = match
        self.mismatch_val = mismatch
        self.gap_val = gap
        self.cell_dict = {}

    # part of the alignment calculation - returns match_val if the alignment is a match, mismatch_val if mismatch
    def delta(self, x, y, i, j):
        if x[i] == y[j]:
            return self.match_val
        else:
            return self.mismatch_val

    # finds the paths for completing the optimal solution
    def find_solution(self, OPT, m, n):
        if m == 0 and n == 0:
            return

        # if n == 0 we cannot do an insert.
        insert = OPT[m][n - 1] + self.gap_val

        # the value of alignment is the top left diagonal cell + the value of match/mismatch
        align = OPT[m - 1][n - 1] + self.delta(self.x, self.y, m - 1, n - 1)

        delete = OPT[m - 1][n] + self.gap_val

        best_choice = max(insert, align, delete)

        if best_choice == insert:
            self.solution[(m, n)] = 'right'
            return self.find_solution(OPT, m, n - 1)
        elif best_choice == align:
            self.solution[(m, n)] = 'diagonal'
            return self.find_solution(OPT, m - 1, n - 1)
        elif best_choice == delete:
            self.solution[(m, n)] = 'down'
            return self.find_solution(OPT, m - 1, n)



    def solve_cell(self, OPT, m, n):
        if m == 0 or n == 0:
            return

        insert = OPT[m][n - 1] + self.gap_val
        align = OPT[m - 1][n - 1] + self.delta(self.x, self.y, m - 1, n - 1)
        delete = OPT[m - 1][n] + self.gap_val

        if align == insert == delete:
            self.cell_dict[(m, n)] = ['down', 'right', 'diagonal']
            return

        best_option = max(align, insert, delete)

        if align == insert and align == best_option:
            self.cell_dict[(m, n)] = ['right', 'diagonal']
            return

        if align == delete and align == best_option:
            self.cell_dict[(m, n)] = ['down', 'diagonal']
            return

        if insert == delete and insert == best_option:
            self.cell_dict[(m, n)] = ['right', 'down']
            return

        if align == best_option:
            self.cell_dict[(m, n)] = ['diagonal']
            return

        if insert == best_option:
            self.cell_dict[(m, n)] = ['right']
            return

        if delete == best_option:
            self.cell_dict[(m, n)] = ['down']
            return


    def alignment(self):
        n = len(self.y)
        m = len(self.x)
        OPT = [[0 for i in range(n + 1)] for j in range(m + 1)]

        for i in range(1, m + 1):
            OPT[i][0] = i * self.gap_val

        for j in range(1, n + 1):
            OPT[0][j] = j * self.gap_val

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                OPT[i][j] = max(
                    OPT[i - 1][j - 1] + self.delta(self.x, self.y, i - 1, j - 1),
                    OPT[i - 1][j] + self.gap_val,
                    OPT[i][j - 1] + self.gap_val,
                )

        self.find_solution(OPT, m, n)

        for i in range(m+1):
            for j in range(n+1):
                self.solve_cell(OPT, i, j)

        return OPT, self.solution, self.cell_dict


def user_menu():
    match = ''
    mismatch = ''
    gap = ''

    input_1 = input("Enter a sequence of letters (this will be displayed on the top row)\n").strip().replace(" ", "")
    seq_1 = ''.join([i for i in input_1 if not i.isdigit()]).upper()

    input_2 = input("Enter another sequence of letters (this will be displayed on the left column)\n").strip().replace(" ", "")
    seq_2 = ''.join([i for i in input_2 if not i.isdigit()]).upper()

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


def is_digit(n):
    is_digit = False

    try:
        a = int(n)
        is_digit = True
    except ValueError:
        is_digit = False

    return is_digit




if __name__ == '__main__':
    y, x, match, mismatch, gap = user_menu()
    sqalign = SequenceAlignment(x, y, match, mismatch, gap)
    graph, solution, arrow_map = sqalign.alignment()
    Graph.build_graph(y, x, graph, arrow_map, solution)

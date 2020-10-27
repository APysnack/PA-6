class SequenceAlignment(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.solution = []
        self.match_val = 5
        self.mismatch_val = -3
        self.gap_val = -2
        self.branch_count = 1
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
            self.solution.append("insert_" + str(self.y[n - 1]))
            return self.find_solution(OPT, m, n - 1)

        if best_choice == align:
            self.solution.append("align_" + str(self.y[n - 1]))
            return self.find_solution(OPT, m - 1, n - 1)

        if best_choice == delete:
            self.solution.append("remove_" + str(self.x[m - 1]))
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

        for line in OPT:
            print(line)

        self.find_solution(OPT, m, n)

        for i in range(m+1):
            for j in range(n+1):
                self.solve_cell(OPT, i, j)

        print(self.cell_dict)

        return OPT[m][n], self.solution[::-1]


if __name__ == '__main__':
    # x = 'TGACGTGC'
    # y = 'TCGACGTCA'
    path_list = []
    y = 'ACTAA'
    x = 'CCTT'
    print('We we want to transform: ' + x + ' to: ' + y)
    sqalign = SequenceAlignment(x, y)
    min_edit, b = sqalign.alignment()
    print('Minimum amount of edit steps are: ' + str(min_edit))
    print(b)
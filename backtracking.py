class BacktrackingSolver:
    def __init__(self, n):
        self.n = n
        self.board = [[0]*n for _ in range(n)]

    def is_safe(self, row, col):
        for i in range(row):
            if self.board[i][col] == 1:
                return False
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(row-1, -1, -1), range(col+1, self.n, 1)):
            if self.board[i][j] == 1:
                return False
        return True

    def solve(self, row=0):
        if row == self.n:
            return True
        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                if self.solve(row + 1):
                    return True
                self.board[row][col] = 0
        return False

    def get_board(self):
        return self.board




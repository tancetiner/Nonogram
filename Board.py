import random


class CellState:
    FILLED = 1
    CROSSED = -1
    UNKNOWN = 0


class Board:
    def __init__(self):
        self.dimension = 0
        self.data = []
        self.rowCounts = []
        self.colCounts = []
        self.rowCountMaxSize = 0
        self.colCountMaxSize = 0
        self.renderedBoard = []

    @staticmethod
    def return_random_bool():
        return random.randint(0, 1)

    @staticmethod
    def initialize_board(dimension):
        board = Board()
        board.dimension = dimension

        data = []
        isEmpty = True

        # Fill the board
        for i in range(dimension):
            row = []
            isEmpty = True
            for j in range(dimension):
                value = Board.return_random_bool()
                if value:
                    isEmpty = False
                row.append(value)
            if isEmpty:
                row[0] = True
            data.append(row)

        # Make sure no column is empty
        for j in range(dimension):
            isEmpty = True
            for i in range(dimension):
                if data[i][j] == 1:
                    isEmpty = False
            if isEmpty:
                data[0][j] = 1

        # Assign the data
        board.data = data

        # Count the row values
        for i in range(dimension):
            rowCount = []
            idx = 0
            count = 0
            while idx < dimension:
                if data[i][idx]:
                    count += 1  # increment if filled
                elif count != 0:
                    rowCount.append(count)  # add to the count list if non-zero
                    count = 0
                idx += 1
            if count != 0:
                rowCount.append(count)

            if len(rowCount) > board.rowCountMaxSize:
                board.rowCountMaxSize = len(rowCount)
            board.rowCounts.append(rowCount)

        # Count the col values
        for j in range(dimension):
            colCount = []
            idx = 0
            count = 0
            while idx < dimension:
                if data[idx][j]:
                    count += 1  # increment if filled
                elif count != 0:
                    colCount.append(count)  # add to the count list if non-zero
                    count = 0
                idx += 1

            if count != 0:
                colCount.append(count)
            if len(colCount) > board.colCountMaxSize:
                board.colCountMaxSize = len(colCount)
            board.colCounts.append(colCount)

        return board

    @staticmethod
    def print_board_without_counts(board):
        for row in board.data:
            print(" ".join(map(str, row)))

    @staticmethod
    def print_board_with_counts(board):
        rowCountMax = board.rowCountMaxSize
        colCountMax = board.colCountMaxSize

        gridDimX = board.dimension + rowCountMax + 1
        gridDimY = board.dimension + colCountMax + 1

        for i in range(gridDimY):
            if i == colCountMax:
                print("-" * gridDimX)
            else:
                rowCount = board.rowCounts[i - colCountMax - 1]
                for j in range(gridDimX):
                    if j == rowCountMax:
                        print("|", end="")
                    elif (
                        i < colCountMax
                        and j > rowCountMax
                        and len(board.colCounts[j - rowCountMax - 1]) >= colCountMax - i
                    ):
                        print(
                            board.colCounts[j - rowCountMax - 1][-colCountMax + i],
                            end="",
                        )
                    elif (
                        i > colCountMax
                        and j < rowCountMax
                        and len(board.rowCounts[i - colCountMax - 1]) >= rowCountMax - j
                    ):
                        print(
                            board.rowCounts[i - colCountMax - 1][-rowCountMax + j],
                            end="",
                        )
                    elif i > colCountMax and j > rowCountMax:
                        if board.data[i - colCountMax - 1][j - rowCountMax - 1]:
                            print("o", end="")
                        else:
                            print("x", end="")
                    else:
                        print(" ", end="")
                print()

    def initialize_rendered_board(self):
        self.renderedBoard = []
        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                row.append(CellState.UNKNOWN)
            self.renderedBoard.append(row)


# ___________________________Helper Functions____________________________________
def checkWinCondition(board: Board):
    for i in range(board.dimension):
        for j in range(board.dimension):
            if board.renderedBoard[i][j] == CellState.UNKNOWN:
                return False
    return True


def checkRowColCompleted(board: Board, position: tuple):
    row = position[0]
    col = position[1]

    rowCount = 0
    colCount = 0

    for i in range(board.dimension):
        if board.renderedBoard[row][i] == CellState.FILLED:
            rowCount += 1

    for i in range(board.dimension):
        if board.renderedBoard[i][col] == CellState.FILLED:
            colCount += 1

    if rowCount == sum(board.rowCounts[row]):
        for i in range(board.dimension):
            if board.renderedBoard[row][i] == CellState.UNKNOWN:
                board.renderedBoard[row][i] = CellState.CROSSED
    if colCount == sum(board.colCounts[col]):
        for i in range(board.dimension):
            if board.renderedBoard[i][col] == CellState.UNKNOWN:
                board.renderedBoard[i][col] = CellState.CROSSED


# ______________________________________________________________________________

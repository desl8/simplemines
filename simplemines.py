"""
A Simple Minesweeper Object
By: @desl8
Spring 2023
Python 3.10.8
"""

# -----import section-----


import random


# -----main section-----


class Game:
    def __init__(self, rows=14, cols=18, mines=40):
        self.rows = int(rows)  # Protects against float or string inputs
        self.columns = int(cols)  # Protects against float or string inputs
        self.mines = int(mines)  # Protects against float or string inputs
        self.board = [
            [Cell(row, col) for col in range(self.columns)] for row in range(self.rows)
        ]  # Create a board asset with instances of the Cell class
        self.game_board = None
        if self.mines >= (
            self.rows * self.columns
        ):  # Are there too many mines for the board?
            raise ValueError("Too many mines for the board")  # Raise the value error

    def add_mines(self):
        minesplaced = 0  # How many mines have been placed?
        while minesplaced < self.mines:  # While not all of the mines have been placed
            row = random.randint(0, (self.rows - 1))  # Pick a random row
            col = random.randint(0, (self.columns - 1))  # Pick a random column
            if not (self.board[row][col]).mine:  # If there is no mine there already
                (self.board[row][col]).switchmine()  # Add a mine
                minesplaced += 1  # One more mine has been placed

    def _clear_mines(self):
        for i in range(self.rows):  # For every row
            for j in range(self.columns):  # For every column in that row
                (self.board[i][j]).clearmine()  # Wipe the mine

    def fetchneighbors(self, row: int, col: int) -> int:
        """Gets the amount of neighbors to a cell

        Args:
            row (int): The row index of the cell
            col (int): The column index of the cell

        Returns:
            int: The number of neighbors for the cell
        """
        topslice = False  # Should the top be excluded?
        bottomslice = False  # Should the bottom be excluded?
        leftslice = False  # Should the left be excluded?
        rightslice = False  # Should the right be excluded?
        neighbors = 0  # Set current neighbors to 0
        row = int(row)  # Protects against non-integer inputs
        col = int(col)  # Protects against non-integer inputs

        if row == 0:  # Is in in the topmost row?
            topslice = True  # Do not check above
        if row == (self.rows - 1):  # Is it in the bottommost row?
            bottomslice = True  # Do not check below
        if col == 0:  # Is it in the leftmost column?
            leftslice = True  # Do not check the left side
        if col == (self.columns - 1):  # Is it in the rightmost column?
            rightslice = True  # Do not check the right side
        if not topslice:  # If the top is being checked
            if self.board[row - 1][col].mine:
                neighbors += 1
        if not topslice and not rightslice:  # If the right and top are being checked
            if self.board[row - 1][col + 1].mine:
                neighbors += 1
        if not rightslice:  # If the right side is being checked
            if self.board[row][col + 1].mine:
                neighbors += 1
        if (
            not bottomslice and not rightslice
        ):  # If the right and bottom are being checked
            if self.board[row + 1][col + 1].mine:
                neighbors += 1
        if not bottomslice:  # If the bottom is being checked
            if self.board[row + 1][col].mine:
                neighbors += 1
        if (
            not bottomslice and not leftslice
        ):  # If the left and bottom are being checked
            if self.board[row + 1][col - 1].mine:
                neighbors += 1
        if not leftslice:  # If the left side is being checked
            if self.board[row][col - 1].mine:
                neighbors += 1
        if not topslice and not leftslice:  # If the left and top are being checked
            if self.board[row - 1][col - 1].mine:
                neighbors += 1
        self.board[row][col].setneighbors(neighbors)
        return neighbors

    def opencell(self, row, col, specialopen=True):
        row = int(row)
        col = int(col)
        if self.board[row][col].open:
            return False
        self.fetchneighbors(row, col)
        fresh = True
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j].open:
                    fresh = False
        self.board[row][col].opencell()
        if fresh and self.board[row][col].mine:  # Did the user try to open on a mine?
            self._clear_mines()  # Clear mines
            self.add_mines()  # Refresh mines
            while self.board[row][col].mine:  # Is there still a mine there?
                self._clear_mines()  # Clear mines
                self.add_mines()  # Refresh mines
        if specialopen:  # Is it using the traditional opening method?
            # Special opening, in this case, is where any cell that has
            # no neighboring bombs will open all cells around it
            if self.board[row][col].neighbors == 0:
                topslice = False
                bottomslice = False
                leftslice = False
                rightslice = (
                    False  # Booleans for ignoring certain "slices" around a cell
                )
                if row == 0:  # If top row
                    topslice = True  # Top will be ignored
                if row == (self.rows - 1):  # If bottom row
                    bottomslice = True  # Bottom will be ignored
                if col == 0:  # Repeat for leftmost and rightmost rows respectively
                    leftslice = True
                if col == (self.columns - 1):
                    rightslice = True
                if (
                    not topslice
                    and not leftslice
                    and not self.board[row - 1][col - 1].open
                ):
                    self.opencell(row - 1, col - 1)
                if not topslice and not self.board[row - 1][col].open:
                    self.opencell(row - 1, col)
                if (
                    not topslice
                    and not rightslice
                    and not self.board[row - 1][col + 1].open
                ):
                    self.opencell(row - 1, col + 1)
                if not leftslice and not self.board[row][col - 1].open:
                    self.opencell(row, col - 1)
                if not rightslice and not self.board[row][col + 1].open:
                    self.opencell(row, col + 1)
                if (
                    not bottomslice
                    and not leftslice
                    and not self.board[row + 1][col - 1].open
                ):
                    self.opencell(row + 1, col - 1)
                if not bottomslice and not self.board[row + 1][col].open:
                    self.opencell(row + 1, col)
                if (
                    not bottomslice  # Is it supposed the check the bottom?
                    and not rightslice  # Is it supposed to check the right?
                    and not self.board[row + 1][
                        col + 1
                    ].open  # If the cell isn't already open
                ):
                    self.opencell(row + 1, col + 1)  # Open the

    def display(self, axes=True, debug=False):
        if axes:
            rowlist = []  # Just a list for the top row if the user wants axes
            rowlist += "■"  # A square for the top-left corner
            for i in range(self.columns):
                rowlist.append(
                    str(i)[-1]
                )  # Add column numbers but print only the end of the number so the board is not offset
        print(" ".join(rowlist))
        for i in range(self.rows):  # For every row in the minesweeper board
            rowlist = []  # Create a blank list of cell values for the row
            if axes:  # Does the user want axes on their board
                rowlist.append(
                    str(i)[-1]
                )  # Add row numbers but print only the end of the number so the board is not offset
            for j in range(self.columns):
                if self.board[i][j].open:
                    if (
                        self.board[i][j].neighbors >= 1
                    ):  # Does the cell have any neighbors?
                        rowlist += str(
                            self.board[i][j].neighbors
                        )  # Print out the number of neighbors to the cell
                    elif self.board[i][j].neighbors == 0:
                        rowlist += " "
                    else:
                        rowlist += "?"  # Something is wrong with the neighbors attribute. Contact Kevin
                else:
                    if (
                        self.board[i][j].mine and debug and not self.board[i][j].flag
                    ):  # Hackers can always find the bombs >:)
                        rowlist += "b"  # Bomb
                    elif self.board[i][j].flag:
                        rowlist += "⚑"  # Flagged cell
                    else:
                        rowlist += "■"  # Mystery cell! :D
            print(" ".join(rowlist))

    def checkstate(self):
        """0 for loss, 1 for still in progress, 2 for win"""
        state = 2  # The player has won unless decided otherwise by this ↓↓↓
        for i in range(self.rows):  # Scan every row
            for j in range(self.columns):  # Scan every column in the row
                if (
                    self.board[i][j].open and self.board[i][j].mine
                ):  # Has the user opened a mined cell?
                    return 0  # Player lost
                if (
                    not self.board[i][j].mine and not self.board[i][j].open
                ):  # Is there an unmined cell that is not open?
                    state = 1  # Game still in progress
        return state  # Return 1 or 2 based on previous assessment

    # def export_board(self, filename):
    # outfile = None


class Cell:
    def __init__(self, row, col):
        self.row = int(row)
        self.col = int(col)
        self.mine = False  # Cell currently has no mine
        self.flag = False  # Cell is currently unflagged
        self.open = False  # Cell in currently unopened
        self.neighbors = 0

    def switchmine(self):
        self.mine = not self.mine  # Swap the boolean state of the mine variable

    def switchflag(self):
        self.flag = not self.flag  # Swap the boolean state of the flag variable

    def opencell(self):
        self.open = True  # Open the cell

    def setneighbors(self, arg):
        self.neighbors = arg  # Set the neighbors variable to the input argument

    def clearmine(self):
        if self.mine:
            self.mine = False  # No mine anymore :D


class GameHandler:  # A Game Manager for debugging purposes
    def __init__(self, rows=14, cols=18, mines=40):
        self.rows = rows
        self.cols = cols
        self.mines = mines

    def rungame(self):
        """Runs the minesweeper game and edits parameters accordingly"""
        self.game_board = Game(self.rows, self.cols, self.mines)  # Create new gameboard
        self.game_board.add_mines()  # Add all of the mines
        self.game_board.display()  # Display the board
        while self.game_board.checkstate() == 1:  # While the game is still in progress
            openinput = "o"  # Input to open a cell
            flaginput = "f"  # Input to flag a cell
            inputtype = input(
                "Enter input type, (o to open cell, f to flag a cell): "  # Get input
            )
            row = int(input("Row: "))  # Row to flag/open
            col = int(input("Column: "))  # Column to flag/open
            if inputtype == openinput:  # Does input match the input to open a cell?
                self.game_board.opencell(row, col)  # Open the cell
            elif inputtype == flaginput:  # Does input match the input to flag a cell?
                self.game_board.board[row][col].switchflag()  # Flag the cell
            self.game_board.display()  # Display the board
        # Now outside of while loop, meaning user won or lost
        if self.game_board.checkstate() == 0:  # Did the user lose?
            print("💥 You Lost! 💥")  # Inform the user of loss
        if self.game_board.checkstate() == 2:  # Did the user win?
            print("✅ You Won! ✅")  # Inform the user of win


def main():
    """Start and run the Minesweeper game"""
    game = GameHandler()  # Open a game manager with default values
    game.rungame()  # Run a game


if __name__ == "__main__":
    main()  # Pretty self explanatory if you ask me

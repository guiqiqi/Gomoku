"""
Draw game interface
Use Tkinter and Canvas to draw interface
Provide a way to draw pieces
"""

import tkinter
import tkinter.messagebox as msg
from typing import Callable, Iterable, NoReturn, Tuple, Union


class Board:
    """
    Gaming Board Interface
    Use canvas to draw horizontal and vertical lines
    Handle mouse click events, generate click
    position parameters and pass them to the middle layer

    Return value:
        True - Black
        False - White
    """
    # White space between the edge of the
    # window and the main interface of the game
    PADDING = 30
    ICONMAP = "logo.ico"
    TITLE = "Gomoku"  # Game window title

    BLACK = "Black"  # Black player
    WHITE = "White"  # White player
    BWIN = "#B52016"  # Win color black
    WWIN = "#EB9B96"  # Win color white

    BGCOLOR = "#FEBE0B"  # Background color for game board
    BHINT = "#333333"  # Black hinter
    WHINT = "#F0F0F0"  # White hinter

    LOCATINGR = 5  # Radius of location point
    OUTLINEMARG = 3  # Pixels margin of outline

    def __init__(self, root: tkinter.Tk, size: int, grids: int) -> None:
        """
        Instantiate a new game board object.
        Draw on the given parent Tk object.
        Parameters:
            root: in which window you want to draw
            size: total game window size
            grids: number of grids (usually 15 or 19)
        """
        # Check for grids number
        if (grids % 2 != 1):
            raise ValueError("Invalid grids number")

        # Patch for invalid size and grids
        self._root = root
        self._root.resizable(False, False)
        self._root.title(self.TITLE)
        self._grids, self._size = grids, size
        if self._size % (grids - 1) != 0:
            self._size = (self._size // (grids - 1)) * (grids - 1)

        # Draw canvas
        self._root = root
        self._board = tkinter.Canvas(
            root, width=self._size + self.PADDING * 2,
            height=self._size + self.PADDING * 2, bg=self.BGCOLOR)
        self._board.pack(anchor=tkinter.CENTER)
        self._unit = self._size // (grids - 1)
        self._board.focus_set()

        # Draw hint piece
        piece = int(self._unit / 3.0)
        self._hinter = self._board.create_oval(
            0, 0, -piece * 2, -piece * 2,
            fill=self.BHINT, outline="")

        # Bind left key and moving
        self._board.bind("<Button-1>", self._click)
        self._board.bind("<Motion>", self._moving)

        # Handle left key function
        self._click_handler = None
        self._restart_handler = None

        # Initial menubar
        menubar = tkinter.Menu(self._root)
        about = tkinter.Menu(menubar)
        controller = tkinter.Menu(menubar)
        menubar.add_cascade(label="Game", menu=controller)
        menubar.add_cascade(label="About", menu=about)

        controller.add_command(label="New Game", 
                               command=self._restart_handler)
        controller.add_separator()
        controller.add_command(label="Exit Game", command=self._exit)

        about.add_command(label="Help", command=self._help)
        about.add_command(label="About", command=self._about)
        root.configure(menu=menubar)

        # Configure icon
        root.iconbitmap(self.ICONMAP)

    @staticmethod
    def _help() -> None:
        """Show help dialog"""
        msg.showinfo("Help", (
            "Please choose the appropriate location.\n"
            "The color of the chess piece following the "
            "prompt of the mouse is the color of the "
            "upcoming chess piece."
        ))

    @staticmethod
    def _about() -> None:
        """Show about info"""
        msg.showinfo("About", (
            "This is a simple Gomoku.\n"
            "Wish you a happy game!"
        ))

    def win(self, who: str, turn: bool, pieces: Iterable[Tuple[int, int]]) -> None:
        """Show congratulations"""
        # Pieces to mark the winning side.
        for row, column in pieces:
            color = self.WWIN if not turn else self.BWIN
            self.play(row, column, color)

        msg.showinfo("Congratulations", "{player} win!".format(player=who))

    @property
    def click(self) -> Union[Callable[[int, int], bool], None]:
        """Return leftkey function"""
        return self._click_handler

    @click.setter
    def click(self, func: Union[Callable[[int, int], bool], None]) -> None:
        """Set leftkey handler"""
        self._click_handler = func

    @property
    def restart(self) -> Union[Callable[[int, int], NoReturn], None]:
        """Return restart function"""
        return self._restart_handler

    @restart.setter
    def restart(self, func: Union[Callable[[int, int], NoReturn], None]) -> None:
        """Set restart handler"""
        self._restart_handler = func

    def _click(self, position: tkinter.Event) -> None:
        """Handle for left key click event"""
        _x, _y = position.x - self.PADDING, position.y - self.PADDING
        if _x < 0 or _y < 0:
            return
        _x -= self._unit // 2
        _y -= self._unit // 2
        row, column = _x // self._unit + 1, _y // self._unit + 1
        if row > self._grids - 1 or column > self._grids - 1:
            return

        # Send row and column data to handler
        if not self._click_handler is None:
            
            # Check handler return value
            # If return True we change color and mark
            # Else do nothing
            try:
                opcode = self._click_handler(row, column)
                color = self.BLACK if opcode else self.WHITE
                self.play(row, column, color)
            except Exception as _error:
                return
                
            # Change hint color
            target = self._hinter
            hintcolor = self.BHINT if not opcode else self.WHINT
            self._board.itemconfig(target, fill=hintcolor)

    def _moving(self, position: tkinter.Event) -> None:
        """Handle moving event"""
        target = self._hinter
        xa, ya, xb, yb = self._board.coords(target)
        nx, ny = (xa + xb) / 2, (ya + yb) / 2
        dx, dy = position.x - nx, position.y - ny
        self._board.move(target, dx, dy)

    def _exit(self) -> None:
        """Destory window and exit game"""
        self._root.destroy()
        __import__("sys").exit(0)

    def play(self, row: int, column: int, color: str) -> None:
        """Drop off at the specified position"""
        _x = row  * self._unit + self.PADDING
        _y = column * self._unit + self.PADDING
        radius = int(self._unit / 3.0)
        position = _x - radius, _y - radius, _x + radius, _y + radius
        self._board.create_oval(*position, fill=color, outline="")

    def draw(self) -> None:
        """Draw vertical and horizontal lines as the game board"""
        for index in range(self._grids):
            # Draw horizontal
            startx = self.PADDING, self.PADDING + self._unit * index
            endx = self.PADDING + self._size, self.PADDING + self._unit * index
            self._board.create_line(*startx, *endx)

            # Draw vertical
            starty = self.PADDING + index * self._unit, self.PADDING
            endy = self.PADDING + index * self._unit, self.PADDING + self._size
            self._board.create_line(*starty, *endy)

        # Draw locating point
        for row, column in {
            (3, 3), (self._grids - 4, self._grids - 4),
            (3, self._grids - 4), (self._grids - 4, 3),
            (self._grids // 2, self._grids // 2)}:
            _x = row  * self._unit + self.PADDING
            _y = column * self._unit + self.PADDING
            positions = _x - self.LOCATINGR, _y - self.LOCATINGR, \
                        _x + self.LOCATINGR, _y + self.LOCATINGR
            self._board.create_oval(*positions, fill=self.BLACK)

        # Draw outline
        self._board.create_rectangle(
            self.PADDING - self.OUTLINEMARG, 
            self.PADDING - self.OUTLINEMARG,
            self._size + self.PADDING + self.OUTLINEMARG, 
            self._size + self.PADDING + self.OUTLINEMARG)


# Test game viewing
if __name__ == "__main__":

    root = tkinter.Tk()
    size = 650
    grids = 15

    value = 0
    checked = set()

    # Test click handler
    def test(row, column):
        global value, checked
        if (row, column) in checked:
            raise ValueError("Checked!")
        value += 1
        checked.add((row, column))
        return True if value % 2 else False

    board = Board(root, size, grids)
    board.click = test
    board.draw()
    root.focus_get()
    root.mainloop()

import wx
from collections import deque


# class that represents the main window of the application
class ChessGridGUI(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Chess Grid")

        # set the size of the window
        self.SetSize(400, 500)

        self.initial_blue_positions = {
            (0, 0): 1,  # Bishop
            (0, 1): 0,  # Pawn
            (0, 2): 2   # King
        }

        self.initial_white_positions = {
            (2, 0): 2,  # King
            (2, 1): 0,  # Pawn
            (2, 2): 1   # Bishop
        }

        # create a panel that will contain all the elements of the window
        self.panel = wx.Panel(self)

        # set color to white
        self.whichColor = "white"

        # string that reflect the current state of the program,
        self.status = "Waiting for user input..."

        # object that will arrange items in a vertical column
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # create a control that will display current color (white or blue)
        self.color_indicator = wx.StaticText(
            self.panel, label=f"Current Color: {self.whichColor.title()}")

        # create a label that keeps the user informed about the current status of the application
        self.status_indicator = wx.StaticText(
            self.panel, label=f"Status: {self.status.title()}")

        # object that helps in arranging the controls in the window in a vertical column
        indicator_sizer = wx.BoxSizer(wx.VERTICAL)

        # ensure that labels expand horizontally to take up any avaiable space when the window is resized
        indicator_sizer.Add(self.color_indicator, flag=wx.EXPAND)
        indicator_sizer.Add(self.status_indicator, flag=wx.EXPAND)

        # the indicators are arranged within the main window´s layout and their content is aligned to the left of the available space
        self.main_sizer.Add(indicator_sizer, flag=wx.ALIGN_LEFT)

        # object that will arrange controls in a grid 3x3, between controls won´t be any space
        self.grid_sizer = wx.GridSizer(3, 3, 0, 0)

        # initalize arrays to store buttons, the color of the buttons and images displayed on the buttons
        self.button_grid = [[None for _ in range(3)] for _ in range(3)]
        self.button_colors = [['empty' for _ in range(3)] for _ in range(3)]
        self.button_images = [[None for _ in range(3)] for _ in range(3)]

        # dictionary that keeps track of which pieces haven´t been used yet
        self.unused_pieces = {'white': [0, 1, 2], 'blue': [0, 1, 2]}

        # images for white and blue chess pieces
        self.white_images = ["images/white_pawn.png",
                             "images/white_bishop.png", "images/white_king.png"]
        self.blue_images = ["images/blue_pawn.png",
                            "images/blue_bishop.png", "images/blue_king.png"]

        # image that will be displayed on an empty button
        self.default_image = "images/default_button.png"

        # create buttons on the grid and the control buttons
        self.create_buttons()
        self.create_control_buttons()

        # self.main_sizer is responsible for managing the size and positioning of elements within self.panel
        self.panel.SetSizer(self.main_sizer)

        # adjust positions and sizes of the buttons and labels based on the current size of a window
        self.Layout()

    # create a grid of buttons
    def create_buttons(self):

        # for each row
        for row in range(3):

            # for each column
            for col in range(3):
                # create a button of size 100x100 pixels and assign it an ID
                button = wx.Button(self.panel, wx.ID_ANY, size=(100, 100))

                # when the button is clicked, self.button_click will be called
                button.Bind(wx.EVT_BUTTON, lambda evt, r=row,
                            c=col: self.button_click(evt, r, c))

		# if there's supposed to be a white chess piece at this position
                if (row, col) in self.initial_white_positions:

                    # index of that white chess piece
                    piece_index = self.initial_white_positions[(row, col)]

                    # work with white chess piece
                    self.whichColor = "white"

                    # update the image of the chess piece on a button
                    self.update_button_image(button, row, col, piece_index)

                    # remove piece_index from the list of white chess pieces that haven´t been yet positioned on the board
                    self.unused_pieces["white"].remove(piece_index)

                elif (row, col) in self.initial_blue_positions:
                    piece_index = self.initial_blue_positions[(row, col)]
                    self.whichColor = "blue"
                    self.update_button_image(button, row, col, piece_index)
                    self.unused_pieces["blue"].remove(piece_index)

		# update the image to indicate that there is no chess piece
                else:
                    self.update_button_image(button, row, col, None)


                # add a grid of buttons to self.main_sizer
                self.grid_sizer.Add(button, flag=wx.EXPAND)

                # store the button based on its current row and column
                self.button_grid[row][col] = button

        self.main_sizer.AddStretchSpacer()

        # add a grid of buttons to self_main_sizer and ensure that grid_sizer is centered within the main_sizer
        self.main_sizer.Add(self.grid_sizer, flag=wx.ALIGN_CENTER)

        # together with the previous AddStretchSpacer causes the grid of buttons to be centered vertically in the window
        self.main_sizer.AddStretchSpacer()

    # create two buttons Change Color and Return
    def create_control_buttons(self):

        # create a new button with the label Change Color and assign it an ID
        change_color_button = wx.Button(self.panel, wx.ID_ANY, "Change Color")

        # when the button (Change Color) is clicked, self.change_color will be called
        change_color_button.Bind(wx.EVT_BUTTON, self.change_color)

        # add the button to self.main_sizer, the button will be centered based on the space given by the sizer
        self.main_sizer.Add(change_color_button, flag=wx.ALIGN_CENTER)

        # create a new button with the label Return and assign it an ID
        return_button = wx.Button(self.panel, wx.ID_ANY, "Return")

        # when the button (Return) is clicked, self.retzrb_board will be called
        return_button.Bind(wx.EVT_BUTTON, self.return_board)

        # add the button to self.main_sizer, the button will be centered based on the space given by the sizer
        self.main_sizer.Add(return_button, flag=wx.ALIGN_CENTER)

    # when a button on the grid is clicked, the button´s image and color is updated
    def button_click(self, event, row, col):

        # retrieve an object from button_grid based on a position passed to the function
        button = self.button_grid[row][col]

        # retrieve the current color of the button
        current_color = self.button_colors[row][col]

        # if the color of the clicked button is the same as the current color
        if current_color == self.whichColor:

            # retrieve the index of the image used on the button
            current_image_index = self.button_images[row][col]

            # if the button has already an image
            if current_image_index is not None:

                # add the index of the image to the list of unused pieces
                self.unused_pieces[self.whichColor].append(current_image_index)

                # remove the button´s image
                self.button_images[row][col] = None

                # set the button´s color is to empty
                self.button_colors[row][col] = 'empty'

                # update the image displayed on the button to show an initial image
                self.update_button_image(button, row, col, None)

            # if there are unused pieces of the current color
            elif len(self.unused_pieces[self.whichColor]) > 0:

                # take the first unused piece of the current color
                next_image_index = self.unused_pieces[self.whichColor].pop(0)

                # the button´s image is updated to show the new piece
                self.update_button_image(button, row, col, next_image_index)

        # if the current button is not assigned any piece and if there are any unused pieced with the current color
        elif current_color == 'empty' and len(self.unused_pieces[self.whichColor]) > 0:

            # take the first unused piece of the current color
            next_image_index = self.unused_pieces[self.whichColor].pop(0)

            # the button´s image is updated to show the new piece
            self.update_button_image(button, row, col, next_image_index)

    def update_button_image(self, button, row, col, image_index):

        # if image_index is not None, it sets the color of the button at the relevant position to white/blue (else to empty)
        self.button_colors[row][col] = self.whichColor if image_index is not None else 'empty'

        # set the image index of the button to the index of the image for the pawn/bishop/king
        self.button_images[row][col] = image_index

        # if there´s no specific image assigned for the button
        if image_index is None:

            # set image_path to default_image which is used for buttons that do not represent any chess piece
            image_path = self.default_image

        # if there is a specific image used for the button
        else:

            # select images based on the current color
            image_list = self.white_images if self.whichColor == 'white' else self.blue_images

            # set image_path to the specific image from the list
            image_path = image_list[image_index]

        # load an image (it can be in any format) from image_path
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)

        # fit the image within the size of the button
        image = image.Scale(
            button.GetSize()[0] - 20, button.GetSize()[1] - 20, wx.IMAGE_QUALITY_HIGH)

        # convert an image to a format suitable for display on a button
        bitmap = wx.Bitmap(image)

        # change the image displayed on the button to the bitmap
        button.SetBitmap(bitmap)

    # switch color from white to blue or from blue to white
    def change_color(self, event):

        # if the current color is white, change it to blue, else change it to white
        self.whichColor = 'white' if self.whichColor == 'blue' else 'blue'

        # update the label that displays the current color
        self.color_indicator.SetLabel(
            f"Current Color: {self.whichColor.title()}")

    # calculate and print the positions of all pieces on the board and the total number of moves taken to get from their initial positions to their current positions
    def return_board(self, event):
        print("Calculating...")
        # the program is now perfoming a calculation
        self.status = "Calculating..."

        # update the text on the label
        self.status_indicator.SetLabel(f"Status: {self.status.title()}")

        # update the text immediately even if the calculation is being performed
        self.status_indicator.Update()

        # list of positions and pieces for white and blue pieces
        white_positions = []
        blue_positions = []

        # iterate through each row and column
        for row in range(3):
            for col in range(3):

                # check if the piece at the current row and column is white
                if self.button_colors[row][col] == 'white':

                    # get the name of chess piece
                    piece = self.get_piece_name(self.button_images[row][col])

                    # add the position and the name of the piece to the list of white positions and pieces
                    white_positions.append(((row, col), piece))

                elif self.button_colors[row][col] == 'blue':
                    piece = self.get_piece_name(self.button_images[row][col])
                    blue_positions.append(((row, col), piece))

        print("White positions and pieces:", white_positions)
        print("Blue positions and pieces:", blue_positions)

        # find legal moves for a chess piece
        def generate_moves(pos, piece, color, state):

            # variable that stores moves depending on the chess piece (and if the chess piece is Pawn, then depending on the color)
            possible_moves = movement_rules[piece] if piece != 'Pawn' else movement_rules[piece][color]

            # store valid moves that the piece can make
            moves = []

            # loop over all possible moves
            for dx, dy in possible_moves:

                # calculate the new position of the chess piece
                new_pos = (pos[0] + dx, pos[1] + dy)

                # if the move is valid (position within the game board, unoccupied or occupied by a piece with different color)
                if 0 <= new_pos[0] < 3 and 0 <= new_pos[1] < 3 and (new_pos not in state or state[new_pos][0] != color):
                    # the new position is added to the list of valid moves
                    moves.append(new_pos)

            # return the list of valid moves for the piece at the position
            return moves

        # update the state of the game board
        def do_next_move(state, pos, new_pos):

            # move the piece at the current position pos to the new position new_pos
            state[new_pos] = state.pop(pos)

            # return updated state of the game board
            return state

        # dictionary that stores the rules for movement of each piece
        movement_rules = {
            'Pawn': {
                'blue': [(1, 0)],
                'white': [(-1, 0)]
            },
            'King': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            'Bishop': [(1, 1), (1, -1), (-1, -1), (-1, 1)],
        }

        # Define the initial and final positions of pieces
        initial_white_positions = [
            ((2, 0), 'King'), ((2, 1), 'Pawn'), ((2, 2), 'Bishop')]
        initial_blue_positions = [
            ((0, 0), 'Bishop'), ((0, 1), 'Pawn'), ((0, 2), 'King')]
        final_white_positions = white_positions
        final_blue_positions = blue_positions

        # Define the state as a dictionary, where keys are positions and values are pieces
        initial_state = {pos: ('white', piece)
                         for pos, piece in initial_white_positions}
        initial_state.update({pos: ('blue', piece)
                              for pos, piece in initial_blue_positions})

        final_state = {pos: ('white', piece)
                       for pos, piece in final_white_positions}
        final_state.update({pos: ('blue', piece)
                            for pos, piece in final_blue_positions})

        # Initialize the list of all possible games with the initial state
        games = deque([(initial_state, [], 'white')])

        # game states that have already been visited
        visited_states = set()

        # While there are still games to explore
        while games:
            # Get the current state, moves, and turn
            state, moves, turn = games.popleft()

            # open/create file and add the state to it
            with open('temp.txt', 'a') as temp_file:
                temp_file.write(f"{state}\n")

            # create a hashable representation of the current game state
            state_hash = hash(frozenset(state.items()))

            # if the state has already been explored
            if state_hash in visited_states:
                # continue with a next iteration
                continue

            # mark the current state as visited
            visited_states.add(state_hash)

            # If the current state is the final state
            if state == final_state:
                with open('results.txt', 'a') as file:

                    # write the moves to the file
                    file.write(str(moves) + '\n')

                print(moves)

                # animates the moves that led to the state
                self.animate_moves(moves)

                break

            # Otherwise, generate all possible next states
            else:
                # For each piece on the board
                for pos, (color, piece) in list(state.items()):
                    # If it is not the current player's turn, skip
                    if color != turn:
                        continue

                    # iterate through the possible new positions that the piece can move to based on its type and current position
                    for new_pos in generate_moves(pos, piece, color, state):
                        # create a new game state by moving the piece from the current to the new position
                        new_state = do_next_move(state.copy(), pos, new_pos)

                        # Change the turn
                        new_turn = 'white' if turn == 'blue' else 'blue'

                        # Add the new state, moves till this point, current move and turn to the list of games
                        games.append(
                            (new_state, moves + [(color, piece, pos, new_pos)], new_turn))

	# the program couldn´t find a solution
        else:
            print("No solution found!")
            self.status = "No solution found!"

            # update the text on the label immediately
            self.status_indicator.SetLabel(f"Status: {self.status.title()}")
            self.status_indicator.Update()

    # set up and start the animation of the chess pieces on the game board
    def animate_moves(self, moves):

        # the animation is in progress
        self.status = "Animating..."

        # update the label to reflect the current status
        self.status_indicator.SetLabel(f"Status: {self.status.title()}")

        # the status is immediately visible to the user
        self.status_indicator.Update()

        # the list of moves that will be animated
        self.moves = moves

        # lists with initial positions of the white and blue chess pieces (they contain a position and the type of piece)
        initial_white_positions = [
            ((2, 0), 'King'), ((2, 1), 'Pawn'), ((2, 2), 'Bishop')]
        initial_blue_positions = [
            ((0, 0), 'Bishop'), ((0, 1), 'Pawn'), ((0, 2), 'King')]

        # loop over each row index of the 3x3 grid
        for row in range(3):

            # loop over each column index of the 3x3 grid
            for col in range(3):
                # the button at the current row and column
                button = self.button_grid[row][col]

                # the image on the button is set to the initial image
                self.update_button_image(button, row, col, None)

                # set the color associated with the button to empty
                self.button_colors[row][col] = 'empty'

                # there´s no chess image of chess piece associated with this button
                self.button_images[row][col] = None

        # set the current active color to white
        self.whichColor = 'white'

        # loop over each tuple (pos - (row, column), piece - type of chess piece)
        for pos, piece in initial_white_positions:
            # map the name of each type of chess piece to an index
            piece_map = {"Pawn": 0, "Bishop": 1, "King": 2}

            # retrieve the index corresponding to the current piece
            piece_index = piece_map[piece]

            # a white piece is on this button
            self.button_colors[pos[0]][pos[1]] = self.whichColor

            # which image should be displayed on this button
            self.button_images[pos[0]][pos[1]] = piece_index

            # retrieve the button at the current position
            button = self.button_grid[pos[0]][pos[1]]

            # update the image displayed on the button to match the current piece
            self.update_button_image(button, pos[0], pos[1], piece_index)

        # the same process repeated for the blue pieces
        self.whichColor = 'blue'
        for pos, piece in initial_blue_positions:
            piece_map = {"Pawn": 0, "Bishop": 1, "King": 2}
            piece_index = piece_map[piece]
            self.button_colors[pos[0]][pos[1]] = self.whichColor
            self.button_images[pos[0]][pos[1]] = piece_index
            button = self.button_grid[pos[0]][pos[1]]
            self.update_button_image(button, pos[0], pos[1], piece_index)

        # counter that keeps track of the current number of moves
        self.move_index = 0

        # trigger the first move in the animation after two seconds
        wx.CallLater(2000, self.do_next_move)

    # animation of a sequence of moves in the chess game
    def do_next_move(self):

        # while there are any moves left to animate
        if self.move_index < len(self.moves):

            # current move to be animated
            move = self.moves[self.move_index]
            self.move_index += 1

            # start and end positions from the current move
            start_row, start_col = move[2]
            end_row, end_col = move[3]

            # map the name of each type of chess piece to an index
            piece_map = {"Pawn": 0, "Bishop": 1, "King": 2}

            # get the index of the piece that is moving
            piece_index = piece_map[move[1]]

            # button representing the starting position of the move
            button = self.button_grid[start_row][start_col]

            # set an initial image to the button at the starting position
            self.update_button_image(button, start_row, start_col, None)

            # update the color and image attributes of the button to indicate that no chess piece is there
            self.button_colors[start_row][start_col] = 'empty'
            self.button_images[start_row][start_col] = None

            # color of the moving chess piece
            self.whichColor = move[0]

            # update color and image attributes at the ending position to indicate that the chess piece has moved there
            self.button_colors[end_row][end_col] = move[0]
            self.button_images[end_row][end_col] = piece_index

            # button representing the ending position
            button = self.button_grid[end_row][end_col]

            # display the image of the moved piece on the button at the ending position
            self.update_button_image(button, end_row, end_col, piece_index)

            # the next move will be done after one second
            wx.CallLater(1000, self.do_next_move)

        # if there are no more moves left to animate
        else:

            # the animation of moves is completed
            self.status = "Done Animating..."

            # update the label for the user
            self.status_indicator.SetLabel(f"Status: {self.status.title()}")

            # ensure that the updated label is displayed to the user
            self.status_indicator.Update()

    # convert an index into a name of a specific type of chess piece
    def get_piece_name(self, piece_index):

        # if there is not chess piece
        if piece_index is None:
            return 'None'

        piece_names = ['Pawn', 'Bishop', 'King']

        # based on the piece_index return the name of the piece
        return piece_names[piece_index]


# Checks if this script is being run directly and not imported as a module
if __name__ == "__main__":
    app = wx.App()
    window = ChessGridGUI()
    window.Show()

    # Starts the main event loop of the application
    app.MainLoop()

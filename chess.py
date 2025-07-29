import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Chess")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (200, 200, 200) # Light grey
DARK_SQUARE = (100, 100, 100)  # Dark grey
HIGHLIGHT_COLOR = (0, 255, 0, 100) # Green with transparency
INVALID_MOVE_COLOR = (255, 0, 0, 100) # Red with transparency for invalid moves

# Board setup
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Chess piece representation (single letters)
# Lowercase for white, uppercase for black
PIECES = {
    'p': 'P', 'r': 'R', 'n': 'N', 'b': 'B', 'q': 'Q', 'k': 'K', # White pieces
    'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K'  # Black pieces (using same letter for display)
}

# Initial board state (FEN-like representation)
# 'p' for white pawn, 'P' for black pawn, etc.
# Lowercase for white, uppercase for black
INITIAL_BOARD = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
]

# Game state variables
board = [row[:] for row in INITIAL_BOARD] # Create a deep copy of the initial board
selected_square = None # (row, col) of the selected piece
turn = 'white' # 'white' or 'black'
message = "" # Message to display to the user

# Font for pieces and messages
FONT_SIZE = int(SQUARE_SIZE * 0.7)
font = pygame.font.Font(None, FONT_SIZE) # Default font
message_font = pygame.font.Font(None, 30)

def draw_board():
    """Draws the chessboard squares."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(SCREEN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    """Draws the chess pieces on the board."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece_code = board[row][col]
            if piece_code != ' ':
                piece_char = PIECES.get(piece_code) # Get the display character (e.g., 'P')
                if piece_char:
                    # Determine piece color based on case of the piece_code (original board representation)
                    text_color = BLACK if piece_code.islower() else WHITE # Black for white pieces, White for black pieces
                    text_surface = font.render(piece_char, True, text_color)
                    text_rect = text_surface.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                              row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    SCREEN.blit(text_surface, text_rect)

def highlight_square(row, col, color=HIGHLIGHT_COLOR):
    """Highlights a given square with a specified color."""
    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA) # Create a transparent surface
    s.fill(color)
    SCREEN.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_from_mouse_pos(pos):
    """Converts mouse position to board (row, col)."""
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def get_piece_info(row, col):
    """Returns the piece code and its color ('white' or 'black') at a given square."""
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None, None
    piece_code = board[row][col]
    if piece_code == ' ':
        return None, None
    color = 'white' if piece_code.islower() else 'black'
    return piece_code, color

def is_path_clear(start_row, start_col, end_row, end_col):
    """Checks if the path between two squares is clear for Rook, Bishop, Queen."""
    dr = end_row - start_row
    dc = end_col - start_col

    if dr == 0: # Horizontal move
        step_c = 1 if dc > 0 else -1
        for c in range(start_col + step_c, end_col, step_c):
            if board[start_row][c] != ' ':
                return False
    elif dc == 0: # Vertical move
        step_r = 1 if dr > 0 else -1
        for r in range(start_row + step_r, end_row, step_r):
            if board[r][start_col] != ' ':
                return False
    elif abs(dr) == abs(dc): # Diagonal move
        step_r = 1 if dr > 0 else -1
        step_c = 1 if dc > 0 else -1
        r, c = start_row + step_r, start_col + step_c
        while r != end_row:
            if board[r][c] != ' ':
                return False
            r += step_r
            c += step_c
    return True

def is_valid_move(start_row, start_col, end_row, end_col):
    """
    Checks if a move is valid according to chess rules for each piece.
    Does not include check/checkmate logic or special moves like castling/en passant.
    """
    global message
    message = ""

    if (start_row, start_col) == (end_row, end_col):
        message = "Cannot move to the same square."
        return False

    piece_code, piece_color = get_piece_info(start_row, start_col)
    if piece_code is None:
        message = "No piece selected."
        return False

    if piece_color != turn:
        message = f"It's {turn}'s turn. Please select your own piece."
        return False

    target_piece_code, target_piece_color = get_piece_info(end_row, end_col)

    if target_piece_code is not None and target_piece_color == piece_color:
        message = "Cannot capture your own piece."
        return False

    # Piece-specific move validation
    piece_type = piece_code.lower() # 'p', 'r', 'n', 'b', 'q', 'k'

    if piece_type == 'p': # Pawn
        # Direction of movement depends on color
        direction = -1 if piece_color == 'white' else 1
        start_rank = 6 if piece_color == 'white' else 1

        # Forward move
        if start_col == end_col:
            if target_piece_code is None: # Cannot capture forward
                if end_row == start_row + direction: # Single step
                    return True
                elif start_row == start_rank and end_row == start_row + 2 * direction: # Two-step initial move
                    if board[start_row + direction][start_col] == ' ': # Path must be clear
                        return True
        # Capture move
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if target_piece_code is not None and target_piece_color != piece_color:
                return True
        message = "Invalid pawn move."
        return False

    elif piece_type == 'r': # Rook
        if (start_row == end_row or start_col == end_col) and is_path_clear(start_row, start_col, end_row, end_col):
            return True
        message = "Invalid rook move."
        return False

    elif piece_type == 'n': # Knight
        dr = abs(start_row - end_row)
        dc = abs(start_col - end_col)
        if (dr == 2 and dc == 1) or (dr == 1 and dc == 2):
            return True
        message = "Invalid knight move."
        return False

    elif piece_type == 'b': # Bishop
        if abs(start_row - end_row) == abs(start_col - end_col) and is_path_clear(start_row, start_col, end_row, end_col):
            return True
        message = "Invalid bishop move."
        return False

    elif piece_type == 'q': # Queen
        if (start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col)) \
           and is_path_clear(start_row, start_col, end_row, end_col):
            return True
        message = "Invalid queen move."
        return False

    elif piece_type == 'k': # King
        dr = abs(start_row - end_row)
        dc = abs(start_col - end_col)
        if dr <= 1 and dc <= 1:
            return True
        message = "Invalid king move."
        return False

    return False # Should not reach here if all pieces are handled

def make_move(start_row, start_col, end_row, end_col):
    """Executes a move on the board."""
    piece_to_move = board[start_row][start_col]
    board[end_row][end_col] = piece_to_move
    board[start_row][start_col] = ' ' # Clear the starting square

    # Switch turns
    global turn
    turn = 'black' if turn == 'white' else 'white'
    global message
    message = "" # Clear message after successful move

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            clicked_row, clicked_col = get_square_from_mouse_pos(mouse_pos)

            if selected_square:
                # A piece is already selected, try to move it
                start_row, start_col = selected_square
                if is_valid_move(start_row, start_col, clicked_row, clicked_col):
                    make_move(start_row, start_col, clicked_row, clicked_col)
                    selected_square = None # Deselect after move
                else:
                    # If invalid move, keep selected or deselect based on preference
                    # For now, deselect and show message
                    selected_square = None
            else:
                # No piece selected, try to select one
                piece_code, piece_color = get_piece_info(clicked_row, clicked_col)
                if piece_code is not None and piece_color == turn:
                    selected_square = (clicked_row, clicked_col)
                    message = "" # Clear message when selecting a valid piece
                elif piece_code is not None and piece_color != turn:
                    message = f"It's {turn}'s turn. Please select your own piece."
                else:
                    message = "No piece selected."


    # Drawing
    SCREEN.fill(BLACK) # Clear screen
    draw_board()
    if selected_square:
        highlight_square(selected_square[0], selected_square[1])
    draw_pieces()

    # Display message
    if message:
        message_surface = message_font.render(message, True, (255, 255, 0)) # Yellow text
        message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT - 20))
        SCREEN.blit(message_surface, message_rect)

    pygame.display.flip() # Update the display

pygame.quit()
sys.exit()

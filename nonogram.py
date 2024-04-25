from Board import *
import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Get window dimensions of the system
WINDOW_WIDTH, WINDOW_HEIGHT = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
ASH_GRAY = (204, 215, 197)
CORAL_PINK = (238, 148, 128)

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Nonogram")

# Initialize the board
board = Board.initialize_board(10)
board.initialize_rendered_board()

# Initialize game variables
currentPos = (0, 0)
health = 3

# Randomly fill some cells
for i in range(board.dimension):
    for j in range(board.dimension):
        if board.data[i][j] == False and random.randint(0, 100) < 20:
            board.renderedBoard[i][j] = CellState.CROSSED

# Constants for the board
DIMENSION = board.dimension
CELL_SIZE = math.ceil(WINDOW_HEIGHT / (2 * DIMENSION))

BOARD_START_HEIGHT = math.ceil(
    WINDOW_HEIGHT / 2 - CELL_SIZE * DIMENSION / 2 + CELL_SIZE / 2
)
BOARD_START_WIDTH = math.ceil(
    WINDOW_WIDTH / 2 - CELL_SIZE * DIMENSION / 2 + CELL_SIZE / 2
)

BOARD_END_HEIGHT = math.ceil(
    WINDOW_HEIGHT / 2 + CELL_SIZE * DIMENSION / 2 + CELL_SIZE / 2
)
BOARD_END_WIDTH = math.ceil(
    WINDOW_WIDTH / 2 + CELL_SIZE * DIMENSION / 2 + CELL_SIZE / 2
)


# Initialize fonts
headerFont = pygame.font.SysFont(None, WINDOW_HEIGHT // 20)
font = pygame.font.SysFont(None, WINDOW_HEIGHT // 30)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_w:
                currentPos = (max(0, currentPos[0] - 1), currentPos[1])
            elif event.key == pygame.K_s:
                currentPos = (min(DIMENSION - 1, currentPos[0] + 1), currentPos[1])
            elif event.key == pygame.K_a:
                currentPos = (currentPos[0], max(0, currentPos[1] - 1))
            elif event.key == pygame.K_d:
                currentPos = (currentPos[0], min(DIMENSION - 1, currentPos[1] + 1))
            elif event.key == pygame.K_RETURN:
                if (
                    board.renderedBoard[currentPos[0]][currentPos[1]]
                    == CellState.UNKNOWN
                ):
                    if board.data[currentPos[0]][currentPos[1]] == True:
                        board.renderedBoard[currentPos[0]][
                            currentPos[1]
                        ] = CellState.FILLED
                    else:
                        health -= 1
                        board.renderedBoard[currentPos[0]][
                            currentPos[1]
                        ] = CellState.CROSSED
                    checkRowColCompleted(board, currentPos)
            elif event.key == pygame.K_RSHIFT:
                if (
                    board.renderedBoard[currentPos[0]][currentPos[1]]
                    == CellState.UNKNOWN
                ):
                    if board.data[currentPos[0]][currentPos[1]] == False:
                        board.renderedBoard[currentPos[0]][
                            currentPos[1]
                        ] = CellState.CROSSED
                    else:
                        health -= 1
                        board.renderedBoard[currentPos[0]][
                            currentPos[1]
                        ] = CellState.FILLED
                    checkRowColCompleted(board, currentPos)

    # Clear the screen
    screen.fill(ASH_GRAY)

    # Print Nonogram at the top on the middle
    text = headerFont.render("Nonogram", True, (0, 0, 0))
    screen.blit(
        text,
        (
            WINDOW_WIDTH / 20 + text.get_width() / 2,
            WINDOW_HEIGHT / 20 + text.get_height(),
        ),
    )

    # Print the health
    text = font.render(f"Health {health}", True, (0, 0, 0))
    screen.blit(
        text,
        (
            WINDOW_WIDTH - WINDOW_WIDTH / 10 - text.get_width(),
            WINDOW_HEIGHT - WINDOW_HEIGHT / 10 - text.get_height(),
        ),
    )

    # Draw the board
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board.renderedBoard[i][j] == CellState.FILLED:
                pygame.draw.rect(
                    screen,
                    CORAL_PINK,
                    (
                        BOARD_START_WIDTH + j * CELL_SIZE,
                        BOARD_START_HEIGHT + i * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )
            elif board.renderedBoard[i][j] == CellState.CROSSED:
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (
                        BOARD_START_WIDTH + j * CELL_SIZE,
                        BOARD_START_HEIGHT + i * CELL_SIZE,
                    ),
                    (
                        BOARD_START_WIDTH + (j + 1) * CELL_SIZE,
                        BOARD_START_HEIGHT + (i + 1) * CELL_SIZE,
                    ),
                )
                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (
                        BOARD_START_WIDTH + j * CELL_SIZE,
                        BOARD_START_HEIGHT + (i + 1) * CELL_SIZE,
                    ),
                    (
                        BOARD_START_WIDTH + (j + 1) * CELL_SIZE,
                        BOARD_START_HEIGHT + i * CELL_SIZE,
                    ),
                )
            else:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        BOARD_START_WIDTH + j * CELL_SIZE,
                        BOARD_START_HEIGHT + i * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )

    # Draw row counts
    for i in range(DIMENSION):
        row = board.rowCounts[i]
        for j in range(len(row)):
            text = font.render(str(row[j]), True, (0, 0, 0))
            screen.blit(
                text,
                (
                    BOARD_START_WIDTH
                    - CELL_SIZE * len(row)
                    + j * CELL_SIZE
                    + CELL_SIZE / 2
                    - text.get_width() / 2,
                    BOARD_START_HEIGHT
                    + i * CELL_SIZE
                    + CELL_SIZE / 2
                    - text.get_height() / 2,
                ),
            )

    # Draw column counts
    for j in range(DIMENSION):
        col = board.colCounts[j]
        for i in range(len(col)):
            text = font.render(str(col[i]), True, (0, 0, 0))
            screen.blit(
                text,
                (
                    BOARD_START_WIDTH
                    + j * CELL_SIZE
                    + CELL_SIZE / 2
                    - text.get_width() / 2,
                    BOARD_START_HEIGHT
                    - CELL_SIZE * len(col)
                    + i * CELL_SIZE
                    + CELL_SIZE / 2
                    - text.get_height() / 2,
                ),
            )

    # Draw grid lines
    for x in range(BOARD_START_WIDTH, BOARD_END_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(
            screen, (0, 0, 0), (x, BOARD_START_HEIGHT), (x, BOARD_END_HEIGHT)
        )
    for y in range(BOARD_START_HEIGHT, BOARD_END_HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(
            screen, (0, 0, 0), (BOARD_START_WIDTH, y), (BOARD_END_WIDTH, y)
        )

    # Draw current position, filled with color
    pygame.draw.rect(
        screen,
        CORAL_PINK,
        (
            BOARD_START_WIDTH + currentPos[1] * CELL_SIZE,
            BOARD_START_HEIGHT + currentPos[0] * CELL_SIZE,
            CELL_SIZE + 1,
            CELL_SIZE + 1,
        ),
        6,
    )

    # Check if the player has won, if yes, print a message and exit the game
    if checkWinCondition(board):
        screen.fill(WHITE)
        text = font.render("You won!", True, (0, 0, 0))
        screen.blit(
            text,
            (
                WINDOW_WIDTH / 2 - text.get_width() / 2,
                WINDOW_HEIGHT / 2 - text.get_height() / 2,
            ),
        )
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Check if the player has lost, if yes, print a message and exit the game
    if health == 0:
        screen.fill(WHITE)
        text = font.render("You lost!", True, (0, 0, 0))
        screen.blit(
            text,
            (
                WINDOW_WIDTH / 2 - text.get_width() / 2,
                WINDOW_HEIGHT / 2 - text.get_height() / 2,
            ),
        )
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

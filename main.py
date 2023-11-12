import pygame
import sys

WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
CIRCLE_SIZE = WIDTH // BOARD_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (150, 76, 60)
BLUE = (0, 90, 150)


class CheckerPiece:
    def __init__(self, screen, color, row, col):
        self.screen = screen
        self.color = color
        self.row = row
        self.col = col
        self.CIRCLE_SIZE = CIRCLE_SIZE
        self.king = False
        self.selected = False

    def draw_piece(self):
        pygame.draw.circle(self.screen, self.color, (
            self.col * self.CIRCLE_SIZE + self.CIRCLE_SIZE // 2,
            self.row * self.CIRCLE_SIZE + self.CIRCLE_SIZE // 2), self.CIRCLE_SIZE // 2)

        if self.king:
            pygame.draw.circle(self.screen, (255, 255, 0), (
                self.col * self.CIRCLE_SIZE + self.CIRCLE_SIZE // 2,
                self.row * self.CIRCLE_SIZE + self.CIRCLE_SIZE // 2), self.CIRCLE_SIZE // 4)

        if self.selected:
            pygame.draw.circle(self.screen, (255, 0, 0), (
                self.col * self.CIRCLE_SIZE + self.CIRCLE_SIZE // 2,
                self.row * self.CIRCLE_SIZE + self.CIRCLE_SIZE // 2), self.CIRCLE_SIZE // 4)


class CheckersBoard:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers")
        self.pieces = []
        self.setup_pieces()
        self.current_player = BROWN
        self.selected_piece = None

    def setup_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.pieces.append(CheckerPiece(self.screen, BROWN, row, col))
                    elif row >= BOARD_SIZE - 3:
                        self.pieces.append(CheckerPiece(self.screen, BLUE, row, col))

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (
                    col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw_piece()

    def handle_click(self, pos):
        col = pos[0] // (WIDTH // BOARD_SIZE)
        row = pos[1] // (HEIGHT // BOARD_SIZE)

        clicked_piece = self.get_piece_at(row, col)

        if clicked_piece and clicked_piece.color == self.current_player:
            if self.selected_piece:
                self.selected_piece.selected = False

            clicked_piece.selected = True
            self.selected_piece = clicked_piece

        elif self.selected_piece:
            self.move_piece(self.selected_piece, row, col)

    def move_piece(self, piece, row, col):
        if self.is_valid_move(piece, row, col):
            if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
                self.remove_opponent_piece(piece, (row, col))

            piece.row, piece.col = row, col

            if row == 0 or row == BOARD_SIZE - 1:
                piece.king = True

            piece.selected = False
            self.selected_piece = None
            self.switch_player()

    def is_valid_move(self, piece, row, col):
        if not (0 <= row < BOARD_SIZE) or not (0 <= col < BOARD_SIZE):
            return False

        direction = 1 if piece.color == BROWN else -1
        if piece.king:

            if abs(row - piece.row) == 1 and abs(col - piece.col) == 1:
                return self.is_target_empty(row, col)

            if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:

                jumped_row = (piece.row + row) // 2
                jumped_col = (piece.col + col) // 2

                for opponent_piece in self.pieces[:]:
                    if opponent_piece.row == jumped_row and opponent_piece.col == jumped_col:
                        self.pieces.remove(opponent_piece)
                        return True

        if abs(row - piece.row) == 1 and abs(col - piece.col) == 1:
            return (row - piece.row) * direction > 0 and self.is_target_empty(row, col)

        if abs(row - piece.row) == 2 and abs(col - piece.col) == 2:
            jumped_row = (piece.row + row) // 2
            jumped_col = (piece.col + col) // 2

            for opponent_piece in self.pieces:
                if opponent_piece.row == jumped_row and opponent_piece.col == jumped_col:
                    if opponent_piece.color != piece.color and self.is_target_empty(row, col):
                        return (row - piece.row) * direction > 0

        return False

    def remove_opponent_piece(self, piece, target):
        jumped_row = (piece.row + target[0]) // 2
        jumped_col = (piece.col + target[1]) // 2

        for opponent_piece in self.pieces[:]:
            if opponent_piece.row == jumped_row and opponent_piece.col == jumped_col:
                self.pieces.remove(opponent_piece)

    def is_target_empty(self, row, col):
        return all(piece.row != row or piece.col != col for piece in self.pieces)

    def get_piece_at(self, row, col):
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None

    def switch_player(self):
        self.current_player = BLUE if self.current_player == BROWN else BROWN

    def check_winner(self):
        brown_pieces = sum(1 for piece in self.pieces if piece.color == BROWN)
        blue_pieces = sum(1 for piece in self.pieces if piece.color == BLUE)

        if brown_pieces == 0:
            return "Blue"
        elif blue_pieces == 0:
            return "Brown"
        else:
            return None


class CheckersGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = CheckersBoard()

    def run(self):
        pygame.init()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.board.handle_click(pos)

            self.screen.fill(WHITE)
            self.board.draw_board()
            self.board.draw_pieces()
            pygame.display.flip()

            winner = self.board.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                running = False

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CheckersGame()
    game.run()

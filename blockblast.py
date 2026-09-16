from processing import *
import random

GRID_SIZE = 8
CELL_SIZE = 48
BOARD_X = 58
BOARD_Y = 60

PALETTE = [
    (245, 93, 62),   # Orange-Red
    (66, 133, 244),  # Blue
    (52, 168, 83),   # Green
    (251, 188, 5),   # Yellow
    (171, 71, 188),  # Purple
]

SHAPE_TEMPLATES = [
    # 1x1
    ([(0, 0)], 0),
    # 2x2 Square
    ([(0, 0), (1, 0), (0, 1), (1, 1)], 1),
    # 3x3 Square
    ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], 2),
    # Horizontal lines
    ([(0, 0), (1, 0)], 3),
    ([(0, 0), (1, 0), (2, 0)], 4),
    ([(0, 0), (1, 0), (2, 0), (3, 0)], 0),
    # Vertical lines
    ([(0, 0), (0, 1)], 1),
    ([(0, 0), (0, 1), (0, 2)], 2),
    ([(0, 0), (0, 1), (0, 2), (0, 3)], 3),
    # L-shapes
    ([(0, 0), (0, 1), (1, 1)], 4),
    ([(0, 0), (1, 0), (0, 1)], 0),
    ([(0, 0), (1, 0), (1, 1)], 1),
    ([(0, 1), (1, 1), (1, 0)], 2),
]

def draw_square(x,y,size, fill_color, stroke_color, corner_weight):
    stroke(fill_color[0], fill_color[1], fill_color[2])
    strokeWeight(1)
    
    offset_y = 0
    while offset_y < size:
        line(x, y + offset_y, x + size, y + offset_y)
        offset_y += 1

    stroke(stroke_color[0], stroke_color[1], stroke_color[2])
    strokeWeight(corner_weight)
    # top
    line(x, y, x + size, y)
    # bottom
    line(x + size, y + size, x, y + size)
    # right
    line(x + size, y, x + size, y + size)
    # left
    line(x, y + size, x, y)


class Board:
    def __init__(self, size, cell_size, origin_x, origin_y):
        self.size = size
        self.cell_size = cell_size
        self.ox = origin_x
        self.oy = origin_y
        
        self.grid = []
        index_row = 0

        while index_row < self.size:
            index_column = 0
            row = []

            while index_column < self.size:
                row.append(0)
                index_column += 1

            self.grid.append(row)
            index_row += 1
    
    def draw(self):
        index_row = 0
        while index_row < self.size:
            index_column = 0

            while index_column < self.size:
                value = self.grid[index_row][index_column]
                
                if value == 0:
                    fill_column = (255,255,255)
                    border_column = (0, 0, 0)
                else:
                    fill_column = PALETTE[value - 1]
                    border_column = PALETTE[value - 1]
                
                cell_x = self.ox + index_column * self.cell_size
                cell_y = self.oy + index_row * self.cell_size
                draw_square(cell_x, cell_y, self.cell_size - 4, fill_column, border_column, 2)

                index_column += 1
            index_row += 1

    def can_place(self, piece, target_r, target_c):
        index = 0
        while index < len(piece.blocks):
            block = piece.blocks[index]
            row = target_r + block[1]
            column = target_c + block[0]
            
            if row < 0 or row >= self.size or column < 0 or column >= self.size:
                return False
            if self.grid[row][column] != 0:
                return False
            index = index + 1
        return True
    
    def place(self, piece, target_r, target_c):
        i = 0
        while i < len(piece.blocks):
            block = piece.blocks[i]
            r = target_r + block[1]
            c = target_c + block[0]
            self.grid[r][c] = piece.color_idx + 1
            i = i + 1

    def clear_lines(self):
        rows_to_clear = []
        cols_to_clear = []

        # Check full rows
        row = 0
        while row < self.size:
            is_full = True
            column = 0
            while column < self.size:
                if self.grid[row][column] == 0:
                    is_full = False
                    break
                column = column + 1
            if is_full:
                rows_to_clear.append(row)
            row = row + 1

        # Check full columns
        column = 0
        while column < self.size:
            is_full = True
            row = 0
            while row < self.size:
                if self.grid[row][column] == 0:
                    is_full = False
                    break
                row = row + 1
            if is_full:
                cols_to_clear.append(column)
            column = column + 1

        # Clear detected rows
        index = 0
        while index < len(rows_to_clear):
            target_row = rows_to_clear[index]
            column = 0
            while column < self.size:
                self.grid[target_row][column] = 0
                column = column + 1
            index = index + 1

        # Clear detected columns
        index = 0
        while index < len(cols_to_clear):
            target_column = cols_to_clear[index]
            row = 0
            while row < self.size:
                self.grid[row][target_column] = 0
                row = row + 1
            index = index + 1

        cleared_count = len(rows_to_clear) + len(cols_to_clear)
        return cleared_count * 100

class Piece:
    def __init__(self, blocks, color_idx, anchor_x, anchor_y):
        self.blocks = blocks
        self.color_idx = color_idx
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.mini_cell = 24
    
    def draw(self):
        color = PALETTE[self.color_idx]
        border_color = (0, 0, 0)
        
        scale_size = self.mini_cell
        if self.is_dragging:
            scale_size = CELL_SIZE

        index = 0
        while index < len(self.blocks):
            block = self.blocks[index]
            blockx = self.x + block[0] * scale_size
            blocky = self.y + block[1] * scale_size
            
            draw_square(blockx, blocky, scale_size - 2, color, border_color, 1)
            index = index + 1

    def contains_point(self, px, py):
        i = 0
        while i < len(self.blocks):
            block = self.blocks[i]
            block_x = self.x + block[0] * self.mini_cell
            block_y = self.y + block[1] * self.mini_cell
            if block_x <= px and px <= block_x + self.mini_cell:
                if block_y <= py and py <= block_y + self.mini_cell:
                    return True
            i = i + 1
        return False

    def reset_pos(self):
        self.x = self.anchor_x
        self.y = self.anchor_y
        self.is_dragging = False

board = None
hand = [0, 0, 0]
score = 0
game_over = False
selected_piece = None
selected_index = -1

def spawn_hand():
    index = 0
    slot_width = width / 3
    while index < len(hand):
        random_select = random.choice(SHAPE_TEMPLATES)
        template = random_select[0]
        color = random_select[1]
        # hand[index] = random_select
    
        piece_x = index * slot_width + (slot_width / 2) - 30
        piece_y = 490
        hand[index] = (Piece(template, color, piece_x, piece_y))

        index += 1

def is_hand_empty():
    index = 0
    while index < len(hand):
        if hand[index] != 0:
            return False
        index = index + 1
    return True

def check_game_over():
    board_size = board.size
    total_cells = board_size * board_size
    can_place = board.can_place
    hand_length = len(hand)
    
    unique_pieces = []
    piece_index = 0
    while piece_index < hand_length:
        piece = hand[piece_index]
        if piece != 0 and piece not in unique_pieces:
            unique_pieces.append(piece)
        piece_index += 1

    piece_index = 0
    unique_piece_count = len(unique_pieces)
    while piece_index < unique_piece_count:
        piece = unique_pieces[piece_index]

        cell_index = 0
        while cell_index < total_cells:
            row = cell_index // board_size
            column = cell_index % board_size
            if can_place(piece, row, column):
                return False
            cell_index += 1

        piece_index += 1

    return True

def setup():
    global board, score, game_over
    size(500, 600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)
    score = 0
    game_over = False
    
    #board.grid[3][3] = 3
    #board.grid[3][4] = 2
    #draw_squre(250,300,CELL_SIZE)
    board.draw()
    spawn_hand()

def draw():
    background(176, 217, 255)
    fill(255)

    board.draw()
    i = 0
    while i < len(hand):
        if hand[i] != 0:
            if not hand[i].is_dragging:
                hand[i].draw()
        i = i + 1

    # Draw selected piece on top
    if selected_piece != None:
        selected_piece.draw()
    # When Game over
    if game_over:
        textSize(36)
        text("YOU LOSE", width / 2 - 100, height / 2 - 20)
        textSize(16)
        text("Click to restart", width / 2 - 70, height / 2 + 20)

    textSize(33)
    text("Score: " + str(score), width/2 - 85, 38)

def is_hand_empty():
    index = 0
    while index < len(hand):
        if hand[index] != 0:
            return False
        index = index + 1
    return True

def mousePressed():
    global selected_piece, selected_index, game_over

    if game_over:
        setup()
        return

    index = 0
    while index < len(hand):
        piece = hand[index]
        if piece != 0:
            if piece.contains_point(mouseX, mouseY):
                selected_piece = piece
                selected_index = index
                piece.is_dragging = True
                piece.drag_offset_x = mouseX - piece.x
                piece.drag_offset_y = mouseY - piece.y
                break
        index = index + 1

def mouseDragged():
    if selected_piece != None:
        selected_piece.x = mouseX - selected_piece.drag_offset_x
        selected_piece.y = mouseY - selected_piece.drag_offset_y

def mouseReleased():
    global selected_piece, selected_index, score, game_over

    if selected_piece == None:
        return

    cell_size = board.cell_size
    target_c = round((selected_piece.x - board.ox) / cell_size)
    target_r = round((selected_piece.y - board.oy) / cell_size)

    if board.can_place(selected_piece, target_r, target_c):
        board.place(selected_piece, target_r, target_c)
        
        score += (len(selected_piece.blocks) * 10) + board.clear_lines()
        hand[selected_index] = 0

        if is_hand_empty():
            spawn_hand()
        
        if check_game_over():
            game_over = True
            
    else:
        selected_piece.reset_pos()

    selected_piece = None
    selected_index = -1
run()
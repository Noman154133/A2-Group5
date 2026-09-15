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
    
    def place(self, piece, target_r, target_c):
        i = 0
        while i < len(piece.blocks):
            block = piece.blocks[i]
            r = target_r + block[1]
            c = target_c + block[0]
            self.grid[r][c] = piece.color_idx + 1
            i = i + 1

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
            block = self.blocks[i]
            blockx = self.x + block[0] * scale_size
            blocky = self.y + block[1] * scale_size
            
            draw_square(blockx, blocky, scale_size - 2, color, border_color, 1)
            index = index + 1

    def contains_point(self, px, py):
    def reset_pos(self):

board = None
hand = [0, 0, 0]
score = 0
game_over = False
selected_piece = None
selected_index = -1

def spawn_hand():
    global hand

    index = 0
    while index < len(hand):
        random_select = random.choice(SHAPE_TEMPLATES)
        hand[index] = random_select

        index += 1

def is_hand_empty():
def check_game_over():
    global game_over

def setup():
    global board, score, game_over
    size(500, 600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)
    score = 0
    game_over = False
    board.grid[3][3] = 3
    #draw_squre(250,300,CELL_SIZE)
    board.draw()
    spawn_hand()

def draw():
    background(176, 217, 255)
    fill(255)

    board.draw()
    i = 0
    while i < len(hand):
        hand[i].draw()
        i = i + 1
        
    # Draw selected piece on top
    if selected_piece != None:
    # When Game over
    if game_over:

def mousePressed():
    global selected_piece, selected_index, game_over

def mouseDragged():

def mouseReleased():
    global selected_piece, selected_index, score, game_over
    if selected_piece == None:
    if board.can_place(selected_piece, target_r, target_c):
# Draft for function designs
# finished and working game
# function design
import random

# --- CONFIGURATION ---
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

def draw_square(x, y, size, fill_color, stroke_color, corner_weight):
    fill(fill_color[0], fill_color[1], fill_color[2])
    stroke(stroke_color[0], stroke_color[1], stroke_color[2])
    strokeWeight(corner_weight)
    rect(x, y, size, size)


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
                    fill_column = (255, 255, 255)
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
        

# --- GLOBAL GAME STATE ---
board = None
hand = [0, 0, 0]
score = 0
current_streak = 0
streak_text = ""
streak_timer = 0
streak_y = 50
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
    
        piece_x = index * slot_width + (slot_width / 2) - 30
        piece_y = 490
        hand[index] = Piece(template, color, piece_x, piece_y)

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
    global board, score, current_streak, streak_timer, game_over
    size(500, 600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)
    score = 0
    current_streak = 0
    streak_timer = 0
    game_over = False
    
    board.draw()
    spawn_hand()

def draw_preview():
    if selected_piece != None:
        target_c = int(round((selected_piece.x - board.ox) / float(board.cell_size)))
        target_r = int(round((selected_piece.y - board.oy) / float(board.cell_size)))

        if board.can_place(selected_piece, target_r, target_c):
            piece_color = PALETTE[selected_piece.color_idx]
            noFill()
            stroke(piece_color[0], piece_color[1], piece_color[2])
            strokeWeight(2)

            block_index = 0
            while block_index < len(selected_piece.blocks):
                block = selected_piece.blocks[block_index]
                ghost_x = board.ox + (target_c + block[0]) * board.cell_size
                ghost_y = board.oy + (target_r + block[1]) * board.cell_size
                rect(ghost_x, ghost_y, board.cell_size - 4, board.cell_size - 4)
                block_index += 1

def draw_hand():
    i = 0
    while i < len(hand):
        if hand[i] != 0:
            if not hand[i].is_dragging:
                hand[i].draw()
        i = i + 1

    if selected_piece != None:
        selected_piece.draw()

def draw_ui():
    global streak_timer

    if streak_timer > 0:
        fill(255, 120, 40)
        textSize(15)
        text(streak_text, 50, streak_y)
        streak_timer -= 1

    if current_streak > 1:
        fill(255, 90, 40)
        textSize(16)
        text("x" + str(current_streak) + " Streak", width - 110, 36)

    fill(255)
    if game_over:
        fill(255)
        textSize(36)
        text("YOU LOSE", width / 2 - 100, height / 2 - 20)
        textSize(16)
        text("Click to restart", width / 2 - 70, height / 2 + 20)
    textSize(33)
    text("Score: " + str(score), width / 2 - 85, 38)

def draw():
    background(176, 217, 255)
    board.draw()
    draw_preview()
    draw_hand()
    draw_ui()

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
    global selected_piece, selected_index, score, current_streak, streak_text, streak_timer, game_over

    if selected_piece == None:
        return

    cell_size = board.cell_size
    target_c = int(round((selected_piece.x - board.ox) / float(cell_size)))
    target_r = int(round((selected_piece.y - board.oy) / float(cell_size)))

    if board.can_place(selected_piece, target_r, target_c):
        board.place(selected_piece, target_r, target_c)
        
        placed_blocks_score = len(selected_piece.blocks) * 10
        cleared_lines_score = board.clear_lines()

        if cleared_lines_score > 0:
            current_streak += 1
            streak_reward = (current_streak - 1) * 75
            total_earned = placed_blocks_score + cleared_lines_score + streak_reward
            score += total_earned

            if current_streak > 1:
                streak_text = "COMBO x" + str(current_streak) + " (+" + str(cleared_lines_score + streak_reward) + ")"
            else:
                streak_text = "CLEAR! +" + str(cleared_lines_score)
            
            streak_timer = 45
        else:
            current_streak = 0
            score += placed_blocks_score

        hand[selected_index] = 0

        if is_hand_empty():
            spawn_hand()
        
        if check_game_over():
            game_over = True
            
    else:
        selected_piece.reset_pos()

    selected_piece = None
    selected_index = -1

def save_game():
    global board, score, current_streak, hand, streak_text, streak_timer

    row_list = []
    r = 0
    while r < board.size:
        col_list = []
        c = 0
        while c < board.size:
            col_list.append(str(board.grid[r][c]))
            c += 1
        row_list.append("[" + ",".join(col_list) + "]")
        r += 1
    line1 = "/".join(row_list)

    line2 = str(score) + "," + str(current_streak)

    hand_list = []
    i = 0
    while i < len(hand):
        piece = hand[i]
        if piece == 0:
            hand_list.append("EMPTY")
        else:
            shape_idx = 0
            s = 0
            while s < len(SHAPE_TEMPLATES):
                if SHAPE_TEMPLATES[s][0] == piece.blocks:
                    shape_idx = s
                    break
                s += 1
            hand_list.append(str(shape_idx) + ":" + str(piece.color_idx))
        i += 1
    line3 = ";".join(hand_list)

    file = open("savegame.txt", "w")
    file.write(line1 + "\n")
    file.write(line2 + "\n")
    file.write(line3 + "\n")
    file.close()

    streak_text = "GAME SAVED"
    streak_timer = 45
    print("Game saved successfully to savegame.txt")

def load_game():
    global board, score, current_streak, hand, game_over, selected_piece, selected_index, streak_text, streak_timer

    try:
        file = open("savegame.txt", "r")
        lines = file.readlines()
        file.close()
    except:
        print("Cannot find savegame.txt")
        return

    if len(lines) < 3:
        return

    line1 = lines[0].strip()
    line2 = lines[1].strip()
    line3 = lines[2].strip()

    rows = line1.split("/")
    r = 0
    while r < len(rows) and r < board.size:
        row_str = rows[r].replace("[", "").replace("]", "")
        cols = row_str.split(",")
        c = 0
        while c < len(cols) and c < board.size:
            board.grid[r][c] = int(cols[c].strip())
            c += 1
        r += 1

    score_parts = line2.split(",")
    score = int(score_parts[0].strip())
    current_streak = int(score_parts[1].strip())

    hand_items = line3.split(";")
    slot_width = width / 3
    i = 0
    while i < len(hand_items) and i < len(hand):
        item = hand_items[i].strip()
        if item == "EMPTY":
            hand[i] = 0
        else:
            parts = item.split(":")
            shape_idx = int(parts[0].strip())
            color_idx = int(parts[1].strip())
            template = SHAPE_TEMPLATES[shape_idx][0]

            piece_x = i * slot_width + (slot_width / 2) - 30
            piece_y = 490
            hand[i] = Piece(template, color_idx, piece_x, piece_y)
        i += 1

    if is_hand_empty():
        spawn_hand()

    selected_piece = None
    selected_index = -1
    game_over = check_game_over()

    streak_text = "GAME LOADED"
    streak_timer = 45
    print("Game loaded successfully from savegame.txt")

def keyPressed():
    if key == 's' or key == 'S':
        save_game()
    elif key == 'l' or key == 'L':
        load_game()
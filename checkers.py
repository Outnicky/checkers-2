import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Colors
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
BG_COLOR = (50, 50, 50)
RED_PIECE = (200, 50, 50)
BLUE_PIECE = (50, 50, 200)
SELECTED = (100, 255, 100)
VALID_MOVE = (255, 255, 100)

# Create window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Goku vs Gojo Checkers")

# Load character images
def load_images():
    """Load and scale character images"""
    size = int(SQUARE_SIZE * 0.8)
    
    # Load Goku
    try:
        goku_img = pygame.image.load('goku.png')
        goku_img = pygame.transform.scale(goku_img, (size, size))
    except:
        goku_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(goku_img, (255, 140, 0), (size//2, size//2), size//2)
        font = pygame.font.Font(None, 24)
        text = font.render('GOKU', True, (0, 0, 0))
        goku_img.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
    
    # Load SSJ3 Goku
    try:
        goku_ssj3_img = pygame.image.load('goku_ssj3.png')
        goku_ssj3_img = pygame.transform.scale(goku_ssj3_img, (size, size))
    except:
        goku_ssj3_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(goku_ssj3_img, (255, 215, 0), (size//2, size//2), size//2)
        font = pygame.font.Font(None, 20)
        text = font.render('SSJ3', True, (0, 0, 0))
        goku_ssj3_img.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
    
    # Load Gojo
    try:
        gojo_img = pygame.image.load('gojo.png')
        gojo_img = pygame.transform.scale(gojo_img, (size, size))
    except:
        gojo_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(gojo_img, (100, 150, 255), (size//2, size//2), size//2)
        font = pygame.font.Font(None, 24)
        text = font.render('GOJO', True, (255, 255, 255))
        gojo_img.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
    
    # Load Gojo no mask
    try:
        gojo_no_mask_img = pygame.image.load('gojo_no_mask.png')
        gojo_no_mask_img = pygame.transform.scale(gojo_no_mask_img, (size, size))
    except:
        gojo_no_mask_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(gojo_no_mask_img, (200, 200, 255), (size//2, size//2), size//2)
        font = pygame.font.Font(None, 18)
        text = font.render('GOJO+', True, (0, 0, 0))
        gojo_no_mask_img.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
    
    return goku_img, goku_ssj3_img, gojo_img, gojo_no_mask_img

goku_image, goku_ssj3_image, gojo_image, gojo_no_mask_image = load_images()

# Load DIO image
def load_dio():
    size = int(SQUARE_SIZE * 0.8)
    try:
        dio_img = pygame.image.load('dio.png')
        dio_img = pygame.transform.scale(dio_img, (size, size))
    except:
        dio_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(dio_img, (200, 180, 0), (size//2, size//2), size//2)
        font = pygame.font.Font(None, 24)
        text = font.render('DIO', True, (0, 0, 0))
        dio_img.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
    return dio_img

dio_image = load_dio()

# Game state
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
piece_states = {}  # Track power-up states: {(row, col): {'kills': int, 'powered_up': bool}}
selected_piece = None
current_player = 'red'  # 'red' = Goku, 'blue' = Gojo
dio_position = None  # Track DIO's position if he appears

# Initialize pieces
def init_board():
    """Place pieces on the board"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:  # Only on dark squares
                if row < 3:
                    board[row][col] = 'blue'
                elif row > 4:
                    board[row][col] = 'red'

def draw_board():
    """Draw the checkers board"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Alternate colors
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )

def draw_pieces():
    """Draw all pieces on the board"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                # Check power-up state
                state = piece_states.get((row, col), {'kills': 0, 'powered_up': False})
                
                # Select character image based on piece type
                if piece == 'dio':
                    img = dio_image
                elif piece == 'red':
                    img = goku_ssj3_image if state['powered_up'] else goku_image
                else:
                    img = gojo_no_mask_image if state['powered_up'] else gojo_image
                
                # Calculate position to center the image
                x = col * SQUARE_SIZE + (SQUARE_SIZE - img.get_width()) // 2
                y = row * SQUARE_SIZE + (SQUARE_SIZE - img.get_height()) // 2
                
                screen.blit(img, (x, y))
                
                # Draw aura for powered-up pieces
                if piece != 'dio' and state['powered_up']:
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    aura_color = (255, 215, 0, 100) if piece == 'red' else (150, 200, 255, 100)
                    s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(s, aura_color, (center_x, center_y), SQUARE_SIZE // 2, 3)
                    screen.blit(s, (0, 0))
                
                # Draw golden aura for DIO
                if piece == 'dio':
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 215, 0, 120), (center_x, center_y), SQUARE_SIZE // 2, 4)
                    screen.blit(s, (0, 0))

def draw_selected(row, col):
    """Highlight selected piece"""
    pygame.draw.rect(
        screen,
        SELECTED,
        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
        5
    )

def draw_valid_moves(moves):
    """Show valid move positions"""
    for row, col in moves:
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(screen, VALID_MOVE, (center_x, center_y), 15)

def get_valid_moves(row, col):
    """Get valid moves for a piece"""
    moves = []
    piece = board[row][col]
    if not piece:
        return moves
    
    # Check if piece is powered up
    state = piece_states.get((row, col), {'kills': 0, 'powered_up': False})
    
    # Powered-up pieces can move in all directions
    if state['powered_up']:
        directions = [-1, 1]  # Both forward and backward
    else:
        # Normal pieces move forward only
        directions = [-1 if piece == 'red' else 1]
    
    # Check diagonal moves
    for direction in directions:
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc
            
            # Simple move
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col, None))
                # Check for capture
                elif board[new_row][new_col] and board[new_row][new_col] != piece:
                    jump_row = new_row + direction
                    jump_col = new_col + dc
                    if 0 <= jump_row < BOARD_SIZE and 0 <= jump_col < BOARD_SIZE:
                        if board[jump_row][jump_col] is None:
                            moves.append((jump_row, jump_col, (new_row, new_col)))
    
    return moves

def domain_expansion(row, col):
    """Gojo's Domain Expansion - destroys adjacent enemy pieces with animation"""
    victims = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if board[new_row][new_col] == 'red':
                    victims.append((new_row, new_col))
    
    # Animation
    for frame in range(30):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        # Expanding circle effect
        radius = int((frame / 30) * SQUARE_SIZE * 2)
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Purple/blue domain effect
        alpha = int(200 - (frame / 30) * 150)
        s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(s, (138, 43, 226, alpha), (center_x, center_y), radius, 5)
        pygame.draw.circle(s, (75, 0, 130, alpha // 2), (center_x, center_y), radius // 2)
        screen.blit(s, (0, 0))
        
        # Text effect
        if frame < 20:
            font = pygame.font.Font(None, 48)
            text = font.render('DOMAIN EXPANSION', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Remove victims
    for v_row, v_col in victims:
        board[v_row][v_col] = None
    
    return len(victims)

def kamehameha(row, col):
    """Goku's Kamehameha - destroys everything ahead with beam animation"""
    victims = []
    # Destroy everything in the forward direction (upward for red/Goku)
    for r in range(row - 1, -1, -1):
        if board[r][col] == 'blue':
            victims.append((r, col))
    
    # Animation
    for frame in range(40):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        # Charging effect
        if frame < 15:
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            for i in range(3):
                radius = int(SQUARE_SIZE // 4 + (frame / 15) * SQUARE_SIZE // 2) + i * 10
                alpha = int(150 - (frame / 15) * 100)
                s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(s, (0, 150, 255, alpha), (center_x, center_y), radius, 3)
                screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 36)
            text = font.render('KA-ME-HA-ME-HA!', True, (255, 255, 0))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 50))
            screen.blit(text, text_rect)
        else:
            # Beam effect
            progress = (frame - 15) / 25
            beam_length = int(progress * row * SQUARE_SIZE)
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            start_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            
            # Main beam
            beam_width = SQUARE_SIZE // 2
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(s, (100, 200, 255, 200), 
                           (center_x - beam_width // 2, start_y - beam_length, 
                            beam_width, beam_length))
            pygame.draw.rect(s, (255, 255, 255, 150), 
                           (center_x - beam_width // 4, start_y - beam_length, 
                            beam_width // 2, beam_length))
            screen.blit(s, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Remove victims
    for v_row, v_col in victims:
        board[v_row][v_col] = None
        if (v_row, v_col) in piece_states:
            del piece_states[(v_row, v_col)]
    
    return len(victims)

def genkidama(row, col, direction):
    """SSJ3 Goku's Spirit Bomb - destroys 3x3 area and 2 squares in direction"""
    victims = []
    
    # 3x3 area
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if board[new_row][new_col] == 'blue':
                    victims.append((new_row, new_col))
    
    # 2 squares in the direction of movement
    for ahead in [1, 2]:
        new_row = row + (direction * ahead)
        if 0 <= new_row < BOARD_SIZE:
            if board[new_row][col] == 'blue':
                victims.append((new_row, col))
    
    # Animation
    for frame in range(50):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Charging phase
        if frame < 25:
            progress = frame / 25
            radius = int(progress * SQUARE_SIZE * 1.5)
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            
            # Multiple energy layers
            pygame.draw.circle(s, (255, 200, 0, 150), (center_x, center_y), radius, 5)
            pygame.draw.circle(s, (255, 255, 100, 100), (center_x, center_y), int(radius * 0.7))
            screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 48)
            text = font.render('GENKIDAMA!', True, (255, 255, 0))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, 50))
            screen.blit(text, text_rect)
        else:
            # Throw phase - ball moves in direction
            progress = (frame - 25) / 25
            throw_distance = int(progress * 2 * SQUARE_SIZE * direction)
            ball_y = center_y + throw_distance
            
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            ball_radius = int(SQUARE_SIZE * 0.8)
            
            # Draw spirit bomb
            pygame.draw.circle(s, (255, 255, 200, 220), (center_x, ball_y), ball_radius)
            pygame.draw.circle(s, (255, 200, 0, 180), (center_x, ball_y), int(ball_radius * 0.7))
            pygame.draw.circle(s, (255, 255, 100, 150), (center_x, ball_y), int(ball_radius * 0.4))
            screen.blit(s, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Remove victims
    for v_row, v_col in victims:
        board[v_row][v_col] = None
        if (v_row, v_col) in piece_states:
            del piece_states[(v_row, v_col)]
    
    return len(victims)

def hollow_purple(row, col, direction):
    """Gojo's Hollow Purple - Red/Blue balls in direction of movement"""
    victims = []
    
    # Destroy everything in the direction of movement
    if direction == 1:  # Moving down
        for r in range(row + 1, BOARD_SIZE):
            if board[r][col] == 'red':
                victims.append((r, col))
    else:  # Moving up
        for r in range(row - 1, -1, -1):
            if board[r][col] == 'red':
                victims.append((r, col))
    
    # Animation
    for frame in range(50):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Phase 1: Red and Blue orbs forming
        if frame < 20:
            progress = frame / 20
            offset = int(progress * SQUARE_SIZE * 0.8)
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            
            # Blue orb (left)
            pygame.draw.circle(s, (0, 100, 255, 200), (center_x - offset, center_y), 35)
            pygame.draw.circle(s, (100, 180, 255, 150), (center_x - offset, center_y), 20)
            
            # Red orb (right)
            pygame.draw.circle(s, (255, 50, 50, 200), (center_x + offset, center_y), 35)
            pygame.draw.circle(s, (255, 150, 150, 150), (center_x + offset, center_y), 20)
            screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 42)
            text = font.render('RED AND BLUE', True, (200, 100, 255))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, 50))
            screen.blit(text, text_rect)
        
        # Phase 2: Orbs merge and shoot
        else:
            progress = (frame - 20) / 30
            
            # Calculate beam parameters based on direction
            if direction == 1:  # Down
                beam_length = int(progress * (BOARD_SIZE - row - 1) * SQUARE_SIZE)
                beam_start_y = center_y
            else:  # Up
                beam_length = int(progress * row * SQUARE_SIZE)
                beam_start_y = center_y - beam_length
            
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            
            # Purple beam
            beam_width = int(SQUARE_SIZE * 0.8)
            pygame.draw.rect(s, (138, 43, 226, 220),
                           (center_x - beam_width // 2, beam_start_y,
                            beam_width, beam_length))
            pygame.draw.rect(s, (200, 100, 255, 180),
                           (center_x - beam_width // 4, beam_start_y,
                            beam_width // 2, beam_length))
            screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 48)
            text = font.render('HOLLOW PURPLE!', True, (200, 100, 255))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 50))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Remove victims
    for v_row, v_col in victims:
        board[v_row][v_col] = None
        if (v_row, v_col) in piece_states:
            del piece_states[(v_row, v_col)]
    
    return len(victims)

def move_piece(from_row, from_col, to_row, to_col, captured):
    """Move a piece and handle captures"""
    piece = board[from_row][from_col]
    board[to_row][to_col] = piece
    board[from_row][from_col] = None
    
    # Calculate movement direction
    move_direction = 1 if to_row > from_row else -1
    
    # Transfer piece state
    if (from_row, from_col) in piece_states:
        piece_states[(to_row, to_col)] = piece_states[(from_row, from_col)]
        del piece_states[(from_row, from_col)]
    else:
        piece_states[(to_row, to_col)] = {'kills': 0, 'powered_up': False}
    
    state = piece_states[(to_row, to_col)]
    
    # Check for transformation when reaching the end
    if not state['powered_up']:
        if (piece == 'red' and to_row == 0) or (piece == 'blue' and to_row == BOARD_SIZE - 1):
            state['powered_up'] = True
            transform_animation(to_row, to_col, piece)
    
    # Check if this was a capture move
    if captured:
        board[captured[0]][captured[1]] = None
        if (captured[0], captured[1]) in piece_states:
            del piece_states[(captured[0], captured[1])]
        
        # Trigger special attacks based on power-up state
        if state['powered_up']:
            # Ultimate attacks for powered-up forms
            if piece == 'blue':  # Gojo no mask
                hollow_purple(to_row, to_col, move_direction)
            elif piece == 'red':  # SSJ3 Goku
                genkidama(to_row, to_col, move_direction)
        else:
            # Regular special attacks
            if piece == 'blue':  # Gojo
                domain_expansion(to_row, to_col)
            elif piece == 'red':  # Goku
                kamehameha(to_row, to_col)

def transformation_genkidama(row, col):
    """Goku's transformation attack - Genkidama backwards destroying everything"""
    victims = []
    
    # Destroy everything backwards (downward for Goku at row 0)
    for r in range(row + 1, BOARD_SIZE):
        if board[r][col]:
            victims.append((r, col))
    
    # Animation
    for frame in range(50):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        if frame < 25:
            # Charging
            progress = frame / 25
            radius = int(progress * SQUARE_SIZE * 1.5)
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 200, 0, 150), (center_x, center_y), radius, 5)
            pygame.draw.circle(s, (255, 255, 100, 100), (center_x, center_y), int(radius * 0.7))
            screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 48)
            text = font.render('GENKIDAMA!', True, (255, 255, 0))
            screen.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, 50)))
        else:
            # Throw backwards
            progress = (frame - 25) / 25
            ball_y = center_y + int(progress * (WINDOW_SIZE - center_y))
            
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            ball_radius = int(SQUARE_SIZE * 0.8)
            pygame.draw.circle(s, (255, 255, 200, 220), (center_x, ball_y), ball_radius)
            pygame.draw.circle(s, (255, 200, 0, 180), (center_x, ball_y), int(ball_radius * 0.7))
            screen.blit(s, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Remove all victims
    for v_row, v_col in victims:
        board[v_row][v_col] = None
        if (v_row, v_col) in piece_states:
            del piece_states[(v_row, v_col)]

def transformation_hollow_purple(row, col):
    """Gojo's transformation attack - Red/Blue balls backwards destroying everything"""
    victims = []
    
    # Destroy everything backwards (upward for Gojo at row 7)
    for r in range(row - 1, -1, -1):
        if board[r][col]:
            victims.append((r, col))
    
    # Animation
    for frame in range(50):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        if frame < 20:
            # Red and Blue orbs forming
            progress = frame / 20
            offset = int(progress * SQUARE_SIZE * 0.8)
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 100, 255, 200), (center_x - offset, center_y), 35)
            pygame.draw.circle(s, (255, 50, 50, 200), (center_x + offset, center_y), 35)
            screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 42)
            text = font.render('RED AND BLUE', True, (200, 100, 255))
            screen.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, 50)))
        else:
            # Purple beam backwards
            progress = (frame - 20) / 30
            beam_length = int(progress * center_y)
            
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            beam_width = int(SQUARE_SIZE * 0.8)
            pygame.draw.rect(s, (138, 43, 226, 220),
                           (center_x - beam_width // 2, center_y - beam_length,
                            beam_width, beam_length))
            screen.blit(s, (0, 0))
            
            font = pygame.font.Font(None, 48)
            text = font.render('HOLLOW PURPLE!', True, (200, 100, 255))
            screen.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 50)))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Remove all victims
    for v_row, v_col in victims:
        board[v_row][v_col] = None
        if (v_row, v_col) in piece_states:
            del piece_states[(v_row, v_col)]

def check_za_warudo():
    """Check if Goku and Gojo are 2 tiles apart to trigger ZA WARUDO"""
    goku_pos = None
    gojo_pos = None
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'red':
                state = piece_states.get((row, col), {})
                if state.get('powered_up'):
                    goku_pos = (row, col)
            elif board[row][col] == 'blue':
                state = piece_states.get((row, col), {})
                if state.get('powered_up'):
                    gojo_pos = (row, col)
    
    if goku_pos and gojo_pos:
        row_diff = abs(goku_pos[0] - gojo_pos[0])
        col_diff = abs(goku_pos[1] - gojo_pos[1])
        # Check if they're exactly 2 tiles apart (adjacent means 1 tile)
        if row_diff <= 4 and col_diff <= 4 and (row_diff + col_diff) < 4:
            return goku_pos, gojo_pos
    return None

def za_warudo(goku_pos, gojo_pos):
    """DIO appears and stops time!"""
    global dio_position
    
    # Calculate DIO spawn position (between Goku and Gojo)
    dio_row = (goku_pos[0] + gojo_pos[0]) // 2
    dio_col = (goku_pos[1] + gojo_pos[1]) // 2
    
    # Find nearest empty dark square
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            r, c = dio_row + dr, dio_col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if (r + c) % 2 == 1 and board[r][c] is None:
                    dio_row, dio_col = r, c
                    break
    
    # ZA WARUDO animation
    for frame in range(60):
        # Green tint effect
        green_overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        alpha = int(150 * (frame / 60))
        green_overlay.fill((0, 100, 0, alpha))
        
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        screen.blit(green_overlay, (0, 0))
        
        # ZA WARUDO text
        if frame > 10:
            font = pygame.font.Font(None, 80)
            text = font.render('ZA WARUDO!', True, (255, 215, 0))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            
            # Pulsing effect
            scale = 1 + 0.2 * abs((frame % 20) - 10) / 10
            scaled_font = pygame.font.Font(None, int(80 * scale))
            text = scaled_font.render('ZA WARUDO!', True, (255, 215, 0))
            text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Spawn DIO
    board[dio_row][dio_col] = 'dio'
    dio_position = (dio_row, dio_col)
    
    # DIO moves 3 times randomly
    import random
    for move_num in range(3):
        # Animation for DIO's movement
        for frame in range(20):
            green_overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            green_overlay.fill((0, 100, 0, 100))
            
            screen.fill(BG_COLOR)
            draw_board()
            draw_pieces()
            screen.blit(green_overlay, (0, 0))
            
            font = pygame.font.Font(None, 48)
            text = font.render(f'DIO MOVE {move_num + 1}/3', True, (255, 215, 0))
            screen.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, 50)))
            
            pygame.display.flip()
            clock.tick(60)
        
        # Find adjacent tiles
        current_row, current_col = dio_position
        adjacent = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = current_row + dr, current_col + dc
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if (new_row + new_col) % 2 == 1:  # Dark squares only
                        adjacent.append((new_row, new_col))
        
        if adjacent:
            target = random.choice(adjacent)
            
            # Kill anything at target
            if board[target[0]][target[1]]:
                if (target[0], target[1]) in piece_states:
                    del piece_states[(target[0], target[1])]
            
            # Move DIO
            board[current_row][current_col] = None
            board[target[0]][target[1]] = 'dio'
            dio_position = target
    
    # DIO disappears
    board[dio_position[0]][dio_position[1]] = None
    dio_position = None
    
    # Final animation
    for frame in range(30):
        green_overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        alpha = int(100 - (frame / 30) * 100)
        green_overlay.fill((0, 100, 0, alpha))
        
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        screen.blit(green_overlay, (0, 0))
        
        font = pygame.font.Font(None, 56)
        text = font.render('TIME RESUMES', True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2)))
        
        pygame.display.flip()
        clock.tick(60)

def transform_animation(row, col, piece):
    """Show transformation animation and trigger transformation attack"""
    for frame in range(40):
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Energy burst effect
        s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        for i in range(5):
            radius = int((frame / 40) * SQUARE_SIZE * 2) + i * 20
            alpha = int(150 - (frame / 40) * 100)
            color = (255, 215, 0, alpha) if piece == 'red' else (150, 200, 255, alpha)
            pygame.draw.circle(s, color, (center_x, center_y), radius, 4)
        screen.blit(s, (0, 0))
        
        # Transformation text
        font = pygame.font.Font(None, 56)
        if piece == 'red':
            text = font.render('SUPER SAIYAN 3!', True, (255, 215, 0))
        else:
            text = font.render('MASK OFF!', True, (150, 200, 255))
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Trigger transformation attack
    if piece == 'red':
        transformation_genkidama(row, col)
    else:
        transformation_hollow_purple(row, col)

def check_winner():
    """Check if there's a winner"""
    has_red = False
    has_blue = False
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'red':
                has_red = True
            elif board[row][col] == 'blue':
                has_blue = True
    
    if has_red and not has_blue:
        return 'red'
    elif has_blue and not has_red:
        return 'blue'
    return None

def victory_animation(winner):
    """Show epic victory animation"""
    import random
    
    if winner == 'red':
        message = 'GOKU WINS PIBBLERSSSS'
        color1 = (255, 140, 0)
        color2 = (255, 215, 0)
    else:
        message = 'GOJO IS BETTER THAN GOKU NERDS'
        color1 = (100, 150, 255)
        color2 = (200, 200, 255)
    
    for frame in range(180):
        screen.fill(BG_COLOR)
        
        # Random flashing background
        flash_color = random.choice([color1, color2, (255, 255, 255)])
        flash_alpha = random.randint(50, 150)
        flash_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
        flash_surface.fill((*flash_color, flash_alpha))
        screen.blit(flash_surface, (0, 0))
        
        # Random explosions
        for _ in range(5):
            exp_x = random.randint(0, WINDOW_SIZE)
            exp_y = random.randint(0, WINDOW_SIZE)
            exp_radius = random.randint(20, 80)
            exp_color = random.choice([color1, color2, (255, 255, 0)])
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, (*exp_color, random.randint(100, 200)), (exp_x, exp_y), exp_radius)
            screen.blit(s, (0, 0))
        
        # Pulsing victory text
        scale = 1 + 0.3 * abs((frame % 30) - 15) / 15
        font_size = int(60 * scale)
        font = pygame.font.Font(None, font_size)
        
        # Text with outline
        text_color = (255, 255, 255) if frame % 10 < 5 else color2
        text = font.render(message, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        
        # Draw outline
        outline_color = (0, 0, 0)
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            outline_text = font.render(message, True, outline_color)
            screen.blit(outline_text, (text_rect.x + dx, text_rect.y + dy))
        
        screen.blit(text, text_rect)
        
        # Random sparkles
        for _ in range(10):
            spark_x = random.randint(0, WINDOW_SIZE)
            spark_y = random.randint(0, WINDOW_SIZE)
            spark_size = random.randint(2, 8)
            pygame.draw.circle(screen, (255, 255, 255), (spark_x, spark_y), spark_size)
        
        # Rotating rays
        ray_count = 12
        for i in range(ray_count):
            angle = (frame * 5 + i * 360 / ray_count) % 360
            import math
            end_x = WINDOW_SIZE // 2 + int(WINDOW_SIZE * math.cos(math.radians(angle)))
            end_y = WINDOW_SIZE // 2 + int(WINDOW_SIZE * math.sin(math.radians(angle)))
            s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            pygame.draw.line(s, (*color1, 50), (WINDOW_SIZE // 2, WINDOW_SIZE // 2), (end_x, end_y), 3)
            screen.blit(s, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

def get_square_from_mouse(pos):
    """Convert mouse position to board coordinates"""
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

# Initialize the board
init_board()

# Main game loop
running = True
clock = pygame.time.Clock()
valid_moves = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_from_mouse(event.pos)
            
            if selected_piece:
                # Try to move to clicked square
                moved = False
                for move_row, move_col, captured in valid_moves:
                    if move_row == row and move_col == col:
                        move_piece(selected_piece[0], selected_piece[1], row, col, captured)
                        current_player = 'blue' if current_player == 'red' else 'red'
                        moved = True
                        
                        # Check for ZA WARUDO after move
                        warudo_check = check_za_warudo()
                        if warudo_check:
                            za_warudo(warudo_check[0], warudo_check[1])
                        
                        # Check for winner
                        winner = check_winner()
                        if winner:
                            victory_animation(winner)
                            running = False
                        
                        break
                
                selected_piece = None
                valid_moves = []
                
                # If didn't move, check if selecting new piece
                if not moved and board[row][col] == current_player:
                    selected_piece = (row, col)
                    valid_moves = get_valid_moves(row, col)
            else:
                # Select a piece
                if board[row][col] == current_player:
                    selected_piece = (row, col)
                    valid_moves = get_valid_moves(row, col)
    
    # Draw everything
    screen.fill(BG_COLOR)
    draw_board()
    draw_pieces()
    
    if selected_piece:
        draw_selected(selected_piece[0], selected_piece[1])
        draw_valid_moves([(m[0], m[1]) for m in valid_moves])
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

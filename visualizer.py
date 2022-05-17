import pygame
import sys
from cell import Cell


pygame.init()


WIDTH = 1200
HEIGHT = 800
CELL_SIZE = 20
GRID_ORIGIN_Y = 200
COLS = WIDTH // CELL_SIZE # 60
ROWS = (HEIGHT - GRID_ORIGIN_Y) // CELL_SIZE # 30

FPS = 60 

# COLORS
NAVY_BLUE = (15, 35, 55)
CYAN = (101, 255, 220)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# FONTS
LARGE_FONT = pygame.font.Font(None, 60)
MEDIUM_FONT = pygame.font.Font(None, 8)
SMALLFONT = pygame.font.Font(None, 28)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path visualizer")

# drawing start node
start_node = pygame.rect.Rect(400, 400, CELL_SIZE, CELL_SIZE)
dragging_start = False

# drawing end node
end_node = pygame.rect.Rect(480, 560, CELL_SIZE, CELL_SIZE)
dragging_end = False

# defining outer boundary
outer_walls = []
walls = []




def draw_toolbar(win):
    pygame.draw.line(win, CYAN, (0, 0), (WIDTH, 0), 3) # TOP
    pygame.draw.line(win, CYAN, (0, 200), (WIDTH, 200)) # BOTTOM
    pygame.draw.line(win, CYAN, (0, 0), (0, 200)) # LEFT
    pygame.draw.line(win, CYAN, (WIDTH, 0), (WIDTH, 200), 3) # RIGHT

    # b = Cell(20, 30, RED, CELL_SIZE)
    # b.draw(win)

    # sample_text = MEDIUM_FONT.render("Toolbar goes here...", True, CYAN)
    # sample_rect = sample_text.get_rect()
    # sample_rect.center = ((WIDTH / 2), 75)
    # win.blit(sample_text, sample_rect)


def draw_grid(win):
    # drawing boundaries
    for row in range(ROWS):
        pygame.draw.rect(win, BLACK, [0, GRID_ORIGIN_Y+(row*CELL_SIZE), CELL_SIZE, CELL_SIZE])
        pygame.draw.rect(win, BLACK, [WIDTH - CELL_SIZE, GRID_ORIGIN_Y+(row*CELL_SIZE), CELL_SIZE, CELL_SIZE])
    for col in range(COLS):
        pygame.draw.rect(win, BLACK, [col*CELL_SIZE, GRID_ORIGIN_Y, CELL_SIZE, CELL_SIZE])
        pygame.draw.rect(win, BLACK, [col*CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE, CELL_SIZE])

    # drawing walls
    draw_walls()


    # drawing gridlines
    for r in range(ROWS):
        pygame.draw.line(win, CYAN, (0, (GRID_ORIGIN_Y + (r*CELL_SIZE))), (WIDTH, (GRID_ORIGIN_Y + (r*CELL_SIZE))))
        for c in range(COLS):
            pygame.draw.line(win, CYAN, (c*CELL_SIZE, GRID_ORIGIN_Y), (c*CELL_SIZE, HEIGHT))
    
    pygame.draw.line(win, CYAN, (0, (GRID_ORIGIN_Y + (ROWS*CELL_SIZE))), (WIDTH, (GRID_ORIGIN_Y + (ROWS*CELL_SIZE))), 3)
    pygame.draw.line(win, CYAN, (COLS*CELL_SIZE, GRID_ORIGIN_Y), (COLS*CELL_SIZE, HEIGHT), 3)


    # drawing the start and end nodes
    pygame.draw.rect(win, GREEN, start_node)
    pygame.draw.rect(win, RED, end_node)


def draw_window(win):
    win.fill(NAVY_BLUE)
    draw_toolbar(win)
    draw_grid(win)

def draw_walls():
    for wall in walls:
        x, y = wall
        pygame.draw.rect(screen, BLACK, [x, y, CELL_SIZE, CELL_SIZE])

def handle_event(e):
    global dragging_end, dragging_start, offset_x, offset_y
    # checking start
    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1:
            if start_node.collidepoint(e.pos):
                dragging_start = True
                mouse_x, mouse_y = e.pos
                offset_x = start_node.x - mouse_x
                offset_y = start_node.y - mouse_y
            elif end_node.collidepoint(e.pos):
                dragging_end = True
                mouse_x, mouse_y = e.pos
                offset_x = end_node.x - mouse_x
                offset_y = end_node.y - mouse_y
            else:
                mouse_x, mouse_y = e.pos
                x, y = get_closest_cell((mouse_x, mouse_y))
                walls.append((x, y))
    elif e.type == pygame.MOUSEBUTTONUP:
        if e.button == 1:
            if dragging_start:
                dragging_start = False
                nx, ny = get_closest_cell((start_node.x, start_node.y))
                start_node.x = nx
                start_node.y = ny
            elif dragging_end:
                dragging_end = False
                nx, ny = get_closest_cell((end_node.x, end_node.y))
                end_node.x = nx
                end_node.y = ny
                print(end_node.x, end_node.y)
    elif e.type == pygame.MOUSEMOTION:
        if dragging_start:
            mouse_x, mouse_y = e.pos
            start_node.x = mouse_x + offset_x
            start_node.y = mouse_y + offset_y
        elif dragging_end:
            mouse_x, mouse_y = e.pos
            end_node.x = mouse_x + offset_x
            end_node.y = mouse_y + offset_y


def get_closest_cell(pos):
    x, y = pos
    new_x = round(x / CELL_SIZE, None) * CELL_SIZE
    y = round(((y - 200) / CELL_SIZE), None)
    new_y = 200 + (y * CELL_SIZE)
    return new_x, new_y


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_event(event)
    
    draw_window(screen)
    pygame.display.flip()
    clock.tick(FPS)
sys.exit()

 

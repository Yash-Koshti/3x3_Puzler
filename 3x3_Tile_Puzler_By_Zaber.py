import pygame
import random
import time
pygame.init()

GAME_WINDOW = pygame.display.set_mode([312, 312])
pygame.display.set_caption("3 x 3 Tile Puzler By Zaber")

_white = (255, 255, 255)
_black = (0, 0, 0)
_brown = (180, 75, 0)
_pink = (255, 40, 240)
_yellow = (255, 255, 150)

_puzzle_block = 100
_puzzle_list = [[pygame.Rect(0, 0, _puzzle_block, _puzzle_block), pygame.Rect(106, 0, _puzzle_block, _puzzle_block), pygame.Rect(212, 0, _puzzle_block, _puzzle_block)],
                [pygame.Rect(0, 106, _puzzle_block, _puzzle_block), pygame.Rect(106, 106, _puzzle_block, _puzzle_block), pygame.Rect(212, 106, _puzzle_block, _puzzle_block)],
                [pygame.Rect(0, 212, _puzzle_block, _puzzle_block), pygame.Rect(106, 212, _puzzle_block, _puzzle_block), pygame.Rect(212, 212, _puzzle_block, _puzzle_block)]]
_selection_box = pygame.Rect(0, 0, 106, 106)
_selection_state = False
_selected_block = _updated_block = []
_selection_img = pygame.image.load('Selection_Frame_2_Transparent.png')

_num_list = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]
_num_list2 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
_lose_list = [[0, 2, 1],
             [3, 4, 5],
             [6, 7, 8]]
_lose = 0
_lose_state = False

#Shuffling the numbers.
_num_list2 = random.sample(_num_list2, len(_num_list2))
tmp = []
_shuffled_list = []
while _num_list2:
    tmp.append(_num_list2[0])
    _num_list2.pop(0)
    if len(tmp) == 3:
        _shuffled_list.append(tmp)
        tmp = []
#for s in range(3): _shuffled_list.append(random.sample(_num_list[s], len(_num_list[s])))
_shuffled_list = random.sample(_shuffled_list, len(_shuffled_list))

_clock = pygame.time.Clock()
_fps = 60
_font = pygame.font.SysFont(None, 70)

def selection(m_pos):
    global _selection_state, _selected_block
    
    for i in range(3):
        for j in range(3):
            if m_pos[0] < _puzzle_list[i][j].bottomright[0] and m_pos[1] < _puzzle_list[i][j].bottomright[1]:
                _selection_box.x = _puzzle_list[i][j].x - 3
                _selection_box.y = _puzzle_list[i][j].y - 3
                _selection_state = True
                _selected_block = [i, j]
                break
        if _selection_state: break
    return

def change_pos(event_key):
    global _updated_block
    
    i, j = _selected_block
    if event_key == pygame.K_UP or event_key == pygame.K_w:
        if (i - 1) >= 0:
            i -= 1
            _updated_block = [i, j]
            swap()
                        
    if event_key == pygame.K_DOWN or event_key == pygame.K_s:
        if (i + 1) <= 2:
            i += 1
            _updated_block = [i, j]
            swap()
                        
    if event_key == pygame.K_RIGHT or event_key == pygame.K_d:
        if (j + 1) <= 2:
            j += 1
            _updated_block = [i, j]
            swap()
                        
    if event_key == pygame.K_LEFT or event_key == pygame.K_a:
        if (j - 1) >= 0:
            j -= 1
            _updated_block = [i, j]
            swap()
    return

def swap():
    global _selection_state
    
    u_num = _shuffled_list[_updated_block[0]][_updated_block[1]]
    s_num = _shuffled_list[_selected_block[0]][_selected_block[1]]
    
    if u_num == 0:
        _shuffled_list[_updated_block[0]][_updated_block[1]] = s_num
        _shuffled_list[_selected_block[0]][_selected_block[1]] = u_num
        _selection_state = False
    return

def game_over(win):
    if win:
        GAME_WINDOW.fill(_brown)
        _end_font = _font.render("YOU WIN!", 1, _black)
        GAME_WINDOW.blit(_end_font, [(GAME_WINDOW.get_width() / 2) - (_end_font.get_width() / 2), (GAME_WINDOW.get_height() / 2) - (_end_font.get_height() / 2)])
    else:
        GAME_WINDOW.fill(_brown)
        _end_font = _font.render("YOU LOSE!", 1, _black)
        GAME_WINDOW.blit(_end_font, [(GAME_WINDOW.get_width() / 2) - (_end_font.get_width() / 2), (GAME_WINDOW.get_height() / 2) - (_end_font.get_height() / 2)])
        
    pygame.display.update()
    time.sleep(5)
    return

def gameloop():
    global _selection_state, _selected_block, _lose, _lose_state
    
    _end_game = False    
    i = j = 0

    while not _end_game:
        GAME_WINDOW.fill(_brown)
        
        #Rendering the puzzle_list.
        for row in _puzzle_list:
            for col in row:
                if _shuffled_list[i][j] != 0:
                    pygame.draw.rect(GAME_WINDOW, _white, col)
                    _num = _font.render(str(_shuffled_list[i][j]), 1, _black)
                    GAME_WINDOW.blit(_num, [col.centerx - (_num.get_width() / 2), col.centery - (_num.get_height() / 2)])
                else:
                    pygame.draw.rect(GAME_WINDOW, _brown, col)
                    _num = _font.render(str(_shuffled_list[i][j]), 1, _brown)
                    GAME_WINDOW.blit(_num, [col.centerx - (_num.get_width() / 2), col.centery - (_num.get_height() / 2)])
                j += 1
            j = 0
            i += 1
        i = j = 0
        
        if _selection_state: GAME_WINDOW.blit(_selection_img, _selection_box)
        
        pygame.display.update()
        _clock.tick(_fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                _end_game = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                _selection_state = False
                selection(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if _selection_state:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        _lose_state = True
                        change_pos(event.key)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        _lose_state = True
                        change_pos(event.key)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        _lose_state = True
                        change_pos(event.key)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        _lose_state = True
                        change_pos(event.key)
                
        if _shuffled_list == _lose_list and _lose_state:
            if _lose == 2:
                _end_game = True
                game_over(False)
            else:
                _lose += 1
                _lose_state = False
        
        if _shuffled_list == _num_list:
            _end_game = True
            game_over(True)
    pygame.quit()
    return
gameloop()

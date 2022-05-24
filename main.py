import pygame as pg
import numpy as np


pg.init()
window_width = 1800
window_height = 900
screen = pg.display.set_mode((window_width, window_height))
grey = pg.Color(220, 220, 220)
white = pg.Color(255, 255, 255)
black = pg.Color(0, 0, 0)
blue = pg.Color(0, 191, 255)
screen.fill(grey)
block_size = 35
FONT = pg.font.Font(None, 40)

word_list = {
    'saffron': 'saffron definition',
    # 'pumpernickel': 'pumpernickel definition',
    'leaven': 'leaven definition',
    'pummel': 'pump definition',
    'x': 'x def',
    'coda': 'coda definition',
    'paladin': 'paladin definition',
    'syncopation': 'syncopation definition',
    'albatross': 'albatross definition',
    'harp': 'harp definition',
    'piston': 'piston definition',
    'caramel': 'caramel definition',
    'coral': 'coral definition',
    'dawn': 'dawn definition',
    'pitch': 'pitch definition',
    'fjord': 'fjord definition',
    'lip': 'lip definition',
    'lime': 'lime definition',
    'mist': 'mist definition',
    'plague': 'plague definition',
    'yarn': 'yarn definition',
    'snicker': 'snicker definition',
    'nig': 'nig definition'
}

word_list = {k.upper():v.upper() for k, v in word_list.items()}
word_list_sorted = {}

for k in sorted(word_list, key=len, reverse=True):
    word_list_sorted[k] = word_list[k]

# print(word_list_sorted)

class Box:
    def __init__(self, x, y, size, text='', is_dead=False):
        self.rect = pg.Rect(x, y, size, size)
        self.text = text
        self.color = white
        self.border_color = black
        self.txt_surface = FONT.render(text, True, black)
        self.active = False
        self.is_dead = is_dead

    def handle_event(self, event):
        if self.is_dead == False:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = blue if self.active else white

            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key != pg.K_BACKSPACE and len(self.text) <= 1:
                        self.text = event.unicode
                        self.active = False
                        self.color = white
                        self.text = self.text.upper()
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                self.txt_surface = FONT.render(self.text, True, black)



    def draw(self, screen):
        if self.is_dead == False:
            pg.draw.rect(screen, self.color, self.rect)
            pg.draw.rect(screen, self.border_color, self.rect, 2)
            screen.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 5))
        else:
            pg.draw.rect(screen, black, self.rect)

    def add_text(self, screen, text):
        self.text = text
        self.txt_surface = FONT.render(self.text, True, black)
        screen.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 5))
        pg.display.flip()

    def add_letter(self, letter):
        self.text = letter

input_boxes = []
def draw_grid_exp(rows, cols):
    x = 15
    y = 15
    for row in range(rows):
        column = []
        for col in range(cols):
            column.append(Box(x, y, block_size))
            x += 34
        input_boxes.append(column)
        x = 15
        y += 34


def draw_grid(rows, cols): # old obsolete version
    x = 15
    y = 15
    for box in range(rows):
        for box in range(cols):
            input_boxes.append(Box(x, y, block_size))
            x += 34
        x = 15
        y += 34
    print(input_boxes)

def place_word(array, row, col, word, is_vertical):
    i_count = 0
    if is_vertical is False:
        for i in range(len(word)):
            array[row][col + i].add_text(screen, word[i])
            i_count += 1
        array[row][col + i_count].is_dead = True

    else:
        for i in range(len(word)):
            array[row + i][col].add_text(screen, word[i])
            i_count += 1
        array[row + i_count][col].is_dead = True
#TODO: rozpisać sobie na kartce logikę is_empty, żeby sprawdzało czy po kolejnym boxie po słowie jest is_dead (jeśli tak, to umieść słowo)
# i żeby sprawdzało czy po bokach słowa nie ma innych słów
# i perhaps czy są jakieś przecinające się słówka
def is_empty(array, row, col, word, is_vertical: bool):
    length = len(word)
    empty_boxes = 1
    if not is_vertical and col + length > len(array[row]):
        return False

    if is_vertical and row + length > len(array):
        return False

    else:
        if is_vertical:
            for i in range(length):
                if array[row + 1][col].text == '' and array[row + 1][col].is_dead is False:
                    empty_boxes += 1
                    row += 1
                    if empty_boxes == length:
                        return True
                else:
                    return False
        if not is_vertical:
            for i in range(length):
                if array[row][col + 1].text == '' and array[row][col + 1].is_dead is False:
                    empty_boxes += 1
                    col += 1
                    if empty_boxes == length:
                        return True
                else:
                    return False
definitions = []

# fill the grid rec
words = [*word_list_sorted]
words_placed = []
unused_words = []
# words.pop(0)
word_placed = False
iteration = 0
un_words = ['SYNCOPATION', 'SAFFRON', 'SNICKER', 'PISTON', 'PLAGUE', 'CORAL', 'PITCH', 'FJORD', 'CODA', 'HARP', 'LIME', 'YARN', 'ALBATROSS', 'X']

def fill_the_grid_rec(word_list, array):
    global word_placed
    global iteration
    words = word_list
    next_word = 0
    print(words)
    if len(words) == 0:
        print('All words were placed')
    else:
        word = words[next_word]
        print(f'current word: {word}')
        for i in range(len(array)):
            for box in array[i]:
                row = i
                col = array[i].index(box)
                if word[0] == box.text:
                    if is_empty(array, row, col, word, False):
                        place_word(array, row, col, word, False)
                        print(f'{word} placed pionowo')
                        word_placed = True
                        break
                    elif is_empty(array, row, col, word, True):
                        place_word(array, row, col, word, True)
                        print(f'{word} placed poziomo')
                        word_placed = True
                        break
            if word_placed:
                break

        if not word_placed:
            print(f'{word} nie pasuje nigdzie')
            unused_words.append(word)
            words.remove(word)
        if word_placed:
            words.remove(word)
            words_placed.append(word)
            word_placed = False
        return fill_the_grid_rec(word_list, array)


def main():
    clock = pg.time.Clock()
    # draw_grid_exp(25,25)
    draw_grid_exp(25,25)
    # fill_the_grid_exp(word_list_sorted)
    # place_word(0, 0, 'LIME', True)
    # print(is_empty(0, 0, 'LIP', True))
    # print(is_empty(3, 0, 'PATRYK', False))
    # input_box1 = Box(300, 300, block_size, 'A')
    # input_box2 = Box(500, 500, block_size)
    # input_boxes = [input_box1, input_box2]
    # draw_grid(25, 30)
    # place_word(0, 0, 'KOCHAM CIE ANIU', False)
    # place_word(5, 2, 'SEKSRUCHANIE', True)
    # input_boxes[13].is_dead = True
    done = False
    # arr = np.array(input_boxes)
    # arr_2d = np.reshape(arr, (25,25))
    # fill_the_grid_exp(word_list_sorted)
    # print(is_empty(arr_2d, 0, 0, 'PUMPERNICKEL', True))
    place_word(input_boxes, 0, 0, 'PUMPERNICKEL', False)
    fill_the_grid_rec(words, input_boxes)
    print(unused_words)

    test_words = ['VELEN', 'LIME', 'PUM', 'NIGGER']
    fill_the_grid_rec(test_words, input_boxes)
    # print(is_empty(input_boxes, 5, 0, 'A', False))
    # print(is_empty(input_boxes, 5, 0, 'AA', False))
    # print(is_empty(input_boxes, 5, 0, 'AAA', False))
    # print(is_empty(input_boxes, 5, 0, 'AAAA', False))
    # print(is_empty(input_boxes, 5, 0, 'AAAAA', False))
    print(is_empty(input_boxes, 0, 23, 'PUMPERNICKEL', False))
    print(is_empty(input_boxes, 23, 0, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', True))

    # fill_the_grid_rec2(unused_words, input_boxes)

    words222 = ['PISTON']
    # fill_the_grid_rec(words222, input_boxes)

    # fill_the_grid_np(word_list_sorted, arr_2d)
    # fill_the_grid_test(word_list_sorted, arr_2d)


    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # for box in input_boxes: # numpy version
            #     box.handle_event(event)
            for i in range(len(input_boxes)): # good 2d version
                for box in input_boxes[i]:
                    box.handle_event(event)

        for i in range(len(input_boxes)): # good 2d version
            for box in input_boxes[i]:
                box.draw(screen)
            # for box in input_boxes:
            #     box.handle_event(event)
        #
        # for box in input_boxes: # numpy version
        #     box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()



# block_size = 35
# for x in range(0, 1050, block_size):
#     for y in range(0, 875, block_size):
#         rect = pygame.Rect(x+10, y+10, block_size, block_size)
#         pygame.draw.rect(SCREEN, white, rect, 1)
#         pygame.display.flip()

# while running:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False
#     for box in input_boxes:
#         box.handle_event(event)
#
#     for box in input_boxes:
#         box.draw(screen)
#
#     pg.display.flip()
#     clock.tick(30)

















# x = 0
# y = 0
# for j in range(5):
#     for i in range(30):
#         pg.draw.rect(DISPLAY, WHITE, Rect(x, y, 40, 40), 2)
#         x += 40
#     y += 100
# # pg.draw.rect(DISPLAY, WHITE, Rect(1, 1, 40, 40), 2)
# # pg.draw.rect(DISPLAY, WHITE, Rect(41, 1, 40, 40), 2)
# pg.draw.rect(DISPLAY, WHITE, Rect(1200, 0, 600, 900))
# while True:
#     pg.display.update()
#     for event in pg.event.get():
#         if event.type == QUIT:
#             pg.quit()
#             # sys.exit()




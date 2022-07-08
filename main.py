import pygame as pg
from word_scraping import words_a, words_b, words_c, words_d, words_e, words_f, words_g, words_h, words_i, words_j, words_k, words_l, words_m, words_n, words_o, words_p, words_r, words_s, words_t, words_u, words_w, words_z
import random


pg.init()
window_width = 1800
window_height = 900
screen = pg.display.set_mode((window_width, window_height))
grey = pg.Color(220, 220, 220)
white = pg.Color(255, 255, 255)
black = pg.Color(0, 0, 0)
blue = pg.Color(0, 191, 255)
screen.fill(grey)
block_size = 40
FONT = pg.font.Font('C:/Users/X/PycharmProjects/pythonProject/crosswords/arial_bold.ttf', 27)
NUMBER_FONT = pg.font.Font('C:/Users/X/PycharmProjects/pythonProject/crosswords/arial.ttf', 12)
ARROW_FONT = pg.font.Font('C:/Users/X/PycharmProjects/pythonProject/crosswords/Symbola.ttf', 10)


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

word_list = {k.upper(): v.upper() for k, v in word_list.items()}
word_list_sorted = {}

for k in sorted(word_list, key=len, reverse=True):
    word_list_sorted[k] = word_list[k]


class Box:
    def __init__(self, x, y, size, text='', is_dead=False):
        self.rect = pg.Rect(x, y, size, size)
        self.text = text
        self.color = white
        self.border_color = black
        self.txt_surface = FONT.render(text, True, black)
        self.number = ''
        self.arrow_vertical = ''
        self.arrow_horizontal = ''
        self.arrow_surface_vertical = ARROW_FONT.render(self.arrow_vertical, True, black)
        self.arrow_surface_horizontal = ARROW_FONT.render(self.arrow_horizontal, True, black)
        self.number_surface = NUMBER_FONT.render(self.number, True, black)
        self.active = False
        self.is_dead = is_dead

    def handle_event(self, event):
        if self.is_dead is not True:
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
        if not self.is_dead:
            pg.draw.rect(screen, self.color, self.rect)
            pg.draw.rect(screen, self.border_color, self.rect, 2)
            screen.blit(self.txt_surface, (self.rect.x + 11, self.rect.y + 10))
            screen.blit(self.number_surface, (self.rect.x + 2, self.rect.y + 2))
            screen.blit(self.arrow_surface_vertical, (self.rect.x + 4, self.rect.y + 14))
            screen.blit(self.arrow_surface_horizontal, (self.rect.x + 16, self.rect.y + 2))
        else:
            pg.draw.rect(screen, black, self.rect)

    def add_text(self, text):
        self.text = text
        self.txt_surface = FONT.render(self.text, True, black)
        # screen.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 10))
        # pg.display.flip()

    def add_number(self, number, is_vertical):
        self.number = number
        self.number_surface = NUMBER_FONT.render(self.number, True, black)
        if is_vertical:
            self.arrow_surface_vertical = ARROW_FONT.render('\u25BC', True, black)
        else:
            self.arrow_surface_horizontal = ARROW_FONT.render('\u27A4', True, black)
        # screen.blit(self.number_surface, (self.rect.x + 2, self.rect.y + 2))
        # pg.display.flip()


input_boxes = []
def draw_grid_exp(rows, cols):
    x = 15
    y = 15
    for row in range(rows):
        column = []
        for col in range(cols):
            column.append(Box(x, y, block_size))
            x += 39
        input_boxes.append(column)
        x = 15
        y += 39


def place_word(array, row, col, word, is_vertical):
    word = word.upper()
    i_count = 0
    if is_vertical is False:
        for i in range(len(word)):
            array[row][col + i].add_text(word[i])
            i_count += 1
        array[row][col + i_count].is_dead = True

    else:
        for i in range(len(word)):
            array[row + i][col].add_text(word[i])
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


def get_word(array, length):
    array_sorted = sorted(array, key=len)
    found = False
    while found is not True:
        word = random.choice(array_sorted)
        if len(word) == length:
            found = True
            return word


def get_word_from_letter(row, column, length):
    letter = input_boxes[row][column].text
    if letter == 'A':
        return get_word(words_a, length)
    if letter == 'B':
        return get_word(words_b, length)
    if letter == 'C':
        return get_word(words_c, length)
    if letter == 'D':
        return get_word(words_d, length)
    if letter == 'E':
        return get_word(words_e, length)
    if letter == 'F':
        return get_word(words_f, length)
    if letter == 'G':
        return get_word(words_g, length)
    if letter == 'H':
        return get_word(words_h, length)
    if letter == 'I':
        return get_word(words_i, length)
    if letter == 'J':
        return get_word(words_j, length)
    if letter == 'K':
        return get_word(words_k, length)
    if letter == 'L':
        return get_word(words_l, length)
    if letter == 'M':
        return get_word(words_m, length)
    if letter == 'N':
        return get_word(words_n, length)
    if letter == 'O':
        return get_word(words_o, length)
    if letter == 'U':
        return get_word(words_u, length)
    if letter == 'P':
        return get_word(words_p, length)
    if letter == 'R':
        return get_word(words_r, length)
    if letter == 'S':
        return get_word(words_s, length)
    if letter == 'T':
        return get_word(words_t, length)
    if letter == 'U':
        return get_word(words_u, length)
    if letter == 'W':
        return get_word(words_w, length)
    if letter == 'Z':
        return get_word(words_z, length)


def fill_the_grid():
    word = get_word(words_z, 15)
    place_word(input_boxes, 0, 0, word, False)
    place_word(input_boxes, 0, 0, get_word(words_z, 13), True)
    place_word(input_boxes, 0, 6, get_word_from_letter(0, 6, 10), True)
    place_word(input_boxes, 8, 6, get_word_from_letter(8, 6, 7), False)

def main():
    clock = pg.time.Clock()
    # draw_grid_exp(25,25)
    draw_grid_exp(20, 20)
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
    fill_the_grid()
    # arr = np.array(input_boxes)
    # arr_2d = np.reshape(arr, (25,25))
    # fill_the_grid_exp(word_list_sorted)
    # # print(is_empty(arr_2d, 0, 0, 'PUMPERNICKEL', True))
    # place_word(input_boxes, 0, 0, 'PUMPERNICKEL', False)
    # fill_the_grid_rec(words, input_boxes)
    # print(unused_words)

    # test_words = ['VELEN', 'LIME', 'PUM', 'NIGGER']
    # fill_the_grid_rec(test_words, input_boxes)
    # print(is_empty(input_boxes, 5, 0, 'A', False))
    # print(is_empty(input_boxes, 5, 0, 'AA', False))
    # print(is_empty(input_boxes, 5, 0, 'AAA', False))
    # print(is_empty(input_boxes, 5, 0, 'AAAA', False))
    # print(is_empty(input_boxes, 5, 0, 'AAAAA', False))
    # print(is_empty(input_boxes, 0, 23, 'PUMPERNICKEL', False))
    # print(is_empty(input_boxes, 23, 0, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', True))
    # input_boxes[0][0].add_number('01', True)
    # input_boxes[0][0].add_number('01 ', False)
    # input_boxes[0][3].add_number('16', True)


    # fill_the_grid_rec2(unused_words, input_boxes)


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


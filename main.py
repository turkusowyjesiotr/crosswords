import pygame as pg
from word_scraping import Words
from definitions_scraping import scrape_definitions
import hourglass
import random
import string
import threading
import time


pg.init()
BACKGROUND = pg.image.load('assets/images/paper.jpg')
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 900
SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
GREY = pg.Color(220, 220, 220)
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
BLUE = pg.Color(0, 191, 255)
PINK = pg.Color(242, 233, 238)
DARK_GREY = pg.Color(90, 90, 90)
DARK_GREY_2 = pg.Color(170, 170, 170)
GOLD = pg.Color(235, 198, 52)
GREEN = pg.Color(0, 128, 0)
RED = pg.Color(255, 0, 0)
block_size = 40
SCREEN.blit(BACKGROUND, (0, 0))
FONT = pg.font.Font('assets/fonts/arial_bold.ttf', 27)
BUTTON_FONT = pg.font.Font('assets/fonts/arial_bold.ttf', 20)
NUMBER_FONT = pg.font.Font('assets/fonts/arial.ttf', 12)
ARROW_FONT = pg.font.Font('assets/fonts/Symbola.ttf', 10)
DEF_FONT = pg.font.Font('assets/fonts/arial.ttf', 15)
LOADING_FONT = pg.font.Font('assets/fonts/arial_bold.ttf', 40)
horizontal_number = 1
vertical_number = 1
special_chars = ['Ą', 'Ę', 'Ć', 'Ó', 'Ł', 'Ś', 'Ń', 'Ź', 'Ż', 'Y', 'X', 'V']
# special_chars = ['ą', 'ę', 'ć', 'ó', 'ł', 'ś', 'ń', 'ź', 'ż']
buttons = []
definitions = []
crossword = 0
show_definitions = False
# words_used = {'seks': ['Lorem Ipsum is simply dummy text of the printing and typesetting Lorem Ipsum is simply dummy text of the printing and typesetting', 'Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.', 'dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa', 'seks seks seks']}
words_used = {}
words_used_vertical = {}
loaded = True
debug_mode = False
moving_sprites = pg.sprite.Group()
loading_icon = hourglass.Hourglass(1300, 400)
moving_sprites.add(loading_icon)
img = pg.image.load('assets/images/load.png')
img = pg.transform.smoothscale(img, (23, 23)).convert_alpha()


class Button:
    def __init__(self, x, y, width, height, elevation, text, button_type):
        self.rect = pg.Rect(x, y, width, height)
        self.bottom_rect = pg.Rect(x, y, width, height)
        self.elevation = elevation
        self.text = text
        self.text_surface = BUTTON_FONT.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.button_type = button_type
        self.color = GREY
        self.bottom_color = DARK_GREY
        self.border_color = BLACK
        self.original = y
        self.pressed = False
        if button_type == 4:
            definitions.append(self)
        else:
            buttons.append(self)

    def update_text(self):
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def button_event(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = DARK_GREY_2
            if pg.mouse.get_pressed()[0]:
                self.rect.y = self.bottom_rect.y
                self.update_text()
                update_game_state()
                self.button_action()
            else:
                self.rect.y = self.original
                self.update_text()
        else:
            self.rect.y = self.original
            self.update_text()
            self.color = GREY

    def draw(self):
        self.bottom_rect.y = self.original + self.elevation
        pg.draw.rect(SCREEN, self.bottom_color, self.bottom_rect)
        pg.draw.rect(SCREEN, self.color, self.rect)
        pg.draw.rect(SCREEN, self.border_color, self.rect, 2)
        SCREEN.blit(self.text_surface, self.text_rect)

    def button_action(self):
        if self.button_type == 0:
            t = threading.Thread(target=loading(True))
            d = threading.Thread(target=crossword_1)
            t.start()
            d.start()
        elif self.button_type == 1:
            t = threading.Thread(target=loading(True))
            d = threading.Thread(target=crossword_2)
            t.start()
            d.start()
        elif self.button_type == 2:
            # found = False
            # occupied = get_occupied_boxes(10, 15, 6, True)
            # print(occupied)
            # boxx = [14, 15]
            # leng = is_empty_backwards(input_boxes, boxx[0], boxx[1], False)
            # print(leng)
            # while not found:
            #     word = get_random_word(12).upper()
            #     print(word)
            #     if word[-1] == input_boxes[boxx[0]][boxx[1]].secret_text:
            #         place_word(input_boxes, boxx[0], boxx[1] - len(word) + 1, word, False)
            #         print('HURRRA! ', word)
            #         found = True
            debug()


class Definition(Button):
    def __init__(self, x, y, width, height, elevation, number, word_used, words_dict, text='', button_type=4):
        # button
        super().__init__(x, y, width, height, elevation, text, button_type)
        self.btn_img = img

        # definition
        self.number = str(number) + '. '
        self.number_surface = DEF_FONT.render(self.number, True, BLACK)
        self.word_used = word_used
        self.words_dict = words_dict
        self.definitions = words_dict.get(self.word_used)
        self.current_def = 0
        self.max_def = len(self.definitions) - 1
        self.definition = self.definitions[self.current_def]
        self.part1 = ''
        self.part2 = ''
        self.part3 = ''
        self.def_surface = DEF_FONT.render(self.definition, True, BLACK)
        self.height = 50
        self.width = 400
        self.pos_y = self.rect.topright[1]
        self.pos_x = self.rect.x + 35
        self.def_rect = pg.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def draw(self):
        super().draw()
        SCREEN.blit(self.btn_img, (self.rect.x + 4, self.rect.y + 4))

    def draw_def(self):
        try:
            print('draw_def ',self.part1, f'word:{self.word_used}')
            self.def_surface = DEF_FONT.render(self.part1, True, BLACK)
            SCREEN.blit(self.def_surface, (self.pos_x + 2, self.pos_y + 2))
            self.def_surface = DEF_FONT.render(self.part2, True, BLACK)
            SCREEN.blit(self.def_surface, (self.pos_x + 2, self.pos_y + 15))
            self.def_surface = DEF_FONT.render(self.part3, True, BLACK)
            SCREEN.blit(self.def_surface, (self.pos_x + 2, self.pos_y + 27))
        except AttributeError:
            self.part1 = 'xxx'

    def wrap_def(self):
        i = 0
        text_width = self.def_rect.left
        if DEF_FONT.size(f'{self.definition}')[0] < self.width:
            return self.definition
        else:
            for letter in self.definition:
                font_width = DEF_FONT.size(f'{letter}')[0]
                text_width += font_width
                if text_width >= self.def_rect.right:
                    space = self.definition.rfind(" ", 0, i)
                    part = self.definition[:space]
                    self.definition = self.definition[space + 1:]
                    return part
                i += 1

    def calc_def(self):
        time.sleep(0.1)
        if DEF_FONT.size(f'{self.definition}')[0] >= self.width*3:
            self.next_definition()
            self.calc_def()
        elif DEF_FONT.size(f'{self.definition}')[0] > self.width*2:
            self.part1 = self.wrap_def()
            self.part1 = self.number + self.part1
            self.part2 = self.wrap_def()
            self.part3 = self.wrap_def()
        elif DEF_FONT.size(f'{self.definition}')[0] > self.width:
            self.part1 = self.wrap_def()
            self.part1 = self.number + self.part1
            self.part2 = self.wrap_def()
            self.part3 = ''
        else:
            self.part1 = self.wrap_def()
            self.part1 = self.number + self.part1
            self.part2 = ''
            self.part3 = ''

    def next_definition(self):
        if self.current_def == self.max_def:
            self.current_def = 0
            self.definition = self.definitions[self.current_def]
        else:
            self.current_def += 1
            self.definition = self.definitions[self.current_def]

    def button_action(self):
        super().button_action()
        if self.button_type == 4:
            self.next_definition()
            self.calc_def()
            update_game_state()


class Box:
    def __init__(self, x, y, size, row, column, text='', is_dead=False):
        self.rect = pg.Rect(x, y, size, size)
        self.text = text
        self.secret_text = ''
        self.color = WHITE
        self.border_color = BLACK
        self.txt_surface = FONT.render(self.text, True, BLACK)
        self.number = ''
        self.arrow_vertical = ''
        self.arrow_horizontal = ''
        self.arrow_surface_vertical = ARROW_FONT.render(self.arrow_vertical, True, BLACK)
        self.arrow_surface_horizontal = ARROW_FONT.render(self.arrow_horizontal, True, BLACK)
        self.number_surface = NUMBER_FONT.render(self.number, True, BLACK)
        self.active = False
        self.final = False
        self.is_dead = is_dead
        self.row = row
        self.column = column

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            if self.rect.collidepoint(event.pos):
                if self.is_dead is False:
                    self.is_dead = True
                else:
                    self.is_dead = False
        if self.is_dead is not True:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                if self.final:
                    self.color = GOLD
                if not self.active and not self.final:
                    self.color = WHITE
                if self.active:
                    self.color = BLUE

            if event.type == pg.KEYDOWN:
                not_active = [pg.K_RALT, pg.K_RIGHT, pg.K_LEFT, pg.K_DOWN, pg.K_BACKSPACE, pg.K_RETURN,
                              pg.K_UP, pg.K_LALT, pg.K_LCTRL, pg.K_RCTRL, pg.K_RSHIFT, pg.K_LSHIFT, pg.K_SPACE]
                if self.active:
                    if event.key == pg.K_RIGHT:
                        length = random.randint(3, 10)
                        word = get_word_from_letter(self.row, self.column, length)
                        if is_empty(input_boxes, self.row, self.column, word, False):
                            place_word(input_boxes, self.row, self.column, word, False)
                    elif event.key == pg.K_DOWN:
                        length = random.randint(3, 10)
                        word = get_word_from_letter(self.row, self.column, length)
                        if is_empty(input_boxes, self.row, self.column, word, True):
                            place_word(input_boxes, self.row, self.column, word, True)
                    elif event.key == pg.K_UP:
                        print(is_empty_backwards(input_boxes, self.row, self.column, True))
                    elif event.key == pg.K_LEFT:
                        print(is_empty_backwards(input_boxes, self.row, self.column, False))
                    elif event.key not in not_active and len(self.text) <= 1:
                        self.text = event.unicode
                        self.active = False
                        self.text = self.text.upper()
                        self.color = GOLD if self.final else WHITE
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]

                if self.secret_text == self.text:
                    self.txt_surface = FONT.render(self.text, True, GREEN)
                else:
                    self.txt_surface = FONT.render(self.text, True, RED)

    def draw(self):
        if not self.is_dead:
            pg.draw.rect(SCREEN, self.color, self.rect)
            pg.draw.rect(SCREEN, self.border_color, self.rect, 2)
            SCREEN.blit(self.txt_surface, (self.rect.x + 11, self.rect.y + 10))
            SCREEN.blit(self.number_surface, (self.rect.x + 2, self.rect.y + 2))
            SCREEN.blit(self.arrow_surface_vertical, (self.rect.x + 4, self.rect.y + 14))
            SCREEN.blit(self.arrow_surface_horizontal, (self.rect.x + 16, self.rect.y + 2))
        else:
            pg.draw.rect(SCREEN, BLACK, self.rect)

    def add_text(self, text):
        self.secret_text = text

    def reveal_text(self):
        self.text = self.secret_text
        self.txt_surface = FONT.render(self.text, True, BLACK)
        self.draw()

    def add_number(self, number, is_vertical):
        self.number = number
        self.number_surface = NUMBER_FONT.render(self.number, True, BLACK)
        if is_vertical:
            self.arrow_surface_vertical = ARROW_FONT.render('\u25BC', True, BLACK)
        else:
            self.arrow_surface_horizontal = ARROW_FONT.render('\u27A4', True, BLACK)


input_boxes = []
def draw_grid(rows, cols):
    x = 15
    y = 15
    for row in range(rows):
        column = []
        for col in range(cols):
            column.append(Box(x, y, block_size, row, col))
            x += 39
        input_boxes.append(column)
        x = 15
        y += 39


def place_word(array, row, col, word, is_vertical):
    global horizontal_number
    global vertical_number
    if word is not None:
        word = word.upper()
        i_count = 0
        if is_vertical is False:
            array[row][col].add_number(str(horizontal_number), False)
            horizontal_number += 1
            for i in range(len(word)):
                array[row][col + i].add_text(word[i])
                i_count += 1
            array[row][col + i_count].is_dead = True

        else:
            array[row][col].add_number(str(vertical_number), True)
            vertical_number += 1
            for i in range(len(word)):
                array[row + i][col].add_text(word[i])
                i_count += 1
            array[row + i_count][col].is_dead = True
    if word is None:
        print('NoneObject passed')


def is_empty_simple(array, row, col, word, is_vertical: bool):
    if word is not None:
        length = len(word) + 1
        if not is_vertical and col + length < len(array[row]):
            return True

        if is_vertical and row + length < len(array):
            return True

        else:
            return False


def is_empty(array, row, col, word, is_vertical: bool):
    if word is not None:
        length = len(word)
        empty_boxes = 0
        if not is_vertical and col + length + 1 > len(array[row]):
            return False

        if is_vertical and row + length + 1 > len(array):
            return False

        else:
            if is_vertical:
                for i in range(length):
                    x = True if array[row + 1][col].secret_text == '' else False
                    y = True if array[row + 1][col].is_dead is False else False
                    z = True if array[row + 1][col + 1].secret_text == '' else False
                    v = True if array[row + 1][col - 1].secret_text == '' else False
                    temp = [x, y, z, v]
                    # if array[row + 1][col].secret_text == '' and array[row + 1][col].is_dead is False:
                    if all(temp):
                        empty_boxes += 1
                        row += 1
                        if empty_boxes == length:
                            return True
                    else:
                        return False
            if not is_vertical:
                for i in range(length):
                    x = True if array[row][col + 1].secret_text == '' else False
                    y = True if array[row][col + 1].is_dead is False else False
                    z = True if array[row + 1][col + 1].secret_text == '' else False
                    v = True if array[row - 1][col + 1].secret_text == '' else False
                    temp = [x, y, z, v]
                    # if array[row][col + 1].secret_text == '' and array[row][col + 1].is_dead is False:
                    if all(temp):
                        empty_boxes += 1
                        col += 1
                        if empty_boxes == length:
                            return True
                    else:
                        return False


def is_empty_backwards(array, row, col, is_vertical: bool):
    length = 0
    counted = False
    if is_vertical:
        while not counted:
            if row == 0:
                return length
            try:
                x = True if array[row - 1][col].secret_text == '' else False
                y = True if array[row - 1][col].is_dead is False else False
                z = True if array[row - 1][col + 1].secret_text == '' else False
                v = True if array[row - 1][col - 1].secret_text == '' else False
                temp = [x, y, z, v]
                if all(temp):
                    length += 1
                    row -= 1
                else:
                    break
            except IndexError:
                break
        return length
    if not is_vertical:
        while not counted:
            if col == 0:
                return length
            try:
                x = True if array[row][col - 1].secret_text == '' else False
                y = True if array[row][col - 1].is_dead is False else False
                z = True if array[row + 1][col - 1].secret_text == '' else False
                v = True if array[row - 1][col - 1].secret_text == '' else False
                temp = [x, y, z, v]
                if all(temp):
                    length += 1
                    col -= 1
                else:
                    break
            except IndexError:
                break
        return length


def get_word(array, length):
    array_sorted = sorted(array, key=len)
    found = False
    while found is not True:
        word = random.choice(array_sorted)
        if len(word) == length:
            return word


def get_word_special_chars(letter):
    if letter == 'ą':
        return random.choice(Words.words_a_pl)
    if letter == 'ę':
        return random.choice(Words.words_e_pl)
    if letter == 'ń':
        return random.choice(Words.words_n_pl)
    if letter == 'ć':
        return random.choice(Words.words_c_pl)
    if letter == 'ó':
        return random.choice(Words.words_o_pl)
    if letter == 'ł':
        return random.choice(Words.words_l_pl)
    if letter == 'ś':
        return random.choice(Words.words_s_pl)
    if letter == 'ź':
        return random.choice(Words.words_x_pl)
    if letter == 'ż':
        return random.choice(Words.words_z_pl)


def get_word_from_letter(row, column, length):
    letter = input_boxes[row][column].secret_text
    print(letter)
    global special_chars
    if letter in special_chars:
        return False
    elif letter == '':
        return None
    else:
        letter = letter.lower()
        return get_word(eval(f'Words.words_{letter}'), length)


def get_random_word(length):
    word = None
    while word is None:
        letter = random.choice(string.ascii_lowercase)
        if letter not in ['q', 'v', 'x', 'y']:
            word = get_word(eval(f'Words.words_{letter}'), length)
    return word


def crossword_1():
    global crossword
    clear()
    final_word = get_random_word(18)
    place_word(input_boxes, 1, 10, final_word, True)
    input_boxes[1][10].add_number('', True)
    input_boxes[1][10].arrow_surface_vertical = NUMBER_FONT.render('', True, BLACK)
    for i in range(1, 19):
        input_boxes[i][10].color = GOLD
        input_boxes[i][10].final = True
    row = 1
    col = 10
    for letter_final in final_word:
        word_placed = False
        while word_placed is not True:
            if letter_final not in special_chars:
                word = get_random_word(random.randint(5, 10))
            else:
                word = get_word_special_chars(letter_final)
            for letter in word:
                if letter == letter_final:
                    column = col - int(word.index(letter_final))
                    if is_empty_simple(input_boxes, row, column, word, False) is True and add_definitions(word, False) is True:
                        place_word(input_boxes, row, column, word, False)
                        row += 1
                        word_placed = True
                        break
                    else:
                        continue
                else:
                    continue

    for i in range(len(input_boxes)):
        for box in input_boxes[i]:
            if box.secret_text == '':
                box.is_dead = True
    draw_definitions()
    loading(False)
    crossword = 1
    update_game_state()


def crossword_2():
    global crossword
    global special_chars
    clear()
    first_placed = False
    word_placed = False
    occupied_boxes = []
    words_horizontal = 0
    words_vertical = 0
    missed_letters = 0
    backwards_words = 0
    backwards_placed = False
    while not first_placed:
        row = random.randint(0, 1)
        col = random.randint(0, 1)
        z = bool(random.getrandbits(1))
        first_word = get_random_word(random.randint(6, 15))
        if add_definitions(first_word, z) is True:
            place_word(input_boxes, row, col, first_word, z)
            print(words_used)
            occupied_boxes = get_occupied_boxes(row, col, len(first_word), z)
            first_placed = True
            if z is True:
                words_vertical += 1
            else:
                words_horizontal += 1
            print(occupied_boxes)
    start_time = time.time()
    while not word_placed:
        print(len(occupied_boxes))
        print('missed letters= ',missed_letters)
        print('words vert= ', words_vertical)
        print('words hor= ', words_horizontal)
        if time.time() - start_time > 120:
            word_placed = True
            backwards_placed = True
        if words_horizontal == 15 and words_vertical == 15:
            word_placed = True
        if missed_letters > 8:
            backwards_placed = not backwards_placed
            print('idziemy backwards')
            while not backwards_placed:
                occupied_boxes_backwards = occupied_boxes
                if backwards_words == 1:
                    backwards_placed = True
                    break

                for box in occupied_boxes_backwards:
                    vert_empty_space = is_empty_backwards(input_boxes, box[0], box[1], True)
                    hor_empty_space = is_empty_backwards(input_boxes, box[0], box[1], False)
                    print('backwards words=',backwards_words)
                    if vert_empty_space >= 4 or hor_empty_space >= 4:
                        if vert_empty_space > hor_empty_space:
                            if is_empty(input_boxes, box[0], box[1], 'A', True):
                                print('znalazlo pionowo na', box)
                                length = vert_empty_space
                                add_def = True
                            else:
                                continue
                        if hor_empty_space > vert_empty_space:
                            if is_empty(input_boxes, box[0], box[1], 'A', False):
                                print('znalazlo poziomo na', box)
                                length = hor_empty_space
                                add_def = False
                            else:
                                continue

                        word = get_random_word(random.randint(4, length)).upper()
                        if word[-1] == input_boxes[box[0]][box[1]].secret_text and add_definitions(word, add_def):
                            if vert_empty_space > hor_empty_space:
                                place_word(input_boxes, box[0] - len(word) + 1, box[1], word, True)
                                backwards_words += 1

                            else:
                                place_word(input_boxes, box[0], box[1] - len(word) + 1, word, False)
                                backwards_words += 1
                    else:
                        print('nie pasuje nigdzie')
                break
            missed_letters = 0
            backwards_words = 0

        else:
            box = random.choice(occupied_boxes)
            if input_boxes[box[0]][box[1]].secret_text in special_chars:
                continue
            else:
                word = get_word_from_letter(box[0], box[1], random.randint(5, 12))
                print(word, box)
                print(missed_letters)
                print('poziomo: ',is_empty(input_boxes, box[0], box[1], word, False))
                print('pionowo: ',is_empty(input_boxes, box[0], box[1], word, True))
                if is_empty(input_boxes, box[0], box[1], word, False) is True:
                    print(f'weszlo na {box[0], box[1]} poziomo')
                    if add_definitions(word, False) is True:
                        place_word(input_boxes, box[0], box[1], word, False)
                        missed_letters = 0
                        words_horizontal += 1
                        temp = get_occupied_boxes(box[0], box[1], len(word), False)
                        for i in temp:
                            occupied_boxes.append(i)

                    # word_placed = True
                elif is_empty(input_boxes, box[0], box[1], word, True) is True:
                    print(f'weszlo na {box[0], box[1]} pionowo')
                    if add_definitions(word, True) is True:
                        place_word(input_boxes, box[0], box[1], word, True)
                        missed_letters = 0
                        words_vertical += 1
                        temp = get_occupied_boxes(box[0], box[1], len(word), True)
                        for i in temp:
                            occupied_boxes.append(i)

                else:
                    print('nie pasuje nigdzie?!')
                    missed_letters += 1
                # word_placed = True
            print(occupied_boxes)
    # while not word_placed:
    for i in range(len(input_boxes)):
        for box in input_boxes[i]:
            if box.secret_text == '':
                box.is_dead = True
    draw_definitions()
    loading(False)
    crossword = 2
    update_game_state()


def get_occupied_boxes(row, col, length, is_vertical):
    coords = []
    if is_vertical:
        for i in range(1, length):
            coords.append([row + i, col])
        return coords
    if not is_vertical:
        for i in range(1, length):
            coords.append([row, col + i])
        return coords


def clear():
    global input_boxes
    global vertical_number
    global horizontal_number
    global words_used
    global words_used_vertical
    global definitions
    global crossword
    SCREEN.blit(BACKGROUND, (0, 0))
    input_boxes = []
    draw_grid(20, 20)
    vertical_number = 1
    horizontal_number = 1
    words_used = {}
    words_used_vertical = {}
    definitions = []
    crossword = 0


def add_definitions(word, is_vertical):
    value = scrape_definitions(word)
    if not value:
        return False
    else:
        if not is_vertical:
            words_used.update({word: value})
            return True
        else:
            words_used_vertical.update({word: value})
            return True


def draw_headers():
    if crossword == 1:
        horizontal_header = FONT.render('Poziomo:', True, BLACK)
        SCREEN.blit(horizontal_header, (900, 30))
    if crossword == 2:
        horizontal_header = FONT.render('Poziomo:', True, BLACK)
        vertical_header = FONT.render('Pionowo:', True, BLACK)
        SCREEN.blit(horizontal_header, (900, 30))
        SCREEN.blit(vertical_header, (1500, 30))


def draw_definitions():
    x = 900
    y = 70
    vertical_y = 70
    vertical_x = 1350
    spacing = 55
    button_size = 30
    elevation = 2
    number = 1
    number_vertical = 1
    for word in words_used:
        if number > 15:
            Definition(vertical_x, vertical_y, button_size, button_size, elevation, number, word, words_used)
            vertical_y += spacing
            number += 1
        else:
            Definition(x, y, button_size, button_size, elevation, number, word, words_used)
            y += spacing
            number += 1
    for word in words_used_vertical:
        Definition(vertical_x, vertical_y, button_size, button_size, elevation, number_vertical, word, words_used_vertical)
        vertical_y += spacing
        number_vertical += 1
    for d in definitions:
        d.calc_def()
    loading(False)
    update_game_state()
    global show_definitions
    show_definitions = True


def update_game_state():
    SCREEN.blit(BACKGROUND, (0, 0))
    draw_buttons()
    for d in definitions:
        d.draw_def()
        d.draw()
    draw_headers()


button0 = Button(125, 810, 150, 75, 4, 'Crossword #1', 0)
button1 = Button(325, 810, 150, 75, 4, 'Crossword #2', 1)
button2 = Button(525, 810, 150, 75, 4, 'Show answers', 2)
def draw_buttons():
    for b in buttons:
        b.draw()


def loading(play_animation):
    global loaded
    if play_animation:
        loaded = False
    if not play_animation:
        loaded = True


def debug():
    for i in range(len(input_boxes)):
        for box in input_boxes[i]:
            box.reveal_text()


def main():
    clock = pg.time.Clock()
    draw_grid(20, 20)
    done = False

    while not done:
        if loaded is False:
            update_game_state()
            moving_sprites.draw(SCREEN)
            moving_sprites.update(0.5)
            loading_text = LOADING_FONT.render(loading_icon.text, True, BLACK)
            SCREEN.blit(loading_text, loading_icon.text_pos)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for i in range(len(input_boxes)):
                for box in input_boxes[i]:
                    box.handle_event(event)
            for b in buttons:
                b.button_event()
                b.draw()

        if show_definitions:
            for d in definitions:
                d.draw()
                d.button_event()

        for i in range(len(input_boxes)):
            for box in input_boxes[i]:
                box.draw()

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()

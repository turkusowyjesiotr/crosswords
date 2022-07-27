import pygame as pg
from word_scraping import words_a, words_b, words_c, words_d, words_e, words_f, words_g, words_h, words_i, words_j, \
    words_k, words_l, words_m, words_n, words_o, words_p, words_r, words_s, words_t, words_u, words_w, words_z, \
    words_c_pl, words_o_pl, words_l_pl, words_s_pl, words_x_pl, words_z_pl, words_a_pl, words_e_pl, \
    words_n_pl
from definitions_scraping import scrape_definitions, quit_driver
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
special_chars = ['Ą', 'Ę', 'Ć', 'Ó', 'Ł', 'Ś', 'Ń', 'Ź', 'Ż']
# special_chars = ['ą', 'ę', 'ć', 'ó', 'ł', 'ś', 'ń', 'ź', 'ż']
buttons = []
definitions = []
crossword = 0
show_definitions = False
# words_used = {'seks': ['Lorem Ipsum is simply dummy text of the printing and typesetting Lorem Ipsum is simply dummy text of the printing and typesetting', 'Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.', 'dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa dupa', 'seks seks seks']}
words_used = {}
loaded = True
debug_mode = False
moving_sprites = pg.sprite.Group()
loading_icon = hourglass.Hourglass(1300, 400)
moving_sprites.add(loading_icon)


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
            debug()
            print(show_definitions)


class Definition(Button):
    def __init__(self, x, y, width, height, elevation, number, word_used, text='', button_type=4):
        # button
        super().__init__(x, y, width, height, elevation, text, button_type)
        img = pg.image.load('assets/images/load.png')
        img = pg.transform.smoothscale(img, (23, 23)).convert_alpha()
        self.btn_img = img

        # definition
        self.number = str(number) + '. '
        self.number_surface = DEF_FONT.render(self.number, True, BLACK)
        self.word_used = word_used
        self.definitions = words_used.get(self.word_used)
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
        self.def_surface = DEF_FONT.render(self.part1, True, BLACK)
        SCREEN.blit(self.def_surface, (self.pos_x + 2, self.pos_y + 2))
        self.def_surface = DEF_FONT.render(self.part2, True, BLACK)
        SCREEN.blit(self.def_surface, (self.pos_x + 2, self.pos_y + 15))
        self.def_surface = DEF_FONT.render(self.part3, True, BLACK)
        SCREEN.blit(self.def_surface, (self.pos_x + 2, self.pos_y + 27))

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
        # pg.draw.rect(SCREEN, self.border_color, self.def_rect, 2)
        # SCREEN.blit(self.number_surface, (self.pos_x - 15, self.pos_y + 2))
        line_spacing = 2
        if DEF_FONT.size(f'{self.definition}')[0] >= self.width*3:
            self.next_definition()
            self.calc_def()
        elif DEF_FONT.size(f'{self.definition}')[0] > self.width*2:
            # self.draw_def(self.wrap_def(), line_spacing)
            # line_spacing += 13
            # self.draw_def(self.wrap_def(), line_spacing)
            # line_spacing += 13
            # self.draw_def(self.wrap_def(), line_spacing)
            self.part1 = self.wrap_def()
            self.part1 = self.number + self.part1
            self.part2 = self.wrap_def()
            self.part3 = self.wrap_def()
        elif DEF_FONT.size(f'{self.definition}')[0] > self.width:
            # self.draw_def(self.wrap_def(), line_spacing)
            # line_spacing += 13
            # self.draw_def(self.wrap_def(), line_spacing)
            self.part1 = self.wrap_def()
            self.part1 = self.number + self.part1
            self.part2 = self.wrap_def()
            self.part3 = ''
        else:
            # self.draw_def(self.wrap_def(), line_spacing)
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
            # self.def_surface = DEF_FONT.render(self.definition, True, BLACK)
            # update_game_state()
            # time.sleep(0.1)
            # for d in definitions:
            #     d.calc_def()
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
                # self.color = BLUE if self.active else WHITE
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
# TODO: rozpisać sobie na kartce logikę is_empty, żeby sprawdzało czy po kolejnym boxie po słowie jest is_dead (jeśli tak, to umieść słowo) \
#  i żeby sprawdzało czy po bokach słowa nie ma innych słów \
#  i perhaps czy są jakieś przecinające się słówka

def is_empty_test(array, row, col, word, is_vertical: bool):
    if word is not None:
        length = len(word) + 1
        empty_boxes = 1
        if not is_vertical and col + length < len(array[row]):
            return True

        if is_vertical and row + length < len(array):
            return True

        else:
            return False


def is_empty(array, row, col, word, is_vertical: bool):
    if word is not None:
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


def get_word(array, length):
    array_sorted = sorted(array, key=len)
    found = False
    while found is not True:
        word = random.choice(array_sorted)
        if len(word) == length:
            return word


def get_word_special_chars(letter):
    if letter == 'ą':
        return random.choice(words_a_pl)
    if letter == 'ę':
        return random.choice(words_e_pl)
    if letter == 'ń':
        return random.choice(words_n_pl)
    if letter == 'ć':
        return random.choice(words_c_pl)
    if letter == 'ó':
        return random.choice(words_o_pl)
    if letter == 'ł':
        return random.choice(words_l_pl)
    if letter == 'ś':
        return random.choice(words_s_pl)
    if letter == 'ź':
        return random.choice(words_x_pl)
    if letter == 'ż':
        return random.choice(words_z_pl)


def get_word_from_letter(row, column, length):
    letter = input_boxes[row][column].text
    global special_chars
    if letter in special_chars:
        return None
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


def get_random_word(length):
    word = None
    while word is None:
        letter = random.choice(string.ascii_uppercase)
        if letter == 'A':
            word = get_word(words_a, length)
        if letter == 'B':
            word = get_word(words_b, length)
        if letter == 'C':
            word = get_word(words_c, length)
        if letter == 'D':
            word = get_word(words_d, length)
        if letter == 'E':
            word = get_word(words_e, length)
        if letter == 'F':
            word = get_word(words_f, length)
        if letter == 'G':
            word = get_word(words_g, length)
        if letter == 'H':
            word = get_word(words_h, length)
        if letter == 'I':
            word = get_word(words_i, length)
        if letter == 'J':
            word = get_word(words_j, length)
        if letter == 'K':
            word = get_word(words_k, length)
        if letter == 'L':
            word = get_word(words_l, length)
        if letter == 'M':
            word = get_word(words_m, length)
        if letter == 'N':
            word = get_word(words_n, length)
        if letter == 'O':
            word = get_word(words_o, length)
        if letter == 'U':
            word = get_word(words_u, length)
        if letter == 'P':
            word = get_word(words_p, length)
        if letter == 'R':
            word = get_word(words_r, length)
        if letter == 'S':
            word = get_word(words_s, length)
        if letter == 'T':
            word = get_word(words_t, length)
        if letter == 'U':
            word = get_word(words_u, length)
        if letter == 'W':
            word = get_word(words_w, length)
        if letter == 'Z':
            word = get_word(words_z, length)
    return word


def fill_the_grid():
    word = get_word(words_z, 15)
    place_word(input_boxes, 0, 0, word, False)
    place_word(input_boxes, 0, 0, get_word(words_z, 13), True)
    place_word(input_boxes, 0, 6, get_word_from_letter(0, 6, 10), True)
    place_word(input_boxes, 8, 6, get_word_from_letter(8, 6, 7), False)


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
                    if is_empty_test(input_boxes, row, column, word, False) is True and add_definitions(word) is True:
                        place_word(input_boxes, row, column, word, False)
                        row += 1
                        print(words_used)
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
    quit_driver()
    draw_definitions()
    loading(False)
    crossword = 1
    update_game_state()


def crossword_2():
    clear()
    first_placed = False
    while not first_placed:
        x = random.randint(0, 1)
        y = random.randint(0, 1)
        z = bool(random.getrandbits(1))
        first_word = get_random_word(random.randint(6, 15))
        if add_definitions(first_word) is True:
            place_word(input_boxes, x, y, first_word, z)
            first_placed = True
            print(words_used)
        else:
            continue
    quit_driver()
    loading(False)
    update_game_state()
    draw_definitions()


def clear():
    global input_boxes
    global vertical_number
    global horizontal_number
    global words_used
    global definitions
    SCREEN.blit(BACKGROUND, (0, 0))
    input_boxes = []
    draw_grid(20, 20)
    vertical_number = 1
    horizontal_number = 1
    words_used = {}
    definitions = []


def add_definitions(word):
    value = scrape_definitions(word)
    if not value:
        return False
    else:
        words_used.update({word: value})
        return True


def draw_headers():
    if crossword == 1:
        crossword1_header = FONT.render('Poziomo:', True, BLACK)
        SCREEN.blit(crossword1_header, (900, 30))
    if crossword == 2:
        crossword1_header = FONT.render('Poziomo:', True, BLACK)
        crossword2_header = FONT.render('Poziomo:', True, BLACK)
        SCREEN.blit(crossword1_header, (900, 30))
        SCREEN.blit(crossword2_header, (1500, 30))


def draw_definitions():
    x = 900
    y = 70
    original_y = 70
    spacing = 55
    button_size = 30
    elevation = 2
    number = 1
    for word in words_used:
        if number > 15:
            x = 1350
            Definition(x, original_y, button_size, button_size, elevation, number, word)
            original_y += spacing
            number += 1
        else:
            Definition(x, y, button_size, button_size, elevation, number, word)
            y += spacing
            number += 1

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
    # draw_definitions()


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

# TODO: dodać teraz scrapowanie definicji i tworzenie im obiektów klasy oraz żeby przypisywało każdej numerek

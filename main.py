import pygame as pg
from word_scraping import words_a, words_b, words_c, words_d, words_e, words_f, words_g, words_h, words_i, words_j, \
    words_k, words_l, words_m, words_n, words_o, words_p, words_r, words_s, words_t, words_u, words_w, words_z, \
    words_c_pl, words_o_pl, words_l_pl, words_s_pl, words_x_pl, words_z_pl, words_a_pl, words_e_pl, \
    words_n_pl
from definitions_scraping import scrape_definitions, quit_driver
import hourglass
import random
import string
import time
import threading


pg.init()
background = pg.image.load('assets/paper.jpg')
window_width = 1800
window_height = 900
screen = pg.display.set_mode((window_width, window_height))
grey = pg.Color(220, 220, 220)
white = pg.Color(255, 255, 255)
black = pg.Color(0, 0, 0)
blue = pg.Color(0, 191, 255)
pink = pg.Color(242, 233, 238)
dark_grey = pg.Color(90, 90, 90)
dark_grey_2 = pg.Color(170, 170, 170)
gold = pg.Color(235, 198, 52)
screen.fill(pink)
block_size = 40
screen.blit(background, (0, 0))
FONT = pg.font.Font('assets/arial_bold.ttf', 27)
BUTTON_FONT = pg.font.Font('assets/arial_bold.ttf', 20)
NUMBER_FONT = pg.font.Font('assets/arial.ttf', 12)
ARROW_FONT = pg.font.Font('assets/Symbola.ttf', 10)
DEF_FONT = pg.font.Font('assets/arial.ttf', 15)
LOADING_FONT = pg.font.Font('assets/arial_bold.ttf', 40)
horizontal_number = 1
vertical_number = 1
special_chars = ['Ą', 'Ę', 'Ć', 'Ó', 'Ł', 'Ś', 'Ń', 'Ź', 'Ż']
# special_chars = ['ą', 'ę', 'ć', 'ó', 'ł', 'ś', 'ń', 'ź', 'ż']
buttons = []
words_used = {}
# definitions = []
loaded = True
moving_sprites = pg.sprite.Group()
loading_icon = hourglass.Hourglass(1300, 400)
moving_sprites.add(loading_icon)


class Button:
    def __init__(self, x, y, width, height, elevation, text, button_type):
        self.rect = pg.Rect(x, y, width, height)
        self.bottom_rect = pg.Rect(x, y, width, height)
        self.elevation = elevation
        self.text = text
        self.text_surface = BUTTON_FONT.render(text, True, black)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.button_type = button_type
        self.color = grey
        self.bottom_color = dark_grey
        self.border_color = black
        self.original = y
        buttons.append(self)

    def update_text(self):
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def button_event(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = dark_grey_2
            if pg.mouse.get_pressed()[0]:
                self.rect.y = self.bottom_rect.y
                self.update_text()
                screen.blit(background, (0, 0))
                draw_buttons()
                self.generate_crossword()
            else:
                self.rect.y = self.original
                self.update_text()
        else:
            self.rect.y = self.original
            self.update_text()
            self.color = grey

    def draw(self):
        self.bottom_rect.y = self.original + self.elevation
        pg.draw.rect(screen, self.bottom_color, self.bottom_rect)
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, self.border_color, self.rect, 2)
        screen.blit(self.text_surface, self.text_rect)
    #TODO: TUTAJ JEST SYF, naucz się threadingu
    def generate_crossword(self):
        if self.button_type == 0:
            # loading(True)
            t = threading.Thread(target=loading2)
            d = threading.Thread(target=crossword_1)
            t.start()
            d.start()
        elif self.button_type == 1:
            loading(False)
        elif self.button_type == 2:
            # definicje_test()
            loading(True)


class Box:
    def __init__(self, x, y, size, row, column, text='', is_dead=False):
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
                # self.color = blue if self.active else white
                if self.final:
                    self.color = gold
                if not self.active and not self.final:
                    self.color = white
                if self.active:
                    self.color = blue
            if event.type == pg.KEYDOWN:
                not_active = [pg.K_RALT, pg.K_RIGHT, pg.K_LEFT, pg.K_DOWN, pg.K_BACKSPACE, pg.K_RETURN,
                              pg.K_UP, pg.K_LALT, pg.K_LCTRL, pg.K_RCTRL, pg.K_RSHIFT, pg.K_LSHIFT, pg.K_SPACE]
                if self.active:
                    if event.key == pg.K_RIGHT:
                        length = random.randint(3,10)
                        word = get_word_from_letter(self.row, self.column, length)
                        if is_empty(input_boxes, self.row, self.column, word, False):
                            place_word(input_boxes, self.row, self.column, word, False)
                    elif event.key == pg.K_DOWN:
                        length = random.randint(3,10)
                        word = get_word_from_letter(self.row, self.column, length)
                        if is_empty(input_boxes, self.row, self.column, word, True):
                            place_word(input_boxes, self.row, self.column, word, True)
                    elif event.key not in not_active and len(self.text) <= 1:
                        self.text = event.unicode
                        self.active = False
                        self.text = self.text.upper()
                        self.color = gold if self.final else white
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                self.txt_surface = FONT.render(self.text, True, black)

    def draw(self):
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

    def add_number(self, number, is_vertical):
        self.number = number
        self.number_surface = NUMBER_FONT.render(self.number, True, black)
        if is_vertical:
            self.arrow_surface_vertical = ARROW_FONT.render('\u25BC', True, black)
        else:
            self.arrow_surface_horizontal = ARROW_FONT.render('\u27A4', True, black)


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
#TODO: rozpisać sobie na kartce logikę is_empty, żeby sprawdzało czy po kolejnym boxie po słowie jest is_dead (jeśli tak, to umieść słowo)
# i żeby sprawdzało czy po bokach słowa nie ma innych słów
# i perhaps czy są jakieś przecinające się słówka

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
    clear()
    final_word = get_random_word(18)
    place_word(input_boxes, 1, 10, final_word, True)
    for i in range(1, 19):
        input_boxes[i][10].color = gold
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
                    # print(word)
                    # print(letter_final, word, 'to słowo pasuje')
                    # print('jest na miejscu', word.index(letter_final))
                    column = col - int(word.index(letter_final))
                    if is_empty_test(input_boxes, row, column, word, False) is True and add_definitions(word) is True:
                        place_word(input_boxes, row, column, word, False)
                        # print(word, ' umieszczone na literze ', letter_final, 'z kolumny: ', column, ' dlugosc: ', column + len(word))
                        row += 1
                        print(words_used)
                        word_placed = True
                        break
                    else:
                        # print(word, ' nie zmiescilo sie')
                        continue
                else:
                    continue

    for i in range(len(input_boxes)):
        for box in input_boxes[i]:
            if box.text == '':
                box.is_dead = True
    # quit_driver()
    loading(False)
    definicje_test()


def clear():
    global input_boxes
    global vertical_number
    global horizontal_number
    input_boxes = []
    draw_grid(20, 20)
    vertical_number = 1
    horizontal_number = 1

def definicje_test():
    draw_definitions()


def add_definitions(word):
    value = scrape_definitions(word)
    if value == []:
        return False
    else:
        words_used.update({word: value})
        return True


def draw_definitions():
    horizontal_x = 920
    vertical_x = 1420
    y = 30
    number = 1
    poziomo = FONT.render('Poziomo:', True, black)
    pionowo = FONT.render('Pionowo:', True, black)
    screen.blit(poziomo, (horizontal_x, y))
    screen.blit(pionowo, (vertical_x, y))
    for word in words_used:
        definitions_list = words_used.get(word)
        definition = definitions_list[0]
        if len(definition) > 55:
            def_part1 = definition[0:55] + '-'
            def_part2 = definition[55:]
            definition_text1 = DEF_FONT.render(f'{number}: ' + def_part1, True, black)
            definition_text2 = DEF_FONT.render('    ' + def_part2, True, black)
            screen.blit(definition_text1, (horizontal_x, y + 50))
            screen.blit(definition_text2, (horizontal_x, y + 66))
        else:
            definition_text = DEF_FONT.render(f'{number}: ' + definition, True, black)
            screen.blit(definition_text, (horizontal_x, y + 50))
        y += 35
        number += 1
        # time.sleep(10)


def update_game_state():
    screen.blit(background, (0, 0))
    draw_buttons()
    # draw_definitions()


button0 = Button(125, 810, 150, 75, 4, 'Crossword #1', 0)
button1 = Button(325, 810, 150, 75, 4, 'Sraka', 1)
button2 = Button(525, 810, 150, 75, 4, 'Clear', 2)
def draw_buttons():
    for b in buttons:
        b.draw()


def loading(play_animation: bool):
    global loaded
    if play_animation is True:
        loaded = False
    else:
        loaded = True
    update_game_state()


def loading2():
    global loaded
    loaded = False
    while loaded is False:
        update_game_state()
        moving_sprites.draw(screen)
        moving_sprites.update(0.5)
        loading_text = LOADING_FONT.render(loading_icon.text, True, black)
        screen.blit(loading_text, loading_icon.text_pos)
        time.sleep(1)


def main():
    clock = pg.time.Clock()
    draw_grid(20, 20)
    draw_buttons()
    done = False

    while not done:
        if loaded is False:
            update_game_state()
            moving_sprites.draw(screen)
            moving_sprites.update(0.5)
            loading_text = LOADING_FONT.render(loading_icon.text, True, black)
            screen.blit(loading_text, loading_icon.text_pos)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for i in range(len(input_boxes)):
                for box in input_boxes[i]:
                    box.handle_event(event)
            for b in buttons:
                b.button_event()
                b.draw()

        for i in range(len(input_boxes)):
            for box in input_boxes[i]:
                box.draw()

        pg.display.flip()
        clock.tick(30)



if __name__ == '__main__':
    main()
    pg.quit()

#TODO: dodać przycisk do debug mode, który będzie włączał dodawanie słów strzałkami

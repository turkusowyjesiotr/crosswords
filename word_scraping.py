from selenium import webdriver
import csv
from selenium.webdriver.common.by import By



alphabet = {'a': 8831, 'b': 10268, 'c': 7997, 'd': 9714, 'e': 3963, 'f': 4608, 'g': 6781, 'h': 4198, 'i': 3066, 'j': 3277, 'k': 16137,
            'l': 4962, 'm': 11647, 'n': 9430, 'o': 9040, 'p': 28125, 'r': 9007, 's': 18932, 't': 7975, 'u': 3696, 'w': 12958, 'z': 9366}
special_chars = {'ć': 128, 'ó': 15, 'ł': 1562, 'ś': 1620, 'ź': 56, 'ż': 1453}
def scrape_letter(dict, letter):
    word_list = []
    count = 0
    max_count = dict[letter]
    while count < max_count:
        driver = webdriver.Chrome('C:/Users/X/Desktop/chromedriver.exe')
        driver.get(f'http://wordlist.eu/slowa/na-litere,{letter}/{count}')
        elem = driver.find_elements(By.XPATH, '//html/body/div[1]/main/div/div/div[2]/div[1]/ul')
        elem_list = [el.text for el in elem]
        elem_list_clear = elem_list[0].split('\n')
        for word in elem_list_clear:
            if '-' not in word and '\'' not in word:
                word_list.append(word)
        driver.quit()
        count += 140
    with open('C:/Users/X/PycharmProjects/pythonProject/crosswords/special_chars.csv', "a", encoding='UTF8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(word_list)


# for key in alphabet:
#     scrape_letter(alphabet, key)
# for key in special_chars:
#     scrape_letter(special_chars, key)


input_special_chars = open('C:/Users/X/PycharmProjects/pythonProject/crosswords/special_chars.csv', "r", encoding='UTF8')
reader_special_chars = csv.reader(input_special_chars)
words_c_pl = next(reader_special_chars)
words_o_pl = next(reader_special_chars)
words_l_pl = next(reader_special_chars)
words_s_pl = next(reader_special_chars)
words_x_pl = next(reader_special_chars)
words_z_pl = next(reader_special_chars)

input_file = open('C:/Users/X/PycharmProjects/pythonProject/crosswords/words.csv', "r", encoding='UTF8')
reader_file = csv.reader(input_file)
words_a = next(reader_file)
words_b = next(reader_file)
words_c = next(reader_file)
words_d = next(reader_file)
words_e = next(reader_file)
words_f = next(reader_file)
words_g = next(reader_file)
words_h = next(reader_file)
words_i = next(reader_file)
words_j = next(reader_file)
words_k = next(reader_file)
words_l = next(reader_file)
words_m = next(reader_file)
words_n = next(reader_file)
words_o = next(reader_file)
words_p = next(reader_file)
words_r = next(reader_file)
words_s = next(reader_file)
words_t = next(reader_file)
words_u = next(reader_file)
words_w = next(reader_file)
words_z = next(reader_file)
print(len(words_a + words_b + words_c + words_d + words_e + words_f + words_g + words_h + words_i + words_j + words_k + words_l + words_m + words_n + words_o
          + words_p + words_r + words_s + words_t + words_u + words_w + words_z))


def check_words_length(array):
    array_sorted = sorted(array, key=len)
    first_word = array_sorted[0]
    last_word = array_sorted[-1]
    print(f'Shortest word is {first_word}, {len(first_word)} and longest word is {last_word}, {len(last_word)}')


aen_letters = ['ą', 'ę', 'ń']
words_with_aen = []
words_a_pl = []
words_e_pl = []
words_n_pl = []
with open('words.csv', 'r', encoding='UTF8') as file:
    reader = csv.reader(file)
    for row in reader:
        for word in row:
            for letter in word:
                if letter in aen_letters:
                    words_with_aen.append(word)
                    if letter == aen_letters[0]:
                        words_a_pl.append(word)
                    elif letter == aen_letters[1]:
                        words_e_pl.append(word)
                    else:
                        words_n_pl.append(word)


print(len(words_with_aen))
# get_word(words_a, 1)






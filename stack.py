import pygame as pg

dict1 = {'aa': [1, 2, 3], 'bb': [4, 5, 6]}
values = dict1.values()
x = dict1.get('aa')
print(x[1])


# import numpy as np
from selenium import webdriver
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

# driver = webdriver.Chrome('C:/Users/X/Desktop/chromedriver.exe')
# driver.get('http://wordlist.eu/slowa/na-litere,a')
# word = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[2]/div[1]/ul/li[1]/a')
# action = ActionChains(driver)
# action.context_click(word).perform()

# def test_function(array):
#     for i in range(3):
#         return array{i} =

#
# lst = [1, 2, 3]
# lst2 = [[0, 0, 0, 1, 2, 3], [0, 0, 0, 1, 2, 3], [0, 0, 0, 1, 2, 3]]
#
# # for i in range(len(lst2)-1):
# #     for element in lst2[i]:
# #         print(element)
#
# def is_empty(i, word):
#     length = len(word)
#     for i in range(length-1):
#         print(1)
#         print('i ruwna sie: ',i)
#
# is_empty(8, 'DAWN')
# # print('dlugosc lst', len(lst))
# # print(lst)
# # iteration = 0
# # while len(lst) != 0:
# #
# #     number = lst[0]
# #     for i in range(len(lst2)):
# #         for j in lst2[i]:
# #             if number != j:
# #                 print(f'{j} to nie {number}')
# #             elif number == j:
# #                 print(f'{j} jest na liście!')
# #                 lst.remove(number)
# #                 print(lst)
# #                 print('dlugosc lst', len(lst))
# #         break
# #
# #
# # print(lst2)
#
# # import pygame as pg
# #
# #
# # pg.init()
# # screen = pg.display.set_mode((640, 480))
# # COLOR_INACTIVE = pg.Color('lightskyblue3')
# # COLOR_ACTIVE = pg.Color('dodgerblue2')
# # FONT = pg.font.Font(None, 32)
# #
# #
# # class InputBox:
# #
# #     def __init__(self, x, y, w, h, text=''):
# #         self.rect = pg.Rect(x, y, w, h)
# #         self.color = COLOR_INACTIVE
# #         self.text = text
# #         self.txt_surface = FONT.render(text, True, self.color)
# #         self.active = False
# #
# #     def handle_event(self, event):
# #         if event.type == pg.MOUSEBUTTONDOWN:
# #             # If the user clicked on the input_box rect.
# #             if self.rect.collidepoint(event.pos):
# #                 # Toggle the active variable.
# #                 self.active = not self.active
# #             else:
# #                 self.active = False
# #             # Change the current color of the input box.
# #             self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
# #         if event.type == pg.KEYDOWN:
# #             if self.active:
# #                 if event.key == pg.K_RETURN:
# #                     print(self.text)
# #                     self.text = ''
# #                 elif event.key == pg.K_BACKSPACE:
# #                     self.text = self.text[:-1]
# #                 else:
# #                     self.text += event.unicode
# #                 # Re-render the text.
# #                 self.txt_surface = FONT.render(self.text, True, self.color)
# #
# #     def update(self):
# #         # Resize the box if the text is too long.
# #         width = max(200, self.txt_surface.get_width()+10)
# #         self.rect.w = width
# #
# #     def draw(self, screen):
# #         # Blit the text.
# #         screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
# #         # Blit the rect.
# #         pg.draw.rect(screen, self.color, self.rect, 2)
# #
# #
# #
# # def main():
# #     clock = pg.time.Clock()
# #     input_box1 = InputBox(100, 100, 140, 32)
# #     input_box2 = InputBox(100, 300, 140, 32)
# #     input_boxes = [input_box1, input_box2]
# #     done = False
# #
# #     while not done:
# #         for event in pg.event.get():
# #             if event.type == pg.QUIT:
# #                 done = True
# #             for box in input_boxes:
# #                 box.handle_event(event)
# #
# #         for box in input_boxes:
# #             box.update()
# #
# #         screen.fill((30, 30, 30))
# #         for box in input_boxes:
# #             box.draw(screen)
# #
# #         pg.display.flip()
# #         clock.tick(30)
# #
# #
# # if __name__ == '__main__':
# #     main()
# #     pg.quit()
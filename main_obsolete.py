# import pygame, sys
#
# buttons = []
# class Button:
# 	def __init__(self,text,width,height,pos,elevation):
# 		#Core attributes
# 		self.pressed = False
# 		self.elevation = elevation
# 		self.dynamic_elecation = elevation
# 		self.original_y_pos = pos[1]
#
# 		# top rectangle
# 		self.top_rect = pygame.Rect(pos,(width,height))
# 		self.top_color = '#475F77'
#
# 		# bottom rectangle
# 		self.bottom_rect = pygame.Rect(pos,(width,height))
# 		self.bottom_color = '#354B5E'
# 		#text
# 		self.text = text
# 		self.text_surf = gui_font.render(text,True,'#FFFFFF')
# 		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
# 		buttons.append(self)
#
# 	def change_text(self, newtext):
# 		self.text_surf = gui_font.render(newtext, True,'#FFFFFF')
# 		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
#
# 	def draw(self):
# 		# elevation logic
# 		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
# 		self.text_rect.center = self.top_rect.center
#
# 		self.bottom_rect.midtop = self.top_rect.midtop
# 		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
#
# 		pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
# 		pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
# 		screen.blit(self.text_surf, self.text_rect)
# 		self.check_click()
#
# 	def check_click(self):
# 		mouse_pos = pygame.mouse.get_pos()
# 		if self.top_rect.collidepoint(mouse_pos):
# 			self.top_color = '#D74B4B'
# 			if pygame.mouse.get_pressed()[0]:
# 				self.dynamic_elecation = 0
# 				self.pressed = True
# 				self.change_text(f"{self.text}")
# 			else:
# 				self.dynamic_elecation = self.elevation
# 				if self.pressed == True:
# 					print('click')
# 					self.pressed = False
# 					self.change_text(self.text)
# 		else:
# 			self.dynamic_elecation = self.elevation
# 			self.top_color = '#475F77'
#
# pygame.init()
# screen = pygame.display.set_mode((500,500))
# pygame.display.set_caption('Gui Menu')
# clock = pygame.time.Clock()
# gui_font = pygame.font.Font(None,30)
#
# button1 = Button('Rome',200,40,(100,200),5)
# button2 = Button('Milan',200,40,(100,250),5)
# button3 = Button('Neaples',200,40,(100,300),5)
#
#
# def buttons_draw():
# 	for b in buttons:
# 		b.draw()
#
# while True:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			pygame.quit()
# 			sys.exit()
#
# 	screen.fill('#DCDDD8')
# 	buttons_draw()
#
# 	pygame.display.update()
# 	clock.tick(60)
#
#
# word_list = {
#     'saffron': 'saffron definition',
#     # 'pumpernickel': 'pumpernickel definition',
#     'leaven': 'leaven definition',
#     'pummel': 'pump definition',
#     'x': 'x def',
#     'coda': 'coda definition',
#     'paladin': 'paladin definition',
#     'syncopation': 'syncopation definition',
#     'albatross': 'albatross definition',
#     'harp': 'harp definition',
#     'piston': 'piston definition',
#     'caramel': 'caramel definition',
#     'coral': 'coral definition',
#     'dawn': 'dawn definition',
#     'pitch': 'pitch definition',
#     'fjord': 'fjord definition',
#     'lip': 'lip definition',
#     'lime': 'lime definition',
#     'mist': 'mist definition',
#     'plague': 'plague definition',
#     'yarn': 'yarn definition',
#     'snicker': 'snicker definition',
#     'nig': 'nig definition'
# }
#
# word_list = {k.upper(): v.upper() for k, v in word_list.items()}
# word_list_sorted = {}
#
# for k in sorted(word_list, key=len, reverse=True):
#     word_list_sorted[k] = word_list[k]
#
#
#
# definitions = []
#
# # fill the grid rec
# words = [*word_list_sorted]
# words_placed = []
# unused_words = []
# # words.pop(0)
# word_placed = False
# iteration = 0
# un_words = ['SYNCOPATION', 'SAFFRON', 'SNICKER', 'PISTON', 'PLAGUE', 'CORAL', 'PITCH', 'FJORD', 'CODA', 'HARP', 'LIME', 'YARN', 'ALBATROSS', 'X']
#
# def fill_the_grid_rec(word_list, array):
#     global word_placed
#     global iteration
#     words = word_list
#     next_word = 0
#     print(words)
#     if len(words) == 0:
#         print('All words were placed')
#     else:
#         word = words[next_word]
#         print(f'current word: {word}')
#         for i in range(len(array)):
#             for box in array[i]:
#                 row = i
#                 col = array[i].index(box)
#                 if word[0] == box.text:
#                     if is_empty(array, row, col, word, False):
#                         place_word(array, row, col, word, False)
#                         print(f'{word} placed pionowo')
#                         word_placed = True
#                         break
#                     elif is_empty(array, row, col, word, True):
#                         place_word(array, row, col, word, True)
#                         print(f'{word} placed poziomo')
#                         word_placed = True
#                         break
#             if word_placed:
#                 break
#
#         if not word_placed:
#             print(f'{word} nie pasuje nigdzie')
#             unused_words.append(word)
#             words.remove(word)
#         if word_placed:
#             words.remove(word)
#             words_placed.append(word)
#             word_placed = False
#         return fill_the_grid_rec(word_list, array)
# # def fill_the_grid_np(word_list, array):
# #     words = [*word_list]
# #     iteration = 0
# #     place_word(array, 0, 0, words[0], True)
# #     words.pop(0)
# #     max_iteration = len(words)
# #     word_placed = False
# #     while iteration < max_iteration:
# #         word = words[iteration]
# #         for box in array.flat:
# #             result = np.where(array == box)
# #             result_lst = list(zip(result[0], result[1]))
# #             print(result_lst)
# #             if word[0] == box.text:
# #                 if is_empty(array, result[0], result[1], word, True):
# #                     place_word(array, result_lst[0], result_lst[1], word, True)
# #                     word_placed = True
# #                     break
# #                 elif is_empty(array, result[0], result[1], word, False):
# #                     place_word(array, result[0], result[1], word, False)
# #                     word_placed = True
# #                     break
# #             if word_placed:
# #                 break
# #         iteration += 1
# # def fill_the_grid_exp(word_list, array):
# #     words = [*word_list]
# #     iteration = 0
# #     place_word(0, 0, words[0], True)
# #     words.pop(0)
# #     max_iteration = len(words)
# #     print(len(words))
# #     print(words)
# #     box_count = 0
# #     word_placed = False
# #     for j in range(max_iteration):
# #
# #         print(f'{iteration} przed for word')
# #         word = words[j]
# #         print(f'{word} - zaczynamy z tym slowem')
# #         for i in range(len(input_boxes)):
# #             for box in input_boxes[i]:
# #                 # print(f'{iteration} po box in input_boxes')
# #                 row = i
# #                 col = input_boxes[i].index(box)
# #                 if word[0] == box.text:
# #                     if is_empty(row, col, word, False) is True:
# #                         place_word(row, col, word, False)
# #                         # iteration += 1
# #                         word_placed = True
# #                         print(f'{iteration} w 1. is_empty')
# #                         print(f'{word} placed poziomo na koordynatach row:{row} col:{col}')
# #                         # words.remove(word)
# #                         break
# #
# #                     elif is_empty(row, col, word, True) is True:
# #                         place_word(row, col, word, True)
# #                         # iteration += 1
# #                         word_placed = True
# #                         print(f'{iteration} w 2. is_empty')
# #                         print(f'{word} placed pionowo na koordynatach row:{row} col:{col}')
# #                         # words.remove(word)
# #                         break
# #
# #                     else:
# #                         if is_empty(row, col, word, False) is False:
# #                             print(f'{word} pierwsza litera pasuje, ale nie da sie dopasowac slowa (poziomo)')
# #                             print(f'{iteration} w is_empty else')
# #                         if is_empty(row, col, word, True) is False:
# #                             print(f'{word} pierwsza litera pasuje, ale nie da sie dopasowac slowa (pionowo)')
# #                             print(f'{iteration} w is_empty else')
# #                         # continue
# #                 if word_placed:
# #                     break
# #
# #             if word_placed:
# #                 break
# #         if not word_placed:
# #             print(f'{word} nie pasuje nigdzie')
# #         if word_placed:
# #             print(f'{word} was placed')
# #         iteration += 1
# #         word_placed = False
# #
# #         # print(f'{word} nie pasuje nigdzie')
# #         # iteration += 1
# #
# # def fill_the_grid(word_list):
# #     words = [*word_list]
# #     empty_boxes = 1
# #     print(words)
# #     place_word(0, 0, words[0], False)
# #     words.pop(0)
# #     print(words)
# #     box_count = 0
# #     iteration = 0
# #     max_iteration = len(words)
# #     word_placed = False
# #
# #     while iteration != max_iteration:
# #         word = words[iteration]
# #         for i in range(len(input_boxes)):
# #             for box in input_boxes[i]:
# #                 index = input_boxes[i].index(box)
# #                 if word[0] == box.text:
# #                     for letter in range(len(word) - 1):
# #
# #                         if input_boxes[i][index + 1].text == '' and input_boxes[i][index + 1].is_dead == False:
# #                             empty_boxes += 1
# #                             print(word + ' pasuje poziomo')
# #                             if empty_boxes == len(word):
# #                                 place_word(i, input_boxes[i].index(box), word, True)
# #                                 empty_boxes = 1
# #                                 word_placed = True
# #                                 print(iteration)
# #                                 print(f'{word} placed')
# #                                 print(words)
# #                                 # iteration += 1
# #                                 break
# #
# #
# #                         elif input_boxes[i + 1][index].text == '' and input_boxes[i + 1][index].is_dead == False:
# #                             empty_boxes += 1
# #                             print(word + ' pasuje pionowo')
# #                             if empty_boxes == len(word):
# #                                 place_word(i, input_boxes[i].index(box), word, False)
# #                                 word_placed = True
# #                                 print(iteration)
# #                                 print(f'{word} placed')
# #                                 print(words)
# #                                 # iteration += 1
# #                                 break
# #
# #
# #                         else:
# #                             print(f'{word} nie pasuje nigdzie')
# #                     if word_placed:
# #                         break
# #
# #                 else:
# #                     box_count += 1
# #             # if word_placed:
# #             #     break
# #         # if word_placed:
# #         #     break
# #         print(f'{word} nie pasuje box numer {box_count}')
# #         iteration += 1
# #         print(iteration)
# #         box_count = 0
# #
# #
# #
# #     # empty_boxes = 1
# #     # word_placed = False
# #     # word, definition = word_list.popitem()
# #     # place_word(0, 0, word, False)
# #     # definitions.append(definition)
# #     # print(word_list)
# #     # keys = [*word_list]
# #     # print(keys)
# #     # while len(keys) > 0:
# #     #     while word_placed != True:
# #     #         for item in keys:
# #     #             word = item
# #     #             for i in range(len(input_boxes)):
# #     #                 for box in input_boxes[i]:
# #     #                     index = input_boxes[i].index(box)
# #     #                     if word[0] == box.text:
# #     #                         for letter in range(len(word)):
# #     #                             if input_boxes[i][index + 1].text == '':
# #     #                                 empty_boxes += 1
# #     #                                 if empty_boxes == len(word):
# #     #                                     print(empty_boxes)
# #     #                                     place_word(i, input_boxes[i].index(box), word, True)
# #     #                                     empty_boxes = 1
# #     #                                     print(word_list_sorted)
# #     #                                     word_placed = True
# #     #                                     keys.pop(keys.index(item))
# #     #
# #     #
# #     #                             elif input_boxes[i+1][index].text == '':
# #     #                                 empty_boxes += 1
# #     #                                 if empty_boxes == len(word):
# #     #                                     place_word(i, input_boxes[i].index(box), word, False)
# #     #                                     empty_boxes = 1
# #     #                                     word_placed = True
# #     #                                     keys.pop(keys.index(item))
# #
# #
# #                     # place_word(i, input_boxes[i].index(box), word, False)
# #
# #
# # def fill_the_grid_test(word_list, array):
# #     words = [*word_list]
# #     iteration = 0
# #     place_word(array, 0, 0, words[0], True)
# #     words.pop(0)
# #     max_iteration = len(words)
# #     print(len(words))
# #     print(words)
# #     box_count = 0
# #     word_placed = False
# #     # while iteration <= max_iteration:
# #
# #     for i in range(len(words)):
# #         word = words[i]
# #         print(i)
# #         row = 0
# #         col = i
# #         place_word(array, row, col, word, True)
# #         print(f'{word} placed on {row}, {col}')
# #         # iteration += 1
# #
# #             #     # print(f'{iteration} po box in input_boxes')
# #
# #             #     place_word(row, col, word, True)
# #             #     word_placed = True
# #             #     print(f'{word} placed')
# #             #     break
# #             # if word_placed:
# #             #     iteration += 1
# #             #     break
# #
# #         # iteration += 1
# #         # print(f'{iteration} iteration')
# # unused_words2 = []
# # def fill_the_grid_rec2(sluwka, array):
# #     global word_placed
# #     global iteration
# #     words = sluwka
# #     # print(words)
# #     if len(words) == 0:
# #         print('All words were placed')
# #     else:
# #         word = words[0]
# #         print(f'current word: {word}')
# #         for i in range(len(array)):
# #             for box in array[i]:
# #                 row = i
# #                 col = array[i].index(box)
# #                 if word[0] == box.text:
# #                     if is_empty(array, row, col, word, False):
# #                         place_word(array, row, col, word, False)
# #                         print(f'{word} placed pionowo')
# #                         word_placed = True
# #                         break
# #                     elif is_empty(array, row, col, word, True):
# #                         place_word(array, row, col, word, True)
# #                         print(f'{word} placed poziomo')
# #                         word_placed = True
# #                         break
# #             if word_placed:
# #                 break
# #         if word_placed:
# #             words.remove(word)
# #         if not word_placed:
# #             # print(f'{word} nie pasuje nigdzie')
# #             # unused_words2.append(word)
# #             words.remove(word)
# #
# #
# #         word_placed = False
# #         # words.remove(word)
# #         return fill_the_grid_rec(words, array)
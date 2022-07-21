import pygame as pg


class Hourglass(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprites = []
        for i in range(28):
            frame = pg.image.load(f'assets/hourglass/frame_{i}_delay-0.04s.gif')
            frame = pg.transform.scale(frame, (400, 400))
            self.sprites.append(frame)
        self.current_sprite = 0
        self.current_text = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.texts = ['GENERATING', 'GENERATING.', 'GENERATING..', 'GENERATING...']
        self.text = self.texts[self.current_text]
        self.text_pos = (x - 135, y + 190)

    def update(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        self.current_text += speed/7
        if int(self.current_text) >= len(self.texts):
            self.current_text = 0
        self.text = self.texts[int(self.current_text)]

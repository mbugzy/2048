import sys
from random import randint, choice

import pygame as pg

import scoresTable

pg.init()

font = pg.font.SysFont('arial', 30)


def paintBG(screen: pg.Surface, screenWidth: int, screenHeight: int, fieldSize: int, score: int):

    screen.fill((100, 100, 100))
    spacer = screenWidth / 9
    textSpacer = spacer
    pg.draw.rect(screen, (180, 180, 150),
                 (spacer, spacer / 3, screenWidth / 3, screenHeight / 6), 0, 5)
    pg.draw.rect(screen, (180, 180, 150),
                 (2 * spacer + screenWidth / 3, spacer / 3, screenWidth / 3, screenHeight / 6), 0, 5)

    spacer = 3
    square = (screenWidth - spacer * (fieldSize + 1)) / fieldSize
    # spacer = screenWidth / 30
    for i in range(fieldSize):
        for j in range(fieldSize):
            pg.draw.rect(screen, (150, 150, 150),
                         (spacer * (i + 1) + square * i, screenHeight / 5 + spacer * (j + 1) + square * j,
                          square, square), 0, 5)
    try:
        bestScore = scoresTable.getBest(fieldSize)
    except:
        bestScore = 0
    if bestScore < score:
        bestScore = score

    texts_and_positions = [
        ('Best Score:', (textSpacer, textSpacer / 3)),
        (str(bestScore), (textSpacer, textSpacer * 1.2)),
        ('Your Score:', (2 * textSpacer + screenWidth / 3, textSpacer / 3)),
        (str(score), (2 * textSpacer + screenWidth / 3, textSpacer * 1.2))
    ]

    for text, position in texts_and_positions:
        rendered_text = font.render(text, True, 'white')
        screen.blit(rendered_text, position)

    pg.display.flip()


class Field:
    def __init__(self, fieldSize):
        self.screenHeight = 500
        self.screenWidth = self.screenHeight / 5 * 4
        self.fieldSize = fieldSize
        self.matrix = [[0 for _ in range(fieldSize)] for __ in range(fieldSize)]
        self.spacer = 3
        self.numbersImages = {}
        for i in range(1, 11):
            self.numbersImages[2 ** i] = pg.image.load(f'sprites/{self.fieldSize}/{2 ** i}.png')
        pg.display.set_caption('2048')
        self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
        self.square = (self.screenWidth - self.spacer * (self.fieldSize + 1)) / self.fieldSize
        self.score = 0
        paintBG(self.screen, self.screenWidth, self.screenHeight, self.fieldSize, self.score)
        pg.display.flip()

    def has_zero(self):
        for row in self.matrix:
            if 0 in row:
                return True
        return False

    def has_same_neighbors(self):
        for i in range(self.fieldSize):
            for j in range(self.fieldSize):
                current = self.matrix[i][j]
                if current == 0:
                    continue
                if i != self.fieldSize - 1:
                    if self.matrix[i + 1][j] == current:
                        return True
                if j != self.fieldSize - 1:
                    if self.matrix[i][j + 1] == current:
                        return True
        return False

    def generate(self):
        i = randint(0, self.fieldSize - 1)
        j = randint(0, self.fieldSize - 1)
        while self.matrix[i][j] != 0:
            i = randint(0, self.fieldSize - 1)
            j = randint(0, self.fieldSize - 1)
        self.matrix[i][j] = choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        self.update()

    def update(self):
        paintBG(self.screen, self.screenWidth, self.screenHeight, self.fieldSize, self.score)
        for i in range(self.fieldSize):
            for j in range(self.fieldSize):
                if self.matrix[i][j] == 0:
                    continue
                self.screen.blit(self.numbersImages[self.matrix[i][j]],
                                 (self.spacer * (j + 1) + self.square * j,
                                  self.screenHeight / 5 + self.spacer * (i + 1) + self.square * i))
                # else:
                #     pg.draw.rect(self.screen, numbersColors[self.matrix[i][j]],
                #                  (self.spacer * (j + 1) + self.square * j,
                #                   self.screenHeight / 5 + self.spacer * (i + 1) + self.square * i,
                #                   self.square, self.square), 0, 5)

        # for x in self.matrix:
        #     print(x)
        pg.display.flip()

    def right(self):
        moved = False
        combined = [False for _ in range(self.fieldSize)]
        for _ in range(self.fieldSize):
            for row in self.matrix:
                for j in range(self.fieldSize - 2, -1, -1):
                    if row[j] == 0:
                        continue
                    if row[j + 1] == 0:
                        row[j + 1] = row[j]
                        row[j] = 0
                        moved = True
                    elif row[j + 1] == row[j] and not combined[j + 1] and not combined[j]:
                        row[j + 1] *= 2
                        row[j] = 0
                        self.score += row[j + 1]
                        moved = True
                        combined[j + 1] = True
        if moved: self.generate()

    def left(self):
        moved = False
        combined = [False for _ in range(self.fieldSize)]
        for _ in range(self.fieldSize):
            for row in self.matrix:
                for j in range(1, self.fieldSize):
                    if row[j] == 0:
                        continue
                    if row[j - 1] == 0:
                        row[j - 1] = row[j]
                        row[j] = 0
                        moved = True
                    elif row[j - 1] == row[j] and not combined[j - 1] and not combined[j]:
                        row[j - 1] *= 2
                        row[j] = 0
                        self.score += row[j - 1]
                        moved = True
                        combined[j - 1] = True
        if moved: self.generate()

    def up(self):
        moved = False
        combined = [[False for _ in range(self.fieldSize)] for __ in range(self.fieldSize)]
        for _ in range(self.fieldSize):
            for i in range(1, self.fieldSize):
                for j in range(self.fieldSize):
                    if self.matrix[i][j] == 0:
                        continue
                    if self.matrix[i - 1][j] == 0:
                        self.matrix[i - 1][j] = self.matrix[i][j]
                        self.matrix[i][j] = 0
                        moved = True
                    elif self.matrix[i - 1][j] == self.matrix[i][j] and not combined[i - 1][j] and not combined[i][j]:
                        self.matrix[i - 1][j] *= 2
                        self.matrix[i][j] = 0
                        self.score += self.matrix[i - 1][j]
                        moved = True
                        combined[i - 1][j] = True
        if moved: self.generate()

    def down(self):
        moved = False
        combined = [[False for _ in range(self.fieldSize)] for __ in range(self.fieldSize)]
        for _ in range(self.fieldSize):
            for i in range(self.fieldSize - 2, -1, -1):
                for j in range(self.fieldSize):
                    if self.matrix[i][j] == 0:
                        continue
                    if self.matrix[i + 1][j] == 0:
                        self.matrix[i + 1][j] = self.matrix[i][j]
                        self.matrix[i][j] = 0
                        moved = True
                    elif self.matrix[i + 1][j] == self.matrix[i][j] and not combined[i + 1][j] and not combined[i][j]:
                        self.matrix[i + 1][j] *= 2
                        self.matrix[i][j] = 0
                        self.score += self.matrix[i + 1][j]
                        moved = True
                        combined[i + 1][j] = True
        if moved: self.generate()

    def run(self):
        self.generate()
        self.generate()
        once = True
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.__init__(self.fieldSize)
                        self.run()
                    if event.key == pg.K_q:
                        pg.quit()
                        scoresTable.askSaveScore(self.score, self.fieldSize)
                        sys.exit()
                    if event.key == pg.K_s:
                        scoresTable.showScores(self.fieldSize)
            while self.has_same_neighbors() or self.has_zero():
                once = True
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        scoresTable.askSaveScore(self.score, self.fieldSize)
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RIGHT:
                            self.right()
                        elif event.key == pg.K_LEFT:
                            self.left()
                        elif event.key == pg.K_UP:
                            self.up()
                        elif event.key == pg.K_DOWN:
                            self.down()
                        elif event.key == pg.K_r:
                            self.__init__(self.fieldSize)
                            self.run()
                        elif event.key == pg.K_q:
                            pg.quit()
                            scoresTable.askSaveScore(self.score, self.fieldSize)
                            sys.exit()
                        elif event.key == pg.K_s:
                            scoresTable.showScores(self.fieldSize)
                        else:
                            continue
                    self.update()

            self.screen.blit(font.render('YOU LOST', True, "red"),
                             (self.screenWidth / 2 - 50, self.screenHeight / 2 - 5))
            pg.display.flip()
            if once:
                once = False
                scoresTable.askSaveScore(self.score, self.fieldSize)


if __name__ == '__main__':
    qwe = Field(3)
    qwe.run()

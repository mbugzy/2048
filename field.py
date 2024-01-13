import contextlib
import sys
from random import randint, choice

with contextlib.redirect_stdout(None):
    import pygame as pg

import scoresTable

pg.init()

font = pg.font.SysFont('arial', 30)


def arialFontGenerator(width, textLen):
    return pg.font.SysFont('arial', min(30, int(width / textLen * 2)))


def paintBG(screen: pg.Surface, screenWidth: int, screenHeight: int, fieldSize: int, score: int):
    screen.fill((100, 100, 100))
    spacer = screenWidth / 27
    textSpacer = spacer
    # Score info
    pg.draw.rect(screen, (180, 180, 150),
                 (spacer, spacer / 3, screenWidth / 3, screenHeight / 6), 0, 5)
    pg.draw.rect(screen, (180, 180, 150),
                 (2 * spacer + screenWidth / 3, spacer / 3, screenWidth / 3, screenHeight / 6), 0, 5)

    # Buttons
    pg.draw.rect(screen, (180, 180, 150),
                 (3 * spacer + 2 * screenWidth / 3, spacer / 3, screenWidth / 5, screenHeight / 18), 0, 5)
    pg.draw.rect(screen, (180, 180, 150),
                 (3 * spacer + 2 * screenWidth / 3, 2 * spacer / 3 + screenHeight / 18, screenWidth / 5,
                  screenHeight / 18), 0, 5)
    pg.draw.rect(screen, (180, 180, 150),
                 (3 * spacer + 2 * screenWidth / 3, spacer + 2 * screenHeight / 18, screenWidth / 5, screenHeight / 18),
                 0, 5)

    spacer = 3
    square = (screenWidth - spacer * (fieldSize + 1)) / fieldSize
    # spacer = screenWidth / 30
    for i in range(fieldSize):
        for j in range(fieldSize):
            pg.draw.rect(screen, (150, 150, 150),
                         (spacer * (i + 1) + square * i, screenHeight / 5 + spacer * (j + 1) + square * j,
                          square, square), 0, 5)
    try:
        bestScore = int(scoresTable.getBest(fieldSize))
    except ValueError:
        bestScore = 0
    if bestScore is None or bestScore == 'nan' or bestScore == 'NaN':
        bestScore = 0
    if bestScore < score:
        bestScore = score

    rendered_text = font.render('Best Score:', True, 'white')
    screen.blit(rendered_text, (textSpacer, textSpacer / 3))

    # Render and blit for bestScore
    rendered_text = arialFontGenerator(screenWidth / 3, len(str(bestScore))).render(str(bestScore), True, 'white')
    screen.blit(rendered_text, (textSpacer, textSpacer * 3))

    # Render and blit for 'Your Score:'
    rendered_text = font.render('Your Score:', True, 'white')
    screen.blit(rendered_text, (2 * textSpacer + screenWidth / 3, textSpacer / 3))

    # Render and blit for score
    rendered_text = arialFontGenerator(screenWidth / 3, len(str(score))).render(str(score), True, 'white')
    screen.blit(rendered_text, (2 * textSpacer + screenWidth / 3, textSpacer * 3))

    rendered_text = arialFontGenerator(screenWidth / 5, 6).render('Scores', True, 'white')
    screen.blit(rendered_text, (3 * textSpacer + 2 * screenWidth / 3, textSpacer / 3 - 3))

    rendered_text = arialFontGenerator(screenWidth / 5, 7).render('Restart', True, 'white')
    screen.blit(rendered_text, (3 * textSpacer + 2 * screenWidth / 3, 2 * textSpacer / 3 + screenHeight / 18))

    rendered_text = arialFontGenerator(screenWidth / 5, 4).render('Undo', True, 'white')
    screen.blit(rendered_text, (3 * textSpacer + 2 * screenWidth / 3, textSpacer + 2 * screenHeight / 18 - 6))
    pg.display.flip()


class Field:
    def __init__(self, fieldSize, load=True):
        self.screenHeight = 500
        self.screenWidth = self.screenHeight / 5 * 4
        self.fieldSize = fieldSize
        self.matrix = []
        self.matrix = [[0 for _ in range(fieldSize)] for __ in range(fieldSize)]
        self.score = 0
        self.prevScore = 0
        self.load = load
        if load:
            try:
                forLoad = open(scoresTable.resource_path(f'saves/{fieldSize}.txt'), 'r')
                for i in range(fieldSize):
                    a = forLoad.readline().split()
                    for j in range(fieldSize):
                        self.matrix[i][j] = int(a[j])
                self.score = int(forLoad.readline())
                if not self.has_same_neighbors() and not self.has_zero():
                    self.matrix = [[0 for _ in range(fieldSize)] for __ in range(fieldSize)]
                    self.score = 0

            except Exception:
                self.load = False
        self.prevMatrix = self.matrix.copy()
        self.spacer = 3
        colorsFirst = [('#EEE4DA', '#776E65'), ('#EEE1C9', '#776E65'), ('#F3B27A', '#FFFFFF'), ('#F69664', '#FFFFFF'),
                       ('#F77C5F', '#FFFFFF'), ('#F75F3B', '#FFFFFF'), ('#EDD073', '#FFFFFF'), ('#EDCC62', '#FFFFFF'),
                       ('#EDC850', '#FFFFFF'), ('#EDC53F', '#FFFFFF'), ('#EDC22E', '#FFFFFF')]
        self.colors = {}
        for i in range(1, fieldSize ** 2 + 1):
            if i > 11:
                self.colors[2 ** i] = ('black', 'white')
                continue
            self.colors[2 ** i] = colorsFirst[i - 1]
        # self.numbersImages = {}
        # for i in range(1, 11):
        #     self.numbersImages[2 ** i] = pg.image.load(
        #         scoresTable.resource_path(f'sprites/{self.fieldSize}/{2 ** i}.png'))
        pg.display.set_caption('2048')

        self.screen = pg.display.set_mode((self.screenWidth, self.screenHeight))
        self.square = (self.screenWidth - self.spacer * (self.fieldSize + 1)) / self.fieldSize
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
                # self.screen.blit(self.numbersImages[self.matrix[i][j]],
                #                  (self.spacer * (j + 1) + self.square * j,
                #                   self.screenHeight / 5 + self.spacer * (i + 1) + self.square * i))
                pg.draw.rect(self.screen, self.colors[self.matrix[i][j]][0],
                             (self.spacer * (j + 1) + self.square * j,
                              self.screenHeight / 5 + self.spacer * (i + 1) + self.square * i,
                              self.square, self.square), 0, 5)
                numberFont = pg.font.SysFont('roman', min(40, int(self.square / len(str(self.matrix[i][j])) * 2)))
                rendered_text = numberFont.render(str(self.matrix[i][j]), True, self.colors[self.matrix[i][j]][1])
                self.screen.blit(rendered_text, (
                    self.spacer * (j + 1) + self.square * j + self.square / 2 - rendered_text.get_width() / 2,
                    self.screenHeight / 5 + self.spacer * (
                            i + 1) + self.square * i + self.square / 2 - rendered_text.get_height() / 2))
        pg.display.flip()

    def right(self):
        moved = False
        combined = [[False for _ in range(self.fieldSize)] for __ in range(self.fieldSize)]
        for _ in range(self.fieldSize):
            for i in range(self.fieldSize):
                for j in range(self.fieldSize - 2, -1, -1):
                    if self.matrix[i][j] == 0:
                        continue
                    if self.matrix[i][j + 1] == 0:
                        self.matrix[i][j + 1] = self.matrix[i][j]
                        self.matrix[i][j] = 0
                        moved = True
                    elif self.matrix[i][j + 1] == self.matrix[i][j] and not combined[i][j + 1] and not combined[i][j]:
                        self.matrix[i][j + 1] *= 2
                        self.matrix[i][j] = 0
                        self.score += self.matrix[i][j + 1]
                        moved = True
                        combined[i][j + 1] = True
        # if moved: self.generate()
        return moved

    def left(self):
        moved = False
        combined = [[False for _ in range(self.fieldSize)] for __ in range(self.fieldSize)]
        for _ in range(self.fieldSize):
            for i in range(self.fieldSize):
                for j in range(1, self.fieldSize):
                    if self.matrix[i][j] == 0:
                        continue
                    if self.matrix[i][j - 1] == 0:
                        self.matrix[i][j - 1] = self.matrix[i][j]
                        self.matrix[i][j] = 0
                        moved = True
                    elif self.matrix[i][j - 1] == self.matrix[i][j] and not combined[i][j - 1] and not combined[i][j]:
                        self.matrix[i][j - 1] *= 2
                        self.matrix[i][j] = 0
                        self.score += self.matrix[i][j - 1]
                        moved = True
                        combined[i][j - 1] = True
        # if moved: self.generate()
        return moved

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
        # if moved: self.generate()
        return moved

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
        # if moved: self.generate()
        return moved

    def undo(self):
        self.matrix = [[j for j in i] for i in self.prevMatrix]
        self.score = self.prevScore
        self.update()

    def run(self):
        if not self.load:
            self.generate()
            self.generate()
        else:
            self.update()
        once = True
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.restart()
                    if event.key == pg.K_q:
                        self.quit()
                    if event.key == pg.K_s:
                        scoresTable.showScores(self.fieldSize)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0]:
                        pos = pg.mouse.get_pos()
                        if (3 * self.spacer + 2 * self.screenWidth / 3 < pos[0]
                                < 3 * self.spacer + 2 * self.screenWidth / 3 + self.screenWidth / 5):
                            if self.spacer / 3 < pos[1] < self.spacer / 3 + self.screenHeight / 18:
                                scoresTable.showScores(self.fieldSize)
                            if (2 * self.spacer / 3 + self.screenHeight / 18 < pos[1]
                                    < 2 * self.spacer / 3 + 2 * self.screenHeight / 18):
                                self.restart()
                            if (self.spacer + 2 * self.screenHeight / 18 < pos[1]
                                    < self.spacer + 2 * self.screenHeight / 18 + self.screenHeight / 18):
                                self.undo()
            while self.has_same_neighbors() or self.has_zero():
                once = True
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.quit()
                    if event.type == pg.KEYDOWN:
                        moved = False
                        tempMatrix = [[j for j in i] for i in self.matrix]
                        tempScore = self.score
                        if event.key == pg.K_RIGHT:
                            moved = self.right()
                        elif event.key == pg.K_LEFT:
                            moved = self.left()
                        elif event.key == pg.K_UP:
                            moved = self.up()
                        elif event.key == pg.K_DOWN:
                            moved = self.down()
                        elif event.key == pg.K_r:
                            self.restart()
                        elif event.key == pg.K_q:
                            self.quit()
                        elif event.key == pg.K_s:
                            scoresTable.showScores(self.fieldSize)
                        if moved:
                            self.prevMatrix = [[j for j in i] for i in tempMatrix]
                            self.prevScore = tempScore
                            self.generate()
                            self.update()
                        # self.update()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if pg.mouse.get_pressed()[0]:
                            pos = pg.mouse.get_pos()
                            if (3 * self.spacer + 2 * self.screenWidth / 3 < pos[0]
                                    < 3 * self.spacer + 2 * self.screenWidth / 3 + self.screenWidth / 5):
                                if self.spacer / 3 < pos[1] < self.spacer / 3 + self.screenHeight / 18:
                                    scoresTable.showScores(self.fieldSize)
                                if (2 * self.spacer / 3 + self.screenHeight / 18 < pos[1]
                                        < 2 * self.spacer / 3 + 2 * self.screenHeight / 18):
                                    self.restart()
                                if (self.spacer + 2 * self.screenHeight / 18 < pos[1]
                                        < self.spacer + 2 * self.screenHeight / 18 + self.screenHeight / 18):
                                    self.undo()

            self.screen.blit(font.render('YOU LOST', True, "red"),
                             (self.screenWidth / 2 - 50, self.screenHeight / 2 - 5))
            pg.display.flip()
            if once:
                once = False
                scoresTable.askSaveScore(self.score, self.fieldSize)

    def quit(self):
        with open(scoresTable.resource_path(f'saves/{self.fieldSize}.txt'), 'w') as file:
            for i in range(self.fieldSize):
                for j in range(self.fieldSize):
                    file.write(str(self.matrix[i][j]) + ' ')
                file.write('\n')
            file.write(str(self.score))
        pg.quit()
        scoresTable.askSaveScore(self.score, self.fieldSize)
        sys.exit()

    def restart(self):
        scoresTable.askSaveScore(self.score, self.fieldSize)
        self.__init__(self.fieldSize, False)
        self.run()


if __name__ == '__main__':
    qwe = Field(3)
    qwe.run()

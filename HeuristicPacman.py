import pygame
import math
from random import randrange
import random
import copy
import os
import xlsxwriter

BoardPath = "Assets/BoardImages/"
ElementPath = "Assets/ElementImages/"
TextPath = "Assets/TextImages/"
DataPath = "Assets/Data/"

pygame.init()

# 28 Across 31 Tall 1: Empty Space 2: Tic-Tak 3: Wall 4: Ghost safe-space 5: Special Tic-Tak
originalGameBoard = [
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,6,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,6,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3],
    [3,2,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3],
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,3,3,3,1,3,3,1,3,3,3,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3],
    [1,1,1,1,1,1,2,1,1,1,3,4,4,4,4,4,4,3,1,1,1,2,1,1,1,1,1,1], # Middle Lane Row: 14
    [3,3,3,3,3,3,2,3,3,1,3,4,4,4,4,4,4,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,1,1,1,1,1,1,1,1,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,3,3,3,3,3,2,3,3,1,3,3,3,3,3,3,3,3,1,3,3,2,3,3,3,3,3,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,2,3,3,3,3,2,3,3,3,3,3,2,3,3,2,3,3,3,3,3,2,3,3,3,3,2,3],
    [3,6,2,2,3,3,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,3,3,2,2,6,3],
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3],
    [3,3,3,2,3,3,2,3,3,2,3,3,3,3,3,3,3,3,2,3,3,2,3,3,2,3,3,3],
    [3,2,2,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,3,3,2,2,2,2,2,2,3],
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3],
    [3,2,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,3,3,3,3,3,3,3,3,3,2,3],
    [3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
]
gameBoard = copy.deepcopy(originalGameBoard)
spriteRatio = 3/2
square = 25 # Size of each unit square
spriteOffset = square * (1 - spriteRatio) * (1/2)
(width, height) = (len(gameBoard[0]) * square, len(gameBoard) * square) # Game screen
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
clock = pygame.time.Clock()
# pelletColor = (165, 93, 53)
pelletColor = (222, 161, 133)


class Game:
    def __init__(self, level, score):
        self.paused = True
        self.ghostUpdateDelay = 1
        self.ghostUpdateCount = 0
        self.pacmanUpdateDelay = 1
        self.pacmanUpdateCount = 0
        self.tictakChangeDelay = 10
        self.tictakChangeCount = 0
        self.ghostsAttacked = False
        self.highScore = 100000
        self.score = score
        self.level = level
        self.lives = 1
        self.won = False #psxrc6's code - determine if the player won or lost the game to write to the excel file
        self.ghosts = [Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 11.5, "blue", 1), Ghost(17.0, 13.5, "pink", 2), Ghost(17.0, 15.5, "orange", 3)]
        self.pacman = Pacman(26.0, 14.5, 1) # Center of Second Last Row
        self.Mspacman = Pacman(26.0, 11.5, 2) # psxrc6's code
        self.total = self.getCount()
        self.ghostScore = 200
        self.levels = [[350, 250], [150, 450], [150, 450], [0, 600]]
        random.shuffle(self.levels)
        # Level index and Level Progress
        self.ghostStates = [[1, 0], [0, 0], [1, 0], [0, 0]]
        index = 0
        for state in self.ghostStates:
            state[0] = randrange(2)
            state[1] = randrange(self.levels[index][state[0]] + 1)
            index += 1
        self.collected = 0
        self.started = False
        self.gameOver = False
        self.gameOverCounter = 0
        self.points = []
        self.pointsTimer = 10
        # Berry Spawn Time, Berry Death Time, Berry Eaten
        self.berryState = [200, 400, False]
        self.berryLocation = [20.0, 13.5]
        self.berries = ["tile080.png", "tile081.png", "tile082.png", "tile083.png", "tile084.png", "tile085.png", "tile086.png", "tile087.png"]
        self.berriesCollected = []
        self.levelTimer = 0
        self.berryScore = 100
        self.lockedInTimer = 100
        self.lockedIn = True
        self.extraLifeGiven = False
        self.musicPlaying = 0
        self.time = 0

    # Driver method: The games primary update method
    def update(self):
        # pygame.image.unload()
        #print(self.ghostStates)
        if self.gameOver:
            self.gameOverFunc()
            return
        if self.paused or not self.started:
            self.drawTilesAround(21, 10)
            self.drawTilesAround(21, 11)
            self.drawTilesAround(21, 12)
            self.drawTilesAround(21, 13)
            self.drawTilesAround(21, 14)
            self.drawReady()
            pygame.display.update()
            return

        self.levelTimer += 1
        self.ghostUpdateCount += 1
        self.pacmanUpdateCount += 1
        self.tictakChangeCount += 1
        self.ghostsAttacked = False
        self.time += 1

        if self.score >= 10000 and not self.extraLifeGiven:
            self.lives += 1
            self.extraLifeGiven = True

        # Draw tiles around ghosts and pacman
        self.clearBoard()
        for ghost in self.ghosts:
            if ghost.attacked:
                self.ghostsAttacked = True

        # Check if the ghost should chase pacman
        index = 0
        for state in self.ghostStates:
            state[1] += 1
            if state[1] >= self.levels[index][state[0]]:
                state[1] = 0
                state[0] += 1
                state[0] %= 2
            index += 1

        index = 0
        for ghost in self.ghosts:
            if not ghost.attacked and not ghost.dead and self.ghostStates[index][0] == 0:
                playerToFollow =  random.randint(0,1) #have a random chance of chasing either player # psxrc6's code
                if playerToFollow == 0: # psxrc6's code
                    ghost.target = [self.pacman.row, self.pacman.col]# psxrc6's code
                else:
                    ghost.target = [self.Mspacman.row, self.Mspacman.col]# psxrc6's code
            index += 1

        if self.levelTimer == self.lockedInTimer:
            self.lockedIn = False

        self.checkSurroundings
        for ghost in self.ghosts:
            ghost.update()
        self.ghostUpdateCount = 0

        if self.tictakChangeCount == self.tictakChangeDelay:
            #Changes the color of special Tic-Taks
            self.flipColor()
            self.tictakChangeCount = 0

        self.pacmanUpdateCount = 0
        self.pacman.update()
        self.Mspacman.update()
        self.pacman.col %= len(gameBoard[0])
        if self.pacman.row % 1.0 == 0 and self.pacman.col % 1.0 == 0:
            if gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 2:
                gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                self.score += 10
                self.collected += 1
                # Fill tile with black
                pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
            elif gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 5 or gameBoard[int(self.pacman.row)][int(self.pacman.col)] == 6:
                gameBoard[int(self.pacman.row)][int(self.pacman.col)] = 1
                self.collected += 1
                # Fill tile with black
                pygame.draw.rect(screen, (0, 0, 0), (self.pacman.col * square, self.pacman.row * square, square, square))
                self.score += 50
                self.ghostScore = 200
                for ghost in self.ghosts:
                    ghost.attackedCount = 0
                    ghost.setAttacked(True)
                    ghost.setTarget()
                    self.ghostsAttacked = True
        self.Mspacman.col %= len(gameBoard[0])
        if self.Mspacman.row % 1.0 == 0 and self.Mspacman.col % 1.0 == 0:
            if gameBoard[int(self.Mspacman.row)][int(self.Mspacman.col)] == 2:
                gameBoard[int(self.Mspacman.row)][int(self.Mspacman.col)] = 1
                self.score += 10
                self.collected += 1
                # Fill tile with black
                pygame.draw.rect(screen, (0, 0, 0), (self.Mspacman.col * square, self.Mspacman.row * square, square, square))
            elif gameBoard[int(self.Mspacman.row)][int(self.Mspacman.col)] == 5 or gameBoard[int(self.Mspacman.row)][int(self.Mspacman.col)] == 6:
                gameBoard[int(self.Mspacman.row)][int(self.Mspacman.col)] = 1
                self.collected += 1
                # Fill tile with black
                pygame.draw.rect(screen, (0, 0, 0), (self.Mspacman.col * square, self.Mspacman.row * square, square, square))
                self.score += 50
                self.ghostScore = 200
                for ghost in self.ghosts:
                    ghost.attackedCount = 0
                    ghost.setAttacked(True)
                    ghost.setTarget()
                    self.ghostsAttacked = True
        self.checkSurroundings()
        self.highScore = max(self.score, self.highScore)

        global running
        if self.collected == self.total:
            #print("You win", str(self.time/30))# psxrc6's code
            game.won = True
            #print(str(self.score))# psxrc6's code
            #print(str(self.lives))# psxrc6's code
            game.running = False
        self.softRender()

    # Render method
    def render(self):
        gameBoard = copy.deepcopy(originalGameBoard)
        screen.fill((0, 0, 0)) # Flushes the screen
        # Draws game elements
        currentTile = 0
        self.displayLives()
        self.displayScore()
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 3: # Draw wall
                    imageName = str(currentTile)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (square, square))

                    #Display image of tile
                    screen.blit(tileImage, (j * square, i * square, square, square))

                    # pygame.draw.rect(screen, (0, 0, 255),(j * square, i * square, square, square)) # (x, y, width, height)
                elif gameBoard[i][j] == 2: # Draw Tic-Tak
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//4)
                elif gameBoard[i][j] == 5: #Black Special Tic-Tak
                    pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)
                elif gameBoard[i][j] == 6: #White Special Tic-Tak
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)

                currentTile += 1
        # Draw Sprites
        for ghost in self.ghosts:
            ghost.draw()
        self.pacman.draw()
        self.Mspacman.draw()# psxrc6's code
        # Updates the screen
        pygame.display.update()


    def softRender(self):
        pointsToDraw = []
        for point in self.points:
            if point[3] < self.pointsTimer:
                pointsToDraw.append([point[2], point[0], point[1]])
                point[3] += 1
            else:
                self.points.remove(point)
                self.drawTilesAround(point[0], point[1])

        for point in pointsToDraw:
            self.drawPoints(point[0], point[1], point[2])

        # Draw Sprites
        for ghost in self.ghosts:
            ghost.draw()
        self.pacman.draw()
        self.Mspacman.draw()# psxrc6's code
        self.displayScore()
        self.displayBerries()
        self.displayLives()
        # for point in pointsToDraw:
        #     self.drawPoints(point[0], point[1], point[2])
        self.drawBerry()
        # Updates the screen
        pygame.display.update()
    def clearBoard(self):
            # Draw tiles around ghosts and pacman
            for ghost in self.ghosts:
                self.drawTilesAround(ghost.row, ghost.col)
            self.drawTilesAround(self.pacman.row, self.pacman.col)
            self.drawTilesAround(self.Mspacman.row, self.Mspacman.col)# psxrc6's code
            self.drawTilesAround(self.berryLocation[0], self.berryLocation[1])
            # Clears Ready! Label
            self.drawTilesAround(20, 10)
            self.drawTilesAround(20, 11)
            self.drawTilesAround(20, 12)
            self.drawTilesAround(20, 13)
            self.drawTilesAround(20, 14)

    def checkSurroundings(self):
        # Check if pacman got killed
        for ghost in self.ghosts:
            if self.touchingPacman(ghost.row, ghost.col) and not ghost.attacked:
                if self.lives == 1:
                    #print("You lose")
                    #print(self.time/30) # game played at 30fps
                    #self.gameOver = True
                    game.running = False
                    #Removes the ghosts from the screen
                    # for ghost in self.ghosts:
                    #     self.drawTilesAround(ghost.row, ghost.col)
                    # self.drawTilesAround(self.pacman.row, self.pacman.col)
                    # self.drawTilesAround(self.Mspacman.row, self.Mspacman.col)# psxrc6's code
                    # self.pacman.draw()
                    # self.Mspacman.draw()# psxrc6's code
                    # pygame.display.update()
                    # pause(10000000)
                    # return
                self.started = False
                #reset()
            elif self.touchingPacman(ghost.row, ghost.col) and ghost.isAttacked() and not ghost.isDead():
                ghost.setDead(True)
                ghost.setTarget()
                ghost.ghostSpeed = 1
                ghost.row = math.floor(ghost.row)
                ghost.col = math.floor(ghost.col)
                self.score += self.ghostScore
                self.points.append([ghost.row, ghost.col, self.ghostScore, 0])
                self.ghostScore *= 2
                #pause(10000000)
        if self.touchingPacman(self.berryLocation[0], self.berryLocation[1]) and not self.berryState[2] and self.levelTimer in range(self.berryState[0], self.berryState[1]):
            self.berryState[2] = True
            self.score += self.berryScore
            self.points.append([self.berryLocation[0], self.berryLocation[1], self.berryScore, 0])
            self.berriesCollected.append(self.berries[(self.level - 1) % 8])

    # Displays the current score
    def displayScore(self):
        textOneUp = ["tile033.png", "tile021.png", "tile016.png"]
        textHighScore = ["tile007.png", "tile008.png", "tile006.png", "tile007.png", "tile015.png", "tile019.png", "tile002.png", "tile014.png", "tile018.png", "tile004.png"]
        index = 0
        scoreStart = 5
        highScoreStart = 11
        for i in range(scoreStart, scoreStart+len(textOneUp)):
            tileImage = pygame.image.load(TextPath + textOneUp[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, (i * square, 4, square, square))
            index += 1
        score = str(self.score)
        if score == "0":
            score = "00"
        index = 0
        for i in range(0, len(score)):
            digit = int(score[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, ((scoreStart + 2 + index) * square, square + 4, square, square))
            index += 1

        index = 0
        for i in range(highScoreStart, highScoreStart+len(textHighScore)):
            tileImage = pygame.image.load(TextPath + textHighScore[index])
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, (i * square, 4, square, square))
            index += 1

        highScore = str(self.highScore)
        if highScore == "0":
            highScore = "00"
        index = 0
        for i in range(0, len(highScore)):
            digit = int(highScore[i])
            tileImage = pygame.image.load(TextPath + "tile0" + str(32 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square, square))
            screen.blit(tileImage, ((highScoreStart + 6 + index) * square, square + 4, square, square))
            index += 1

    def drawBerry(self):
        if self.levelTimer in range(self.berryState[0], self.berryState[1]) and not self.berryState[2]:
            # print("here")
            berryImage = pygame.image.load(ElementPath + self.berries[(self.level - 1) % 8])
            berryImage = pygame.transform.scale(berryImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(berryImage, (self.berryLocation[1] * square, self.berryLocation[0] * square, square, square))

    def drawPoints(self, points, row, col):
        pointStr = str(points)
        index = 0
        for i in range(len(pointStr)):
            digit = int(pointStr[i])
            tileImage = pygame.image.load(TextPath + "tile" + str(224 + digit) + ".png")
            tileImage = pygame.transform.scale(tileImage, (square//2, square//2))
            screen.blit(tileImage, ((col) * square + (square//2 * index), row * square - 20, square//2, square//2))
            index += 1

    def drawReady(self):
        ready = ["tile274.png", "tile260.png", "tile256.png", "tile259.png", "tile281.png", "tile283.png"]
        for i in range(len(ready)):
            letter = pygame.image.load(TextPath + ready[i])
            letter = pygame.transform.scale(letter, (int(square), int(square)))
            screen.blit(letter, ((11 + i) * square, 20 * square, square, square))

    def gameOverFunc(self):
        global running
        if self.gameOverCounter == 12:
            running = False
            self.recordHighScore()
            return

        # Resets the screen around pacman
        self.drawTilesAround(self.pacman.row, self.pacman.col)
        self.drawTilesAround(self.Mspacman.row, self.Mspacman.col)

        # Draws new image
        pacmanImage = pygame.image.load(ElementPath + "tile" + str(116 + self.gameOverCounter) + ".png")
        pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(pacmanImage, (self.pacman.col * square + spriteOffset, self.pacman.row * square + spriteOffset, square, square))
        pygame.display.update()
        #pause(5000000)
        self.gameOverCounter += 1

    def displayLives(self):
        # 33 rows || 28 cols
        # Lives[[31, 5], [31, 3], [31, 1]]
        livesLoc = [[34, 3], [34, 1]]
        for i in range(self.lives - 1):
            lifeImage = pygame.image.load(ElementPath + "tile054.png")
            lifeImage = pygame.transform.scale(lifeImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(lifeImage, (livesLoc[i][1] * square, livesLoc[i][0] * square - spriteOffset, square, square))

    def displayBerries(self):
        firstBerrie = [34, 26]
        for i in range(len(self.berriesCollected)):
            berrieImage = pygame.image.load(ElementPath + self.berriesCollected[i])
            berrieImage = pygame.transform.scale(berrieImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(berrieImage, ((firstBerrie[1] - (2*i)) * square, firstBerrie[0] * square + 5, square, square))

    def touchingPacman(self, row, col):
        if (row - 0.5 <= self.pacman.row and row >= self.pacman.row and col == self.pacman.col):
            return True
        elif (row + 0.5 >= self.pacman.row and row <= self.pacman.row and col == self.pacman.col):
            return True
        elif (row == self.pacman.row and col - 0.5 <= self.pacman.col and col >= self.pacman.col):
            return True
        elif (row == self.pacman.row and col + 0.5 >= self.pacman.col and col <= self.pacman.col): 
            return True
        elif (row == self.pacman.row and col == self.pacman.col): 
            return True
        if(row - 0.5 <= self.Mspacman.row and row >= self.Mspacman.row and col == self.Mspacman.col):# psxrc6's code:
            return True
        elif(row + 0.5 >= self.Mspacman.row and row <= self.Mspacman.row and col == self.Mspacman.col):# psxrc6's code)
            return True
        elif(row == self.Mspacman.row and col - 0.5 <= self.Mspacman.col and col >= self.Mspacman.col):# psxrc6's code:
            return True
        elif(row == self.Mspacman.row and col + 0.5 >= self.Mspacman.col and col <= self.Mspacman.col):# psxrc6's code: 
            return True
        elif(row == self.Mspacman.row and col == self.Mspacman.col):# psxrc6's code :
            return True
        return False

    def drawTilesAround(self, row, col):
        row = math.floor(row)
        col = math.floor(col)
        for i in range(row-2, row+3):
            for j in range(col-2, col+3):
                if i >= 3 and i < len(gameBoard) - 2 and j >= 0 and j < len(gameBoard[0]):
                    imageName = str(((i - 3) * len(gameBoard[0])) + j)
                    if len(imageName) == 1:
                        imageName = "00" + imageName
                    elif len(imageName) == 2:
                         imageName = "0" + imageName
                    # Get image of desired tile
                    imageName = "tile" + imageName + ".png"
                    tileImage = pygame.image.load(BoardPath + imageName)
                    tileImage = pygame.transform.scale(tileImage, (square, square))
                    #Display image of tile
                    screen.blit(tileImage, (j * square, i * square, square, square))

                    if gameBoard[i][j] == 2: # Draw Tic-Tak
                        pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//4)
                    elif gameBoard[i][j] == 5: #Black Special Tic-Tak
                        pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)
                    elif gameBoard[i][j] == 6: #White Special Tic-Tak
                        pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)

    # Flips Color of Special Tic-Taks
    def flipColor(self):
        global gameBoard
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 5:
                    gameBoard[i][j] = 6
                    pygame.draw.circle(screen, pelletColor,(j * square + square//2, i * square + square//2), square//2)
                elif gameBoard[i][j] == 6:
                    gameBoard[i][j] = 5
                    pygame.draw.circle(screen, (0, 0, 0),(j * square + square//2, i * square + square//2), square//2)

    def getCount(self):
        total = 0
        for i in range(3, len(gameBoard) - 2):
            for j in range(len(gameBoard[0])):
                if gameBoard[i][j] == 2 or gameBoard[i][j] == 5 or gameBoard[i][j] == 6:
                    total += 1
        return total

    def getHighScore(self):
        file = open(DataPath + "HighScore.txt", "r")
        highScore = int(file.read())
        file.close()
        return highScore

    def recordHighScore(self):
        file = open(DataPath + "HighScore.txt", "w").close()
        file = open(DataPath + "HighScore.txt", "w+")
        file.write(str(self.highScore))
        file.close()

class Pacman:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.mouthOpen = False
        self.pacSpeed = 1/2
        self.mouthChangeDelay = 5
        self.mouthChangeCount = 0
        self.dir = 0 # 0: North, 1: East, 2: South, 3: West
        self.newDir = 0
        self.player = player# psxrc6's code
        self.target = []
        self.lastLoc = [26,14]

    def update(self):
        self.lastLoc = [self.row, self.col]
        if self.newDir == 0:
            if canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 1:
            if canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 2:
            if canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
                self.dir = self.newDir
                return
        elif self.newDir == 3:
            if canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed
                self.dir = self.newDir
                return

        if self.dir == 0:
            if canMove(math.floor(self.row - self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row -= self.pacSpeed
        elif self.dir == 1:
            if canMove(self.row, math.ceil(self.col + self.pacSpeed)) and self.row % 1.0 == 0:
                self.col += self.pacSpeed
        elif self.dir == 2:
            if canMove(math.ceil(self.row + self.pacSpeed), self.col) and self.col % 1.0 == 0:
                self.row += self.pacSpeed
        elif self.dir == 3:
            if canMove(self.row, math.floor(self.col - self.pacSpeed)) and self.row % 1.0 == 0:
                self.col -= self.pacSpeed

    # Draws pacman based on his current state
    def draw(self):
        if not game.started:
            pacmanImage = pygame.image.load(ElementPath + "tile112.png")
            pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
            screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))
            return

        if self.mouthChangeCount == self.mouthChangeDelay:
            self.mouthChangeCount = 0
            self.mouthOpen = not self.mouthOpen
        self.mouthChangeCount += 1
        # pacmanImage = pygame.image.load("Sprites/tile049.png")
        if self.dir == 0:
            if self.player == 2:# psxrc6's code
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(ElementPath + "msp_up.png")# psxrc6's code
                else:
                    pacmanImage = pygame.image.load(ElementPath + "msp_up_closed.png")# psxrc6's code
            elif self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile049.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile051.png")
        elif self.dir == 1:
            if self.player == 2:# psxrc6's code
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(ElementPath + "msp_right.png")# psxrc6's code
                else:
                    pacmanImage = pygame.image.load(ElementPath + "msp_right_closed.png")# psxrc6's code
            elif self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile052.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile054.png")
        elif self.dir == 2:
            if self.player == 2:# psxrc6's code
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(ElementPath + "msp_down.png")# psxrc6's code
                else:
                    pacmanImage = pygame.image.load(ElementPath + "msp_down_closed.png")# psxrc6's code
            elif self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile053.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile055.png")
        elif self.dir == 3:
            if self.player == 2:# psxrc6's code
                if self.mouthOpen:
                    pacmanImage = pygame.image.load(ElementPath + "msp_left.png")# psxrc6's code
                else:
                    pacmanImage = pygame.image.load(ElementPath + "msp_left_closed.png")# psxrc6's code
            elif self.mouthOpen:
                pacmanImage = pygame.image.load(ElementPath + "tile048.png")
            else:
                pacmanImage = pygame.image.load(ElementPath + "tile050.png")

        pacmanImage = pygame.transform.scale(pacmanImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(pacmanImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    def calcDistance(self, a,b):
        dR = a[0] - b[0]
        dC = a[1] - b[1]
        return math.sqrt((dR * dR) + (dC * dC))

    def MoveToTarget(self):

        potentialMoves = [ [1, 0, self.pacSpeed],#how the direction will impact the position of pacman. i.e(0 will move pacman up so up the rows on the gameboard) 
                [3, 0, -self.pacSpeed],#position [0] is the direction to move in (0,1,2,3) 
                [2, self.pacSpeed, 0], #position [1] is the movement through the rows
                [0, -self.pacSpeed, 0]] #position [2] is the movement in the cols
                #in a BFS style, testing breadth before depth
        MinDistance = 10000
        bestMove = -1
        for newMove in potentialMoves:
            DistanceForNewMove = self.calcDistance(self.target, [self.row + newMove[1], self.col + newMove[2]]) #calculate the distance of the new move to the target
            if(DistanceForNewMove < MinDistance): #calculate if the distance will be less by doing this move

                if ((self.lastLoc[0] == self.row + newMove[1] and self.lastLoc[1] == self.col + newMove[2]) == False): #check if the new move will move the pacman back to its last location

                    if newMove[0] == 0: #test moving up
                        if self.validMove(math.floor(self.row + newMove[1]), int(self.col + newMove[2])): #check if its a valid move
                            bestMove = newMove[0] #set the new best move to up
                            MinDistance = DistanceForNewMove #update the minDistance by doing this move

                    elif newMove[0] == 1:
                        if self.validMove(int(self.row + newMove[1]), math.ceil(self.col + newMove[2])):
                            bestMove = newMove[0]#set the new best move to right
                            MinDistance = DistanceForNewMove

                    elif newMove[0] == 2:
                        if self.validMove(math.ceil(self.row + newMove[1]), int(self.col + newMove[2])):
                            bestMove = newMove[0]#set the new best move to down
                            MinDistance = DistanceForNewMove

                    elif newMove[0] == 3:
                        if self.validMove(int(self.row + newMove[1]), math.floor(self.col + newMove[2])):
                            bestMove = newMove[0]#set the new best move to left
                            MinDistance = DistanceForNewMove
        return bestMove

    def validMove(self, TestRow, TestCol):
        if TestRow < 0 or TestCol > len(gameBoard[0]) - 1:
            return True
        if gameBoard[TestRow][TestCol] == 3:
            return False #if its a wall then the move is not valid
        return True

    def FindNearestPowerPill(self):
        PacMinPillDistance = 10000
        for l in range(3, len(gameBoard) - 2):
                    for m in range(len(gameBoard[0])):
                        if gameBoard[l][m] == 6:
                            PacnewDist = self.calcDistance([l,m], [self.row, self.col])
                            if(PacnewDist < PacMinPillDistance):
                                powerPillOnMap = True
                                PacMinPillDistance = PacnewDist
                                self.target = [l,m]

    def FindNearestPill(self):
        PacMinPillDistance = 1000
        for l in range(3, len(gameBoard) - 2):
            for m in range(len(gameBoard[0])):
                if gameBoard[l][m] == 2:
                    PacnewDist = self.calcDistance([l,m], [self.row, self.col])
                    if(PacnewDist < PacMinPillDistance):
                        PacMinPillDistance = PacnewDist
                        self.target = [l,m]

class Ghost:
    def __init__(self, row, col, color, changeFeetCount):
        self.row = row
        self.col = col
        self.attacked = False
        self.color = color
        self.dir = randrange(4)
        self.dead = False
        self.changeFeetCount = changeFeetCount
        self.changeFeetDelay = 5
        self.target = [-1, -1]
        self.ghostSpeed = 1/2
        self.lastLoc = [-1, -1]
        self.attackedTimer = 240
        self.attackedCount = 0
        self.deathTimer = 120
        self.deathCount = 0

    def update(self):
        # print(self.row, self.col)
        if self.target == [-1, -1] or (self.row == self.target[0] and self.col == self.target[1]) or gameBoard[int(self.row)][int(self.col)] == 4 or self.dead:
            self.setTarget()
        self.setDir()
        self.move()

        if self.attacked:
            self.attackedCount += 1

        if self.attacked and not self.dead:
            self.ghostSpeed = 1/4

        if self.attackedCount == self.attackedTimer and self.attacked:
            if not self.dead:
                self.ghostSpeed = 1/2
                self.row = math.floor(self.row)
                self.col = math.floor(self.col)

            self.attackedCount = 0
            self.attacked = False
            self.setTarget()

        if self.dead and gameBoard[self.row][self.col] == 4:
            self.deathCount += 1
            self.attacked = False
            if self.deathCount == self.deathTimer:
                self.deathCount = 0
                self.dead = False
                self.ghostSpeed = 1/2

    def draw(self): # Ghosts states: Alive, Attacked, Dead Attributes: Color, Direction, Location
        ghostImage = pygame.image.load(ElementPath + "tile152.png")
        currentDir = ((self.dir + 3) % 4) * 2
        if self.changeFeetCount == self.changeFeetDelay:
            self.changeFeetCount = 0
            currentDir += 1
        self.changeFeetCount += 1
        if self.dead:
            tileNum = 152 + currentDir
            ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
        elif self.attacked:
            if self.attackedTimer - self.attackedCount < self.attackedTimer//3:
                if (self.attackedTimer - self.attackedCount) % 31 < 26:
                    ghostImage = pygame.image.load(ElementPath + "tile0" + str(70 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
                else:
                    ghostImage = pygame.image.load(ElementPath + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
            else:
                ghostImage = pygame.image.load(ElementPath + "tile0" + str(72 + (currentDir - (((self.dir + 3) % 4) * 2))) + ".png")
        else:
            if self.color == "blue":
                tileNum = 136 + currentDir
                ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
            elif self.color == "pink":
                tileNum = 128 + currentDir
                ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
            elif self.color == "orange":
                tileNum = 144 + currentDir
                ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")
            elif self.color == "red":
                tileNum = 96 + currentDir
                if tileNum < 100:
                    ghostImage = pygame.image.load(ElementPath + "tile0" + str(tileNum) + ".png")
                else:
                    ghostImage = pygame.image.load(ElementPath + "tile" + str(tileNum) + ".png")

        ghostImage = pygame.transform.scale(ghostImage, (int(square * spriteRatio), int(square * spriteRatio)))
        screen.blit(ghostImage, (self.col * square + spriteOffset, self.row * square + spriteOffset, square, square))

    def isValidTwo(self, cRow, cCol, dist, visited):
        if cRow < 3 or cRow >= len(gameBoard) - 5 or cCol < 0 or cCol >= len(gameBoard[0]) or gameBoard[cRow][cCol] == 3:
            return False
        elif visited[cRow][cCol] <= dist:
            return False
        return True

    def isValid(self, cRow, cCol):
        if cCol < 0 or cCol > len(gameBoard[0]) - 1:
            return True
        for ghost in game.ghosts:
            if ghost.color == self.color:
                continue
            if ghost.row == cRow and ghost.col == cCol and not self.dead:
                return False
        if not ghostGate.count([cRow, cCol]) == 0:
            if self.dead and self.row < cRow:
                return True
            elif self.row > cRow and not self.dead and not self.attacked and not game.lockedIn:
                return True
            else:
                return False
        if gameBoard[cRow][cCol] == 3:
            return False
        return True

    def setDir(self): #Very inefficient || can easily refactor
        # BFS search -> Not best route but a route none the less
        dirs = [[0, -self.ghostSpeed, 0],
                [1, 0, self.ghostSpeed],
                [2, self.ghostSpeed, 0],
                [3, 0, -self.ghostSpeed]
        ]
        random.shuffle(dirs)
        best = 10000
        bestDir = -1
        for newDir in dirs:
            if self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]]) < best:
                if not (self.lastLoc[0] == self.row + newDir[1] and self.lastLoc[1] == self.col + newDir[2]):
                    if newDir[0] == 0 and self.col % 1.0 == 0:
                        if self.isValid(math.floor(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 1 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.ceil(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 2 and self.col % 1.0 == 0:
                        if self.isValid(math.ceil(self.row + newDir[1]), int(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
                    elif newDir[0] == 3 and self.row % 1.0 == 0:
                        if self.isValid(int(self.row + newDir[1]), math.floor(self.col + newDir[2])):
                            bestDir = newDir[0]
                            best = self.calcDistance(self.target, [self.row + newDir[1], self.col + newDir[2]])
        self.dir = bestDir

    def calcDistance(self, a, b):
        dR = a[0] - b[0]
        dC = a[1] - b[1]
        return math.sqrt((dR * dR) + (dC * dC))

    def setTarget(self):
        if gameBoard[int(self.row)][int(self.col)] == 4 and not self.dead:
            self.target = [ghostGate[0][0] - 1, ghostGate[0][1]+1]
            return
        elif gameBoard[int(self.row)][int(self.col)] == 4 and self.dead:
            self.target = [self.row, self.col]
        elif self.dead:
            self.target = [14, 13]
            return

        # Records the quadrants of each ghost's target
        quads = [0, 0, 0, 0]
        for ghost in game.ghosts:
            # if ghost.target[0] == self.row and ghost.col == self.col:
            #     continue
            if ghost.target[0] <= 15 and ghost.target[1] >= 13:
                quads[0] += 1
            elif ghost.target[0] <= 15 and ghost.target[1] < 13:
                quads[1] += 1
            elif ghost.target[0] > 15 and ghost.target[1] < 13:
                quads[2] += 1
            elif ghost.target[0]> 15 and ghost.target[1] >= 13:
                quads[3] += 1

        # Finds a target that will keep the ghosts dispersed
        while True:
            self.target = [randrange(31), randrange(28)]
            quad = 0
            if self.target[0] <= 15 and self.target[1] >= 13:
                quad = 0
            elif self.target[0] <= 15 and self.target[1] < 13:
                quad = 1
            elif self.target[0] > 15 and self.target[1] < 13:
                quad = 2
            elif self.target[0] > 15 and self.target[1] >= 13:
                quad = 3
            if not gameBoard[self.target[0]][self.target[1]] == 3 and not gameBoard[self.target[0]][self.target[1]] == 4:
                break
            elif quads[quad] == 0:
                break

    def move(self):
        # print(self.target)
        self.lastLoc = [self.row, self.col]
        if self.dir == 0:
            self.row -= self.ghostSpeed
        elif self.dir == 1:
            self.col += self.ghostSpeed
        elif self.dir == 2:
            self.row += self.ghostSpeed
        elif self.dir == 3:
            self.col -= self.ghostSpeed

        # Incase they go through the middle tunnel
        self.col = self.col % len(gameBoard[0])
        if self.col < 0:
            self.col = len(gameBoard[0]) - 0.5

    def setAttacked(self, isAttacked):
        self.attacked = isAttacked

    def isAttacked(self):
        return self.attacked

    def setDead(self, isDead):
        self.dead = isDead

    def isDead(self):
        return self.dead

game = Game(1, 0)
ghostsafeArea = [15, 13] # The location the ghosts escape to when attacked
ghostGate = [[15, 13], [15, 14]]


def canMove(row, col):
    if col == -1 or col == len(gameBoard[0]):
        return True
    if gameBoard[int(row)][int(col)] != 3:
        return True
    return False

# Reset after death
def reset():
    global game
    game.won = False
    game.ghosts = [Ghost(14.0, 13.5, "red", 0), Ghost(17.0, 11.5, "blue", 1), Ghost(17.0, 13.5, "pink", 2), Ghost(17.0, 15.5, "orange", 3)]
    for ghost in game.ghosts:
        ghost.setTarget()
    game.pacman = Pacman(26.0, 14.5,1)
    game.Mspacman = Pacman(26.0, 12.5,2)
    game.lives = 1
    game.paused = False
    game.score = 0
    game.time = 0
    game.collected = 0
    screen.fill((0, 0, 0)) # Flushes the screen
    # Draws game elements
    currentTile = 0
    game.displayLives()
    game.displayScore()
    global gameBoard
    gameBoard = copy.deepcopy(originalGameBoard)
    game.render()
    
def pause(time):
    cur = 0
    while not cur == time:
        cur += 1

def runGame_n_times(n,HeuristicType):
    data = [[] for j in range(n)] #create an array to store the player's data
    for i in range(0,n):
        game.running = True
        game.paused = False
        game.started = True
        onLaunchScreen = False
        PacMinPillDistance = 800
        MsMinPillDistance = 800
        powerPillOnMap = True
        reset()
        while game.running:
            if(HeuristicType == 0): #both Searching for PowerPills then normal pills

                powerPillOnMap = LookForPowerPills()
                if(powerPillOnMap): #prioritise collecting the closest power
                    game.pacman.FindNearestPowerPill()
                    game.Mspacman.FindNearestPowerPill()

                else: #if there are no more power pills find the rest of the pills
                    game.Mspacman.FindNearestPill()
                    game.pacman.FindNearestPill()
                game.pacman.newDir = game.pacman.MoveToTarget()
                game.Mspacman.newDir = game.Mspacman.MoveToTarget()

            elif(HeuristicType == 1): #Pacman looking for normal pills and Ms looking for powerPills

                powerPillOnMap = LookForPowerPills()
                if(powerPillOnMap): #prioritise collecting the closest power
                    game.Mspacman.FindNearestPowerPill()

                else: #if there are no more power pills find the rest of the pills
                    game.Mspacman.FindNearestPill()

                game.pacman.FindNearestPill()
                game.pacman.newDir = game.pacman.MoveToTarget()
                game.Mspacman.newDir = game.Mspacman.MoveToTarget()

            elif(HeuristicType == 2): #both looking for normal pills

                game.Mspacman.FindNearestPill()
                game.pacman.FindNearestPill()

                game.pacman.newDir = game.pacman.MoveToTarget()
                game.Mspacman.newDir = game.Mspacman.MoveToTarget()

            elif(HeuristicType == 3):#Mspacman looking for normal pills and Pacman looking for powerPills
                powerPillOnMap = LookForPowerPills()
                if(powerPillOnMap): #prioritise collecting the closest power
                    game.pacman.FindNearestPowerPill()

                else: #if there are no more power pills find the rest of the pills
                    game.pacman.FindNearestPill()

                game.Mspacman.FindNearestPill()
                game.pacman.newDir = game.pacman.MoveToTarget()
                game.Mspacman.newDir = game.Mspacman.MoveToTarget()

            if not onLaunchScreen:
                game.update()

        data[i] = [i,game.score,game.time/15, ((1/(game.time/15) )*10) *(2* game.score), game.collected, game.won, HeuristicType] #hybrid fitness between time survived and average score. Score more of an impact than time (want the pacman to be collecting score not avoiding ghosts)
    return data

def writeToFile(data):
    #print(data)
    #write all the data to an excel file
    workbook = xlsxwriter.Workbook('Heuristic.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 10)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Game_Run', bold)
    worksheet.write('B1', 'Score', bold)
    worksheet.write('C1', 'Time', bold)
    worksheet.write('D1', 'Hybrid', bold)
    worksheet.write('E1', 'Collected', bold)
    worksheet.write('F1', 'Won/Lost', bold)
    worksheet.write('G1', 'CollaborationType', bold)
    dataEntry = 1
    for i in range(0, len(data)):
        CurrentData = data[i]
        #print(CurrentData)
        for j in range(len(CurrentData)):
            #print(CurrentData[j])
            worksheet.write(dataEntry, 0, CurrentData[j][0] +1)
            worksheet.write(dataEntry, 1, CurrentData[j][1])
            worksheet.write(dataEntry, 2, CurrentData[j][2])
            worksheet.write(dataEntry, 3, CurrentData[j][3])
            worksheet.write(dataEntry, 4, CurrentData[j][4])
            if(CurrentData[j][5] == True):
                worksheet.write(dataEntry, 5, "Won")
            elif(CurrentData[j][5] == False):
                worksheet.write(dataEntry, 5, "Lost")

            worksheet.write(dataEntry, 6, CurrentData[j][6])

            dataEntry += 1
        dataEntry += 2
    workbook.close()

def LookForPowerPills():
    for l in range(3, len(gameBoard) - 2): #first 3 rows are walls
        for m in range(len(gameBoard[0])):
            if gameBoard[l][m] == 6:
                return True #if theres a power pill on the board return true
    return False

def runHeuristic_n_times(n, gameRuns):
    data = []
    for i in range(n):
        data.append(runGame_n_times(gameRuns, i)) #run the game 10 times with different collaboration type each time

    writeToFile(data)
runHeuristic_n_times(4, 10)

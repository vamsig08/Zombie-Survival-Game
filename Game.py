import pygame
import os
import random

# Defining window to draw game in
WIDTH, HEIGHT = 1100, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")

# Global veriable heaven
PURPLE = (216, 191, 216)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
MAX_BULLETS = 4
BULLET_VEL = 7
CHAR_WIDTH, CHAR_HEIGHT = 70, 70

# Values for cheacking if the player is in fact alive or not
player1Alive = True
player2Alive = True

# pre-set player health
Player1Health = 100
Player2Health = 100

# All image loading and setting from the assets folder
grass_Image = pygame.image.load(os.path.join('ASSETS', 'grass.png'))
grass = pygame.transform.scale(grass_Image, (WIDTH, HEIGHT))
charizard_Image = pygame.image.load(os.path.join('ASSETS', 'charizard.png'))
charizard = pygame.transform.scale(charizard_Image, (CHAR_WIDTH, CHAR_HEIGHT))
sonic_Image = pygame.image.load(os.path.join('ASSETS', 'sonic.png'))
sonic = pygame.transform.scale(sonic_Image, (CHAR_WIDTH, CHAR_HEIGHT))
enemy1_Image = pygame.image.load(os.path.join('ASSETS', 'enemy1.png'))
enemy1 = pygame.transform.scale(enemy1_Image, (CHAR_WIDTH, CHAR_HEIGHT))
enemy2_Image = pygame.image.load(os.path.join('ASSETS', 'enemy2.png'))
enemy2 = pygame.transform.scale(enemy2_Image, (CHAR_WIDTH, CHAR_HEIGHT))
rick_Image = pygame.image.load(os.path.join('ASSETS', 'rick.png'))
rick = pygame.transform.scale(rick_Image, (CHAR_WIDTH, CHAR_HEIGHT))
enemiesImageArr = [enemy1, enemy2, rick]

# letters for game over
LetterA_Image = pygame.image.load(os.path.join('ASSETS', 'A.png'))
LetterA = pygame.transform.scale(LetterA_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterE1_Image = pygame.image.load(os.path.join('ASSETS', 'E.png'))
LetterE1 = pygame.transform.scale(LetterE1_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterE2_Image = pygame.image.load(os.path.join('ASSETS', 'E.png'))
LetterE2 = pygame.transform.scale(LetterE2_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterG_Image = pygame.image.load(os.path.join('ASSETS', 'G.png'))
LetterG = pygame.transform.scale(LetterG_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterM_Image = pygame.image.load(os.path.join('ASSETS', 'M.png'))
LetterM = pygame.transform.scale(LetterM_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterO_Image = pygame.image.load(os.path.join('ASSETS', 'O.png'))
LetterO = pygame.transform.scale(LetterO_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterR_Image = pygame.image.load(os.path.join('ASSETS', 'R.png'))
LetterR = pygame.transform.scale(LetterR_Image, (CHAR_WIDTH, CHAR_HEIGHT))
LetterV_Image = pygame.image.load(os.path.join('ASSETS', 'V.png'))
LetterV = pygame.transform.scale(LetterV_Image, (CHAR_WIDTH, CHAR_HEIGHT))

# heart artwork for health
fullHeart_Image = pygame.image.load(os.path.join('ASSETS', 'fullHeart.png'))
fullHeart = pygame.transform.scale(fullHeart_Image, (30, 30))
halfHeart_Image = pygame.image.load(os.path.join('ASSETS', 'halfHeart.png'))
halfHeart = pygame.transform.scale(halfHeart_Image, (30, 30))
emptyHeart_Image = pygame.image.load(os.path.join('ASSETS', 'emptyHeart.png'))
emptyHeart = pygame.transform.scale(emptyHeart_Image, (30, 30))


# Draw window will blit the player and enemies onto the WIN, and also keep track of player alive
# When player isnt alive, it will display game over
def draw_window(player1, player2, player_1_bullets, player_2_bullets, enemyArr):
    if player1Alive == True or player2Alive == True:
        WIN.fill(PURPLE)
        WIN.blit(grass, (0, 0))
        if player1Alive == True:
            WIN.blit(charizard, (player1.x, player1.y))
        if player2Alive == True:
            WIN.blit(sonic, (player2.x, player2.y))
        for enemy in enemyArr:
            WIN.blit(enemy[0], (enemy[1].x, enemy[1].y))
        for bullet in player_1_bullets:
            pygame.draw.rect(WIN, RED, bullet)
        for bullet in player_2_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)
    else:
        WIN.blit(LetterG, (200, 200))
        WIN.blit(LetterA, (300, 200))
        WIN.blit(LetterM, (400, 200))
        WIN.blit(LetterE1, (500, 200))
        WIN.blit(LetterO, (600, 200))
        WIN.blit(LetterV, (700, 200))
        WIN.blit(LetterE2, (800, 200))
        WIN.blit(LetterR, (900, 200))
    # update the display
    pygame.display.update()


# Defines player 1 movement
def player1_movement(keys_pressed, player1):
    if keys_pressed[pygame.K_w] and player1.y - VEL > 0:  # UP
        player1.y -= VEL
    if keys_pressed[pygame.K_a] and player1.x - VEL > 0:  # LEFT
        player1.x -= VEL
    if keys_pressed[pygame.K_s] and player1.y + VEL + player1.height < HEIGHT:  # DOWN
        player1.y += VEL
    if keys_pressed[pygame.K_d] and player1.x + VEL + player1.width < WIDTH:  # RIGHT
        player1.x += VEL


# Defines player 2 movement
def player2_movement(keys_pressed, player2):
    if keys_pressed[pygame.K_UP] and player2.y - VEL > 0:  # UP
        player2.y -= VEL
    if keys_pressed[pygame.K_LEFT] and player2.x - VEL > 0:  # LEFT
        player2.x -= VEL
    if keys_pressed[pygame.K_DOWN] and player2.y + VEL + player2.height < HEIGHT:  # DOWN
        player2.y += VEL
    if keys_pressed[pygame.K_RIGHT] and player2.x + VEL + player2.width < WIDTH:  # RIGHT
        player2.x += VEL


# This sets the enemies to chase the closest player
def chasePlayer(player1, player2, enemy):
    chasePlayer = player1
    if player1Alive and player2Alive:
        distPlayer1 = (abs(player1.x - enemy.x) ** 2 + abs(player1.y - enemy.y) ** 2) ** (1 / 2)
        distPlayer2 = (abs(player2.x - enemy.x) ** 2 + abs(player2.y - enemy.y) ** 2) ** (1 / 2)
        if distPlayer1 > distPlayer2:
            chasePlayer = player2
    elif player2Alive:
        chasePlayer = player2
    if enemy.x < chasePlayer.x:
        enemy.x += 1
    if enemy.x > chasePlayer.x:
        enemy.x -= 1
    if enemy.y < chasePlayer.y:
        enemy.y += 1
    if enemy.y > chasePlayer.y:
        enemy.y -= 1


# If the player is hit, it will decrease the health of players
def hitPlayer(player1, player2, enemy):
    global Player1Health, Player2Health
    global player1Alive, player2Alive
    # if enemy.x == player1.x and enemy.y == player1.y:
    if enemy.colliderect(player1):
        Player1Health = Player1Health - 2
        if Player1Health <= 0:
            player1Alive = False
    if enemy.colliderect(player2):
        # if enemy.x == player2.x and enemy.y == player2.y:
        Player2Health = Player2Health - 2
        if Player2Health <= 0:
            player2Alive = False


# Checks if the bullet will hit the enemy
def hitEnemies(enemyArr, bullet):
    for enemy in enemyArr:
        if bullet.colliderect(enemy[1]):
            enemyArr.remove(enemy)


# Will blit the game over when players both die
def gameOver(G, A, M, E, O, V, e, R):
    if player1Alive == False and player2Alive == False:
        WIN.blit(LetterG, (G.x, G.y))
        WIN.blit(LetterA, (A.x, A.y))
        WIN.blit(LetterM, (M.x, M.y))
        WIN.blit(LetterE1, (E.x, E.y))
        WIN.blit(LetterO, (O.x, O.y))
        WIN.blit(LetterV, (V.x, V.y))
        WIN.blit(LetterE2, (e.x, e.y))
        WIN.blit(LetterR, (R.x, R.y))
    pygame.display.update()


# Displays the current amount of health that the player has
def playerHealth(player1, player2):
    global Player1Health
    global Player2Health
    pygame.font.init()

    if Player1Health <= 100 and Player1Health > 85:
        WIN.blit(fullHeart, (0, 0))
        WIN.blit(fullHeart, (15, 0))
        WIN.blit(fullHeart, (30, 0))
    if Player1Health <= 85 and Player1Health > 75:
        WIN.blit(fullHeart, (0, 0))
        WIN.blit(fullHeart, (15, 0))
        WIN.blit(halfHeart, (30, 0))
    if Player1Health <= 75 and Player1Health > 65:
        WIN.blit(fullHeart, (0, 0))
        WIN.blit(fullHeart, (15, 0))
        WIN.blit(emptyHeart, (30, 0))
    if Player1Health <= 65 and Player1Health > 45:
        WIN.blit(fullHeart, (0, 0))
        WIN.blit(halfHeart, (15, 0))
        WIN.blit(emptyHeart, (30, 0))
    if Player1Health <= 45 and Player1Health > 25:
        WIN.blit(fullHeart, (0, 0))
        WIN.blit(emptyHeart, (15, 0))
        WIN.blit(emptyHeart, (30, 0))
    if Player1Health <= 25 and Player1Health > 0:
        WIN.blit(halfHeart, (0, 0))
        WIN.blit(emptyHeart, (15, 0))
        WIN.blit(emptyHeart, (30, 0))
    if Player1Health <= 0:
        WIN.blit(emptyHeart, (0, 0))
        WIN.blit(emptyHeart, (15, 0))
        WIN.blit(emptyHeart, (30, 0))

    if Player2Health <= 100 and Player2Health > 85:
        WIN.blit(fullHeart, (0, 25))
        WIN.blit(fullHeart, (15, 25))
        WIN.blit(fullHeart, (30, 25))
    if Player2Health <= 85 and Player2Health > 75:
        WIN.blit(fullHeart, (0, 25))
        WIN.blit(fullHeart, (15, 25))
        WIN.blit(halfHeart, (30, 25))
    if Player2Health <= 75 and Player2Health > 65:
        WIN.blit(fullHeart, (0, 25))
        WIN.blit(fullHeart, (15, 25))
        WIN.blit(emptyHeart, (30, 25))
    if Player2Health <= 65 and Player2Health > 45:
        WIN.blit(fullHeart, (0, 25))
        WIN.blit(halfHeart, (15, 25))
        WIN.blit(emptyHeart, (30, 25))
    if Player2Health <= 45 and Player2Health > 25:
        WIN.blit(fullHeart, (0, 25))
        WIN.blit(emptyHeart, (15, 25))
        WIN.blit(emptyHeart, (30, 25))
    if Player2Health <= 25 and Player2Health > 0:
        WIN.blit(halfHeart, (0, 25))
        WIN.blit(emptyHeart, (15, 25))
        WIN.blit(emptyHeart, (30, 25))
    if Player2Health <= 0:
        WIN.blit(emptyHeart, (0, 25))
        WIN.blit(emptyHeart, (15, 25))
        WIN.blit(emptyHeart, (30, 25))

    pygame.display.update()


# The bullets that fire from each player, after pressing 'ctrl' on ether side will fire the bullets
def bulletMovement(player_1_bullets, player_2_bullets):
    if len(player_1_bullets) > 0:
        player_1_bullets[0].y += BULLET_VEL
        player_1_bullets[1].y -= BULLET_VEL
        player_1_bullets[2].x += BULLET_VEL
        player_1_bullets[3].x -= BULLET_VEL
        if player_1_bullets[0].y > HEIGHT and player_1_bullets[1].y < 0 and player_1_bullets[2].x > WIDTH and \
                player_1_bullets[3].x < 0:
            player_1_bullets.clear()

    if len(player_2_bullets) > 0:
        player_2_bullets[0].y += BULLET_VEL
        player_2_bullets[1].y -= BULLET_VEL
        player_2_bullets[2].x += BULLET_VEL
        player_2_bullets[3].x -= BULLET_VEL
        if player_2_bullets[0].y > HEIGHT and player_2_bullets[1].y < 0 and player_2_bullets[2].x > WIDTH and \
                player_2_bullets[3].x < 0:
            player_2_bullets.clear()


# Defines the beginning rectangles to collide, keeps track of bullet spawning
# And also will randomly spawn the enemies
def main():
    player1 = pygame.Rect(200, 200, CHAR_WIDTH, CHAR_HEIGHT)
    player2 = pygame.Rect(700, 200, CHAR_WIDTH, CHAR_HEIGHT)
    G = pygame.Rect(200, 200, CHAR_WIDTH, CHAR_WIDTH)
    A = pygame.Rect(300, 200, CHAR_WIDTH, CHAR_WIDTH)
    M = pygame.Rect(400, 200, CHAR_WIDTH, CHAR_WIDTH)
    E = pygame.Rect(500, 200, CHAR_WIDTH, CHAR_WIDTH)
    O = pygame.Rect(600, 200, CHAR_WIDTH, CHAR_WIDTH)
    V = pygame.Rect(700, 200, CHAR_WIDTH, CHAR_WIDTH)
    e = pygame.Rect(800, 200, CHAR_WIDTH, CHAR_WIDTH)
    R = pygame.Rect(900, 200, CHAR_WIDTH, CHAR_WIDTH)

    enemyArr = []
    player_1_bullets = []
    player_2_bullets = []

    clock = pygame.time.Clock()
    run = True
    spawnTime = 0
    while run:
        # control the frame rate
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(player_1_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(
                    player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5)
                bullet1 = pygame.Rect(
                    player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5)
                bullet2 = pygame.Rect(
                    player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5)
                bullet3 = pygame.Rect(
                    player1.x + player1.width, player1.y + player1.height // 2 - 2, 10, 5)
                player_1_bullets.append(bullet)
                player_1_bullets.append(bullet1)
                player_1_bullets.append(bullet2)
                player_1_bullets.append(bullet3)

            if event.key == pygame.K_RCTRL and len(player_2_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(
                    player2.x, player2.y + player2.height // 2 - 2, 10, 5)
                bullet1 = pygame.Rect(
                    player2.x, player2.y + player2.height // 2 - 2, 10, 5)
                bullet2 = pygame.Rect(
                    player2.x, player2.y + player2.height // 2 - 2, 10, 5)
                bullet3 = pygame.Rect(
                    player2.x, player2.y + player2.height // 2 - 2, 10, 5)
                player_2_bullets.append(bullet)
                player_2_bullets.append(bullet1)
                player_2_bullets.append(bullet2)
                player_2_bullets.append(bullet3)

        keys_pressed = pygame.key.get_pressed()
        if (player1Alive == True):
            player1_movement(keys_pressed, player1)
        if (player2Alive == True):
            player2_movement(keys_pressed, player2)

        if spawnTime > 30:
            offset = 60
            randomArrSpawn = [pygame.Rect(random.randint(0, 1099), 0 - offset, CHAR_WIDTH, CHAR_HEIGHT),
                              pygame.Rect(0 - offset, random.randint(0, 599), CHAR_WIDTH, CHAR_HEIGHT),
                              pygame.Rect(1099 + offset, random.randint(0, 599), CHAR_WIDTH, CHAR_HEIGHT),
                              pygame.Rect(random.randint(0, 1099), 599 + offset, CHAR_WIDTH, CHAR_HEIGHT)]
            enemy = [enemiesImageArr[random.randint(0, len(enemiesImageArr) - 1)], randomArrSpawn[random.randint(0, 3)],
                     True]
            enemyArr.append(enemy)
            spawnTime = 0

        for enemy in enemyArr:
            chasePlayer(player1, player2, enemy[1])
            hitPlayer(player1, player2, enemy[1])
        for bullet in player_2_bullets:
            hitEnemies(enemyArr, bullet)
        for bullet in player_1_bullets:
            hitEnemies(enemyArr, bullet)

        playerHealth(player1, player2)
        gameOver(G, A, M, E, O, V, e, R)
        bulletMovement(player_1_bullets, player_2_bullets)
        draw_window(player1, player2, player_1_bullets, player_2_bullets, enemyArr)

        spawnTime += 1

    # shut down Pygame
    pygame.quit()


if __name__ == "__main__":
    main()

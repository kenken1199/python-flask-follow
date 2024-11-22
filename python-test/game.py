import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("簡単なゲーム")

# 色とキャラクターの設定
background_color = (255, 255, 255)
character_color = (0, 128, 255)
character_size = 50
character_x, character_y = screen_width // 2, screen_height // 2
character_speed = 0.1

# メインループ
running = True
while running:
    # イベントの処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed
    if keys[pygame.K_UP]:
        character_y -= character_speed
    if keys[pygame.K_DOWN]:
        character_y += character_speed

    # 画面をクリアしてから再描画
    screen.fill(background_color)
    pygame.draw.rect(screen, character_color, (character_x, character_y, character_size, character_size))
    pygame.display.flip()

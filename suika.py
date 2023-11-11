import pygame
import pymunk
import pymunk.pygame_util
import random

# Pygameの初期化
pygame.init()

# ゲームウィンドウの設定
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Pymunkのスペース（物理空間）を設定
space = pymunk.Space()
space.gravity = (0, 900)

# 床と壁を追加する関数
def add_walls_and_floor(space, width, height):
    # 床を追加
    floor = pymunk.Segment(space.static_body, (0, height - 50), (width, height - 50), 1)
    floor.elasticity = 0.8
    floor.friction = 1
    space.add(floor)
    
    # 左の壁を追加
    left_wall = pymunk.Segment(space.static_body, (0, 0), (0, height), 1)
    left_wall.elasticity = 0.8
    left_wall.friction = 1
    space.add(left_wall)
    
    # 右の壁を追加
    right_wall = pymunk.Segment(space.static_body, (width, 0), (width, height), 1)
    right_wall.elasticity = 0.8
    right_wall.friction = 1
    space.add(right_wall)

# 床と壁を追加
add_walls_and_floor(space, width, height)

# フルーツクラスの定義
class Fruit:
    def __init__(self, position, size, evolution, space):
        self.body = pymunk.Body(1, float('inf'))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, size)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        self.evolution = evolution
        self.space = space
        self.space.add(self.body, self.shape)

# フルーツの色を設定
fruit_colors = {
    'strawberry': (255, 0, 0),
    'grape': (128, 0, 128),
    'orange': (255, 165, 0),
    # ...他の果物の色も追加...
}

fruit_positions = [(100, -30), (200, -30), (300, -30), (400, -30), (500, -30)]
fruit_sizes = [20, 25, 30, 35, 40]

# フルーツの進化ルール
evolution_rules = {
    'strawberry': 'grape',
    'grape': 'orange',
    # ...他の進化ルールも追加...
}

def generate_fruit(space):
    position = random.choice(fruit_positions)
    size = random.choice(fruit_sizes)
    evolution = random.choice(list(evolution_rules.keys()))
    return Fruit(position, size, evolution, space)

# フルーツの生成
fruits = []

# ゲームのメインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # マウスがクリックされたときにフルーツを生成する
        if event.type == pygame.MOUSEBUTTONDOWN:
            # マウスの位置にフルーツを生成する
            mouse_position = pygame.mouse.get_pos()
            fruit = generate_fruit(space)
            fruit.body.position = mouse_position
            fruits.append(fruit)

    # 物理演算を進める
    space.step(1/50)

    # 画面をクリア
    screen.fill((255, 255, 255))

    # フルーツと物理空間を描画
    space.debug_draw(draw_options)

    # フルーツの進化処理
    for fruit in fruits:
        # ここに進化のロジックを追加...
        pass

    # 画面を更新
    pygame.display.flip()

    # FPSを設定
    clock.tick(50)

pygame.quit()
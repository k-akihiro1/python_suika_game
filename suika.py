import pygame
import pymunk
import pymunk.pygame_util
import random

# Pygameの初期化
pygame.init()

# ゲームウィンドウの設定
width, height = 500, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)
font = pygame.font.SysFont(None, 36)  # スコア表示用のフォント

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
        self.color = fruit_colors[evolution]  # 色を保持する
        self.space = space
        self.space.add(self.body, self.shape)

# フルーツの色を設定
fruit_colors = {
    'strawberry': (255, 0, 0),
    'grape': (128, 0, 128),
    'orange': (255, 165, 0),
    'persimmon': (255, 140, 0),
    'apple': (0, 255, 0),
    'pear': (255, 255, 0),
    'pineapple': (255, 223, 0),
    'peach': (255, 218, 185),
    'melon': (0, 255, 127),
    'watermelon': (155, 0, 0)
}

fruit_positions = [(100, -30), (200, -30), (300, -30), (400, -30), (500, -30)]
# フルーツサイズの辞書
fruit_sizes = {
    'strawberry': 20,
    'grape': 25,
    'orange': 30,
    'persimmon': 35,
    'apple': 40,
    'pear': 45,
    'pineapple': 50,
    'peach': 55,
    'melon': 60,
    'watermelon': 65
}


# 初期フルーツの色を設定（これらはクリックで生成されない）
initial_fruit_colors = {
    'strawberry': (255, 0, 0),
    'grape': (128, 0, 128),
    'orange': (255, 165, 0),
}

# フルーツの進化ルール
evolution_rules = {
    'strawberry': ('grape', 1),
    'grape': ('orange', 3),
    'orange': ('persimmon', 6),
    'persimmon': ('apple', 10),
    'apple': ('pear', 15),
    'pear': ('pineapple', 21),
    'pineapple': ('peach', 28),
    'peach': ('melon', 36),
    'melon': ('watermelon', 45),
    'watermelon': (None, 55)  # スイカはこれ以上進化しない
}

# スコア変数
score = 0

# フルーツ生成関数（クリックで生成されるフルーツ）
def generate_fruit(space):
    position = random.choice(fruit_positions)
    evolution = random.choice(list(initial_fruit_colors.keys()))
    size = fruit_sizes[evolution]  # 進化段階に応じたサイズを辞書から取得
    fruit = Fruit(position, size, evolution, space)
    # ランダムな初速を与える
    impulse = random.uniform(-100, 100), 0  # X軸方向にランダムな速度、Y軸方向には0
    fruit.body.apply_impulse_at_local_point(impulse)
    return fruit

# 衝突コールバック関数を更新
def collision_handler(arbiter, space, data):
    global score, fruits
    fruit_shape1, fruit_shape2 = arbiter.shapes
    fruit1, fruit2 = fruit_shape1.body, fruit_shape2.body

    # Identify the Fruit instances from the shapes.
    fruit1_instance = next((f for f in fruits if f.body == fruit1), None)
    fruit2_instance = next((f for f in fruits if f.body == fruit2), None)

    # Check if both are fruits and have the same evolution state.
    if fruit1_instance and fruit2_instance and fruit1_instance.evolution == fruit2_instance.evolution:
        # Get the slower fruit.
        slower_fruit = fruit1_instance if fruit1.velocity.length < fruit2.velocity.length else fruit2_instance
        faster_fruit = fruit2_instance if slower_fruit == fruit1_instance else fruit1_instance

        # Evolve the slower fruit.
        next_evolution, points = evolution_rules[slower_fruit.evolution]
        if next_evolution:
            # Update the score.
            score += points
            # Create a new fruit with the next evolution.
            new_fruit = Fruit(slower_fruit.body.position, fruit_sizes[next_evolution], next_evolution, space)
            new_fruit.body.velocity = slower_fruit.body.velocity  # Maintain the velocity after evolution.
            new_fruit.color = fruit_colors[next_evolution]  # Assign the color of the next evolution.
            fruits.append(new_fruit)
            # Remove the old fruits.
            space.remove(fruit_shape1, fruit1)
            space.remove(fruit_shape2, fruit2)
            fruits.remove(fruit1_instance)
            fruits.remove(fruit2_instance)
            
            # Apply a small impulse to the new fruit to avoid stacking
            impulse = random.uniform(-50, 50), random.uniform(100, 200)  # Adjust the values as needed
            new_fruit.body.apply_impulse_at_local_point(impulse)
            # Apply an opposite impulse to the old fruit to ensure separation
            opposite_impulse = (-impulse[0], -impulse[1])
            slower_fruit.body.apply_impulse_at_local_point(opposite_impulse)
    return True

# 衝突ハンドラーの設定
handler = space.add_default_collision_handler()
handler.begin = collision_handler

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

  # フルーツが画面下部にあるかチェックし、削除
  for fruit in fruits[:]:
    if fruit.body.position.y > height - 50:  # 床の位置を考慮
      space.remove(fruit.shape, fruit.body)
      fruits.remove(fruit)


  # フルーツと物理空間を描画
  space.debug_draw(draw_options)

  # フルーツの描画
  for fruit in fruits:
    # 進化したフルーツの色を取得
    fruit_color = fruit_colors[fruit.evolution]
    pygame.draw.circle(screen, fruit_color, (int(fruit.body.position.x), int(fruit.body.position.y)), int(fruit.shape.radius))

  # スコアを描画
  score_text = font.render(f'Score: {score}', True, (0, 0, 0))
  screen.blit(score_text, (width - 200, 10))  # スコアを右上に表示

  # 画面を更新
  pygame.display.flip()

  # FPSを設定
  clock.tick(50)

pygame.quit()

import pygame
import random
import time
import sys

# 初始化pygame
pygame.init()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 游戏设置
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("双人贪吃蛇对战")
clock = pygame.time.Clock()

class Snake:
    def __init__(self, pos, color, controls):
        self.body = [pos]
        self.direction = RIGHT
        self.color = color
        self.controls = controls  # 按键控制 (上, 下, 左, 右)
        self.score = 0
        self.grow_to = 3  # 初始长度
        self.alive = True
        self.speed_boost = False
        self.boost_timer = 0
        self.invincible = False
        self.invincible_timer = 0
    
    def get_head(self):
        return self.body[0]
    
    def update(self):
        if not self.alive:
            return
            
        # 检查加速状态
        if self.speed_boost and time.time() - self.boost_timer > 5:
            self.speed_boost = False
            
        # 检查无敌状态
        if self.invincible and time.time() - self.invincible_timer > 3:
            self.invincible = False
            
        # 移动蛇
        head = self.get_head()
        new_head = ((head[0] + self.direction[0]) % GRID_WIDTH, 
                    (head[1] + self.direction[1]) % GRID_HEIGHT)
        
        # 检查是否撞到自己
        if new_head in self.body[1:] and not self.invincible:
            self.alive = False
            return
            
        self.body.insert(0, new_head)
        
        if self.grow_to > len(self.body):
            pass  # 蛇还在生长
        else:
            self.body.pop()
    
    def grow(self):
        self.grow_to += 1
        self.score += 10
    
    def draw(self, surface):
        if not self.alive:
            return
            
        for segment in self.body:
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                              GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
            
        # 绘制蛇头
        head = self.get_head()
        head_rect = pygame.Rect(head[0] * GRID_SIZE, head[1] * GRID_SIZE, 
                              GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, WHITE, head_rect, 3)
    
    def handle_keys(self, keys):
        if keys[self.controls[0]] and self.direction != DOWN:
            self.direction = UP
        elif keys[self.controls[1]] and self.direction != UP:
            self.direction = DOWN
        elif keys[self.controls[2]] and self.direction != RIGHT:
            self.direction = LEFT
        elif keys[self.controls[3]] and self.direction != LEFT:
            self.direction = RIGHT
    
    def activate_speed_boost(self):
        self.speed_boost = True
        self.boost_timer = time.time()
    
    def activate_invincible(self):
        self.invincible = True
        self.invincible_timer = time.time()

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.type = "normal"  # normal, speed_boost, invincible
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
        # 随机决定食物类型
        food_type = random.random()
        if food_type < 0.7:  # 70%普通食物
            self.type = "normal"
            self.color = RED
        elif food_type < 0.9:  # 20%加速食物
            self.type = "speed_boost"
            self.color = BLUE
        else:  # 10%无敌食物
            self.type = "invincible"
            self.color = YELLOW
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

class Game:
    def __init__(self):
        self.snake1 = Snake((10, 10), GREEN, (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d))
        self.snake2 = Snake((30, 10), PURPLE, (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT))
        self.food = Food()
        self.game_over = False
        self.winner = None
        self.font = pygame.font.SysFont('Arial', 25)
        self.big_font = pygame.font.SysFont('Arial', 50)
    
    def update(self):
        if self.game_over:
            return
            
        # 处理按键
        keys = pygame.key.get_pressed()
        self.snake1.handle_keys(keys)
        self.snake2.handle_keys(keys)
        
        # 更新蛇的位置
        self.snake1.update()
        self.snake2.update()
        
        # 检查蛇是否相撞
        self.check_collisions()
        
        # 检查是否吃到食物
        self.check_food()
        
        # 检查游戏是否结束
        if not self.snake1.alive and not self.snake2.alive:
            self.game_over = True
            if self.snake1.score > self.snake2.score:
                self.winner = "玩家1 (绿色)"
            elif self.snake2.score > self.snake1.score:
                self.winner = "玩家2 (紫色)"
            else:
                self.winner = "平局"
    
    def check_collisions(self):
        # 检查蛇1是否撞到蛇2
        if self.snake2.alive and not self.snake1.invincible:
            head1 = self.snake1.get_head()
            if head1 in self.snake2.body[1:]:
                self.snake1.alive = False
            elif head1 == self.snake2.get_head() and not self.snake2.invincible:
                self.snake1.alive = False
                self.snake2.alive = False
        
        # 检查蛇2是否撞到蛇1
        if self.snake1.alive and not self.snake2.invincible:
            head2 = self.snake2.get_head()
            if head2 in self.snake1.body[1:]:
                self.snake2.alive = False
            elif head2 == self.snake1.get_head() and not self.snake1.invincible:
                self.snake1.alive = False
                self.snake2.alive = False
    
    def check_food(self):
        # 检查蛇1是否吃到食物
        if self.snake1.alive and self.snake1.get_head() == self.food.position:
            if self.food.type == "normal":
                self.snake1.grow()
            elif self.food.type == "speed_boost":
                self.snake1.activate_speed_boost()
                self.snake1.score += 5  # 额外加分
            elif self.food.type == "invincible":
                self.snake1.activate_invincible()
                self.snake1.score += 15  # 额外加分
            self.food.randomize_position()
            # 确保食物不会出现在蛇身上
            while self.food.position in self.snake1.body or self.food.position in self.snake2.body:
                self.food.randomize_position()
        
        # 检查蛇2是否吃到食物
        if self.snake2.alive and self.snake2.get_head() == self.food.position:
            if self.food.type == "normal":
                self.snake2.grow()
            elif self.food.type == "speed_boost":
                self.snake2.activate_speed_boost()
                self.snake2.score += 5  # 额外加分
            elif self.food.type == "invincible":
                self.snake2.activate_invincible()
                self.snake2.score += 15  # 额外加分
            self.food.randomize_position()
            # 确保食物不会出现在蛇身上
            while self.food.position in self.snake1.body or self.food.position in self.snake2.body:
                self.food.randomize_position()
    
    def draw(self, surface):
        surface.fill(BLACK)
        
        # 绘制网格
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(surface, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, (40, 40, 40), (0, y), (WIDTH, y))
        
        # 绘制食物和蛇
        self.food.draw(surface)
        self.snake1.draw(surface)
        self.snake2.draw(surface)
        
        # 绘制分数
        score1_text = self.font.render(f"玩家1: {self.snake1.score}", True, GREEN)
        score2_text = self.font.render(f"玩家2: {self.snake2.score}", True, PURPLE)
        surface.blit(score1_text, (10, 10))
        surface.blit(score2_text, (WIDTH - 150, 10))
        
        # 绘制状态
        status1 = "存活" if self.snake1.alive else "死亡"
        status2 = "存活" if self.snake2.alive else "死亡"
        status1_text = self.font.render(f"状态: {status1}", True, GREEN)
        status2_text = self.font.render(f"状态: {status2}", True, PURPLE)
        surface.blit(status1_text, (10, 40))
        surface.blit(status2_text, (WIDTH - 150, 40))
        
        # 绘制特殊状态
        if self.snake1.speed_boost:
            boost_text = self.font.render("加速!", True, BLUE)
            surface.blit(boost_text, (10, 70))
        if self.snake1.invincible:
            invincible_text = self.font.render("无敌!", True, YELLOW)
            surface.blit(invincible_text, (10, 100))
            
        if self.snake2.speed_boost:
            boost_text = self.font.render("加速!", True, BLUE)
            surface.blit(boost_text, (WIDTH - 150, 70))
        if self.snake2.invincible:
            invincible_text = self.font.render("无敌!", True, YELLOW)
            surface.blit(invincible_text, (WIDTH - 150, 100))
        
        # 游戏结束显示
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            game_over_text = self.big_font.render("游戏结束!", True, WHITE)
            winner_text = self.big_font.render(f"胜利者: {self.winner}", True, WHITE)
            restart_text = self.font.render("按R键重新开始，按ESC键退出", True, WHITE)
            
            surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
            surface.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2))
            surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    
    def reset(self):
        self.__init__()

def main():
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()
        
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        
        # 根据蛇的加速状态调整帧率
        if (game.snake1.alive and game.snake1.speed_boost) or (game.snake2.alive and game.snake2.speed_boost):
            clock.tick(FPS * 2)  # 加速时帧率加倍
        else:
            clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
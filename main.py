import pygame
import sys
import math
import random

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
BLUE = (0, 0, 255)
LIGHT_GREEN = (144, 238, 144)

GRID_SIZE = 40
TOWER_COST = 50
UPGRADE_COST = 30
STARTING_GOLD = 200
UNLOCK_COST = 30

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

class Enemy:
    def __init__(self, path, image):
        self.path = path
        self.x, self.y = self.path[0]
        self.path_index = 0
        self.speed = 1.0
        self.max_health = 100
        self.health = self.max_health
        self.reached_end = False
        self.image = image

    def move(self):
        if self.path_index + 1 < len(self.path):
            target = self.path[self.path_index + 1]
            dx, dy = target[0] - self.x, target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.x += dx * self.speed
                self.y += dy * self.speed
            if distance((self.x, self.y), target) < 2:
                self.path_index += 1
        else:
            self.reached_end = True

    def draw(self, screen):
        rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, rect)

        # Vẽ thanh máu
        health_bar_width = 20
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - 10, self.y - 20, health_bar_width, 4))
        pygame.draw.rect(screen, GREEN, (self.x - 10, self.y - 20, health_bar_width * health_ratio, 4))

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 6
        self.damage = damage

    
    def move(self):
        if not self.target: return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0: return
        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist

    def has_hit(self):
        return distance((self.x, self.y), (self.target.x, self.target.y)) < 10

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 5)




class Tower:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.range = 120
        self.fire_rate = 60  # càng nhỏ bắn càng nhanh
        self.timer = 0
        self.level = 1
        self.damage = 25

    def upgrade(self):
        self.level += 1
        self.range += 15
        self.fire_rate = max(20, self.fire_rate - 5)
        self.damage += 10

    def in_range(self, enemy):
        return distance((self.x, self.y), (enemy.x, enemy.y)) <= self.range

    def update(self, enemies, bullets):
        self.timer += 1
        if self.timer >= self.fire_rate:
            for enemy in enemies:
                if self.in_range(enemy):
                    bullets.append(Bullet(self.x, self.y, enemy, self.damage))
                    self.timer = 0
                    break

    def draw(self, screen):
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.range, 1)

class Game:
    def __init__(self):
        

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)

        self.path = [(0, 300), (200, 300), (200, 100), (600, 100), (600, 400), (800, 400)]
        self.tower_image = pygame.image.load("assets/tower.png").convert_alpha()
        self.enemy_image = pygame.image.load("assets/enemy.png").convert_alpha()
        # set size
        self.tower_image = pygame.transform.scale(self.tower_image, (40, 40))
        self.enemy_image = pygame.transform.scale(self.enemy_image, (40, 40))
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.gold = STARTING_GOLD
        self.health = 10
        self.wave = 0
        self.waiting_for_wave = True
        self.message = ""
        self.message_timer = 0

        self.buildable = []
        self.locked_positions = []
        self.unlocked_positions = []

        self.generate_buildable_positions()

    def generate_buildable_positions(self):
        candidates = []
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                pos = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
                if any(distance(pos, p) <= GRID_SIZE * 2 for p in self.path):
                    candidates.append(pos)
        random.shuffle(candidates)
        self.buildable = candidates[:20]
        for pos in self.buildable:
            if random.random() < 0.3:
                self.locked_positions.append(pos)
            else:
                self.unlocked_positions.append(pos)

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            for y in range(0, HEIGHT, GRID_SIZE):
                pygame.draw.rect(self.screen, GRAY, pygame.Rect(x, y, GRID_SIZE, GRID_SIZE), 1)
        for pos in self.locked_positions:
            pygame.draw.circle(self.screen, RED, pos, 5)
        for pos in self.unlocked_positions:
            pygame.draw.circle(self.screen, (50, 50, 50), pos, 3)

    def draw_path(self):
        for i in range(len(self.path) - 1):
            pygame.draw.line(self.screen, YELLOW, self.path[i], self.path[i + 1], 8)

    def draw_ui(self):
        self.screen.blit(self.font.render(f"Gold: {self.gold}", True, GOLD), (10, 10))
        self.screen.blit(self.font.render(f"Health: {self.health}", True, RED), (10, 40))
        self.screen.blit(self.font.render(f"Wave: {self.wave}", True, WHITE), (10, 70))
        if self.waiting_for_wave:
            self.screen.blit(self.font.render("Press SPACE for next wave", True, GREEN), (WIDTH // 2 - 100, 10))
        if self.message:
            self.screen.blit(self.font.render(self.message, True, RED), (WIDTH // 2 - 100, HEIGHT - 40))

    def spawn_wave(self):
        self.wave += 1
        for i in range(5 + self.wave):
            enemy = Enemy(self.path, self.enemy_image)
            enemy.health += self.wave * 10
            enemy.max_health = enemy.health
            enemy.speed += min(0.2 * self.wave, 3.0)  # giới hạn tốc độ tăng
            enemy.x -= i * 60
            self.enemies.append(enemy)


    def handle_events(self):
        
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = pygame.mouse.get_pos()
                for tower in self.towers:
                    if distance((mx, my), (tower.x, tower.y)) < 20:
                        if self.gold >= UPGRADE_COST:
                            tower.upgrade()
                            self.gold -= UPGRADE_COST
                        else:
                            self.message = "Not enough gold to upgrade!"
                            self.message_timer = pygame.time.get_ticks()
                        return

            if event.type == pygame.QUIT:
                return False
                

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                for pos in self.buildable:
                    if distance((mx, my), pos) < GRID_SIZE // 2:
                        if pos in self.locked_positions:
                            if self.gold >= UNLOCK_COST:
                                self.gold -= UNLOCK_COST
                                self.locked_positions.remove(pos)
                                self.unlocked_positions.append(pos)
                                pygame.draw.circle(self.screen, LIGHT_GREEN, pos, 10)
                                pygame.display.flip()
                                pygame.time.delay(100)
                            else:
                                self.message = "Not enough gold to unlock!"
                                self.message_timer = pygame.time.get_ticks()
                        elif pos in self.unlocked_positions and self.gold >= TOWER_COST:
                            self.towers.append(Tower(*pos, self.tower_image))
                            self.gold -= TOWER_COST
                        break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.waiting_for_wave:
                    self.spawn_wave()
                    self.waiting_for_wave = False
        return True

    def update(self):
        for tower in self.towers:
            tower.update(self.enemies, self.bullets)

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.target.health <= 0:
                self.bullets.remove(bullet)
            elif bullet.has_hit():
                bullet.target.health -= bullet.damage
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.gold += 10
            elif enemy.reached_end:
                self.enemies.remove(enemy)
                self.health -= 1

        if not self.enemies and not self.waiting_for_wave:
            self.waiting_for_wave = True

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_path()
        self.draw_ui()

        for tower in self.towers:
            tower.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        if self.health <= 0:
            self.screen.blit(self.font.render("Game Over", True, RED), (WIDTH // 2 - 60, HEIGHT // 2))

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()

import pygame
import sys

# --- Khởi tạo ---
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kimetsu: Path of the Slayer (V1.5)")

# Màu sắc & Font
WHITE, BLACK, RED, BLUE = (255,255,255), (0,0,0), (255,0,0), (0,100,255)
GOLD, GREEN = (255,215,0), (50,205,50)
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 40, bold=True)

class Tanjiro:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.points = 0 # Điểm nâng cấp nội tại
        
        # 5 Mức Nội Tại như bạn yêu cầu
        self.max_hp = 1000
        self.hp = 1000
        self.technique = 1  # Kỹ thuật
        self.speed = 5      # Tốc độ di chuyển
        self.agility = 1    # Độ dẻo
        self.breathing = 0  # Hơi thở (Khóa đến lv 20)

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level += 1
            self.exp = 0
            self.points += 3 # Mỗi cấp tặng 3 điểm
            return True
        return False

# Khởi tạo nhân vật
player_data = Tanjiro()
clock = pygame.time.Clock()

def draw_ui():
    # Vẽ bảng trạng thái bên trái
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, 250, HEIGHT))
    
    texts = [
        f"CẤP ĐỘ: {player_data.level}",
        f"Kinh nghiệm: {player_data.exp}/{player_data.level*100}",
        f"Điểm nâng cấp: {player_data.points}",
        "--- NỘI TẠI ---",
        f"[1] Máu: {player_data.max_hp} (+300)",
        f"[2] Kỹ thuật: {player_data.technique}",
        f"[3] Tốc độ: {player_data.speed}",
        f"[4] Độ dẻo: {player_data.agility}",
        f"[5] Hơi thở: {player_data.breathing if player_data.level >= 20 else 'KHÓA'}"
    ]
    
    for i, t in enumerate(texts):
        color = GOLD if "Điểm" in t else WHITE
        txt_surface = font.render(t, True, color)
        screen.blit(txt_surface, (20, 50 + i*35))

    # Thanh máu
    pygame.draw.rect(screen, RED, (300, 20, 400, 20))
    current_hp_width = (player_data.hp / player_data.max_hp) * 400
    pygame.draw.rect(screen, GREEN, (300, 20, max(0, current_hp_width), 20))

# --- Vòng lặp chính ---
running = True
while running:
    screen.fill((50, 50, 50)) # Nền xám cho chuyên nghiệp hơn tí
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Nhấn phím số 1,2,3,4,5 để nâng cấp điểm
        if event.type == pygame.KEYDOWN and player_data.points > 0:
            if event.key == pygame.K_1:
                player_data.max_hp += 300
                player_data.hp = player_data.max_hp
                player_data.points -= 1
            elif event.key == pygame.K_2:
                player_data.technique += 1
                player_data.points -= 1
            elif event.key == pygame.K_3:
                player_data.speed += 1
                player_data.points -= 1
            elif event.key == pygame.K_4:
                player_data.agility += 1
                player_data.points -= 1
            elif event.key == pygame.K_5 and player_data.level >= 20:
                player_data.breathing += 1
                player_data.points -= 1

    # Giả lập đi bộ luyện tập để tăng Exp (Nhấn phím T)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_t]:
        if player_data.gain_exp(1):
            print("Lên cấp!")

    draw_ui()
    
    # Hướng dẫn tạm thời
    hint = font.render("Giữ 'T' để LUYỆN TẬP (Tăng Exp) | Nhấn 1-5 để NÂNG CẤP khi có điểm", True, WHITE)
    screen.blit(hint, (270, HEIGHT - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

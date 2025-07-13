import pygame
import random

pygame.init()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)


FONT = pygame.font.SysFont("arial", 24)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yacht Game - Pygame Version")

dice = [random.randint(1, 6) for _ in range(5)]
dice_locked = [False] * 5
reroll_count = 3
total_score = 0


categories = [
    "one", "two", "thr", "fou", "fiv", "six",
    "thr_of_a_kind", "fou_of_a_kind", "FullHouse",
    "smallstrate", "largestrate", "Yatchu", "chance"
]
used_categories = {}


dice_rects = [pygame.Rect(300 + i * 70, 400, 50, 50) for i in range(5)]


category_buttons = [pygame.Rect(50, 100 + i * 30, 200, 25) for i in range(len(categories))]


def draw_text(text, x, y, color=BLACK):
    label = FONT.render(str(text), True, color)
    screen.blit(label, (x, y))

def roll_dice():
    for i in range(5):
        if not dice_locked[i]:
            dice[i] = random.randint(1, 6)

def get_score(category, dice):
    from collections import Counter
    counts = Counter(dice)
    total = sum(dice)

    if category == "one":
        return dice.count(1) * 1
    elif category == "two":
        return dice.count(2) * 2
    elif category == "thr":
        return dice.count(3) * 3
    elif category == "fou":
        return dice.count(4) * 4
    elif category == "fiv":
        return dice.count(5) * 5
    elif category == "six":
        return dice.count(6) * 6
    elif category == "thr_of_a_kind":
        return total if 3 in counts.values() else 0
    elif category == "fou_of_a_kind":
        return total if 4 in counts.values() else 0
    elif category == "FullHouse":
        return 25 if sorted(counts.values()) == [2, 3] else 0
    elif category == "smallstrate":
        straights = [set([1,2,3,4]), set([2,3,4,5]), set([3,4,5,6])]
        return 30 if any(s.issubset(dice) for s in straights) else 0
    elif category == "largestrate":
        return 40 if sorted(dice) in ([1,2,3,4,5], [2,3,4,5,6]) else 0
    elif category == "Yatchu":
        return 50 if max(counts.values()) == 5 else 0
    elif category == "chance":
        return total
    return 0


running = True
while running:
    screen.fill(WHITE)


    for i in range(5):
            if dice_locked[i]:
                image=pygame.image.load("lock6 ({}).png".format(dice[i]))
                image = pygame.transform.scale(image, (50, 50))
                screen.blit(image, (dice_rects[i].x, dice_rects[i].y))
            else:
                image=pygame.image.load("pixil-frame-0 ({}).png".format(dice[i]))
                image = pygame.transform.scale(image, (50, 50))
                screen.blit(image, (dice_rects[i].x, dice_rects[i].y))


    for i, cat in enumerate(categories):
        color = RED if cat in used_categories else GRAY
        pygame.draw.rect(screen, color, category_buttons[i], border_radius=8) 
        draw_text(cat, category_buttons[i].x + 5, category_buttons[i].y + 2)


    draw_text(f"Reroll: {reroll_count}", 600, 100)
    draw_text(f"Total Score: {total_score}", 600, 140)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            for i in range(5):
                if dice_rects[i].collidepoint(pos):
                    dice_locked[i] = not dice_locked[i]


            for i, rect in enumerate(category_buttons):
                if rect.collidepoint(pos) and categories[i] not in used_categories:
                    score = get_score(categories[i], dice)
                    total_score += score
                    used_categories[categories[i]] = score
                    reroll_count = 3
                    dice = [random.randint(1, 6) for _ in range(5)]
                    dice_locked = [False] * 5

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and reroll_count > 0:
                roll_dice()
                reroll_count -= 1

    pygame.display.flip()

pygame.quit()

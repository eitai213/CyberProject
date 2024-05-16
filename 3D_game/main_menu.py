import pygame
from setting import *
from game import *
import sys

# הפעלת Pygame
pygame.init()

# יצירת חלון המשחק
screen = pygame.display.set_mode(RES)
pygame.display.set_caption('Treasure Hunt')

# הגדרת צבעים
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# פונקציה ליצירת אובייקט טקסט
def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


# פונקציה לצייר כפתור
def draw_button(screen, text, x, y, width_button, height_button, ic, ac, text_size=36):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width_button > mouse[0] > x - width_button and y + height_button > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x - (width_button // 2), y, width_button, height_button))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, ic, (x - (width_button // 2), y, width_button, height_button))

    small_text = pygame.font.Font(None, text_size)  # שימוש בפונט ברירת מחדל של Pygame
    text_surf, text_rect = text_objects(text, small_text)
    text_rect.center = (x, (y + (height_button / 2)))
    screen.blit(text_surf, text_rect)

    return False


# פונקציה להתחלת המשחק
def start_game():
    print("The game has started!")


# פונקציה להצגת מסך טעינה
def loading_screen():
    screen.fill(WHITE)
    large_text = pygame.font.Font(None, 72)
    text_surf, text_rect = text_objects("Loading...", large_text)
    text_rect.center = (HALF_WIDTH, HALF_HEIGHT)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def start_single_player_game():
    a = Game(screen=screen, treasure_place=treasure_place())
    a.run()



def create_server():
    pass


def join_to_other_server():
    pass


def start_multiplayer_game():
    pass





# לולאת המשחק הראשית
def main_menu():
    # הצגת מסך טעינה
    loading_screen()

    # תזמון זמן טעינה של 3 שניות לדוגמה
    pygame.time.delay(3000)

    while True:
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        if draw_button(screen, "Single Player Game", HALF_WIDTH, HALF_HEIGHT - 100, 400, 50, (0, 255, 0), (0, 200, 0)):
            start_single_player_game()

        if draw_button(screen, "Multiplayer Game", HALF_WIDTH, HALF_HEIGHT, 400, 50, (0, 255, 0), (0, 200, 0)):
            start_game()

        if draw_button(screen, "setting", HALF_WIDTH, HALF_HEIGHT + 100, 400,50, (100, 50, 50), (200, 50, 50)):
            pass

        if draw_button(screen, "Quit", HALF_WIDTH, HALF_HEIGHT + 200, 400, 50, (255, 0, 0), (200, 0, 0)):
            pygame.quit()
            sys.exit()

        pygame.display.update()



main_menu()

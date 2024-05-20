import pygame
from setting import *
from server import *
from  client import *
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

    if x + width_button // 2 > mouse[0] > x - width_button // 2 and y + height_button > mouse[1] > y:
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
    screen.fill((230, 200, 50))
    large_text = pygame.font.Font(None, 72)
    text_surf, text_rect = text_objects("Loading...", large_text)
    text_rect.center = (HALF_WIDTH, HALF_HEIGHT)
    screen.blit(text_surf, text_rect)
    pygame.display.update()




background = pygame.image.load('assets/background_Treasure_Hunt.png')
background = pygame.transform.scale(background, RES)
def draw_background():
    global background
    screen.blit(background, (0, 0))


def clean_the_window():
    screen.fill(WHITE)
    pygame.display.update()


def back_button():
    clean_the_window()
    main_menu()


def start_single_player_game():
    a = Game(screen=screen, treasure_place=treasure_place())
    a.run()



def create_server():
    clean_the_window()

    server = Server()
    client = Client()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if draw_button(screen, "Start", HALF_WIDTH, HALF_HEIGHT, 400, 50,(255, 255, 0),(0, 255, 0)):
            server.run_server()
            client.run_client()
            main_menu()
            break

        if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
            back_button()
            break

        pygame.display.update()


def join_to_other_server():
    pass



# לולאת המשחק הראשית של מסך ה-Multiplayer Game
def start_multiplayer_game():
    pygame.mouse.set_visible(True)
    print("ok!!!")
    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        if draw_button(screen, "create room", HALF_WIDTH + 300, HALF_HEIGHT, 300, 150, (255, 255, 0), (0, 255, 0)):
            create_server()
            break

        if draw_button(screen, "join", HALF_WIDTH - 300, HALF_HEIGHT, 300, 150, (255, 255, 0), (0, 255, 0)):
            join_to_other_server()
            break

        if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
            back_button()
            break

        print("not ok")
        pygame.display.update()




# לולאת המשחק הראשית
def main_menu():

    pygame.mouse.set_visible(True)

    while True:

        draw_background()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        if draw_button(screen, "Single Player Game", HALF_WIDTH, HALF_HEIGHT - 100, 400, 50, (255, 255, 0), (0, 200, 0)):
            clean_the_window()
            start_single_player_game()
            main_menu()
            break


        if draw_button(screen, "Multiplayer Game", HALF_WIDTH, HALF_HEIGHT, 400, 50, (255, 255, 0), (0, 200, 0)):
            clean_the_window()
            start_multiplayer_game()
            main_menu()
            break

        if draw_button(screen, "How To Play?", HALF_WIDTH, HALF_HEIGHT + 100, 400,50, (255, 255, 50), (0, 200, 0)):
            clean_the_window()

            text_lines = HOW_TO_PLAY_TEXT
            font = pygame.font.Font(None, 36)
            # יצירת רשימה לשמירת אובייקטי הטקסט ומיקומם על המסך
            text_objects = []

            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (400, 100 + i * 50)  # העמקת השורה ב-50 פיקסלים בין כל שורה לשורה
                text_objects.append((text_surface, text_rect))

            while True:
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
                    back_button()
                    break


        if draw_button(screen, "Quit", HALF_WIDTH, HALF_HEIGHT + 200, 400, 50, (255, 255, 0), (200, 0, 0)):
            pygame.quit()
            sys.exit()


        pygame.display.update()



loading_screen()


pygame.time.delay(3000)

main_menu()

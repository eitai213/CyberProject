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
GRAY = (200, 200, 200)
ACTIVE_COLOR = pygame.Color('dodgerblue2')

# הגדרת גופן
font = pygame.font.Font(None, 36)




text_boxes = []

# פונקציה ליצירת תיבת טקסט חדשה
def create_text_box(x, y):
    box = {'rect': pygame.Rect(x, y, 200, 50), 'color': GRAY, 'text': '', 'active': False}
    text_boxes.append(box)


# פונקציה לציור תיבות הטקסט
def draw_text_boxes(screen):
    for box in text_boxes:
        color = ACTIVE_COLOR if box['active'] else GRAY
        txt_surface = font.render(box['text'], True, BLACK)
        width = max(200, txt_surface.get_width() + 10)
        box['rect'].w = width
        screen.blit(txt_surface, (box['rect'].x + 5, box['rect'].y + 5))
        pygame.draw.rect(screen, color, box['rect'], 2)






"""//////////////////////////////////////////////////////////////////////"""


# פונקציה ליצירת אובייקט טקסט
def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def draw_text(text, x, y, text_size, color=BLACK):
    large_text = pygame.font.Font(None, text_size)
    text_surf, text_rect = text_objects(str(text), large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


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



def create_server(name_player):
    clean_the_window()

    server = Server()

    server_thread = threading.Thread(target=server.run_server, daemon=True)

    server_thread.start()

    draw_text(f"Server IP : {server.get_server_ip()}", HALF_WIDTH - 50, HALF_HEIGHT - 300, 80)

    client = Client(server_ip=server.get_server_ip(), name_player=name_player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if draw_button(screen, "Start", HALF_WIDTH, HALF_HEIGHT, 400, 50, (255, 255, 0), (0, 255, 0)):
            server.start = 1
            client.run_client()

            break

        if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
            back_button()
            break

        pygame.display.update()


def join_to_other_server(ip_server, name_player):
    clean_the_window()
    if ip_server:
        pass
    else:
        ip_server = discover_server()

    draw_text("waiting for the host,", HALF_WIDTH, HALF_HEIGHT - 50, 50)
    draw_text("to start the match", HALF_WIDTH, HALF_HEIGHT, 50)
    pygame.display.update()

    client = Client(server_ip=ip_server, name_player=name_player)
    if client.run_client():
        return
    else:
        clean_the_window()
        large_text = pygame.font.Font(None, 30)
        text_surf, text_rect = text_objects("server not found", large_text, (255, 0, 0))
        text_rect.center = (HALF_WIDTH - 300, HALF_HEIGHT - 20)
        screen.blit(text_surf, text_rect)
        pygame.display.update()
        start_multiplayer_game()





# לולאת המשחק הראשית של מסך ה-Multiplayer Game
def start_multiplayer_game():
    global active_box
    global text_boxes

    pygame.mouse.set_visible(True)

    create_text_box(HALF_WIDTH - 100, 50)
    create_text_box(HALF_WIDTH - 400, HALF_HEIGHT - 80)


    draw_text("input your name:", HALF_WIDTH, 35, 36)
    draw_text("input the IP server:", HALF_WIDTH - 300, HALF_HEIGHT - 100, 36)

    name_player = text_boxes[0]['text']
    ip_server = text_boxes[1]['text']


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for box in text_boxes:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if box['rect'].collidepoint(event.pos):
                        active_box = box
                        box['active'] = True
                    else:
                        box['active'] = False

                if event.type == pygame.KEYDOWN:
                    if box['active']:
                        if event.key == pygame.K_RETURN:
                            box['active'] = False
                            active_box = None
                        elif event.key == pygame.K_BACKSPACE:
                            box['text'] = box['text'][:-1]
                            pygame.draw.rect(screen, WHITE, (box['rect']))
                        else:
                            box['text'] += event.unicode


        if draw_button(screen, "create room", HALF_WIDTH + 300, HALF_HEIGHT, 300, 150, (255, 255, 0), (0, 255, 0)):
            create_server(name_player)
            pygame.mouse.set_visible(True)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
                    back_button()
                    break

                pygame.display.update()

        if draw_button(screen, "join", HALF_WIDTH - 300, HALF_HEIGHT, 300, 150, (255, 255, 0), (0, 255, 0)):
            join_to_other_server(ip_server=ip_server, name_player=name_player)
            pygame.mouse.set_visible(True)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
                    back_button()
                    break

                pygame.display.update()

        if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
            back_button()
            break

        draw_text_boxes(screen)

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
            pygame.mouse.set_visible(True)
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
                    back_button()
                    break
                pg.display.update()



        if draw_button(screen, "Multiplayer Game", HALF_WIDTH, HALF_HEIGHT, 400, 50, (255, 255, 0), (0, 200, 0)):
            clean_the_window()
            start_multiplayer_game()
            main_menu()
            break

        if draw_button(screen, "How To Play?", HALF_WIDTH, HALF_HEIGHT + 100, 400, 50, (255, 255, 50), (0, 200, 0)):
            clean_the_window()

            text_lines = HOW_TO_PLAY_TEXT
            font = pygame.font.Font(None, 50)
            # יצירת רשימה לשמירת אובייקטי הטקסט ומיקומם על המסך

            text_objects = []
            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = (HALF_WIDTH, 100 + i * 50)  # העמקת השורה ב-50 פיקסלים בין כל שורה לשורה
                text_objects.append((text_surface, text_rect))

            while True:
                screen.fill(WHITE)  # נקה את המסך בכל פריים

                for text_surface, text_rect in text_objects:
                    screen.blit(text_surface, text_rect)  # צייר את הטקסט מחדש בכל פריים

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if draw_button(screen, "back", HALF_WIDTH, HEIGHT - 100, 200, 50, (255, 255, 0), (0, 255, 0)):
                    back_button()
                    break

                pygame.display.update()


        if draw_button(screen, "Quit", HALF_WIDTH, HALF_HEIGHT + 200, 400, 50, (255, 255, 0), (200, 0, 0)):
            pygame.quit()
            sys.exit()


        pygame.display.update()



loading_screen()


pygame.time.delay(3000)

main_menu()

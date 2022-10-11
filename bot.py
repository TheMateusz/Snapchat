import threading
import pygame, sys
import pygame.locals
import time
from pyautogui import *
import pyautogui as pag
import pyautogui, pyperclip, keyboard

pygame.init()

WHITE = (255, 255, 255)
ACTIVE_COLOR = pygame.Color('dodgerblue1')
INACTIVE_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.Font(None, 24)

def draw_button(button, screen):
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])

def create_button(x, y, w, h, text, callback):
    text_surf = FONT.render(text, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'callback': callback,
        }
    return button

def dragUp(px, time=0.5):
    now = pag.position()
    pag.dragTo(now[0], now[1]-px, time, button='left')

def moveDown(px, time=0.5):
    now = pag.position()
    pag.moveTo(now[0], now[1]+px, time)

def moveUp(px, time=0.5):
    now = pag.position()
    pag.moveTo(now[0], now[1]-px, time)

def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    done = False
    number = 0
    loop = True
    yourMessage = "Hej, jesteś może bi lub less ?"

    def mess_send_loop():
        time.sleep(3)
        while not done:
            if pyautogui.locateOnScreen('new.png') != None:
                print("WIDZE")
                center = pyautogui.locateCenterOnScreen('new.png')
                pyautogui.click(center)
                pyperclip.copy(yourMessage)
                time.sleep(0.5)
                pag.hotkey('ctrl', 'v')
                time.sleep(0.2)
                pag.hotkey('enter')
                time.sleep(0.5)
                pag.press('escape')
            else:
                time.sleep(0.5)
                postBeforeDrag = pag.position()
                dragUp(300, time=0.5)
                pag.moveTo(postBeforeDrag[0], postBeforeDrag[1])                
            if (loop == False):
                break
            print("STOP PETLA")
            print(loop)

    def add_friend_loop():
        time.sleep(3)
        while not done:
            if pyautogui.locateOnScreen('add.png') != None:
                center = pyautogui.locateCenterOnScreen('add.png')
                pyautogui.click(center)
                time.sleep(0.5)
            else:
                time.sleep(0.5)
                postBeforeDrag = pag.position()
                dragUp(300, time=0.5)
                pag.moveTo(postBeforeDrag[0], postBeforeDrag[1])
            if (loop == False):
                break
            print("STOP PETLA")
            print(loop)

    def mess():
        print("mess start")
        nonlocal loop
        loop = True
        my_thread = threading.Thread(target=mess_send_loop, args=())
        my_thread.start()

    def add_friend(): 
        print("add start")
        nonlocal loop
        loop = True
        my_thread = threading.Thread(target=add_friend_loop, args=())
        my_thread.start()

    def stop(): 
        print("Zatrzymano procesy")
        nonlocal loop
        loop = False

    def quit_game():
        nonlocal done
        done = True

    mess_btn = create_button(10, 10, 400, 40, 'Pisanie wiadomości', mess)
    add_friend_btn = create_button(10, 60, 400, 40, 'Dodawanie znajomych', add_friend)
    stop_btn = create_button(10, 110, 400, 40, 'Zatrzymaj proces', stop)
    close_btn = create_button(10, 160, 400, 40, 'Zamknij program', quit_game)
    # A list that contains all buttons.
    button_list = [mess_btn, add_friend_btn, stop_btn, close_btn]

    while not done:
        for event in pygame.event.get():    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop()
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:
                        if button['rect'].collidepoint(event.pos):
                            button['callback']()
            elif event.type == pygame.MOUSEMOTION:
                for button in button_list:
                    if button['rect'].collidepoint(event.pos):
                        button['color'] = ACTIVE_COLOR
                    else:
                        button['color'] = INACTIVE_COLOR

        screen.fill(WHITE)
        for button in button_list:
            draw_button(button, screen)
        pygame.display.update()
        clock.tick(30)

main()
import pygame
import random
import os

import tkinter as tk
resolution_screen = tk.Tk()
SX = resolution_screen.winfo_screenwidth()
SY = resolution_screen.winfo_screenheight()

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SX, SY))
pygame.display.set_caption("Words")
        
direc = os.path.dirname(os.path.abspath(__file__)).replace('\'', '/')

w_order = []
for x in range(1324):
    while True:
        n = random.randint(0, 1324-1)
        if n in w_order:
            continue
        else:
            w_order.append(n)
            break
        
word_time_gap = [((.5)**(x/60))*8*((3+5*random.random())/8) for x in range(1324)]

class Word:
    def __init__(self, n_word) -> None:
        with open(f"{direc}/palabras_español.txt", "r", encoding = "utf-8") as file:
            self.word = file.read().split("\n")[w_order[n_word]]
        
        self.t = ((.5)**(n_word/60))*12
        self.v = .9/(self.t*60)
        self.pos = [.2 + .6*random.random(), -.1]
        
        font = pygame.font.Font(f"{direc}/CONSOLA.TTF", int(.08*SY))
        self.img = font.render(str(self.word), True, "black")
    
    def fall(self) -> None:
        self.pos[1] += self.v
        
    def draw(self) -> None:
        screen.blit(self.img, self.img.get_rect(center = (self.pos[0]*SX, self.pos[1]*SY)))
        
font = pygame.font.Font(f"{direc}/CONSOLA.TTF", int(.08*SY))
        
m = 0
nw = 0
words = []
playing = True

cword = ""
points = 0
while playing:
    m += 1/60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.dict['unicode'] == "\x08":
                cword = cword[0:-1]
            elif event.dict['unicode'].isalpha():
                cword += event.dict['unicode']
        
    # EVENTS
    if m > sum(word_time_gap[0:nw]):
        words.append(Word(nw))
        nw += 1
    
    for x in words[:]:
        if x.word == cword:
            words.remove(x)
            cword = ""
            points += 1
            continue
        
        if x.pos[1] > .78:
            playing = False
        x.fall()
    
    # DRAW
    screen.fill(tuple(130 for x in range(3)))
    pygame.draw.rect(screen, "black", (0, SY*.8, SX, SY*.2))
    
    for x in words:
        x.draw()
    
    img_points = font.render(str(points), True, "white")
    screen.blit(img_points, img_points.get_rect(bottomright = (SX-SX*.05, SY-SX*.05)))
    img_cword = font.render(str(cword), True, "white")
    screen.blit(img_cword, img_cword.get_rect(bottomleft = (SX*.05, SY-SX*.05)))
            
    pygame.display.update()
    clock.tick(60)

print(f"Puntos: {points}")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    screen.fill("black")
    
    font = pygame.font.Font(f"{direc}/CONSOLA.TTF", int(.15*SY))
    img = font.render("GAME OVER", True, "red")
    screen.blit(img, img.get_rect(center = (SX/2, SY/2)))
    
    pygame.display.update()
    clock.tick(60)
import pygame

running=True

pygame.init()

width,height=(500,500)

screen=pygame.display.set_mode((width,height))

pygame.display.set_caption('Snake Game')

import math

wCells=20
hCells=20

snakeS=[(5,5),(6,5),(7,5),(8,5)]

def grid(screen,xOffset,yOffset):
    for x in range(wCells+1):
        for y in range(hCells+1):
            if((x+y)%2==0):
                pygame.draw.rect(screen,(121, 98, 191),pygame.Rect((math.ceil(x*(width/wCells))+xOffset,math.ceil(y*(height/hCells))+yOffset),(math.ceil(width/wCells),math.ceil(height/hCells))),50)
            else:
                pygame.draw.rect(screen,(98, 131, 191),pygame.Rect((math.ceil(x*(width/wCells))+xOffset,math.ceil(y*(height/hCells))+yOffset),(math.ceil(width/wCells),math.ceil(height/hCells))),50)

def drawSnake(screen,snakeS,xOffset,yOffset):
    for i,e in enumerate(snakeS[:-1]):
        if(e[0]-snakeS[i+1][0] != 0):
            v=sign((snakeS[i+1][0]*(math.ceil(width/wCells)))-(e[0]*(math.ceil(width/wCells))))
            #print(sign(v),v)
            for z in range(abs(math.floor((snakeS[i+1][0]*math.ceil((width/wCells)))-(e[0]*math.ceil((width/wCells)))))):
                pygame.draw.circle(screen,(0, 0, 0),(e[0]*math.ceil((width/wCells))+xOffset+math.ceil((width/wCells)/2)+(z*v),e[1]*math.ceil(height/hCells)+yOffset+math.ceil((height/hCells)/2)),math.ceil((height/hCells)/4))
        else:
            v=sign((snakeS[i+1][1]*math.ceil(height/hCells))-(e[1]*math.ceil(height/hCells)))
            for z in range(abs(math.floor((snakeS[i+1][1]*math.ceil(height/hCells))-(e[1]*math.ceil(height/hCells))))):
                pygame.draw.circle(screen,(0, 0, 0),(e[0]*math.ceil(width/wCells)+xOffset+math.ceil((width/wCells)/2),e[1]*math.ceil(height/hCells)+(z*v)+yOffset+math.ceil((height/hCells)/2)),math.ceil((height/hCells)/4))

import os

#print(os.listdir('letters')[:2] + os.listdir('letters')[2:])

l=os.listdir('letters')
l.remove('.DS_Store')

charImgs=[pygame.transform.scale(pygame.image.load('letters/'+i),(32,32)) for i in l]


#input(charImgs)

#input(l)

abcs='EM 8o9O:R4c57VA62sr3eG10'

hsp=1
vsp=0

keys=[]

def sign(x):
    if(x==0):
        return 0
    return abs(x)/x

def tick(snakeS,hsp,vsp):
    for i in range(len(snakeS[:-1])):
        #print('h')
        snakeS[i] = snakeS[i+1]
    snakeS[-1]=(snakeS[-1][0]+sign(hsp),snakeS[-1][1]+sign(vsp))
    return snakeS

appleX=0
appleY=0

import random

def makeApple(hsp,vsp):
    appleX=random.randint(0,wCells-1)
    appleY=random.randint(0,hCells-1)
    while ((appleX,appleY) in snakeS):
        appleX+=1
        if(appleX>wCells):
            appleX=0
            appleY+=1
        if(appleY>hCells):
            hsp=0
            vsp=0
    return hsp,vsp,(appleX,appleY)

def drawApple(apple,screen,xOffset,yOffset):
    pygame.draw.circle(screen,(255,0,0),((apple[0]*math.ceil(width/wCells))+xOffset+math.ceil((width/wCells)/2),(apple[1]*math.ceil(height/hCells))+yOffset+math.ceil((height/hCells)/2)),math.ceil((height/hCells)/4))

def gameOver(screen):
    print((width/2)-((len('GAME OVER')-1)),(height/2)-32)
    drawText(screen,'GAME OVER',(width/2)-((len('GAME OVER')-1)*16),(height/2)-32)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if((event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN) or (event.type==pygame.QUIT)):
                quit()

def check(apple,snakeS,hsp,vsp,screen):
    if(snakeS[-1]==apple):
        snakeS.insert(0,[])
        hsp,vsp,apple=makeApple(hsp,vsp)
    elif(snakeS[-1][0]>(wCells-1) or snakeS[-1][0]<0 or snakeS[-1][1]>(hCells-1) or snakeS[-1][1]<0):
        gameOver(screen)
        return 0,0,snakeS,apple
    else:
        for i in snakeS[:-1]:
            if(i==snakeS[-1]):
                gameOver(screen)
                return 0,0,snakeS,apple
    return hsp,vsp,snakeS,apple

def drawText(screen,str,x,y):
    for i in range(len(str)):
        screen.blit(charImgs[abcs.find(str[i])],(x+(charImgs[0].get_width()*i),y))

tickWait=0.1
tickF=0
deltaTime=0
getTicksLastFrame=0

xOffset=0
yOffset=0

hsp,vsp,apple=makeApple(hsp,vsp)

while running:
    t = pygame.time.get_ticks()
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            running=False
        elif(event.type==pygame.KEYDOWN):
            keys.append(event.key)
        elif(event.type==pygame.KEYUP):
            keys.remove(event.key)
    if(len(keys) > 0):
        if(snakeS[-1][1]-snakeS[-2][1] != 0):
            if(pygame.K_LEFT in keys):
                hsp=-1
                vsp=0
            elif(pygame.K_RIGHT in keys):
                hsp=1
                vsp=0
        if(snakeS[-1][0]-snakeS[-2][0] != 0):
            if(pygame.K_UP in keys):
                hsp=0
                vsp=-1
            elif(pygame.K_DOWN in keys):
                hsp=0
                vsp=1
    #print(hsp,vsp)
    tickF+=deltaTime
    #print(tickF)
    if(tickF>=tickWait):
        tickF=0
        hsp,vsp,snakeS,apple=check(apple,snakeS,hsp,vsp,screen)
        snakeS=tick(snakeS,hsp,vsp)
    screen.fill((255,255,255))
    grid(screen,xOffset,yOffset)
    drawApple(apple,screen,xOffset,yOffset)
    drawSnake(screen,snakeS,xOffset,yOffset)
    drawText(screen,'score: '+str(len(snakeS)-4),0,0)
    pygame.display.flip()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

# -*- coding: utf-8 -*-

import pgsurface
import pygame
import sys
import random
from threading import Timer
from pygame.locals import * #导入一些常用的函数和常量
from sys import exit #向sys模块借一个exit函数用来退出程序

#地图背景
back_ground = [];
#障碍物数组
block = [];
#背景云数组
cloud = [];
#鸡腿数组
c_thigh = [];
#地图宽度
screen_wight = 35
#游戏是否开始
game_start = 0;
#得分
score = 0;
#鸡腿数
chicken_cont = 0;

#Version major
V_Major = 1
#Version minor
V_Minor = 1

#定义几个基本颜色
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)

################################################################
#Pallas cat class
#参数说明：new_g:默认重力加速度
################################################################
class CPallas:
    jump = 0;
    pos_x = 0;
    pos_y = 0;
    g = 9;
    up_force = 0;
    button = 480;
    pic_n = 0;#代表pallas当前显示图片的编号
    def __init__(self,new_g):
        self.jump = 0;
        self.pos_x = 100;
        self.pos_y = 480;
        self.g = new_g;
        self.pic_n = 0;
    ################################################################
    #画一个Pallas
    #参数说明：
    ################################################################
    def DrawPallas(self,screen,tick):
        #self.Dynamic(tick);

        if self.jump == 1:
            screen.blit(pallas_ball,(self.pos_x,self.pos_y));
        else:
            if self.pic_n < 10 or GetGameStart() == 0:
                screen.blit(pallas_ball,(self.pos_x,self.pos_y));
            else:
                screen.blit(pallas_ball_rev,(self.pos_x,self.pos_y));
            if(GetGameStart() == 1):
                self.pic_n = self.pic_n + 1;
            if self.pic_n >= 20:
                self.pic_n = 0;            
    ################################################################
    #碰撞检测
    #参数说明：
    ################################################################
    def CollisionProcess(self,screen):
        for i in range(1,5):
            tag_left = 50 + i * 20;
            tag_butt = 500 - 20;

            if(block[i] == 1 or block[i] == 2):
                if(self.pos_x + 50 >= tag_left and self.pos_x + 50<= tag_left + 70):
                    if(self.pos_y +30 >= tag_butt):
                        return 1;
                    return 0;
        return 0;
    ################################################################
    #鸡腿的碰撞检测
    #参数说明：
    ################################################################
    def ChickenthighCollision(self,screen):
        for i in range(2,4):
            tag_left = 50 +  i * 20;
            tag_butt = 500 - 150;

            if(c_thigh[i] == 1):
                if(self.pos_y <= tag_butt):
                    c_thigh[i] = 2;
                    return 1;
                return 0;
        return 0;
    ################################################################
    #运动解算
    #参数说明：
    ################################################################
    def Dynamic(self,tick):
        self.pos_y = round(self.pos_y - self.up_force);
        if(self.pos_y >= self.button):
            self.pos_y = self.button;
            self.jump = 0;
        self.up_force = self.up_force - self.g * tick;
    ################################################################
    #跳跃的处理
    #参数说明：
    ################################################################
    def Jump(self,jumper):
        if self.jump == 0:
            self.up_force = jumper;
            self.jump = 1;
################################################################
#检测游戏是否开始
#参数说明：
################################################################
def GetGameStart():
    global game_start;

    return game_start;
################################################################
#设置游戏开始
#参数说明：set：设置
################################################################
def SetGameStart(set):
    global game_start;

    game_start = set;
################################################################
#生成指定范围内的随机数
#参数说明：lower：随机数范围下限
#        upper：随机数范围上限
################################################################
def randomer(lower,upper):
    return round(random.uniform(lower,upper))

def unSameRandomer(lower,upper,diff):
    res = randomer(lower,upper);
    while (res < before + diff and res > before - diff):
        res = randomer(lower,upper);
    return res;
    

################################################################
#创建一个空地图背景
#参数说明：lower：随机数范围下限
#        upper：随机数范围上限
################################################################
def CreataMap():
    for i in range(screen_wight):
        back_ground.append(randomer(0,5));
    for i in range(screen_wight):
        block.append(0);
    for i in range(screen_wight):
        cloud.append(0);
    for i in range(screen_wight):
        c_thigh.append(0);

################################################################
#Exit app
#参数说明：Null
################################################################
def exitApp():
    sys.exit()

################################################################
#Event process
#参数说明：pallas:
################################################################
def EventProcess(pallas):
    for event in pygame.event.get():
            if event.type == QUIT:
                exitApp()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exitApp()
                elif event.key == K_SPACE:
                    ##Game over的时候是不能跳的
                    if GetGameStart() != 2:
                        pallas.Jump(20);
                        #未开始游戏的时候可以通过这个启动游戏
                        if GetGameStart() == 0:
                            SetGameStart(1);                  
                elif event.key == K_a:
                    if GetGameStart() == 0:
                        SetGameStart(1);
                    elif GetGameStart() == 1:
                        SetGameStart(0);
                    elif GetGameStart() == 2:
                        ResetGame();
################################################################
#画鸡腿得分
#参数说明：Null
################################################################
def DrawChickenScore(screen):
    screen.blit(chicken_thigh,(50,205));
    pgsurface.DrawString(screen,":"+str(chicken_cont),30,0,0,0,110,200);                        
################################################################
#reDrawMap
#参数说明：Null
################################################################
cloud_counter = 0;

def UpdataMap():
    global cloud_counter;
    #生成地图背景
    back_ground.append(randomer(0,5));
    del back_ground[0]

    #生成障碍物
    #如果前面若干个已经有障碍物了，则取消障碍物的生成，以免障碍太多
    global screen_wight;
    count = 0;
    for i in range(screen_wight - 20 , screen_wight):
        count = count + block[i];
    #没有障碍，则生成一个
    if count == 0:
        blocker = randomer(0,500)
        if(blocker >= 98 and blocker < 110):
            block.append(2);
        elif(blocker >= 145 and blocker < 146):
            block.append(1);
        elif(blocker >= 351 and blocker < 353):
            block.append(1);
        elif(blocker >= 480 and blocker < 489):
            block.append(1);
        else:
            block.append(0);
    else:
        block.append(0);
    del block[0]

    #生成鸡腿
    blocker = randomer(0,50);
    if(blocker == 32):
        c_thigh.append(1);
    else:
        c_thigh.append(0);
    del c_thigh[0];

    #生成云
    if cloud_counter >= 5:
        UpdataCloud();
        cloud_counter = 0;
    else:
        cloud_counter = cloud_counter + 1;

def UpdataCloud():
    #生成背景云
    blocker = randomer(0,100);
    if(blocker >=50 and blocker <62):
        if cloud[screen_wight - 1] != 1 and cloud[screen_wight - 2] != 1 and cloud[screen_wight - 3] != 1:
            cloud.append(1);
        else:
            cloud.append(0);
    else:
        cloud.append(0);
    del cloud[0];

def DrawMap(screen):
    global back_ground
    #先画背景
    for i in range(screen_wight):
        pygame.draw.line(screen,black,(50 + i*20,500+back_ground[i]) , (50 + i * 20 + 20,500+back_ground[i]) , 2)
        if(block[i] == 1):
            screen.blit(rock_1,(50 + i * 20,500 - 20));
        elif(block[i] == 2):
            screen.blit(rock_2,(50 + i * 20,500 - 20));
        if cloud[i] == 1:
            screen.blit(cloud_1,(50 + i * 20,500 - 200));
        if c_thigh[i] == 1:
            screen.blit(chicken_thigh,(50 + i * 20 ,500 - 150));
        elif c_thigh[i] == 2:
            pgsurface.DrawString(screen,"10",30,0,0,0,50 + i * 20,500 - 150)
################################################################
#   Set score
################################################################
def SetScore(type,point):
    global score;
    if type == 0:
        score = score + point;
    else:
        score = point;

################################################################
#   Reset game
################################################################
def ResetGame():

    CreataMap();
    SetGameStart(0);
    SetScore(1,0);
    chicken_cont = 0;
################################################################
#欢迎画面
#参数说明：screen
################################################################
def DrawWelcomeScreen(screen):
    pgsurface.DrawString(screen,"Jumping Pallas",35,0,0,0,300,180);
    pgsurface.DrawString(screen,"V"+str(V_Major)+"."+str(V_Minor),16,0,0,0,390,240);
    pgsurface.DrawString(screen,"Press Space to start and jump",16,0,0,0,310,270);
    pgsurface.DrawString(screen,"Press A to restart",16,0,0,0,350,300);
    pgsurface.DrawString(screen,"Press ESC to escape",16,0,0,0,330,330);

################################################################
#   Main process
################################################################

screen = pgsurface.InitSystem(800,600,0,"Jumping Pallas")

topScreen = pgsurface.cTopMenu()
cPallas = CPallas(0.06);
ResetGame();

#装入主要的图像元素
#装入pallas
pallas_ball = pygame.image.load("pallas_1_gray.png").convert_alpha();
pallas_ball.set_colorkey(white);
pallas_ball = pallas_ball.convert_alpha();

pallas_ball_rev = pygame.image.load("pallas_2.bmp").convert_alpha();
pallas_ball_rev.set_colorkey(white);
pallas_ball_rev = pallas_ball_rev.convert_alpha();

#装入其他元素
#装入石头
rock_1 = pygame.image.load("rock_1.png").convert_alpha();
rock_1.set_colorkey(white);
rock_1 = rock_1.convert_alpha();

rock_2 = pygame.image.load("rock_2.png").convert_alpha();
rock_2.set_colorkey(white);
rock_2 = rock_2.convert_alpha();
#装入云
cloud_1 = pygame.image.load("cloud.png").convert_alpha();
cloud_1.set_colorkey(white);
cloud_1 = cloud_1.convert_alpha();
#装入鸡腿
chicken_thigh = pygame.image.load("chickenthigh.png").convert_alpha();
chicken_thigh.set_colorkey(white);
chicken_thigh = chicken_thigh.convert_alpha();

#减速器计时器初始化
dealycount = 0;

clock = pygame.time.Clock();

#########################3
# Main loop
while True:
    EventProcess(cPallas);
    screen.fill(white)#清空窗口
    pygame.Surface.convert_alpha(screen);
    screen.set_alpha(128);

    if (GetGameStart() == 0):
        DrawWelcomeScreen(screen);
    else:
        pgsurface.DrawString(screen,"score:" + str(score),20,0,0,0,600,200);
        DrawChickenScore(screen);
        if (GetGameStart() == 1):
            dealycount = dealycount + 1;
            if(dealycount >= 5):
                
                UpdataMap();
                SetScore(0,1);
                dealycount = 0;
                #检测碰撞事件
                if(cPallas.CollisionProcess(screen) == 1):
                    SetGameStart(2);
                #吃到鸡腿
                if(cPallas.ChickenthighCollision(screen) == 1):
                    SetScore(0,10);
                    chicken_cont = chicken_cont + 1;
        if(GetGameStart() == 2):
            pgsurface.DrawString(screen,"Game Over",30,0,0,0,300,200);
    
    tick = clock.tick()
    #pgsurface.DrawString(screen,"tick:" + str(tick),20,0,0,0,100,100);

    DrawMap(screen);
    cPallas.Dynamic(tick);
    cPallas.DrawPallas(screen,11);
    pygame.display.update()#刷新一下画面
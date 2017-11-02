# -*- coding: utf-8 -*-

import pygame
import sys
import time
from pygame.locals import * #导入一些常用的函数和常量
from sys import exit #向sys模块借一个exit函数用来退出程序

################################################################
#   Global Alrgument
################################################################
mouse_pos_x = 0;
mouse_pos_y = 0;

class nonAgumentMessage:
    M_QUIT = 1;

################################################################
#Init PyGame
#参数说明：Screen_X、Screen_Y     屏幕分辨率
#         screen_pos            全屏还是窗口。1为全屏，2为窗口
#        title                  窗体标题
################################################################
def InitSystem(Screen_X,Screen_Y,screen_pos,title):
    pygame.init() #初始化pygame
    screen = pygame.display.set_mode((Screen_X, Screen_Y), 0, 32)#创建了一个窗口
    pygame.display.set_caption(title)#设置窗口标题

    return screen

################################################################
#Draw string
#参数说明：screen    窗体实例
#        strD      字符串
#        size      字号
#        nR        RGB颜色R
#        nG        RGB颜色G
#        nB        RGB颜色B
#        nX        位置X
#        nY        位置Y
################################################################
def DrawString(screen,strD,size,nR,nG,nB,nX,nY):
    font_temp = pygame.font.SysFont("arial", size)
    strData = font_temp.render(strD,True,(nR,nG,nB))
    screen.blit(strData,(nX,nY))

################################################################
#   Button class
################################################################
class cButton:
    top = 0;
    left = 0;
    weight = 0;
    hight = 0;
    
    colorR = 255;
    colorG = 255;
    clolrB = 255;
    buttonString = "simple"
    buttomStringSize = 16

    def __init__(self,nX,nY,nW,nH,R,G,B,string,ssize):
        self.top = nY
        self.left =nX
        self.hight = nH
        self.weight = nW
        self.colorR = R
        self.colorG = G
        self.clolrB = B
        self.buttonString = string
        self.buttomStringSize = ssize
    ##########################################################
    #   Detective locate in button zone
    ##########################################################    
    def inButton(self,nX,nY):
        print("x=",self.left,"Y=",self.top,"right=",self.weight+self.left,"buttom=",self.top+self.hight);
        if nX >= self.left and nX <= self.left + self.weight:
            if nY >= self.top and nY <= self.top + self.hight:
                return 1
        return 0
    ##########################################################
    #   Draw a button
    ########################################################## 
    def drawButton(self,screen):
        #draw rect
        my_rect=pygame.Rect(self.left,self.top,self.weight,self.hight)
        pygame.draw.rect(screen,[255,255,255],my_rect,3)
        #then,draw string
        DrawString(screen,self.buttonString,self.buttomStringSize,self.colorR,self.colorG,self.clolrB,self.left + round(self.weight/2) - round(len(self.buttonString)/2*self.buttomStringSize/2),self.top + round(self.hight/2) - round(self.buttomStringSize/2))

################################################################
#   Data list class
################################################################
class cList:
    left = 0;
    top = 0;
    right = 0;
    button = 0;
    listLen = 0;#表单的列数
    list_type = 0;#表单格式。0为带外框仅有竖线网格。1为镂空。2为仅有外框。3为无外框有横线

    str_size = 16;#默认16号字体
    element_weight = [];
    ##########################################################
    #   Init basic List
    ########################################################## 
    def __init__(self,x,y,right,button,strsize,lens,type):
        self.left = x;
        self.top = y;
        self.right = right;
        self.button = button;
        self.listLen = lens;
        self.str_size = strsize;
        self.list_type = type;

        for i in range(0,lens):
            self.element_weight.append(round(self.right/self.listLen));
    ##########################################################
    #   Draw a line in list
    ########################################################## 
    def DrawLine(self,screen,source,line):
        weight = self.left + 6;
        y_offset = self.top + 2 + (self.str_size + 10) * (line - 1);
        for i in range(self.listLen):
            DrawString(screen,source[i],self.str_size,167,167,167,weight,y_offset);
            weight = weight + self.element_weight[i];
    ##########################################################
    #   Set weight
    ##########################################################
    def SetElementWeight(self,weight,block):
        if weight >= self.right:
            return 0;
        if block > self.listLen:
            return 0;
        
        self.element_weight[block - 1] = weight;

        seto = 0;
        for i in range(0 , block):
            seto = seto + self.element_weight[i];
        for i in range(block,self.listLen):
            self.element_weight[i] = (self.right - seto) / (self.listLen - block);
        return 1;
    ##########################################################
    #   Draw List's block
    ########################################################## 
    def DrawBlock(self,screen):
        
        #带外框和竖线网格
        if self.list_type == 0:
            #画围框
            my_rect=pygame.Rect(self.left,self.top,self.right,self.button)
            pygame.draw.rect(screen,[255,255,255],my_rect,3)
            x = self.left;
            #画分割线
            for i in range(self.listLen - 1):
                x = x + self.element_weight[i];
                pygame.draw.line(screen,(255,255,255),(x,self.top),(x,self.top + self.button),1)
        #全镂空
        elif self.list_type == 1:
            return 1;
        elif self.list_type == 2:
            #画围框
            my_rect=pygame.Rect(self.left,self.top,self.right,self.button)
            pygame.draw.rect(screen,[255,255,255],my_rect,3)
        elif self.list_type == 3:
            y = self.top + 5;

            my_rect=pygame.Rect(self.left,self.top,self.right,self.button)
            pygame.draw.rect(screen,[255,255,255],my_rect,3)
            for i in range(round(self.button/(self.str_size + 10)) -  1):
                y = self.top + 5 + (self.str_size + 10) * (i + 1);
                pygame.draw.line(screen,(255,255,255),(self.left,y),(self.left + self.right,y),1)
                
################################################################
#   Screen class
################################################################
class cTopMenu:
    quitButton = cButton(240,120,70,70,167,167,167,u"Quit",16)
    quitMessage = 0;

    enumMessage = nonAgumentMessage();
    def __init__(self):
        self.quitMessage = 0;
    def paintString(self,screen):
        DrawString(screen,time.strftime("%Y-%m-%d", time.localtime()),16,255,167,167,20,15)
        DrawString(screen,time.strftime("%H:%M:%S", time.localtime()),40,255,25,25,20,50)
        DrawString(screen,u"X:" + u" " + str(mouse_pos_x),16,255,167,167,20,150)
        DrawString(screen,u"Y:" + u" " + str(mouse_pos_y),16,255,167,167,20,170) 
    def paint(self,screen):
        #Draw rect rim
        my_rect=pygame.Rect(10,10,300,100)
        pygame.draw.rect(screen,[255,255,255],my_rect,3)
        self.quitButton.drawButton(screen)

    def getSurfaceMessage(self):
        res = self.quitMessage;
        self.quitMessage = 0;
        return res;
    def insertMessage(self,messaged):
        self.quitMessage = messaged;
        return 1;
    def pgEventProcess(self):
        global mouse_pos_x;
        global mouse_pos_y;

        for event in pygame.event.get():
            if event.type == QUIT:
                self.insertMessage(1);#接收到退出事件后退出程序
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.insertMessage(1);
            if event.type == MOUSEMOTION:#mouse move
                mouse_pos_x,mouse_pos_y = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:#mouse button down
                mouse_prosess = pygame.mouse.get_pressed()
                if mouse_prosess[0] == 1:
                    if cTopMenu.quitButton.inButton(mouse_pos_x,mouse_pos_y) == 1:
                        self.insertMessage(1);
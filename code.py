#!/usr/bin/env python
# coding: utf-8

# Have a seat, drink a cup of tea and enjoy my code ^^

# In[1]:


#import
import pygame as pg, sys
from pygame.locals import *
from pygame import mixer
import os,random,numpy as np
import math


# In[2]:


#init
pg.init()
screen_w,screen_h=1600,900
state='intro'
screen=pg.display.set_mode((screen_w,screen_h))
pg.display.set_caption('Earth Saver')

#time
FPS=60
ticks=0
clock=pg.time.Clock()
start_tick=pg.time.get_ticks()
font_time=pg.font.SysFont('Consolas',60)
frequency=2
Time=30

#point
points=[]
for i in range(3):
    points.append(0)
font_point=pg.font.SysFont('Kid Games Regular',80)
font_point_outro=pg.font.SysFont('Kid Games Regular',100)
#life
life_limit=3
life=life_limit
life_timestamp=-999


# In[3]:


#functions
def Scale(img,Scale):
    (w,h)=(img.get_width(),img.get_height())
    img=pg.transform.scale(img,(w/Scale,h/Scale))
    return img

def DisplayImage(img,posx,posy):
    (w,h)=(img.get_width(),img.get_height())
    screen.blit(img,(posx-w/2,posy-h/2))

def is_over(rect,pos):
    return True if rect.collidepoint(pos[0], pos[1]) else False

def is_rect_over(rect1,rect2):
    return True if rect1.colliderect(rect2) else False

def getsize(image):
    return (image.get_width(),image.get_height())

def load_images(path_to_directory,id):
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.png'):
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = (pg.image.load(path).convert_alpha(),id)
    return image_dict

def calc_dis(a,b):
    return float(((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5)

def calc_step(cat,bin,speed):
    dis=calc_dis(cat,bin)
    time=float(dis)/speed
    if time<=0.0000001:
        return (0,0)
    return (int((bin[0]-cat[0])/time), int((bin[1]-cat[1])/time))
    """rad=math.atan2(bin[1]-cat[1],bin[0]-cat[0])
    dis=math.hypot(bin[0]-cat[0],bin[1]-cat[1])
    dis=int(dis)
    dx=math.cos(rad)
    dy=math.sin(rad)
    if dis==0:
        return (0,0)
    else: return (dx*speed,dy*speed)"""
    
def overlap_check(rect):
    global Trash_temp,Bin_images,Cat
    for trash in Trash_temp:
        if is_rect_over(rect,trash[1]):
            return 0
    for bin in Bin_images:
        if is_rect_over(rect,bin[2]):
            return 0
    if is_rect_over(rect,Cat[1]):
            return 0
    return 1

def overlap_bin_check(rect,id):
    global Bin_images
    for bin in Bin_images:
        if id!=bin[1] and is_rect_over(rect,bin[2]):
            return 1
    if id!=3 and is_rect_over(Cat[1],rect):
        return 1
    return 0

def is_circle_over(pos,center,radius):
    dis=math.sqrt((pos[0]-center[0])**2 + (pos[1]-center[1])**2)
    return dis<=radius


# In[4]:


#graphics intro

screen_intro=pg.image.load('sources/screen_intro.png').convert_alpha()
screen_intro=pg.transform.scale(screen_intro,(screen_w,screen_h))

intro_start=pg.image.load('sources/start.png').convert_alpha()
intro_start=Scale(intro_start,2.5)
(start_w,start_h)=getsize(intro_start)
start_rect=pg.Rect(0,0,start_w,start_h)
start_rect.center=(screen_w/2,380)
intro_start2=Scale(intro_start,0.8)
start_mask=0

intro_ins=pg.image.load('sources/intro_instruction.png').convert_alpha()
intro_ins=Scale(intro_ins,2.3)
(ins_w,ins_h)=getsize(intro_ins)
ins_rect=pg.Rect(0,0,ins_w,ins_h)
ins_rect.center=(screen_w/2,550)
intro_ins2=Scale(intro_ins,0.8)
ins_mask=0


# In[5]:


#graphics instruction

ins_load=load_images("sources/ins",0)
ins_pages=[]
for ins in ins_load:
    ins_pages.append(ins_load[ins][0])
ins_tmp=0

back_center=(85,705)
front_center=(1515,705)
ins_radius=80

quit_center=(1348,85)
quit_radius=60


# In[6]:


#graphics main

screen_main=pg.image.load('sources/screen_main.png').convert_alpha()
screen_main=pg.transform.scale(screen_main,(screen_w,screen_h))
limy=230

glove=pg.image.load('sources/glove.png').convert_alpha()
glove=Scale(glove,10)
(glove_w,glove_h)=getsize(glove)
glove_rect=pg.Rect(0,0,glove_w,glove_h) 

Trash_load=load_images("sources/trash_0",0)|load_images("sources/trash_1",1)|load_images("sources/trash_2",2)
Trash_images=[]
Trash_init=10
Trash_tmp_choose=-1
for trash in Trash_load:
    Trash_images.append(Trash_load[trash])
Trash_temp=[]

bin_x=1050
bin_y=710
bin_dis=210
Bin_images=[]
for i in range(3):
    bin_file_name='sources/Bin/'+str(i)+'.png'
    bin_image=pg.image.load(bin_file_name)
    bin_image=Scale(bin_image,4)
    (bin_w,bin_h)=getsize(bin_image)
    Bin_images.append((bin_image,i,pg.Rect(bin_x+i*bin_dis,bin_y,bin_w,bin_h)))
Bin_tmp_choose=-1

hearts=[]
for i in range(1,4):
    heart_file_name='sources/heart/'+str(i)+'.png'
    heart_image=pg.image.load(heart_file_name)
    heart_image=Scale(heart_image,4)
    (heart_w,heart_h)=getsize(heart_image)
    hearts.append(heart_image)

cat_images=[]
for i in range(3):
    cat_file_name='sources/cat/cat_'+str(i)+'.png'
    img=pg.image.load(cat_file_name)
    img=Scale(img,15)
    (cat_w,cat_h)=getsize(img)
    cat_images.append(img)
cat_choose=-1
(cat_w,cat_h)=getsize(cat_images[2])
Cat=(cat_images[2],pg.Rect(0,0,cat_w,cat_h))
cat_sleep_pos=(300,300)
Cat[1].center=cat_sleep_pos
cat_init_speed=6
cat_speed_a=1.1
cat_speed_frequency=5
cat_sleep=6
cat_aim=(Bin_images[0][2].x,Bin_images[0][2].y)
cat_sleep_timestamp=0
cat_awake=0
cat_old_pos=cat_sleep_pos
cat_state=2

marks=[]
marks.append(Scale(pg.image.load('sources/0.png').convert_alpha(),2))
marks.append(Scale(pg.image.load('sources/1.png').convert_alpha(),2))
marks_temp=[]
mark_last=FPS*0.3


# In[7]:


#graphic pause

pause=Scale(pg.image.load('sources/Pause.png').convert_alpha(),5)
(pause_w,pause_h)=getsize(pause)
pause_rect=pg.Rect(0,0,pause_w,pause_h)
pause_rect.center=(70,60)
pause_radius=55

resume=pg.image.load('sources/resume.png').convert_alpha()
resume_home_center=(340,440)
resume_resume_center=(800,450)
resume_again_center=(1230,450)
resume_radius=140

mute=Scale(pg.image.load('sources/mute.png').convert_alpha(),5)
(mute_w,mute_h)=getsize(mute)
mute_rect=pg.Rect(0,0,mute_w,mute_h)
mute_rect.center=(180,60)
mute_radius=55
unmute=Scale(pg.image.load('sources/unmute.png').convert_alpha(),5)

sound_state=0

hint_load=load_images("sources/hint",0)
hints=[]
for item in hint_load:
    (item_w,item_h)=getsize(hint_load[item][0])
    item_rect=pg.Rect(0,0,item_w,item_h)
    item_rect.center=(screen_w/2,screen_h/2)
    hints.append((hint_load[item][0],item_rect))
hints_choose=-1


# In[8]:


#graphic outro
screen_outro=pg.image.load('sources/screen_outro.png').convert_alpha()
screen_outro=Scale(screen_outro,3.5)
screen_outro_background=pg.image.load('sources/screen_outro_back.png').convert_alpha()
again_outro_rect=pg.Rect(640,570,300,130)
home_center=(530,660)
home_radius=80


# In[9]:


#sounds

#intro
intro_click=mixer.Sound("sources/sfx/start_pop.mp3")
intro_click.set_volume(0.3)

#main game
drag=mixer.Sound("sources/sfx/drag.mp3")
drag.set_volume(0.3)
res_sound=[]
res_sound.append(mixer.Sound("sources/sfx/incorrect.mp3"))
res_sound.append(mixer.Sound("sources/sfx/correct.mp3"))
res_sound[0].set_volume(0.5)

crash_sound=mixer.Sound("sources/sfx/crash.mp3")
crash_sound.set_volume(0.2)

cat_sound=mixer.Sound("sources/sfx/cat.mp3")
cat_signal=0

#outro
victory=mixer.Sound("sources/sfx/VICTORY.mp3")


# In[10]:


#reset
def reset():
    global ticks,life,Cat,cat_speed,points,Trash_temp,Bin_images,marks_temp,sound_state
    ticks=0
    life=life_limit
    Trash_temp.clear()
    marks_temp.clear()
    Cat[1].center=cat_sleep_pos
    for i in range(3):
        Bin_images[i][2].center=(bin_x+i*bin_dis,bin_y)
        points[i]=0
    sound_state=0
    mixer.music.stop()
    mixer.music.load("sources/sfx/background.mp3")
    mixer.music.play(-1)


# In[11]:


#intro
def intro():
    global state,start_mask,ins_mask,ins_tmp,ticks
    for event in pg.event.get():
        if event.type==QUIT:
            pg.quit()
            sys.exit()
        pos=pg.mouse.get_pos()
        if is_over(start_rect,pos):
            start_mask=1
            if event.type==pg.MOUSEBUTTONDOWN:
                intro_click.play()
                state='main_game'
                reset()
        else: start_mask=0
        if is_over(ins_rect,pos):
            ins_mask=1
            if event.type==pg.MOUSEBUTTONDOWN:
                intro_click.play()
                state='instruction'
        else: ins_mask=0
    DisplayImage(screen_intro,screen_w/2,screen_h/2)
    if start_mask==0:
        DisplayImage(intro_start,start_rect.centerx,start_rect.centery)
    else: DisplayImage(intro_start2,start_rect.centerx,start_rect.centery)
    if ins_mask==0:
        DisplayImage(intro_ins,ins_rect.centerx,ins_rect.centery)
    else: DisplayImage(intro_ins2,ins_rect.centerx,ins_rect.centery)
    #pg.draw.rect(screen,(0,255,0),ins_rect)
    #pg.draw.rect(screen,(0,0,0),start_rect)
    pg.display.update()


# In[12]:


#instruction

def instruction():
    global state,ins_tmp
    pos=pg.mouse.get_pos()
    for event in pg.event.get():
        if (event.type==QUIT):
            pg.quit()
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            if is_circle_over(pos,back_center,ins_radius):
                intro_click.play()
                ins_tmp-=1
                if ins_tmp<0:
                    ins_tmp=5
            if is_circle_over(pos,front_center,ins_radius):
                intro_click.play()
                ins_tmp+=1
                if ins_tmp>5:
                    ins_tmp=0
            if is_circle_over(pos,quit_center,quit_radius):
                intro_click.play()
                ins_tmp=0
                state='intro'
    screen.blit(ins_pages[ins_tmp],(0,0))
    pg.display.update()


# In[13]:


#main game

def main_game():
    global ticks,cat_speed,cat_sleep,cat_signal,seconds,Trash_tmp_choose,Bin_tmp_choose,cat_choose,cat_sleep_timestamp,state,cat_aim
    global cat_speed_a,cat_speed_frequency,cat_old_pos,sound_state,hints_choose,life,life_timestamp,points,Cat
    seconds=int(ticks/FPS)
    cat_speed=cat_init_speed + cat_speed_a**(seconds/cat_speed_frequency)
    if (life==0):
        mixer.music.stop()
        if sound_state==0:
            victory.play()
        state='outro'
    text_life=str(life).rjust(2)
    if ticks%FPS==0 and seconds%frequency==0:
        while len(Trash_temp)<Trash_init:
            Trash_random=random.choice(Trash_images)
            coor_random=(np.random.randint(50,1300), np.random.randint(270,700))
            while overlap_check(pg.Rect(coor_random[0],coor_random[1],Trash_random[0].get_width(),Trash_random[0].get_height()))==0:
                coor_random=(np.random.randint(50,1400), np.random.randint(270,800))
            (tmp_w,tmp_h)=(Trash_random[0].get_width(),Trash_random[0].get_height())
            Trash_temp.append((Trash_random,pg.Rect(coor_random[0],coor_random[1],tmp_w,tmp_h)))
    pg.mouse.set_visible(0)
    pos=pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type==QUIT:
            pg.quit()
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            if sound_state==0:
                drag.play() 
            if Trash_tmp_choose==-1:
                for i in range(0,len(Trash_temp)):
                    if is_over(Trash_temp[i][1],pos):
                        Trash_tmp_choose=i
                        break
            if Bin_tmp_choose==-1:
                    for i in range(3):
                        if is_over(Bin_images[i][2],pos):
                            if event.button==1:
                                Bin_tmp_choose=i
                            if event.button==3:
                                hints_choose=i
            if hints_choose!=-1 and event.button==1:
                if not is_over(hints[hints_choose][1],pos):
                    hints_choose=-1

            if cat_choose==-1:
                if is_over(Cat[1],pos):
                    cat_choose=1
                    cat_signal=0
                    cat_sleep_timestamp=ticks
                    cat_aim=Bin_images[points.index(max(points))][2].center
            if is_circle_over(pos,pause_rect.center,pause_radius):
                state='pause'
            if is_circle_over(pos,mute_rect.center,mute_radius):
                sound_state=(sound_state+1)%2
                if sound_state==0:
                    mixer.music.unpause()
                else: mixer.music.pause()
        if event.type==pg.MOUSEBUTTONUP:
            Trash_tmp_choose=Bin_tmp_choose=cat_choose=-1 

    if Trash_tmp_choose!=-1 and cat_choose==-1 and Bin_tmp_choose==-1:
        Trash_temp[Trash_tmp_choose][1].center=pos
    if Bin_tmp_choose!=-1 and cat_choose==-1:
        tmp=pg.Rect.copy(Bin_images[Bin_tmp_choose][2])
        tmp.center=pos
        if not overlap_bin_check(tmp,Bin_tmp_choose):
            Bin_images[Bin_tmp_choose][2].center=pos

    if cat_choose!=-1:
        tmp=pg.Rect.copy(Cat[1])
        tmp.center=pos
        if not overlap_bin_check(tmp,3):
            Cat[1].center=pos
        Cat[1].y=max(Cat[1].y,limy)
    elif (ticks-cat_sleep_timestamp>=cat_sleep*FPS):
        if cat_signal==0:
            cat_signal=1
        if cat_aim==Cat[1].center:
            cat_aim=Bin_images[np.random.randint(0,3)][2].center
        (stepx,stepy)=calc_step(Cat[1].center,cat_aim,cat_speed)
        Cat[1].centerx+=stepx 
        Cat[1].centery+=stepy
        if abs(Cat[1].centerx-cat_aim[0])<=10 and abs(Cat[1].centery-cat_aim[1])<=10:
            Cat[1].center=cat_aim
            cat_sleep_timestamp=ticks
            cat_sleep=np.random.randint(3,8)
            max_tmp=points.index(max(points))
            cat_aim=Bin_images[max_tmp][2].center

    screen.blit(screen_main,(0,0))
    for trash in Trash_temp:
        bin_tmp=(9999,-1)
        for Bin in Bin_images:
            if Bin_tmp_choose==-1 and Trash_tmp_choose==-1:
                if is_rect_over(trash[1],Bin[2]):
                    bin_tmp=min(bin_tmp,(calc_dis(trash[1].center,Bin[2].center),Bin[1]))
            if (bin_tmp[1]!=-1):
                marks_temp.append((trash[1].center,(Bin[1]==trash[0][1]),ticks,0))
                if sound_state==0:
                    res_sound[Bin[1]==trash[0][1]].play()
                Trash_temp.remove(trash)
                if Bin[1]==trash[0][1]:
                    points[Bin[1]]+=1
                break

    for Bin in Bin_images:
        if is_rect_over(Bin[2],Cat[1]) and Bin_tmp_choose!=Bin[1] and ticks-life_timestamp>3*FPS:
            life_timestamp=ticks
            points[Bin[1]]=0
            cat_aim=cat_sleep_pos
            life-=1
            if(life>0):
                if sound_state==0:
                    crash_sound.play()
            break

    for object in Bin_images:
        object[2].y=max(object[2].y,limy)
        DisplayImage(object[0],object[2].centerx,object[2].centery)
    for object in Trash_temp:
        object[1].y=max(object[1].y,limy)
        screen.blit(object[0][0],(object[1].x,object[1].y))
    if (Cat[1].center==cat_old_pos) or cat_choose!=-1:
        cat_state=2
    else:
        if (Cat[1].centerx>cat_old_pos[0]):
            cat_state=0
        else: cat_state=1
    screen.blit(cat_images[cat_state],(Cat[1].x,Cat[1].y))
    cat_old_pos=Cat[1].center
    for mark in marks_temp:
        DisplayImage(marks[mark[1]],mark[0][0],mark[0][1])
        if ticks-mark[2]>=mark_last:
            marks_temp.remove(mark)
    if hints_choose!=-1:
        DisplayImage(hints[hints_choose][0],screen_w/2,screen_h/2)
        
    if life>0:
        DisplayImage(hearts[life-1],1050,90)
    screen.blit(pause,(pause_rect.x,pause_rect.y))
    if sound_state==0:
        screen.blit(unmute,(mute_rect.x,mute_rect.y))
    else: 
        screen.blit(mute,(mute_rect.x,mute_rect.y))
   # pg.draw.circle(screen,(0,0,0),pause_rect.center,pause_radius)

    sum_point=0
    for i in range(3):
        sum_point+=points[i]
    text_point=str(sum_point).rjust(3)
    screen.blit(font_point.render(text_point,True,(255,204,0)),(1380,60))
    if cat_signal==1:
        if sound_state==0:
            cat_sound.play()
        cat_signal=2
    DisplayImage(glove,pos[0],pos[1])
    pg.display.update()
    ticks+=1
    clock.tick(FPS)


# In[14]:


#pause 

def Pause():
    global state
    pg.mouse.set_visible(1)
    for event in pg.event.get():
        if event.type==QUIT:
            pg.quit()
            sys.exit()
        pos=pg.mouse.get_pos()
        if event.type==pg.MOUSEBUTTONDOWN:
            if is_circle_over(pos,resume_home_center,resume_radius):
                mixer.music.stop()
                state='intro'
        if event.type==pg.MOUSEBUTTONDOWN:
            if is_circle_over(pos,resume_resume_center,resume_radius):
                state='main_game'
        if event.type==pg.MOUSEBUTTONDOWN:
            if is_circle_over(pos,resume_again_center,resume_radius):
                mixer.music.stop()
                reset()
                state='main_game'
    screen.blit(resume,(0,0))
 


# In[15]:


#outro
def outro():
    global again_mask,state,seconds,life,Bin_images
    pg.mouse.set_visible(1)
    for event in pg.event.get():
        if event.type==QUIT:
            pg.quit()
            sys.exit()
        pos=pg.mouse.get_pos()
        if event.type==pg.MOUSEBUTTONDOWN:
            if is_over(again_outro_rect,pos):
                    state='main_game'
                    reset()
            if is_circle_over(pos,home_center,home_radius):
                state='intro'
    sum_point=0
    for i in range(3):
        sum_point+=points[i]
    text_point=str(sum_point).rjust(3)
    screen.blit(screen_outro_background,(0,0))
    DisplayImage(screen_outro,screen_w/2,screen_h/2)
    screen.blit(font_point_outro.render(text_point,True,(255,204,0)),(740,390))


# In[16]:


#main code
while True:
    if state=='intro':
        intro()
    if state=='instruction':
        instruction()
    if state=='main_game':
        main_game()
    if state=='pause':
        Pause()
    if state=='outro':
        outro()
    pg.display.update()


# In[ ]:


#test... nothing to do with the main code 
import pygame as pg
pg.init()
screen_w=1600
screen_h=900
state='intro'
width, height = pg.display.Info().current_w, pg.display.Info().current_h
#screen_w,screen_h=width,height
screen=pg.display.set_mode((screen_w,screen_h),pg.RESIZABLE)
pg.display.set_caption('Earth Saver')
print(width,height)

def DisplayImage(img,posx,posy):
    (w,h)=(img.get_width(),img.get_height())
    screen.blit(img,(posx-w/2,posy-h/2))

def load_images(path_to_directory):
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.png'):
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = pg.image.load(path).convert_alpha()
    return image_dict

img_set=load_images('sources/trash_0')
img=[]
for tmp in img_set:
    img.append(img_set[tmp])
main=pg.image.load('sources/screen_main.png')
while (True):
    #print(pg.display.Info().current_h,pg.display.Info().current_w)
    screen.blit(main,(0,0))
    cnt=0
    for image in img:
        cnt+=1
        DisplayImage(image,200+300*(cnt%5),200+100*(cnt/5))
    for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
    pg.display.update()


# Finally, the dusk of a compelling code ~~~
# 

# Author: Nguyen Cao Minh Tuan aka JarvisHunter.
# Supporters: Thai Gia Huy, Le Anh Thong.

import pygame, sys
import time
import mosquitto
from threading import Thread


white = (255, 255, 255)
red = (255, 0, 0)
 
pygame.init()
myfont = pygame.font.SysFont("monospace", 18)
myfont2 = pygame.font.SysFont("monospace",24)
pygame.display.set_caption('Robot Command')
bck = pygame.image.load('cipi_CC.png')
size = [1024, 780]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
 

# using this to set the size of the rectange
# using this to also move the rectangle
step = 20
 
# by default the key repeat is disabled
# call set_repeat() to enable it
pygame.key.set_repeat(50, 50)

sens1 = ""
sens2 = ""
sens3 = ""
sens4 = ""

nav1 = ""
nav2 = ""
nav3 = ""
nav4 = ""

stat1 = ""
stat2 = ""
stat3 = ""
stat4 = "SS"

warn1 = ""
warn2 = ""

def multitext(strq,x_cord,y_cord):
    mystr = strq.splitlines()
    for tx in mystr:
      labelz = myfont.render(tx,1,(3,3,3))
      screen.blit(labelz,(x_cord,y_cord))
      y_cord = y_cord + 30


def on_connect(mosq, obj, rc):
    if rc == 0:
      stat4 = "CONNECTED"
    
def on_message(mosq, obj, msg):
    pass

def on_publish(mosq, obj, mid):
    stat3 = "PUBLISHED"

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

def on_log(mosq, obj, level, string):
    pass

def on_disconnect(mosq, obj, rc):
    if rc == 0:
      stat4 = "DISCONNECTED"


def mosthread():
    mqttc.loop(20)
    time.sleep(0.001)

#mqttc setup
mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("test.mosquitto.org", 1883, 60)
time.sleep(2)



while True:
    for event in pygame.event.get():
        mqttc.loop()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # check if key is pressed
        # if you use event.key here it will give you error at runtime
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                nav1 = "LEFT"
            if event.key == pygame.K_RIGHT:
                nav1 = "RIGHT"
            if event.key == pygame.K_UP:
                mqttc.publish("teleop","OK")
            if event.key == pygame.K_DOWN:
                nav1 = "DOWN"

            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_1:
                stat1 = "Speed 1"
            if event.key == pygame.K_2:
                stat1 = "Speed 2"
            if event.key == pygame.K_3:
                stat1 = "Speed 3"


            # checking if left modifier is pressed
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                if event.key == pygame.K_LEFT:
                    x = 0
                if event.key == pygame.K_RIGHT:
                    x = 640 - step
                if event.key == pygame.K_UP:
                    y = 0
                if event.key == pygame.K_DOWN:
                    y = 480 - step
 
 
    screen.fill(white)
    screen.blit(bck,(0,0))

    label = myfont.render(sens1, 1, (200,200,200))
    screen.blit(label, (54, 130))
    label = myfont.render(sens2,1,(200,200,200))
    screen.blit(label, (54,150))
    label = myfont.render(sens3,1,(200,200,200))
    screen.blit(label, (54,170))
    label = myfont.render(sens4,1,(200,200,200))
    screen.blit(label, (54,190))


    label = myfont.render(nav1, 1, (200,200,200))
    screen.blit(label, (54, 300))
    label = myfont.render(nav2,1,(200,200,200))
    screen.blit(label, (54,320))
    label = myfont.render(nav3,1,(200,200,200))
    screen.blit(label, (54,340))
    label = myfont.render(nav4,1,(200,200,200))
    screen.blit(label, (54,360))

    label = myfont.render(stat1, 1, (200,200,200))
    screen.blit(label, (54, 470))
    label = myfont.render(stat2,1,(200,200,200))
    screen.blit(label, (54,490))
    label = myfont.render(stat3,1,(200,200,200))
    screen.blit(label, (54,510))
    label = myfont.render(stat4,1,(200,200,200))
    screen.blit(label, (54,530))

    label = myfont2.render(warn1,1,(200,20,20))
    screen.blit(label, (520,675))
    label = myfont2.render(warn2,1,(200,20,20))
    screen.blit(label, (520,696))

    
    #multitext(mytx,200,200)
    
    pygame.display.update()
    clock.tick(30)

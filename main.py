import math
from turtle import Turtle, Screen
import random
import pygame
screen = Screen()
screen.title('Space Invaders')
screen.update()
screen.bgpic('space.png')

screen.register_shape("spaceinvaders-videogames.gif")
screen.register_shape("sp.gif")
screen.tracer(0)

screen.setup(700, 500)
player = Turtle()
player.shape('spaceinvaders-videogames.gif')
player.setheading(90)
player.speed = 0
player.color('green')
player.shapesize(stretch_len=2, stretch_wid=1)
player.penup()
player.hideturtle()
player.goto(0, -200)
player.showturtle()

screen.listen()

#Set the Score to 0
score = 0

#draw a score
score_pen = Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(0,230)
score_string = "Score : %s" %score
score_pen.write(score_string, False, align="left", font = ("Arial", 12, "normal"))
score_pen.hideturtle()



def player_go_right():
    player.speed = 1

def player_go_left():
    player.speed = -1


def move_player():
    x = player.xcor()
    x += player.speed
    if x < -320:
        x = -320
    if x > 320:
        x = 320
    player.setx(x)

number_of_enemies = 30
enemies = []

for i in range (number_of_enemies):
    enemies.append(Turtle())

enemy_start_x = -225
enemy_start_y = 180
enemy_number = 0

for enemy in enemies:
    enemy.hideturtle()
    enemy.color('red')
    enemy.shape('sp.gif')
    enemy.speed(0)
    enemy.penup()
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setposition(x, y)
    enemy.showturtle()
    enemy_number +=1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.2

bullet = Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed = 20
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bullet_speed = 8


bullet_state = "ready"
pygame.mixer.init()

def play_fire():
    pygame.mixer.music.load("shoot02wav-14562.mp3")
    pygame.mixer.music.play(loops=0)


def play_explosion():
    pygame.mixer.music.load("hq-explosion-6288.mp3")
    pygame.mixer.music.play(loops=0)

def fire_bullet():
    global bullet_state
    if bullet_state == 'ready':
        bullet_state = 'fire'
        x =player.xcor()
        y = player.ycor()+10
        bullet.setposition(x,y)
        bullet.showturtle()
        play_fire()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+ math.pow(t1.ycor() - t2.ycor(),2))
    # that means (t1.xcor() - t2.xcor()) square  + (t1.ycor() - t2.ycor()) square
    if distance < 15 :
        return True
    else:
        return False

screen.onkeypress(player_go_right, 'Right')
screen.onkeypress(player_go_left, "Left")
screen.onkeypress(fire_bullet,'space')

game_is_on = True
while game_is_on:
    screen.update()
    move_player()
    for enemy in enemies:
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        # move the enemy back and down
        if enemy.xcor() > 300:
            #moves all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 20
                e.sety(y)
            #Change enemy direction
            enemyspeed *= -1

        elif enemy.xcor()<-300:
            for e in enemies:
                y = e.ycor()
                y -= 20
                e.sety(y)
            enemyspeed *= -1


        # check for a collision between the bullet and the enemy
        if isCollision(bullet, enemy):
            # reset the bullet
            bullet.hideturtle()
            bullet_state = 'ready'
            bullet.setposition(0, -400)
            # reset the enemy

            enemy.setposition(0, 20000)
            play_explosion()
            score_pen.clear()
            score += 1
            score_string = "Score : %s" % score
            score_pen.write(score_string, False, align="left", font=("Arial", 12, "normal"))

        if isCollision(enemy, player):
            player.hideturtle()
            enemy.hideturtle()
            game_is_on = False

    if bullet_state =='fire':
        y = bullet.ycor()
        y += 10
        bullet.sety(y)
    if bullet.ycor() >250:
        bullet_state = 'ready'



screen.mainloop()
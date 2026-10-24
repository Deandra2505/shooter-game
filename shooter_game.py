from random import randint, choice
from time import time as timer
from pygame import *





font.init()
font1 = font.SysFont("Arial", 40)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))
font2 = font.Font("Arial", 30)





mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")





img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_heart = "heart.png"
img_bomb = "bomb.png"
img_lightning = "lightning.png"





score = 0
goal = 20
lost = 0
max_lost = 10
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1





class PowerUp(GameSprite):
    def __init__(self, item_type, player_x, player_y, size_x, size_y, player_speed):
        self.item_type = item_type
        if item_type == "heart":
            img_file = img_heart
        elif item_type == "bomb":
            img_file = img_bomb
        elif item_type == "lightning":
            img_file = img_lightning
        
        super().__init__(img_file, player_x, player_y, size_x, size_y, player_speed)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()





win_width = 700
win_height = 500
display.set_caption("Shooter Game - Skill & Power-ups")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))





ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

powerups = sprite.Group()
for i in range(1, 2):
    heart = PowerUp("heart",img_heart, randint(80, win_width - 80), -40, 80, 50, randint(1, 1))
    powerups.add(heart)
bombs = sprite.Group()  
for i in range(1, 2):
    bomb = PowerUp("bomb",img_bomb, randint(80, win_width - 80), -40, 80, 50, randint(1, 1))
    bombs.add(bomb)
lightnings = sprite.Group()
for i in range(1, 2):
    lightning = PowerUp("lightning",img_lightning, randint(80, win_width - 80), -40, 80, 50, randint(1, 1))
    lightnings.add(lightning)


bullets = sprite.Group()





lightning_boost_active = False
lightning_boost_start = 0
last_powerup_time = timer()





finish = False
run = True
rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True





            if e.key == K_r and finish:
                finish = False
                score = 0
                lost = 0
                num_fire = 0
                life = 3
                ship.speed = 10
                lightning_boost_active = False
                
                for b in bullets:
                    b.kill()
                for m in monsters:
                    m.kill()
                for p in powerups:
                    p.kill()

                for i in range(1, 6):
                    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                    monsters.add(monster)

    if not finish:
        window.blit(background, (0, 0))





        now = timer()
        if now - last_powerup_time > 5:
            type_choice = choice(["heart", "bomb", "lightning"])
            p_item = PowerUp(type_choice, randint(50, win_width - 50), -40, 40, 40, randint(2, 4))
            powerups.add(p_item)
            last_powerup_time = now





        if lightning_boost_active and now - lightning_boost_start > 6:
            ship.speed = 10
            lightning_boost_active = False





        ship.update()
        monsters.update()
        powerups.update()
        bullets.update()





        ship.reset()
        monsters.draw(window)
        powerups.draw(window)
        bullets.draw(window)





        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False





        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)





        hit_monsters = sprite.spritecollide(ship, monsters, True)
        for h in hit_monsters:
            life -= 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)





        hit_powerups = sprite.spritecollide(ship, powerups, True)
        for p in hit_powerups:
            if p.item_type == "heart":
                if life < 5:
                    life += 1
                
            elif p.item_type == "bomb":
                count = 0
                for m in list(monsters):
                    if count < 3:
                        m.kill()
                        score += 1
                        count += 1
                        new_monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                        monsters.add(new_monster)

            elif p.item_type == "lightning":
                ship.speed = 17
                lightning_boost_active = True
                lightning_boost_start = timer()





        if life <= 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))





        if score >= goal:
            finish = True
            window.blit(win, (200, 200))





        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if lightning_boost_active:
            text_lightning = font2.render("LIGHTNING BOOST!", 1, (0, 255, 255))
            window.blit(text_lightning, (10, 80))

        if life >= 3:
            life_color = (0, 255, 0)
        elif life == 2:
            life_color = (255, 255, 0)
        else:
            life_color = (255, 0, 0)





        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

    display.update()
    time.delay(50)













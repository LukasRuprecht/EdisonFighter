import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0 idle, #1 run, #2 jump, #3 attack1, #4 attack2, #5 hit, #6 death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.punch_cooldown = 0
        self.kick_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.attack_sound = sound



    def load_images(self, sprite_sheet, animation_steps):
        #extract images from a spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                #(x coordinate, y coordine, x size, y size)
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list


    def move(self, screen_width, screen_height, surface, target):
        SPEED = 6
        GRAVITY = 1
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        #get keypresses
        key = pygame.key.get_pressed()




        #CAN ONLY PERFORM OTHER ACTIONS IF NOT CURRENTLY ATTACKING
        if self.attacking == False and self.alive == True:
            #check player one controls
            if self.player ==1:
                #movement (WASD CONTROLS)
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if self.jump == False and key[pygame.K_w]:
                    self.vel_y = -20
                    self.jump = True
                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)
                    #determine which key
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            #check player two controls
            if self.player == 2:
                #movement (WASD CONTROLS)
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                #jump
                if self.jump == False and key[pygame.K_UP]:
                    self.vel_y = -20
                    self.jump = True
                #attack
                if key[pygame.K_o]:
                    self.attack(surface, target)
                    #determine which key
                    if key[pygame.K_o]: #punch
                        self.attack_type = 1
                    if key[pygame.K_p]:
                        self.attack_type = 2
                if key[pygame.K_p]: #kick
                    ##PUT A PAUSE HERE #look into row and column lists, once it is the right selection,


                    self.attack(surface, target)
                        #determine which key
                    if key[pygame.K_o]:
                            self.attack_type = 1
                    if key[pygame.K_p]:
                            self.attack_type = 2










        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #check if at edge of screen, ensures player stays on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 35:
            self.vel_y = 0
            dy = screen_height - 35 - self.rect.bottom
            self.jump = False

            #ensure players face each other
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True




            #apply the attack cooldown (maybe change to time measure?)
            if self.punch_cooldown > 0:
                self.punch_cooldown -= 1
            if self.kick_cooldown > 0:
                self.kick_cooldown -= 1


        #update player x and y position
        self.rect.x += dx
        self.rect.y += dy


    #handle animation updates
    def update(self):
        #check the action the player is trying to do
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)#6: Death
        elif self.hit == True:
            self.update_action(5)#5: Hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) #3: attack1
            elif self.attack_type == 2:
                self.update_action(4) #4: attack2

        elif self.jump == True:
            self.update_action(2) #2: Jump
        elif self.running == True:
            self.update_action(1) #1: Run
        else:
            self.update_action(0)#0: idle


        animation_cooldown = 50
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished (to then loop it)
        if self.frame_index >= len(self.animation_list[self.action]):
            #add another check before setting frame index to 0 automatically
            #check if the player is dead, end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #check if an attack was executed, stop attacking and add cooldowns
                if self.action == 3: #PUNCH
                    self.attacking = False
                    self.punch_cooldown = 10
                if self.action == 4: #KICK
                    self.attacking = False
                    self.kick_cooldown = 40
                #check if damage was taken
                if self.action == 5: #HIT
                    self.hit = False
                    #if the player was in the middle of an attack, stop the attack when hit
                    self.attacking = False
                    self.punch_cooldown = 10



    def attack(self, surface, target):
        if self.punch_cooldown == 0 and self.kick_cooldown == 0:
            #declare player is attacking to disallow other actions
            self.attacking = True
            #adjust attack if facing other direction
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 *self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                self.attack_sound.play()
                target.health -= 10
                target.hit = True
            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)




    def update_action(self, new_action):
        #check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #UPDATE the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #draw rectangle and blit image
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
from guizero import App, Box, Drawing, Text, PushButton, Window
from random import randint, choice
from gameplay.classs import Angry_bird

#CONSTANTS
HEIGHT=450
WIDTH=600

class Gameplay(Box):
    def __init__(self, base, on_success):
        super().__init__(base, width=600, height=450)
        self.on_success = on_success

        self.hide()
        # TEST SELF START
        #self.start("test1", "test2","red","chuck")


    def proceed(self, winner):
        self.hide()
        self.victory.destroy()
        self.on_success(winner)

  
    def start(self, player1, player2, player1_char, player2_char):
        self.show()
        self.player1 = player1
        self.player2 = player2
        self.player1_char = player1_char
        self.player2_char = player2_char

        red = Angry_bird("red", 0.06, 0.004, 8, "sword assault")
        chuck = Angry_bird("chuck", 0.08, 0.004, 4, "thunder spell")
        bomb = Angry_bird("bomb", 0.1, 0.006, 6, "explosion ahoy")
        jays = Angry_bird("jays", 0.04, 0.002, 4, "wicked potion")

        #PLAYER1 
        if player1_char == "red":
            self.player1_obj = red
        elif player1_char == "chuck":
            self.player1_obj = chuck
        elif player1_char == "bomb":
            self.player1_obj = bomb
        elif player1_char == "jays":
            self.player1_obj = jays

          #PLAYER2
        if player2_char == "red":
            self.player2_obj = red
        elif player2_char == "chuck":
            self.player2_obj = chuck
        elif player2_char == "bomb":
            self.player2_obj = bomb
        elif player2_char == "jays":
            self.player2_obj = jays

        while len(super().children) > 0:
            super().children[0].destroy()
        
        self.build()

  
    def build(self):
        self.no_jump = False
        
        #SPLITTING THE AREA
        health_bar_canvas=Box(self, height=40, width=WIDTH)
        health_bar_canvas.bg="light sky blue"
        
        text_canvas=Box(self, height=30, width=WIDTH)
        text_canvas.bg="light sky blue"
        
        self.gameplay_canvas= Drawing(self, height=380, width=WIDTH)
        self.gameplay_canvas.bg="light sky blue"
  
        #CLOUD AND GROUND DRAWINGS
        self.gameplay_canvas.image(0, -60, "gameplay/gifs/cloud.png")
        self.gameplay_canvas.image(340, -60, "gameplay/gifs/cloud.png")
        self.gameplay_canvas.image(-130, 210, "gameplay/gifs/ground.png")
        
        #DRAWING HEALTH BARS
        self.canvas = Drawing(health_bar_canvas, width=WIDTH, height=40, align="bottom")
      
        #[x(starting length point),y(top left point),x(ending length point),y(bottom right)]
        #p1 health bar. end poing gets smaller for p1 if they lose health
        self.p1_health_frac = 1
        self.p2_health_frac = 1
        
        self.canvas.rectangle(10, 10, 210, 40, color="black", outline=False)
        self.p1_bar = self.canvas.rectangle(10, 10, 10 + (self.p1_health_frac * 200), 40, color="green", outline=False)
        
        #p2 health bar. starting point gets bigger for p2 if they lose health
        self.canvas.rectangle(390, 10, 590, 40, color="black", outline=False)
        self.p2_bar = self.canvas.rectangle(590 - (self.p2_health_frac * 200), 10, 590, 40, color="green", outline=False)
        
        #SPECIAL POWERS TEXTS
        self.sp1_status_txt = None
        self.sp2_status_txt = None
        
        #power available
        def change_sp_status():
            #delete "special attack available" for p1 and p2
            txt_drawing_canvas.delete(self.sp1_status_txt)
            txt_drawing_canvas.delete(self.sp2_status_txt)
            #if charge=True available will come on for p1
            if self.player1_obj.get_charge():
                self.sp1_status_txt = txt_drawing_canvas.text(20, 0, "special attack AVAILABLE", size=10, color="green")
            else:
                self.sp1_status_txt = txt_drawing_canvas.text(10, 0, "special attack UNAVAILABLE", size=10, color="red")
            #p2
            if self.player2_obj.get_charge():
                self.sp2_status_txt = txt_drawing_canvas.text(400, 0, "special attack AVAILABLE", size=10, color="green")
            else:
                self.sp2_status_txt = txt_drawing_canvas.text(390, 0, "special attack UNAVAILABLE", size=10, color="red")

        txt_drawing_canvas = Drawing(text_canvas, width=WIDTH, height=20, align="bottom")
        change_sp_status()
    
        #GIFS
        def gitter(agent):
            src, gif, gif_pos = agent
            sway = randint(-6, 6)
            self.gameplay_canvas.delete(gif)
            agent[1] = self.gameplay_canvas.image(gif_pos[0] + sway, gif_pos[1], src)

        p1_gif_src = f"gameplay/gifs/{self.player1_char}.png"
        p1_gif_pos = [30, 160]
        p1_gif_img = self.gameplay_canvas.image(30, 160, p1_gif_src)
        
        p2_gif_src = f"gameplay/gifs/{self.player2_char}_flip.png"
        p2_gif_pos = [440, 170]
        p2_gif_img = self.gameplay_canvas.image(440, 170, p2_gif_src)
    
        #MOVING THE CHARS
        agents = [
          [p1_gif_src, p1_gif_img, p1_gif_pos], 
          [p2_gif_src, p2_gif_img, p2_gif_pos],
        ]
        
        super().children[0].repeat(200, gitter, args=[agents[0]])
        super().children[0].repeat(300, gitter, args=[agents[1]])
        
        def jump(agent):
            LOSS = 5
            FLOOR = 160 if agent == agents[0] else 170
            CAP = 400
            
            src, gif, gif_pos = agent
            if gif_pos[1] <= FLOOR:
                gif_pos[1] -= self.speed
                self.speed -= LOSS
                self.no_jump = True
            elif gif_pos[1] >= CAP:
                gif_pos[1] = FLOOR
                self.no_jump = False
                try:
                    self.jump_box.destroy()
                except ValueError:
                    return
            else:
                gif_pos[1] = FLOOR
                self.no_jump = False
                try:
                    self.jump_box.destroy()
                except ValueError:
                    return
                
        
        def move_char(board, agent, direction):
            src, gif, gif_pos = agent
            board.delete(gif)
          
            if agent==agents[0]:
                if direction == "left":
                    gif_pos[0] = max(0, gif_pos[0] - 15) 
                elif direction == "right":
                    gif_pos[0] = min((p2_gif_pos[0]-120), gif_pos[0] + 15)
                elif direction == "up":
                    self.jump_box = Box(self)
                    self.speed = 30
                    self.jump_box.repeat(80, lambda : jump(agent))
                       
            elif agent==agents[1]:
                if direction == "left":
                    gif_pos[0] = max((p1_gif_pos[0]+120), gif_pos[0] - 15) 
                elif direction == "right":
                    gif_pos[0] = min(440, gif_pos[0] + 15)
                elif direction == "up":
                    self.jump_box = Box(self)
                    self.speed = 30
                    self.jump_box.repeat(80, lambda : jump(agent))
              
            agent[1] = board.image(gif_pos[0], gif_pos[1], src)

        #ATTACK COMMANDS
        def attack(attacker, defender):
            src, gif, atk_pos = attacker
            src, gif, def_pos = defender
        
            imgs = ["boom","ouch","pow","bang","pow2"]
            distance = agents[1][2][0] - agents[0][2][0]
            
            #if the x axis of the right hand char is subtracted of the lef hand char's. 140 is the min distance required to attack each other 
            #attack animations
            if distance <= 140:      
                blocked = False
                
                #hp loss from attacks
                if attacker==agents[0]:
                    def_pos[0] = min(440, def_pos[0] + 100)
                    if self.player2_obj.get_shield()<1:
                        lose_hp(self, 2, self.player1_obj.get_strength())
                    else:
                        self.player2_obj.set_shield(self.player2_obj.get_shield()-1)
                        blocked = True
                      
                if attacker==agents[1]:
                    def_pos[0] = max(0, def_pos[0] - 100)
                    if self.player1_obj.get_shield()<1:
                        lose_hp(self, 1, self.player2_obj.get_strength())
                    else:
                        self.player1_obj.set_shield(self.player1_obj.get_shield()-1)
                        blocked = True
                #if statement saying when to show shield pic vs attack effects
                if not blocked:
                    img = f"gameplay/gifs/{choice(imgs)}"
                    sound_effect = self.gameplay_canvas.image((agents[1][2][0] + distance/2) - randint(150, 200) ,0, f"{img}.png")
                else:
                    img = "assets/shield"
                    sound_effect = self.gameplay_canvas.image((defender[2][0] - 60) , -40, f"{img}.png")
                self.after(500, lambda : self.gameplay_canvas.delete(sound_effect))

        

        def charge(player):
            player.set_charge(True)
            change_sp_status()
        
        def special_attack(attacker,defender):
            distance = agents[1][2][0] - agents[0][2][0]
            #avoids loads of indents
            if distance > 140:
                return
            atk_src, atk_gif, atk_pos = attacker
            def_src, def_gif, def_pos = defender

            char_attacks = {
                "red" : "sword.png",
                "chuck" : "lightning.png",
                "bomb" : "explosion.png",
                "jays" : "potion.png"
            }

            img = char_attacks[self.player1_obj.get_name() if attacker == agents[0] else self.player2_obj.get_name()]
            sound_effect = self.gameplay_canvas.image((agents[1][2][0] + distance/2) - randint(150, 200) ,0, f"assets/{img}")
            #pushing def back upon attack and ensuring SA deals x2 damage
            if defender == agents[0]:
                def_pos[0] = max(0, def_pos[0] - 100)
                lose_hp(self, 1, self.player2_obj.get_strength()*2)
                self.player2_obj.set_charge(False)
                #changes the SA status on the screen
                change_sp_status()
                #resets status back to true
                self.after(5000, charge, [self.player2_obj])
                print(self.player2_obj.get_charge())
            else:
                def_pos[0] = min(440, def_pos[0] + 100)
                lose_hp(self, 2, self.player1_obj.get_strength()*2)
                self.player1_obj.set_charge(False)
                change_sp_status()
                #lambda here allows args to be passed to the func brackets rather than storing it separate as "args=[]"
                self.after(5000, lambda: charge(self.player1_obj))
            self.after(500, lambda : self.gameplay_canvas.delete(sound_effect))
                    

        #KEY PRESSES
        def on_keypress(event):
            key = event.key
            if key == "d":
                move_char(self.gameplay_canvas, agents[0], "right")
                lose_hp(self, 1, self.player1_obj.get_stamina())
              
            elif key == "a":  
                move_char(self.gameplay_canvas, agents[0], "left")
                lose_hp(self, 1, self.player1_obj.get_stamina())
              
            elif key == "w" and not self.no_jump:
                self.no_jump = True
                move_char(self.gameplay_canvas, agents[0], "up")
                lose_hp(self, 1, self.player1_obj.get_stamina())
              
            elif key == "j" and self.player2 != "bot": 
                move_char(self.gameplay_canvas, agents[1], "left")
                lose_hp(self, 2, self.player2_obj.get_stamina())
              
            elif key == "l" and self.player2 != "bot":  
                move_char(self.gameplay_canvas, agents[1], "right")
                lose_hp(self, 2, self.player2_obj.get_stamina())
              
            elif (key == "i" and not self.no_jump) and self.player2 != "bot":
                self.no_jump = True
                move_char(self.gameplay_canvas, agents[1], "up")
                lose_hp(self, 2, self.player2_obj.get_stamina())
              
            elif key == "q" and not self.no_jump:
                attack(agents[0], agents[1])
            elif key == "o" and not self.no_jump:
                attack(agents[1], agents[0])

              #special attack only av if player not jumping and has SA charged
            elif (key == "e" and not self.no_jump) and self.player1_obj.get_charge():
                special_attack(agents[0], agents[1])
            elif (key == "u" and not self.no_jump) and self.player2_obj.get_charge():
                special_attack(agents[1], agents[0])

            #BOT
            if self.player2=="bot" and key == "d":
                move_char(self.gameplay_canvas, agents[1], "left")
            elif (key == "q" or key == "e") and (not self.no_jump and self.player2=="bot"):
                rand_num = randint(1,3)
                if rand_num == 1:
                    self.after(200, lambda: move_char(self.gameplay_canvas, agents[1], "up"))   
                elif rand_num == 2:
                    self.after(200, lambda: attack(agents[1], agents[0]))
                elif rand_num == 3:
                    self.after(200, lambda: special_attack(agents[1], agents[0]))

        self.master.when_key_pressed = on_keypress

        self.gameover = False
        
        def end_game(winner):
            self.gameover = True
            self.victory = Window(self.master, height=50, width=400)
            Text(self.victory, text = f"well done {winner} you did itttt yayyy")
            self.after(5000, lambda: self.proceed(winner))
        
        def lose_hp(self, player, hp):
            if self.gameover:
                return
            if player == 1:
                self.p1_health_frac -= hp
            else:
                self.p2_health_frac -= hp
            try:
                self.canvas.delete(self.p1_bar)
                self.canvas.delete(self.p2_bar)
            except AttributeError:
                pass

            #ends the game and stops health from going less than 0
            if self.p1_health_frac < 0:
                self.p1_health_frac = 0
                end_game(self.player2)
            if self.p2_health_frac < 0:
                self.p2_health_frac = 0
                end_game(self.player1)
                
            #HEALTH BAR COLOURS                
            #player 1 health bar
            if self.p1_health_frac > 0.5: # green
                self.p1_bar = self.canvas.rectangle(10, 10, 10 + (self.p1_health_frac * 200), 40, color="green", outline=False)
            elif self.p1_health_frac > 0.2: # yellow
                self.p1_bar = self.canvas.rectangle(10, 10, 10 + (self.p1_health_frac * 200), 40, color="yellow", outline=False)
            else:# red
                self.p1_bar = self.canvas.rectangle(10, 10, 10 + (self.p1_health_frac * 200), 40, color="red", outline=False)
              
            #player 2 health bar
            if self.p2_health_frac > 0.5: # green
                self.p2_bar = self.canvas.rectangle(590 - (self.p2_health_frac * 200), 10, 590, 40, color="green", outline=False)
            elif self.p2_health_frac > 0.2: # yellow
                self.p2_bar = self.canvas.rectangle(590 - (self.p2_health_frac * 200), 10, 590, 40, color="yellow", outline=False)
            else:# red
                self.p2_bar = self.canvas.rectangle(590 - (self.p2_health_frac * 200), 10, 590, 40, color="red", outline=False)

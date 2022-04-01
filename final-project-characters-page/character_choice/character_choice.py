from guizero import Box, Text, Picture, PushButton

#CONSTANTS
HEX_RED = "#e77979"
HEX_YEL = "#e7de79"
HEX_BLK = "#858585"
HEX_BLU = "#73a2ce"


class Character_choice(Box):
    def __init__(self, base, on_success):
        super().__init__(base, width=600, height=450)
        self.on_success = on_success

        #if this is True, it is P1 turn
        self.turn = True
        self.player1_char = None
        self.player2_char = None

        self.hide()

    def proceed(self):
        if self.player1_char is None or self.player2_char is None:
            print("Cannot proceed to gameplay waiting for character choice")
            return
        self.hide()
        self.on_success(self.player1, 
                        self.player2, 
                        self.player1_char,
                        self.player2_char)

    def start(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        while len(super().children) > 0:
            super().children[0].destroy()

        self.turn = True
        self.player1_char = None
        self.player2_char = None
        
        self.build()
        self.show()

    def unselect_character(self, character):
        if character == "red":
            char_btn, char_txt = self.red_choose
        elif character == "chuck":
            char_btn, char_txt = self.chuck_choose
        elif character == "bomb":
            char_btn, char_txt = self.bomb_choose
        elif character == "jays":
            char_btn, char_txt = self.jays_choose
        else:
            return
        char_txt.value = ""
        char_btn.show()

    def select_character(self, character):
        if character == "red":
            char_btn, char_txt = self.red_choose
        elif character == "chuck":
            char_btn, char_txt = self.chuck_choose
        elif character == "bomb":
            char_btn, char_txt = self.bomb_choose
        elif character == "jays":
            char_btn, char_txt = self.jays_choose
        else:
            return
          
        if self.turn:
            self.player1_char = character
        else:
            self.player2_char = character

        char_txt.value = "CHOSEN"
        char_btn.hide()

    def choose_character(self, new_character):
        if self.turn:
            old_character = self.player1_char
        else:
            old_character = self.player2_char

        self.unselect_character(old_character)
        self.select_character(new_character)

        self.turn = not self.turn
        if self.player2 != "bot":
            self.choose_header.value = "REMAINING PLAYER: PICK A CHARACTER"
        else:
            self.choose_header.value = f"{self.player1}: PICK BOT'S CHARACTER"

        self.proceed()

    def build(self):
        top_canvas = Box(self, height=40, width=600)

        red_canvas = Box(self, height=400, width=150, align="left")
        red_canvas.bg = HEX_RED

        chuck_canvas = Box(self, height=400, width=150, align="left")
        chuck_canvas.bg = HEX_YEL

        bomb_canvas = Box(self, height=400, width=150, align="left")
        bomb_canvas.bg = HEX_BLK

        jays_canvas = Box(self, height=400, width=150, align="left")
        jays_canvas.bg = HEX_BLU

        #heading boxes
        red_header = Box(red_canvas, height=40, width=150, align="top")

        chuck_header = Box(chuck_canvas, height=40, width=150, align="top")

        bomb_header = Box(bomb_canvas, height=40, width=150, align="top")

        jays_header = Box(jays_canvas, height=40, width=150, align="top")

        #picture boxes
        red_pic = Box(red_canvas, height=150, width=150, align="top")

        chuck_pic = Box(chuck_canvas, height=150, width=150, align="top")

        bomb_pic = Box(bomb_canvas, height=150, width=150, align="top")

        jays_pic = Box(jays_canvas, height=150, width=150, align="top")

        #headings
        self.choose_header = Text(top_canvas,
                                  text="WINNER OF COIN TOSS: PICK A CHARACTER",
                                  size=20,
                                  align="bottom")

        Text(red_header, text="RED", size=20, align="bottom")

        Text(chuck_header, text="CHUCK", size=20, align="bottom")

        Text(bomb_header, text="BOMB", size=20, align="bottom")

        Text(jays_header, text="JAYS", size=20, align="bottom")

        #pictures
        Picture(red_pic, image="assets/red.png", align="bottom")

        Picture(chuck_pic, image="assets/chuck.png", align="bottom")

        Picture(bomb_pic, image="assets/bomb.png", align="bottom")

        Picture(jays_pic, image="assets/jays.png", align="bottom")

        #character details
        red_details = "\n\nStriking power:60/100\nStamina:60/100\nDefence shield:80/100\n\n~Special attack~\nSWORD ASSAULT"
        Text(red_canvas, text=red_details, size=9)

        chuck_details = "\n\nStriking power:80/100\nStamina:60/100\nDefence shield:40/100\n\n~Special attack~\nTHUNDER SPELL"
        Text(chuck_canvas, text=chuck_details, size=9)

        bomb_details = "\n\nStriking power:100/100\nStamina:20/100\nDefence shield:60/100\n\n~Special attack~\nEXPLOSION AHOY"
        Text(bomb_canvas, text=bomb_details, size=9)

        jays_details = "\n\nStriking power:40/100\nStamina:100/100\nDefence shield:40/100\n\n~Special attack~\nWICKED POTION"
        Text(jays_canvas, text=jays_details, size=9)

        #choose buttons
        red_choose_btn = PushButton(red_canvas,
                                    text="CHOOSE",
                                    width=8,
                                    command=self.choose_character,
                                    args=["red"])
        red_choose_btn.text_size = 10

        chuck_choose_btn = PushButton(chuck_canvas,
                                      text="CHOOSE",
                                      width=8,
                                      command=self.choose_character,
                                      args=["chuck"])
        chuck_choose_btn.text_size = 10

        bomb_choose_btn = PushButton(bomb_canvas,
                                     text="CHOOSE",
                                     width=8,
                                     command=self.choose_character,
                                     args=["bomb"])
        bomb_choose_btn.text_size = 10

        jays_choose_btn = PushButton(jays_canvas,
                                     text="CHOOSE",
                                     width=8,
                                     command=self.choose_character,
                                     args=["jays"])
        jays_choose_btn.text_size = 10

        #TEXT WHEN P1 HAS PICKED
        red_choose_txt = Text(red_canvas, text="", size=10)
        chuck_choose_txt = Text(chuck_canvas, text="", size=10)
        bomb_choose_txt = Text(bomb_canvas, text="", size=10)
        jays_choose_txt = Text(jays_canvas, text="", size=10)

        self.red_choose = [red_choose_btn, red_choose_txt]
        self.chuck_choose = [chuck_choose_btn, chuck_choose_txt]
        self.bomb_choose = [bomb_choose_btn, bomb_choose_txt]
        self.jays_choose = [jays_choose_btn, jays_choose_txt]


# #CHARACTER INSTANCES
# red_char=angry_bird("red", 60, 60, 80, "sword assault")
# chuck_char=angry_bird("chuck", 80, 60, 40, "sword assault")
# bomb_char=angry_bird("bomb", 100, 20, 60, "sword assault")
# jays_char=angry_bird("jays", 40, 100, 40, "sword assault")
# high stamina = less health bar loss on movement
# high striking power = takes more off op's health bar upon attack
# high defence shield = has less taken off health bar upon attack

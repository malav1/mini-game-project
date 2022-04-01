from guizero import Box, Text, PushButton, Picture
from random import randint

class Coin_toss(Box):
    def __init__(self, base, on_success):
        super().__init__(base, width=600, height=450)
        self.bg = "cornsilk"
        self.on_success = on_success
      
        self.hide()

        # SELF START FOR TESTING
        # self.start("test1","test2")
    
    def proceed(self):
        self.hide()
        self.on_success(self.player1, self.player2)

    def start(self, player1, player2):
        self.show()
        self.player1 = player1
        self.player2 = player2

        while len(super().children) > 0:
            super().children[0].destroy()
          
        self.build()

  
    def build(self):     
      
        app = Box(self, width = 450, height = 400)
        
        app.bg = "white"
        Text(app, text = "Welcome to Angry Birds-Feathers Unleashed.", color = "red", size = 14)
        
        Text(app, text = "First you must complete the coin toss below.\n  Winner gets first character choice. Players take turns\n to attack until one player is defeated.\n The winner gets 1 point added to their name on the leaderboard.", size = 12)
        
        #COIN GIF
        coin_box = Box(app, width = 450, height = 250)
        
        Picture(coin_box, image="cointoss/coin2.gif")
        
        display_text = Text(coin_box, text = "Either player flip the coin:")
        
        #FLIP COIN
        def answer():
            if self.player2 != "bot":
                coinflip = randint(0,1)
               # 0 = Heads | 1 = Tails
                if coinflip == 0:
                    display_text.value = f"{self.player1} wins the coin flip"
                else:
                    display_text.value = f"{self.player2} wins the coin flip"
            else:
                display_text.value = f"{self.player1} wins the coin flip as player 2 is a bot"
                
        flip_box = Box(app, width = 450, height = 50, align = "bottom")
        flip_box.bg = "white"
        flip_button = PushButton(flip_box, text = "FLIP COIN", width = 225, height = 50, command = lambda: [answer(), self.after(3000, self.proceed)])

        

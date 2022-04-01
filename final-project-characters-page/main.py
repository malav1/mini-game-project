#HOW THE PAGES INTERACT WITH EACH OTHER
from guizero import App
from signin.signin import Sign_in
from cointoss.cointoss import Coin_toss
from character_choice.character_choice import Character_choice
from gameplay.gameplay import Gameplay
from leaderboard.leaderboard import Leaderboard

global app
app = App(title="ttest", width=600, height=450)
app.bg = "white"

def tt(p1, p2, c1, c2):
    print(f"{p1} chose {c1}")
    print(f"{p2} chose {c2}")

leaderboard_page = Leaderboard(app, None)

gameplay_page = Gameplay(app, on_success=leaderboard_page.start)

character_choice_page = Character_choice(app, on_success=gameplay_page.start)

cointoss_page = Coin_toss(app, on_success=character_choice_page.start)

signin_page = Sign_in(app, on_success=cointoss_page.start)
leaderboard_page.on_success=signin_page.start
app.display()

#constructor,start,proceed(transition method which only occurs, on success method

#the proceed method attempts to move on. the beginning of the next page is the start method.
from guizero import Box, Text, TextBox, PushButton

class Sign_in(Box):
    def __init__(self, base, on_success):
        super().__init__(base, width=600, height=450)

        self.on_success = on_success
    
        self.player1 = None
        self.player2 = None

        # COMMENTED FOR TESTING
        self.build()

    def start(self):
        self.show()

        # self.left_usrnm_box.value = ""
        # self.right_usrnm_box.value = ""
        # self.left_pass_box.value = ""
        # self.right_pass_box.value = ""
        # self.left_granted.hide()
        # self.right_granted.hide()

        while len(super().children) > 0:
            super().children[0].destroy()

        self.player1 = None
        self.player2 = None
      
        self.build()
      
    def proceed(self):
        if self.player1 is None or self.player2 is None:
            print("Could not proceed since a player is missing")
            return

        self.hide()
        self.on_success(self.player1, self.player2)

  
    
    def auth_user(self, username, password):
        file = open("signin/users.csv", "r")
        for record in file:
            record = record.strip().split(",")
            if record[0] == username and record[1] == password:
                file.close()
                return True
        file.close()
        return False

    def authenticate(self, side):
        if side == "left":
            username = self.left_usrnm_box.value
            password = self.left_pass_box.value
            valid = self.auth_user(username, password)
            if valid:
                self.player1 = username
                self.left_error.hide()
                self.left_granted.show()
            else:
                self.left_error.show()
        elif side == "right":
            username = self.right_usrnm_box.value
            password = self.right_pass_box.value
            valid = self.auth_user(username, password)
            if valid:
                self.player2 = username
                self.right_granted.show()
                self.right_error.hide()
            else:
                self.right_error.show()
        self.proceed()

    def build(self):
        top_canvas = Box(self, height=80, width=600)
        left_canvas = Box(self, height=450, width=300, align="left")
        right_canvas = Box(self, height=450, width=300, align="right")

        #texts, textboxes and buttons
        Text(top_canvas,
             text="ANGRY BIRDS: FEATHERS UNLEASHED",
             size=20,
             align="bottom",
             color="red")

        Text(left_canvas, text="\nPLAYER 1", size=20)
        Text(right_canvas, text="\nPLAYER 2", size=20)

        Text(left_canvas, text="\nUsername:", size=15)
        Text(right_canvas, text="\nUsername:", size=15)

        self.left_usrnm_box = TextBox(left_canvas, width=20)
        self.right_usrnm_box = TextBox(right_canvas, width=20)

        Text(left_canvas, text="\nPassword:", size=15)
        Text(right_canvas, text="\nPassword:", size=15)

        self.left_pass_box = TextBox(left_canvas, width=20)
        self.right_pass_box = TextBox(right_canvas, width=20)

        Box(left_canvas, width=300, height=20)
        Box(right_canvas, width=300, height=20)

        left_signin = PushButton(left_canvas,
                                 text="SIGN IN",
                                 command=self.authenticate,
                                 args=["left"])
        left_signin.text_size = 12
        right_signin = PushButton(right_canvas,
                                  text="SIGN IN",
                                  command=self.authenticate,
                                  args=["right"])
        right_signin.text_size = 12

        self.left_error = Text(left_canvas,
                               text="Incorrect username or password",
                               size=10,
                               color="red")
        self.left_error.hide()
        self.right_error = Text(right_canvas,
                                text="Incorrect username or password",
                                size=10,
                                color="red")
        self.right_error.hide()

        self.left_granted = Text(left_canvas,
                                 text="Waiting for other player...",
                                 size=10,
                                 color="green")
        self.left_granted.hide()
        self.right_granted = Text(right_canvas,
                                  text="Waiting for other player...",
                                  size=10,
                                  color="green")
        self.right_granted.hide()


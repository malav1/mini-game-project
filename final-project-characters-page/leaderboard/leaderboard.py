from guizero import Box, Text, PushButton


class Leaderboard(Box):
    def __init__(self, base, on_success, new_score=None):
        super().__init__(base, width=600, height=450)
        self.bg = "white"
        self.hide()
        
    def load_list(self):
        output = []
        file = open("leaderboard/scores.csv","r")
        for line in file:
            output.append(line.strip().split(","))
        file.close()
        return output

    def proceed(self):
        self.hide()
        self.on_success()

    def save(self, player):
        not_found = True
        scores = self.load_list()
        for i, user in enumerate(scores):
            if user[0] == player:
                not_found = False
                user[1] = str(int(user[1]) + 1)

                if i == 0:
                    break
                
                while int(scores[i-1][1]) < int(user[1]):
                    scores.insert(i-1, scores.pop(i))
                    i -= 1
                break
        if not_found:
            file = open("leaderboard/scores.csv", "a")
            file.write(f"{player},1\n")
            file.close()
            return

        file = open("leaderboard/scores.csv", "w")
        for score in scores:
            file.write(f"{score[0]},{score[1]}\n")
        file.close()

    def load(self):
        self.ranking = []

        file = open("leaderboard/scores.csv", "r")
        for record in file:
            record = record.strip().split(",")
            self.ranking.append({
                "username": record[0],
                "score": int(record[1])
            })

        def sort_key(item):
            return item["score"]

        self.ranking = sorted(self.ranking, key=sort_key, reverse=True)[:10]

    def start(self, winner):
        self.winner = winner
        self.save(winner)
        self.show()
        self.load()

        while len(super().children) > 0:
            super().children[0].destroy()
      
        self.build()
      
    def build(self):
        Text(self, text="Leaderboard", size=30)
        board = Box(self, width=500, height=320, layout="grid")

        Text(board, text=f"Rank", size=18, width=6, grid=[0, 0])
        Text(board, text=f"Username", size=18, width=12, grid=[1, 0])
        Text(board, text=f"Score", size=18, width=6, grid=[2, 0])

        for i, record in enumerate(self.ranking):
            Text(board, text=f"{i+1}", grid=[0, i + 1])
            Text(board, text=record['username'], grid=[1, i + 1])
            Text(board, text=record['score'], grid=[2, i + 1])

        PushButton(self, text="Restart", command=self.proceed)

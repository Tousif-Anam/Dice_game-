import random
import json
from rich import print
from rich.table import Table

# Dice class
class Dice:
    def roll(self):
        return random.randint(1, 6)


# Player class
class Player:
    def __init__(self, id):
        self.id = id
        self.score = 0


# Game class
class Game:
    def __init__(self):
        self.players = []
        self.dice = Dice()

    # create players
    def create_players(self):
        while True:
            n = input("Enter number of players (2-4): ")
            if n.isdigit() and 2 <= int(n) <= 4:
                n = int(n)
                break
            print("Invalid input")

        for i in range(n):
            self.players.append(Player(i + 1))

    # show score board
    def show_scores(self):
        table = Table(title="Score Board")

        table.add_column("Player")
        table.add_column("Score")

        for p in self.players:
            table.add_row(str(p.id), str(p.score))

        print(table)

    # save game
    def save_game(self):
        data = []
        for p in self.players:
            data.append({"id": p.id, "score": p.score})

        with open("data.json", "w") as f:
            json.dump(data, f)

        print("[green]Game Saved[/green]")

    # load game
    def load_game(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)

            self.players = []

            for item in data:
                p = Player(item["id"])
                p.score = item["score"]
                self.players.append(p)

            print("[green]Game Loaded[/green]")
            return True

        except:
            print("[red]No saved game[/red]")
            return False

    # player turn
    def play_turn(self, player):
        print(f"\n[bold yellow]Player {player.id} Turn[/bold yellow]")
        print(f"Score: {player.score}")

        temp = 0

        while True:
            x = input("Roll? (y/n): ")

            if x != "y":
                break

            val = self.dice.roll()
            print(f"[cyan]Dice: {val}[/cyan]")

            if val == 1:
                print("[red]Turn Over[/red]")
                temp = 0
                break
            else:
                temp += val

            print(f"Turn score: {temp}")

        player.score += temp
        print(f"Total score: {player.score}")

    # check winner
    def check_winner(self):
        for p in self.players:
            if p.score >= 50:
                return p
        return None

    # start game
    def start(self):
        print("[bold green]Welcome to Pig Dice Game[/bold green]")

        ch = input("Load game? (y/n): ")

        if ch == "y":
            ok = self.load_game()
            if not ok:
                self.create_players()
        else:
            self.create_players()

        while True:
            for p in self.players:
                self.play_turn(p)

                self.save_game()
                self.show_scores()

                winner = self.check_winner()
                if winner:
                    print(f"\n[bold green]Winner Player {winner.id}[/bold green]")
                    print(f"Score: {winner.score}")
                    return


# run game
g = Game()
g.start()

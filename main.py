import random
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name="blank"):
        self.name = name
        self.health = 3
        self.items = []

    def ask_tactic(self, players: list["Player"]):
        pass


class human_player(Player):
    def ask_tactic(self, players: list["Player"]):
        print(
            "which player to shoot? player count: "
            + [i for i in range(len(players))].__str__()
        )
        a: int = int(input())

        return a


class ai_player(Player):
    def ask_tactic(self, players: list["Player"]):
        a = random.randrange(0, len(players))  # assuming exclusive range
        print(f"ai chose: {a}")
        return int(a)


class Shell:
    def __init__(self, state):
        self.state: str = state

    def shoot_player(self, player: Player):
        if self.state == "live":
            print("shot LIVE at " + player.name)
            player.health = player.health - 1
        else:
            print("shot BLANK at " + player.name)


class game_state:
    def __init__(self, players: list[Player]):
        self.turn_count = 0
        self.players = players
        self.current_shells: list[Shell] = []
        self.current_shell = 0

    def turn(self):
        self.turn_count = self.turn_count + 1

        print(
            f"{self.turn_count}. Turn; Players: "
            + str([[player.name, player.health] for player in self.players])
        )

        for player in self.players:
            if len(self.current_shells) == 0:
                self.generate_shells(self.current_shells)
            target_index = player.ask_tactic(players=self.players)  # ask for target
            self.current_shells[self.current_shell].shoot_player(
                self.players[target_index]
            )  # shoot
            self.current_shells.remove(
                self.current_shells[self.current_shell]
            )  # remove used shell

            if self.any_players_dead():
                break

    def any_players_dead(self):
        for player in self.players:
            if player.health <= 0:
                return True
        return False

    def get_game_status(self):
        return {"turn_count": self.turn_count, "players": self.players}

    def game_over(self) -> bool:
        for player in self.players:
            if player.health <= 0:
                print(f"player: {player.name} is dead!")
                return True
        return False

    def generate_shells(self, mag: list[Shell], mag_size=5):
        self.current_shells.clear()
        for _ in range(mag_size):
            a: int = int(random.randrange(0, 2))
            shell = None
            if a == 0:
                shell = Shell("live")
            else:
                shell = Shell("blank")

            mag.append(shell)
        print(f"new shells: " + str([shell.state for shell in self.current_shells]))


def start():
    print("starting game")
    players = [human_player(name="human"), ai_player(name="AI")]
    game = game_state(players=players)

    while not game.game_over():
        game.turn()


if __name__ == "__main__":
    start()

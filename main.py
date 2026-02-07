import random
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name="blank"):
        self.name = name
        self.health = 3
        self.items = []

    @abstractmethod
    def ask_tactic(self, players: list["Player"]):
        pass


class HumanPlayer(Player):
    def ask_tactic(self, players: list["Player"]):
        print(
            "which player to shoot? player count: "
            + [i for i in range(len(players))].__str__()
        )
        a: int = int(input())

        return a


class AIPlayer(Player):
    def ask_tactic(self, players: list["Player"]):
        a = random.randrange(0, len(players))  # assuming exclusive range
        print(f"ai chose: {a}")
        return int(a)


class Shell:
    def __init__(self, state):
        self.state: str = state

    def shoot_player(self, player: Player, shooter: Player = None):
        if self.state == "live":
            print(f"{shooter.name} shot LIVE at " + player.name)
            player.health = player.health - 1
        else:
            print(f"{shooter.name} shot BLANK at " + player.name)


class game_state:
    def __init__(self, players: list[Player]):
        self.turn_count = 0
        self.players = players
        self._all_players = players # includes dead players too
        self.current_shells: list[Shell] = []
        self.current_shell = 0

    def turn(self):
        self.turn_count = self.turn_count + 1

        print(
            f"{self.turn_count}. Turn; Players: "
            + str([[player.name, player.health] for player in self._all_players])
        )

        for player in self.players:
            if len(self.current_shells) == 0:
                self.generate_shells(self.current_shells)
            target_index = player.ask_tactic(players=self.players)  # ask for target
            self.current_shells[self.current_shell].shoot_player(
                self.players[target_index], shooter=player
            )  # shoot
            self.current_shells.pop(self.current_shell)

            if self.any_players_dead():
                break

    def any_players_dead(self):
        alive_count = 0 # support for multiple people
        for player in self.players:
            if player.health > 0:
                alive_count = alive_count + 1
            else:
                print(f"{player.name} is dead and is removed from the game!")
                self.players.remove(player)
        
        if alive_count == 1:
            return True
        return False

    def get_game_status(self):
        return {"turn_count": self.turn_count, "players": self.players}

    def game_over(self) -> bool:
        if self.any_players_dead():
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
    print("starting game",end="\n\n")
    players = [HumanPlayer(name="human"), HumanPlayer(name="human2"), AIPlayer(name="AI"), AIPlayer(name="AI2"), AIPlayer(name="AI3")]
    game = game_state(players=players)

    while not game.game_over():
        game.turn()
        print("\n\n")


if __name__ == "__main__":
    start()

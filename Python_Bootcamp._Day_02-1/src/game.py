from collections import Counter

class Game(object):

    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()
        self.start_game()

    def play(self, player1, player2):
        for i in range(self.matches):
            first = player1.get_answer()
            second = player2.get_answer()
            if first and second:
                player1.add(2)
                player2.add(2)
            elif not first and not second:
                player1.add(0)
                player2.add(0)
            elif not first and second:
                player2.sub(1)
                player1.add(3)
            else:
                player1.sub(1)
                player2.add(3)
            player1.set_war_answer(second)
            player2.set_war_answer(first)
        self.registry[str(player1)] += player1.get_amount()
        self.registry[str(player2)] += player2.get_amount()
        player1.Clear()
        player2.Clear()

    def start_game(self):
        players = [Cheater(), Cooperator(), Grudger(), Wannabe(), Detective()]
        for i in range(5):
            for j in range(i + 1, 5):
                self.play(players[i], players[j])

    def top3(self):
        sorted_keys = sorted(self.registry, key=self.registry.get, reverse=True)
        print(sorted_keys[0], self.registry[sorted_keys[0]])
        print(sorted_keys[1], self.registry[sorted_keys[1]])
        print(sorted_keys[2], self.registry[sorted_keys[2]])
        return self.registry[sorted_keys[0]], self.registry[sorted_keys[1]], self.registry[sorted_keys[2]]


class Player:

    def __init__(self):
        self.amount_sweets : int = 0
        self.war_answer = True
        self.my_answer = True

    def add(self, amount):
        self.amount_sweets += amount
    
    def sub(self, amount):
        if self.amount_sweets > 0:
            self.amount_sweets -= amount

    def get_amount(self):
        return self.amount_sweets

    def set_war_answer(self, answer):
        self.war_answer = answer


class Cheater(Player):
    
    def __init__(self):
        self.amount_sweets : int = 0

    def get_answer(self):
        return False
    

    def __str__(self):
        return "cheater"
    
    def Clear(self):
        self.__init__()

class Cooperator(Player):
    
    def __init__(self):
        self.amount_sweets : int = 0

    def get_answer(self):
        return True

    def __str__(self):
        return "cooperator"
    
    def Clear(self):
        self.__init__()

class Grudger(Player):

    def __init__(self):
        self.amount_sweets : int = 0
        self.war_answer = True
        self.cheat = False

    def get_answer(self):
        if not self.cheat and not self.war_answer:
            self.cheat = True
        if self.cheat:
            return False
        else:
            return True

    def __str__(self):
        return "grudger"

    def Clear(self):
        self.__init__()

class Wannabe(Player):

    def __init__(self):
        self.amount_sweets : int = 0
        self.war_answer = True

    def get_answer(self):
        if self.war_answer:
            return True
        else:
            return False

    def __str__(self):
        return "wannabe"
    
    def Clear(self):
        self.__init__()


class Detective(Player):

    def __init__(self):
        self.cheat_act = False
        self.cheat = False
        self.war_answer = True
        self.amount_sweets : int = 0
        self.counter = 0

    def get_answer(self):
        if not self.war_answer and self.counter <= 3:
            self.cheat = True
        if self.counter == 1:
            self.counter += 1
            return False
        elif self.counter <= 3:
            self.counter += 1
            return True
        else:
            if not self.cheat:
                return False
            else:
                if self.war_answer:
                    return True
                else:
                    return False

    def Clear(self):
        self.__init__()

    def __str__(self):
        return "detective"


class Detective(Player):

    def __init__(self):
        self.cheat_act = False
        self.cheat = False
        self.war_answer = True
        self.amount_sweets : int = 0
        self.counter = 0

    def get_answer(self):
        if not self.war_answer and self.counter <= 3:
            self.cheat = True
        if self.counter == 1:
            self.counter += 1
            return False
        elif self.counter <= 3:
            self.counter += 1
            return True
        else:
            if not self.cheat:
                return False
            else:
                if self.war_answer:
                    return True
                else:
                    return False

    def Clear(self):
        self.__init__()

    def __str__(self):
        return "detective"


def main():
    game = Game()
    if game.top3() == (58, 48, 47):
        print("OK")
    else:
        print("ERROR")

if __name__ == "__main__":
    main()
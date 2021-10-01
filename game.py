from typing import List
from collections import deque


class Player:
    def __init__(self, name: str):
        self.name = name
        self.purse = 0
        self.in_penalty_box = False


class Board:
    def __init__(self):
        self.pawn_location = dict()

    def place_pawn(self, pawn: int, place: int = 0):
        self.pawn_location[pawn] = place

    def move_pawn(self, pawn: int, steps: int):
        self.pawn_location[pawn] = (self.pawn_location[pawn] + steps) % 12
        return self.pawn_location[pawn]

    def get_pawn_cat(self, pawn: int):
        return self.get_cat(self.pawn_location[pawn])

    def get_cat(self, place: int):
        if place == 3 or place == 7 or place == 11: return "Rock"
        if place == 0 or place == 4 or place == 8: return "Pop"
        if place == 1 or place == 5 or place == 9: return "Science"
        if place == 2 or place == 6 or place == 10: return "Sports"


class QuestionsDecks:
    def __init__(self):
        self.pop_questions = deque()
        self.science_questions = deque()
        self.sports_questions = deque()
        self.rock_questions = deque()

        for i in range(50):
            self.pop_questions.append(self.create_question("Pop", i))
            self.science_questions.append(self.create_question("Science", i))
            self.sports_questions.append(self.create_question("Sports", i))
            self.rock_questions.append(self.create_question("Rock", i))

    def create_question(self, cat: str, index: int) -> str:
        return f"{cat} Question {index}"

    def get_question(self, cat: str) -> str:
        if cat == "Pop":
            return self.pop_questions.popleft()
        if cat == "Science":
            return self.science_questions.popleft()
        if cat == "Sports":
            return self.sports_questions.popleft()
        if cat == "Rock":
            return self.rock_questions.popleft()

class Game:
    def __init__(self, coins_to_win: int = 6):
        self.coins_to_win = coins_to_win
        self.players: List[Player] = []
        self.board = Board()
        self.questions_decks = QuestionsDecks()
        self.currentPlayer = 0
        self.isGettingOutOfPenaltyBox: bool = False

    def current_player(self) -> Player:
        return self.players[self.currentPlayer]

    def add(self, playerName: str) -> bool:
        self.board.place_pawn(self.howManyPlayers())
        self.players.append(Player(playerName))
        print(f"{playerName} was added")
        print(f"They are player number {self.howManyPlayers()}")
        return True

    def howManyPlayers(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        print(f"{self.current_player().name} is the current player")
        print(f"They have rolled a {roll}")

        if self.current_player().in_penalty_box:
            if roll % 2 != 0:
                print(f"{self.current_player().name} is getting out of the penalty box")
                self.isGettingOutOfPenaltyBox = True
                self.movePlayerAndAskQuestion(roll)
            else:
                print(f"{self.current_player().name} is not getting out of the penalty box")
                self.isGettingOutOfPenaltyBox = False
        else:
            self.movePlayerAndAskQuestion(roll)

    def movePlayerAndAskQuestion(self, roll: int) -> None:
        current_place = self.board.move_pawn(self.currentPlayer, roll)
        current_cat = self.board.get_pawn_cat(self.currentPlayer)
        print(f"{self.current_player().name}'s new location is {current_place}")
        print(f"The category is {current_cat}")
        print(self.questions_decks.get_question(current_cat))

    def goto_next_player(self):
        self.currentPlayer = (self.currentPlayer + 1) % self.howManyPlayers()

    def gain_coin(self):
        self.current_player().purse += 1
        print(f"{self.current_player().name} now has {self.current_player().purse} Gold Coins.")

    def was_correctly_answered(self) -> bool:
        if self.current_player().in_penalty_box and not self.isGettingOutOfPenaltyBox:
            self.goto_next_player()
            return False
        else:
            print("Answer was correct!!!!")
            self.gain_coin()
            current_player_won = self.current_player().purse == self.coins_to_win
            if current_player_won:
                print (f"{self.current_player().name} has won!!")
            self.goto_next_player()
            return current_player_won

    def wrong_answer(self) -> bool:
        print("Question was incorrectly answered")
        print(f"{self.current_player().name} was sent to the penalty box")
        self.current_player().in_penalty_box = True
        self.goto_next_player()
        return False

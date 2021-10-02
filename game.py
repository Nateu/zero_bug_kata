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
        self.amount_of_coins_to_win = coins_to_win
        self.players: List[Player] = []
        self.board = Board()
        self.questions_decks = QuestionsDecks()
        self.current_player_index = 0
        self.is_getting_out_of_penalty_box: bool = False

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def add_player(self, playerName: str) -> bool:
        self.board.place_pawn(self.player_count())
        self.players.append(Player(playerName))
        print(f"{playerName} was added.\nThey are player number {self.player_count()}.")
        return True

    def player_count(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        print(f"{self.get_current_player().name} is the current player.\nThey have rolled a {roll}.")

        if self.get_current_player().in_penalty_box:
            if roll % 2 != 0:
                print(f"{self.get_current_player().name} is getting out of the penalty box.")
                self.is_getting_out_of_penalty_box = True
                self.move_player_and_ask_question(roll)
            else:
                print(f"{self.get_current_player().name} is not getting out of the penalty box.")
                self.is_getting_out_of_penalty_box = False
        else:
            self.move_player_and_ask_question(roll)

    def move_player_and_ask_question(self, roll: int) -> None:
        current_place = self.board.move_pawn(self.current_player_index, roll)
        current_cat = self.board.get_pawn_cat(self.current_player_index)
        print(f"{self.get_current_player().name}'s new location is {current_place}.\nThe category is {current_cat}.\n{self.questions_decks.get_question(current_cat)}.")

    def next_players_turn(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count()

    def current_player_gains_coin(self):
        self.get_current_player().purse += 1
        print(f"{self.get_current_player().name} now has {self.get_current_player().purse} Gold Coins.")

    def check_if_current_player_has_won(self):
        return self.get_current_player().purse == self.amount_of_coins_to_win

    def correctly_answered(self) -> bool:
        if self.get_current_player().in_penalty_box and not self.is_getting_out_of_penalty_box:
            self.next_players_turn()
            return False
        else:
            print("Answer was correct!!!!")
            self.current_player_gains_coin()
            current_player_won = self.check_if_current_player_has_won()
            if current_player_won:
                print (f"{self.get_current_player().name} has won!!")
            self.next_players_turn()
            return current_player_won

    def incorrectly_answered(self) -> bool:
        print("Question was incorrectly answered.")
        print(f"{self.get_current_player().name} was sent to the penalty box.")
        self.get_current_player().in_penalty_box = True
        self.next_players_turn()
        return False

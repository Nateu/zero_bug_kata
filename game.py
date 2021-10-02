from typing import List
from collections import deque


class Player:
    def __init__(self, name: str):
        self.name = name
        self.purse = 0


class Board:
    def __init__(self):
        self.pawn_location = dict()
        self.pawn_penalty_box = dict()

    def place_pawn(self, pawn: int, place: int = 0) -> None:
        self.pawn_location[pawn] = place

    def move_pawn(self, pawn: int, steps: int) -> int:
        self.pawn_location[pawn] = (self.pawn_location[pawn] + steps) % 12
        return self.pawn_location[pawn]

    def get_pawns_category(self, pawn: int) -> str:
        return self.get_category(self.pawn_location[pawn])

    def get_category(self, place: int) -> str:
        if place == 3 or place == 7 or place == 11: return "Rock"
        if place == 0 or place == 4 or place == 8: return "Pop"
        if place == 1 or place == 5 or place == 9: return "Science"
        if place == 2 or place == 6 or place == 10: return "Sports"

    def put_pawn_in_penalty_box(self, pawn: int) -> None:
        self.pawn_penalty_box[pawn] = True

    def remove_pawn_from_penalty_box(self, pawn: int) -> None:
        self.pawn_penalty_box[pawn] = False

    def is_pawn_in_penalty_box(self, pawn: int) -> bool:
        return self.pawn_penalty_box[pawn]


class QuestionsDecks:
    def __init__(self):
        self.decks = dict()
        self.decks["Pop"] = deque()
        self.decks["Science"] = deque()
        self.decks["Sports"] = deque()
        self.decks["Rock"] = deque()

        for counter in range(50):
            self.decks["Pop"].append(self.create_question("Pop", counter))
            self.decks["Science"].append(self.create_question("Science", counter))
            self.decks["Sports"].append(self.create_question("Sports", counter))
            self.decks["Rock"].append(self.create_question("Rock", counter))

    def create_question(self, category: str, index: int) -> str:
        return f"{category} Question {index}"

    def get_question(self, category: str) -> str:
        return self.decks[category].popleft()

class Game:
    def __init__(self, coins_to_win: int = 6):
        self.amount_of_coins_to_win = coins_to_win
        self.players: List[Player] = []
        self.board = Board()
        self.questions_decks = QuestionsDecks()
        self.current_player_index = -1
        self.is_getting_out_of_penalty_box: bool = False

    def add_player(self, player_name: str) -> bool:
        self.board.place_pawn(self.player_count())
        self.board.remove_pawn_from_penalty_box(self.player_count())
        self.players.append(Player(player_name))
        print(f"{player_name} was added.\nThey are player number {self.player_count()}.")
        return True

    def player_count(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        self.set_new_current_player()
        print(f"{self.get_current_player().name} is the current player.\nThey have rolled a {roll}.")

        if self.board.is_pawn_in_penalty_box(self.current_player_index):
            if roll % 2 != 0:
                print(f"{self.get_current_player().name} is getting out of the penalty box.")
                self.is_getting_out_of_penalty_box = True
                self.move_player_and_ask_question(roll)
            else:
                print(f"{self.get_current_player().name} is not getting out of the penalty box.")
        else:
            self.move_player_and_ask_question(roll)

    def set_new_current_player(self):
        self.next_players_turn()
        self.is_getting_out_of_penalty_box = False

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_players_turn(self):
        self.current_player_index = (self.current_player_index + 1) % self.player_count()

    def move_player_and_ask_question(self, roll: int) -> None:
        current_place = self.board.move_pawn(self.current_player_index, roll)
        current_category = self.board.get_pawns_category(self.current_player_index)
        print(f"{self.get_current_player().name}'s new location is {current_place}.\nThe category is {current_category}.\n{self.questions_decks.get_question(current_category)}.")

    def correctly_answered(self) -> bool:
        if not self.board.is_pawn_in_penalty_box(self.current_player_index) or self.is_getting_out_of_penalty_box:
            print("Answer was correct!!!!")
            self.current_player_gains_coin()
            self.board.remove_pawn_from_penalty_box(self.current_player_index)
        return self.finish_turn()

    def current_player_gains_coin(self):
        self.get_current_player().purse += 1
        print(f"{self.get_current_player().name} now has {self.get_current_player().purse} Gold Coins.")

    def finish_turn(self):
        if self.check_if_current_player_has_won():
            print (f"{self.get_current_player().name} has won!!")
        return self.check_if_current_player_has_won()

    def check_if_current_player_has_won(self):
        return self.get_current_player().purse == self.amount_of_coins_to_win

    def incorrectly_answered(self) -> bool:
        print(f"Question was incorrectly answered.\n{self.get_current_player().name} was sent to the penalty box.")
        self.board.put_pawn_in_penalty_box(self.current_player_index)
        return self.finish_turn()

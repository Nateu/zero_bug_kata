from typing import List
from collections import deque


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.purse = 0

    def get_wealth(self) -> int:
        return self.purse

    def add_coins(self, amount: int = 1) -> int:
        self.purse += amount
        return self.get_wealth()

    def __repr__(self) -> str:
        return self.name


class Board:
    def __init__(self, size: int = 12, categories: [str] = ["Pop", "Science", "Sports", "Rock"]) -> None:
        self.pawn_location = dict()
        self.pawn_penalty_box = dict()
        self.categories = categories
        self.size = size

    def place_pawn(self, pawn: int, place: int = 0) -> None:
        self.pawn_location[pawn] = place

    def move_pawn(self, pawn: int, steps: int) -> int:
        self.pawn_location[pawn] = (self.pawn_location[pawn] + steps) % self.size
        return self.pawn_location[pawn]

    def get_pawns_category(self, pawn: int) -> str:
        return self.get_category(self.pawn_location[pawn])

    def get_category(self, place: int) -> str:
        number_of_categories = len(self.categories)
        return self.categories[place % number_of_categories]

    def put_pawn_in_penalty_box(self, pawn: int) -> None:
        self.pawn_penalty_box[pawn] = True

    def remove_pawn_from_penalty_box(self, pawn: int) -> None:
        self.pawn_penalty_box[pawn] = False

    def is_pawn_in_penalty_box(self, pawn: int) -> bool:
        return self.pawn_penalty_box[pawn]

    def list_all_categories(self) -> [str]:
        return self.categories


class QuestionsDecks:
    def __init__(self, categories: [str]) -> None:
        self.decks = dict()
        for category in categories:
            self.decks[category] = deque()

        for counter in range(50):
            for category, deck in self.decks.items():
                deck.append(self.create_question(category, counter))

    def create_question(self, category: str, index: int) -> str:
        return f"{category} Question {index}"

    def get_question(self, category: str) -> str:
        question = self.decks[category].popleft()
        self.decks[category].append(question)
        return question


class Game:
    def __init__(self, coins_to_win: int = 6, max_players: int = 6) -> None:
        self.amount_of_coins_to_win = coins_to_win
        self.players: List[Player] = []
        self.board = Board()
        self.questions_decks = QuestionsDecks(self.board.list_all_categories())
        self.current_player_index = -1
        self.is_getting_out_of_penalty_box: bool = False
        self.max_players = max_players

    def add_player(self, player_name: str) -> bool:
        if self.player_count() >= self.max_players:
            print(f"Max number of players is {self.max_players}.")
            return False
        self.board.place_pawn(self.player_count())
        self.board.remove_pawn_from_penalty_box(self.player_count())
        self.players.append(Player(player_name))
        print(f"{player_name} was added.\nThey are player number {self.player_count()}.")
        return True

    def player_count(self) -> int:
        return len(self.players)

    def roll(self, roll: int) -> None:
        if self.player_count() < 2:
            print(f"Min number of players is 2.")
            return False
        self.set_new_current_player()
        print(f"{self.get_current_player()} is the current player.\nThey have rolled a {roll}.")

        if self.board.is_pawn_in_penalty_box(self.current_player_index):
            if roll % 2 != 0:
                print(f"{self.get_current_player()} is getting out of the penalty box.")
                self.is_getting_out_of_penalty_box = True
                self.move_player_and_ask_question(roll)
            else:
                print(f"{self.get_current_player()} is not getting out of the penalty box.")
        else:
            self.move_player_and_ask_question(roll)

    def set_new_current_player(self) -> None:
        self.next_players_turn()
        self.is_getting_out_of_penalty_box = False

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_players_turn(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % self.player_count()

    def move_player_and_ask_question(self, roll: int) -> None:
        current_place = self.board.move_pawn(self.current_player_index, roll)
        current_category = self.board.get_pawns_category(self.current_player_index)
        print(f"{self.get_current_player()}'s new location is {current_place}.\nThe category is {current_category}.\n{self.questions_decks.get_question(current_category)}.")

    def correctly_answered(self) -> bool:
        if not self.board.is_pawn_in_penalty_box(self.current_player_index) or self.is_getting_out_of_penalty_box:
            print("Answer was correct!!!!")
            self.current_player_gains_coin()
            self.board.remove_pawn_from_penalty_box(self.current_player_index)
        return self.finish_turn()

    def current_player_gains_coin(self) -> None:
        print(f"{self.get_current_player()} now has {self.get_current_player().add_coins()} Gold Coins.")

    def finish_turn(self) -> bool:
        if self.check_if_current_player_has_won():
            print (f"{self.get_current_player()} has won!!")
        return self.check_if_current_player_has_won()

    def check_if_current_player_has_won(self) -> bool:
        return self.get_current_player().get_wealth() == self.amount_of_coins_to_win

    def incorrectly_answered(self) -> bool:
        print(f"Question was incorrectly answered.\n{self.get_current_player()} was sent to the penalty box.")
        self.board.put_pawn_in_penalty_box(self.current_player_index)
        return self.finish_turn()

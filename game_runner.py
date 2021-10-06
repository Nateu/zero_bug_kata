from random import randrange, seed
from game import Game


if __name__ == '__main__':

    not_a_winner = False

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    seed(11)

    while True:
        roll = randrange(5) + 1
        game.roll(roll)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break

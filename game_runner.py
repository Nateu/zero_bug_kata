from random import randrange
from game import Game

def write_log(s: str):
    with open("command.log", "a") as log_file:
        log_file.write(s)
        log_file.write("\r")


if __name__ == '__main__':

    winner = False

    game = Game(15)

    game.add('Chet')
    write_log("game.add('Chet')")
    game.add('Pat')
    write_log("game.add('Pat')")
    game.add('Sue')
    write_log("game.add('Sue')")

    while True:
        roll = randrange(5) + 1
        game.roll(roll)
        write_log(f"game.roll({roll})")

        if randrange(9) == 7:
            winner = game.wrong_answer()
            write_log("game.wrong_answer()")
        else:
            winner = game.was_correctly_answered()
            write_log("game.was_correctly_answered()")
        
        if winner: break
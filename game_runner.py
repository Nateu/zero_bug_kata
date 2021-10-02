from random import randrange
from game import Game

def write_log(s: str):
    with open("command.log", "a") as log_file:
        log_file.write(s)
        log_file.write("\r")


if __name__ == '__main__':

    winner = False

    game = Game(15)

    game.add_player('Chet')
    write_log("game.add_player('Chet')")
    game.add_player('Pat')
    write_log("game.add_player('Pat')")
    game.add_player('Sue')
    write_log("game.add_player('Sue')")

    while True:
        roll = randrange(5) + 1 # roll a d6
        game.roll(roll)
        write_log(f"game.roll({roll})")

        if randrange(9) == 7: # one in 9 chance someone answers wrong
            winner = game.incorrectly_answered()
            write_log("game.incorrectly_answered()")
        else:
            winner = game.correctly_answered()
            write_log("game.correctly_answered()")
        
        if winner: break
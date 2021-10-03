from mamba import describe, context, it, before
from expects import expect, equal
from game import Game

def add_two_players(game):
    game.add_player("Player 1")
    game.add_player("Player 2")


with describe('Given we play a short game of trivial persuit') as self:
    with before.each:
        self.game = Game(coins_to_win=1, max_players=2)
    
    with context('when we roll a die with less than 2 players'):
        with it('should return False'):
            expect(self.game.roll(3)).to(equal(None))

    with context('when we have 2 players'):
        with before.each:
            add_two_players(self.game)

        with context('and we try add a thrid'):
            with it('should return False'):
                expect(self.game.add_player("Player 3")).to(equal(False))

with describe('Given we play a short 2 player game of trivial persuit') as self:
    with before.each:
        self.game = Game(coins_to_win=1, max_players=2)
        add_two_players(self.game)

    with context('when the first player rolls a 2'):
        with it('should return Sports'):
            expect(self.game.roll(2)).to(equal('Sports'))

    with context('when the first player rolls a 2'):
        with before.each:
            self.game.roll(2)

        with context('and they answer correctly'):
            with it('should return True'):
                expect(self.game.correctly_answered()).to(equal(True))

        with context('and they answer incorrectly'):
            with it('should return False'):
                expect(self.game.incorrectly_answered()).to(equal(False))

    with context('when the second player rolls a also answers incorrectly'):
        with before.each:
            self.game.roll(2)
            self.game.incorrectly_answered()
            self.game.roll(1)
            self.game.incorrectly_answered()

        with context('and the first player rolls an even number'):
            with it('should return None'):
                expect(self.game.roll(2)).to(equal(None))

        with context('and the first player rolls an odd number'):
            with it('should return None'):
                expect(self.game.roll(3)).to(equal('Science'))

with describe('Given we are half way into a medium length game with 2 player') as self:
    with before.each:
        self.game = Game(coins_to_win=3, max_players=2)
        add_two_players(self.game)
        self.game.roll(2) #P1 -> Sports
        self.game.correctly_answered() #P1 -> 1 Coin
        self.game.roll(1) #P2 -> Science
        self.game.incorrectly_answered() #P2 -> penalty box
        self.game.roll(2) #P1 -> Pop
        self.game.correctly_answered() #P1 -> 2 Coin
        self.game.roll(3) #P2 -> Pop
        self.game.correctly_answered() #P2 -> out of penalty box & 1 Coin
        self.game.roll(3) #P1 -> Rock
        self.game.incorrectly_answered() #P1 -> penalty box

    with context('and the second player rolls a even number after just leaving the penalty box'):
        with it('should return Sports'):
            expect(self.game.roll(2)).to(equal('Sports'))

with describe('Given the first question of the game is incorrectly answered') as self:
    with before.each:
        self.game = Game(coins_to_win=3, max_players=2)
        add_two_players(self.game)
        self.game.incorrectly_answered() #P1 -> penalty box

    with context('and the first player answers a second question'):
        with it('should return False'):
            expect(self.game.correctly_answered()).to(equal(False))

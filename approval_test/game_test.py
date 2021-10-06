import unittest
from approvaltests.approvals import verify
from subprocess import run


class ApprovalTest(unittest.TestCase):
    def test_game(self):
        output = run(["python", "game_runner.py"], capture_output=True).stdout
        verify(output)


if __name__ == "__main__":
    unittest.main()

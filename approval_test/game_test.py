import unittest
from approvaltests.approvals import verify
from subprocess import run

class GameTest(unittest.TestCase):
    def test_script(self):
        output = run(["python", "scripted_run.py"], capture_output=True).stdout
        verify(output)

if __name__ == "__main__":
    unittest.main()
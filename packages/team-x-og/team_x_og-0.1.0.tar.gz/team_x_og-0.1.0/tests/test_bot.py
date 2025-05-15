import unittest
from team_x_og import TeamXBot, TokenInvalidError, BotRunningError

class TestTeamXBot(unittest.TestCase):
    def test_empty_token(self):
        with self.assertRaises(TokenInvalidError):
            TeamXBot("")

    def test_multiple_instances(self):
        bot1 = TeamXBot("DUMMY_TOKEN")
        with self.assertRaises(BotRunningError):
            TeamXBot("ANOTHER_TOKEN")

if __name__ == "__main__":
    unittest.main()
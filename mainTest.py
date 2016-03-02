

# Initialize the game
import game
import player
testGame = game.Game()

corp = player.Player('corp');
runner = player.Player('runner');

outcome = testGame.playthrough(corp, runner);
import chess.uci as uci
import evolveyourchess as eyc
from tqdm import tqdm
import sys

from require import require
config = require('./config.py')

# read pgns into games
print('Loading PGNs')
all_games = []
for pgn_filepath in sys.argv[1:]:
    with open(pgn_filepath) as f:
        all_games += list(eyc.parse_pgns(f))

engine = uci.popen_engine(config.ENGINE)
analyzer = eyc.Analyzer(engine)

for color in ['White', 'Black']:

    games = [game for game in all_games if game.headers[color] == 'pcattori']
    print('\nConstructing {} graph'.format(color))
    graph = eyc.Graph(tqdm(games), color[0].lower())

    print('Finding MCB for', color)
    position, _, move = analyzer.most_common_blunder(graph, progress=tqdm)
    board = eyc.Board(position)
    print(board.fen())
    print(board)
    print('You played: {} ({} times)'.format(
        board.san(move['move']), len(move['play_refs'])))
    recommended = analyzer.consult(position)['pv'][1][0]
    print('EYC recommends:', board.san(recommended))

engine.quit()


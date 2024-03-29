import evolveyourchess as eyc
from tqdm import tqdm
import sys

# read pgns into games
print('Loading PGNs')
all_games = []
for pgn_filepath in sys.argv[2:]:
    with open(pgn_filepath) as f:
        all_games += list(eyc.parse_pgns(f))

analyzer = eyc.Analyzer()

for color in ['White', 'Black']:

    games = [game for game in all_games if game.headers[color] == sys.argv[1]]
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


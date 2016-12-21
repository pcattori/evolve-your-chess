import evolveyourchess as eyc
import chess.pgn as pgn

def parse_pgns(f):
    while True:
        game = pgn.read_game(f)
        if game is None:
            break
        yield game

def eco_from_position(openings):
    position_lookup = {}
    for eco, name, moves in openings:
        board = eyc.Board()
        for move in moves:
            board.push_san(move)
        position_lookup[board.FEN()] = (eco, name)
    return position_lookup


import chess.pgn as pgn

def parse_pgns(f):
    while True:
        game = pgn.read_game(f)
        if game is None:
            break
        yield game


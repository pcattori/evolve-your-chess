import evolveyourchess as eyc
import chess.uci as uci
import contextlib

def fake_castling(board_color):
    fake_fen = eyc.FEN(
        board_color.board, board_color.color, 'KQkq', '-', '0', '0')
    board = eyc.Board(fake_fen)
    board.clean_castling_rights()
    return board.castling_xfen()

def fake_position(board_color):
    return eyc.FEN(
        board_color.board, board_color.color,
        fake_castling(board_color),
        '-', '0', '0')

@contextlib.contextmanager
def info_handler(engine):
    info_handlers = engine.info_handlers
    info_handler = uci.InfoHandler()
    engine.info_handlers.append(info_handler)
    yield info_handler
    engine.info_handlers = info_handlers

class Analyzer:
    def __init__(self, chess_engine, movetime=1e2):
        self.engine = chess_engine

    def consult(self, position):
        with info_handler(self.engine) as info:
            self.engine.position(eyc.Board(position))
            self.engine.go(movetime=self.movetime)
            return info.info

    def cp_diff(self, start_position, end_position):
        start_score = self.consult(start_position)['score'][1]
        end_score = self.consult(end_position)['score'][1]
        if start_score.cp is None or end_score.cp is None:
            raise NotImplementedError('Analyzer cannot handle checkmate detection')
        return start_score.cp - (end_score.cp * -1)

    def most_common_blunder(self, graph, centipawns=100, progress=lambda loop: loop):
        # transitions by frequency
        transitions_by_frequency = sorted(
            graph.edges(data=True),
            key=lambda e: len(e[2]['play_refs']),
            reverse=True)
        for start_pos, end_pos, move in progress(transitions_by_frequency):
            # skip other player's moves
            if start_pos.color != graph.color:
                continue

            # blunder detection
            if self.cp_diff(fake_position(start_pos), fake_position(end_pos)) > centipawns:
                return start_pos, end_pos, move
        return None

    def most_common_blunder_position(self, centipawns=100):
        # for each node, see how many blunders occurred from that position
        pass

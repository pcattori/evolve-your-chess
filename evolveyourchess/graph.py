import collections
import networkx as nx

import evolveyourchess as eyc

# nodes
BoardColor = collections.namedtuple('BoardColor', ['board', 'color'])
def board_color(position):
    return BoardColor(position.board, position.color)

# edges
Transition = collections.namedtuple('Transition', ['start', 'end', 'move'])

# metadata
PlayReference = collections.namedtuple('PlayReference', ['game', 'ply', 'fen'])

def graph(games):
    nodes = collections.defaultdict(list)
    edges = collections.defaultdict(list)
    for game in games:
        # compute stateless positions
        board = eyc.Board()
        positions = [board_color(board.FEN())]
        moves = []
        for move in game.main_line():
            moves.append(move)
            board.push(move)
            positions.append(board.FEN())

        # construct nodes from positions
        for ply, position in enumerate(positions):
            ref = PlayReference(game, ply, position)
            nodes[board_color(position)].append(ref)

        # construct edges from moves
        for ply, move in enumerate(moves):
            transition = Transition(
                board_color(positions[ply]),
                board_color(positions[ply + 1]),
                move)
            start_ref = PlayReference(game, ply, positions[ply])
            end_ref = PlayReference(game, ply + 1, positions[ply + 1])
            edges[transition].append((start_ref, end_ref))

    return nodes, edges

# TODO better name??
class Graph(nx.DiGraph):
    def __init__(self, games, color):
        self.games = games
        self.color = color
        super().__init__()

        nodes, edges = graph(games)
        # wire nodes with edges to form graph
        for node, play_refs in nodes.items():
            self.add_node(node, play_refs=play_refs)
        for edge, play_refs in edges.items():
            self.add_edge(
                edge.start, edge.end, move=edge.move,
                play_refs=play_refs)


import chess
import collections
import matplotlib.pyplot as plt
import networkx as nx
import pgn
import re
import sys
from tqdm import tqdm

def with_pieces(board):
    return str(board) \
        .replace('K', '♚') \
        .replace('Q', '♛') \
        .replace('R', '♜') \
        .replace('B', '♝') \
        .replace('N', '♞') \
        .replace('P', '♟') \
        .replace('k', '♔') \
        .replace('q', '♕') \
        .replace('r', '♖') \
        .replace('b', '♗') \
        .replace('n', '♘') \
        .replace('p', '♙')

def only_moves(moves):
    # ignore comments wrapped in curly brackets
    for move in moves[:-1]:
        if re.match(r'{[^}]*}', move):
            continue
        else:
            yield move

def fen(board):
    # treat positions as stateless
    # TODO handle castling rights and en-passant possibility more gracefully
    return ' '.join(board.fen().split()[:-2])

def game_tree(games):
    tree = nx.DiGraph()

    nodes = collections.defaultdict(int)
    edges = collections.defaultdict(int)
    for game in tqdm(games):
        board = chess.Board()
        positions = [fen(board)]
        moves = []
        for move in only_moves(game.moves):
            moves.append(move)
            board.push_san(move)
            positions.append(fen(board))

        for position in positions:
            nodes[position] += 1

        transitions = zip(positions, moves, positions[1:])
        for transition in transitions:
            edges[transition] += 1

    for node in nodes:
        tree.add_node(node)
    for edge, weight in edges.items():
        pos1, move, pos2 = edge
        tree.add_edge(pos1, pos2, move=move, weight=weight)

    return tree

if __name__ == '__main__':
    username = input('username? > ')

    # read pgns
    print('reading pgns')
    with open(sys.argv[1], 'r') as f:
        games = pgn.loads(f.read())

    print('filtering games by color')
    white_games = [game for game in games if game.white == username]
    black_games = [game for game in games if game.black == username]

    print('creating white move tree')
    white_tree = game_tree(white_games)

    position = fen(chess.Board())
    #print(next(iter(white_tree.edges(data=True))))
    while True:
        print(chess.Board(position + ' 0 0'))
        moves = [
            (edge[2]['move'], edge[2]['weight'])
            for edge in white_tree.edges(data=True)
            if edge[0] == position
        ]
        moves = sorted(moves, key=lambda m: m[1], reverse=True)
        print(list(enumerate(moves)))
        move = moves[int(input('which move? > '))][0]
        print('chose: "{}"'.format(move))
        board = chess.Board(position + ' 0 0')
        board.push_san(move)
        position = fen(board)


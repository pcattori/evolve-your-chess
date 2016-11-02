import collections
import networkx as nx
import pgn
import re
import sys
from tqdm import tqdm

def move_filter(move):
    comment_pattern = r'{[^}]*}'
    score_pattern = r'(?:1-0)|(?:0-1)|(?:1/2-1/2)'
    return \
        not re.match(comment_pattern, move) and \
        not re.match(score_pattern, move)

def stateless_board(position_color):
    return Board('{} KQkq - 0 0'.format(position_color))

def game_tree(games):
    tree = nx.DiGraph()

    nodes = collections.defaultdict(int)
    edges = collections.defaultdict(int)
    for game in tqdm(games):
        board = Board()
        positions = [board.stateless_fen()]
        moves = []
        for move in filter(move_filter, game.moves):
            moves.append(move)
            board.push_san(move)
            positions.append(board.stateless_fen())

        for position in positions:
            nodes[position] += 1

        transitions = zip(positions, moves, positions[1:])
        for transition in transitions:
            edges[transition] += 1

    for node in nodes:
        tree.add_node(node)
    for edge, weight in edges.items():
        from_pos, move, to_pos = edge
        tree.add_edge(from_pos, to_pos, move=move, weight=weight)

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

    position = Board().stateless_fen()
    while True:
        print(stateless_board(position))
        moves = [
            (edge[2]['move'], edge[2]['weight'])
            for edge in white_tree.edges(data=True)
            if edge[0] == position
        ]
        moves = sorted(moves, key=lambda m: m[1], reverse=True)
        print(list(enumerate(moves)))
        move = moves[int(input('which move? > '))][0]
        print('chose: "{}"'.format(move))
        board = stateless_board(position)
        board.push_san(move)
        position = board.stateless_fen()


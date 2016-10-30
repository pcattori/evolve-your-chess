import collections
import matplotlib.pyplot as plt
import networkx as nx
import pgn
import re
import sys
from tqdm import tqdm

def only_moves(moves):
    for move in moves:
        if re.match(r'{[^}]*}', move):
            continue
        else:
            yield move

def game_tree(games):
    tree = nx.DiGraph()

    nodes = set()
    edges = collections.defaultdict(int)
    for game in tqdm(games):

        # compute moves
        moves = []
        for i, move in enumerate(only_moves(game.moves)):
            ply = '{}{}'.format((i // 2) + 1, '.' if i % 2 == 0 else '...')
            moves.append((ply, move))

        # construct nodes from moves
        nodes.update(moves)

        # construct edges from moves
        transitions = zip(['start'] + moves, moves)
        for transition in transitions:
            edges[transition] += 1

    for node in nodes:
        tree.add_node(node)
    for edge, weight in edges.items():
        tree.add_edge(*edge, weight=weight)

    return tree

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
print('creating black move tree')
black_tree = game_tree(black_games)

node = 'start'
while True:
    moves = [
        (edge[1], edge[2]['weight'])
        for edge in white_tree.edges(data=True)
        if edge[0] == node]
    moves = sorted(moves, key=lambda m: m[1], reverse=True)

    print(list(enumerate(moves)))
    node = moves[int(input('which move? > '))][0]
    print('chose: "{}"'.format(node))

# print('plotting')
# pos = nx.spring_layout(white_tree)
# nx.draw_networkx_nodes(white_tree, pos, node_size=700)
# nx.draw_networkx_edges(white_tree, pos, width=6)
# nx.draw_networkx_labels(white_tree, pos, font_size=20, font_family='sans-serif')
#
# plt.axis('off')
# plt.savefig("weighted_graph.png") # save as png
# plt.show() # display


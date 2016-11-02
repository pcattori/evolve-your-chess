from bs4 import BeautifulSoup
import collections
import json
import re
import requests
import os

from require import require
Board = require('../lib/board.py').Board
config = require('../config.py')

# utils

EcoEntry = collections.namedtuple('EcoEntry', ['eco', 'name', 'moves'])

def parse_moves(moves):
    moves = re.split(r'\d+\.', moves)[1:]
    return tuple(ply for move in moves for ply in move.strip().split())

# TODO factor out into lib
def eco_from_position(openings):
    position_lookup = {}
    for eco, name, moves in openings:
        board = Board()
        for move in moves:
            board.push_san(move)
        position_lookup[board.stateless_fen()] = (eco, name)
    return position_lookup

# scrape

if __name__ == '__main__':
    response = requests.get('http://www.365chess.com/eco.php')
    soup = BeautifulSoup(response.text, 'html.parser')
    ecotree = soup.find(id='ecotree')
    lines = ecotree.find_all('div', class_='line')

    openings = set()
    for line in lines:
        eco, name = line.find('div', class_='opname').a.string.split(' ', 1)
        name = name.strip()
        moves = line.find('div', class_='opmoves')
        if moves is None:
            moves = line.find('div', class_='fright')
        moves = parse_moves(moves.string)
        openings.add(EcoEntry(eco, name, moves))

    with open(os.path.join(config.DATA, 'eco.json'), 'w') as f:
        for opening in openings:
            print(json.dumps(opening._asdict()), file=f)


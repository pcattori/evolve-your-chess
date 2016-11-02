from bs4 import BeautifulSoup
import collections
import re
import requests

from require import require
Board = require('./board.py').Board

# utils

EcoEntry = collections.namedtuple('EcoEntry', ['eco', 'name', 'moves'])

def parse_moves(moves):
    moves = re.split(r'\d+\.', moves)[1:]
    return tuple(ply for move in moves for ply in move.strip().split())

# scrape

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

# convert to stateless FEN
position_names = {}
for eco, name, moves in openings:
    board = Board()
    for move in moves:
        board.push_san(move)
    position_names[board.stateless_fen()] = (eco, name)

print(len(position_names))
print(next(iter(position_names.items())))

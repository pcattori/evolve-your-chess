from bs4 import BeautifulSoup
import collections
import re
import requests

# utils

EcoEntry = collections.namedtuple('EcoEntry', ['eco', 'name', 'moves'])

def parse_moves(moves):
    moves = re.split(r'\d+\.', moves)[1:]
    return tuple(tuple(move.strip().split()) for move in moves)

# scrape

response = requests.get('http://www.365chess.com/eco.php')
soup = BeautifulSoup(response.text, 'html.parser')
ecotree = soup.find(id='ecotree')
lines = ecotree.find_all('div', class_='line')

openings = set()
for line in lines:
  eco, name = line.find('div', class_='opname').a.string.split(' ', 1)
  moves = line.find('div', class_='opmoves')
  if moves is None:
    moves = line.find('div', class_='fright')
  moves = parse_moves(moves.string)
  openings.add(EcoEntry(eco, name, moves))

print(len(openings))
print(next(iter(openings)))


# evolve-your-chess

Improve your chess via batch analysis and Darwinian selection!


## Installing

```sh
$ git clone https://github.com/pcattori/evolve-your-chess
$ cd evolve-your-chess
$ python setup.py develop # link to the library
$ pip install -r example/requirements.txt # install external dependencies
```

## Running

```sh
$ python example/evolve.py <path/to/pgns>
```

## Utilities

UNDOCUMENTED FEATURES - MAY BE OUTDATED - USE AT YOUR OWN RISK

### Fetching your chess.com PGNs

See `fetch/chess_dot_com_pgns.py`

Requires [`chromedriver`](https://sites.google.com/a/chromium.org/chromedriver/)
to be installed and binary to be placed at `chess-trainer/bin/chromedriver`

### Fetching ECO

See `fetch/eco.py`


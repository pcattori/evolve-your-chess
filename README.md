# evolve-your-chess

Improve your chess via batch analysis and Darwinian selection!


## Installing

```sh
$ git clone https://github.com/pcattori/evolve-your-chess
$ cd evolve-your-chess
$ pip install -e . # link to the library
$ pip install -r example/requirements.txt # install external dependencies
```

WARNING: You will need a copy of [Stockfish](https://stockfishchess.org/) that is accessible to EYC until EYC bundles in its chess engine dependencies.

## Running

```sh
$ python example/evolve.py <your-chess.com-username> [... paths/to/pgns]
```

Example:

![evolve-example](assets/evolve.png)

Some things to know:
- MCB stands for "Most Common Blunder"
- EYC sorts your moves by frequency and short-circuits once it finds the first move in that list that Stockfish considers a blunder. That's why the "Finding MCB" progress bars do not complete.

# Fetch utilities

## Install

```sh
$ pip install -e .[fetch]
```

## chess.com PGN fetcher

Requires [`chromedriver`](https://sites.google.com/a/chromium.org/chromedriver/)

```sh
python fetch/chess_dot_com_pgns.py \
    --driver <path/to/chromedriver> \
    --output <path/to/output-directory>
```

Downloads PGNs from [your chess.com archives](https://www.chess.com/games/archive).

For short, you can use `-d` for `--driver` and `-o` for `--output`.

You can specify a number of chess.com archive pages with the `-p` or `--pages` flag.

### Advanced search

You can leverage chess.com's advanced search capabilities to specify which games to download.

1. Navigate to [your chess.com archives](https://www.chess.com/games/archive).
2. Click  "Advanced" in the Archive search panel.
    ![simple-search](assets/simple-search.png)
3. Set your search filters in the Archive advanced search panel
    ![advanced-search](assets/advanced-search.png)
4. Click "Search"
5. Copy the URL that appears in your browser

Pass that URL (surrounded by quotes) to the fetcher via the `-f` or `--filter-url` flag.

Make sure your search actually returned some results on chess.com first!

## ECO JSON fetcher

```sh
python fetch/eco.py
```

will print newline-delimited ECO records to your stdout.


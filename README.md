# evolve-your-chess (EYC)

Improve your chess via batch analysis and Darwinian selection!

In other words, let EYC find your "Most Common Blunder" (MCB).

:zap: Batteries included: Comes bundled with [Stockfish 8](https://stockfishchess.org/)



## Table of Contents

  * [evolve\-your\-chess (EYC)](#evolve-your-chess-eyc)
  * [Table of Contents](#table-of-contents)
    * [Install](#install)
    * [Running Example](#running-example)
  * [Fetch utilities](#fetch-utilities)
    * [Install](#install-1)
    * [chess\.com PGN fetcher](#chesscom-pgn-fetcher)
      * [Options](#options)
      * [Advanced search](#advanced-search)
    * [ECO JSON fetcher](#eco-json-fetcher)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

## Install

```sh
$ git clone https://github.com/pcattori/evolve-your-chess
$ cd evolve-your-chess
$ pip install -e . # link to the library
```

## Running Example

Make sure you have followed the [installation instructions](#installing), then:

```sh
$ pip install -r example/requirements.txt
$ python example/evolve.py <your-chess.com-username> [... paths/to/pgns]
```

Example:

![evolve-example](assets/evolve.png)

# Fetch utilities

## Install

Follow the [base installation instructions](#installing), but replace `pip install -e .` with:

```sh
$ pip install -e .[fetch]
```

## chess.com PGN fetcher

:zap: Batteries included: Comes bundled with [`chromedriver`](https://sites.google.com/a/chromium.org/chromedriver/) so that [selenium](https://github.com/SeleniumHQ/selenium) can download PGNs for you.

*Requires:* [ChromeDriver expects you to have Chrome installed in the default location for your platform.](https://sites.google.com/a/chromium.org/chromedriver/getting-started)

```sh
$ eyc-chess-dot-com-pgns
```

Downloads PGNs from [your chess.com archives](https://www.chess.com/games/archive).

### Options

`-f` or `--filter-url` to provide a chess.com advanced search URL.
See [Advanced search](#advanced-search) for more details.

`-o` or `--output` to specify download directory.
Defaults to `~/Downloads`.

`-p` or `--pages` to specify the number of chess.com archive pages to download.
Defaults to `20`.

`-d` or `--driver` to specify a different selenium driver.
Defaults to built-in `chromedriver`.
*warning* drivers other than `chromedriver` are not officially supported

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

Make sure your search actually returned some results on chess.com first before
trying it with `eyc-chess-dot-com-pgns`!

## ECO JSON fetcher

```sh
$ eyc-eco
```

will print newline-delimited ECO records to your stdout.


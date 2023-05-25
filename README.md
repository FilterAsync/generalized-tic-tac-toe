# Generalized Tic Tac Toe

A generalized version of traditional Tic Tac Toe: play Tic Tac Toe with arbitrary board size and number of marks to win. Given $n$ and $m$, one can play $n \times n$ board with $m$ number of marks to win. A player wins when placing $m$ pieces of his choice in a consecutive order. The game may end in a draw if no one wins.


This game is made with [pygame](https://github.com/pygame/pygame) library.

## Play the game
Run the `main.py` script with the following arguments:
1. board width and
2. number of marks to win.


The default values will be used if one of the arguments is invalidated.

## Features
You can play with AI or another person.
|   Key     | Description                     |
|:---------:|---------------------------------|
|   `G`     | Change gamemode (AI or player). |
|   `R`     | Restart the game.               |
|   `0`     | Use random algorithm for AI.    |
|   `1`     | Use minimax algorithm for AI.   |

## Contribution
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing
The code in this project is licensed under MIT license.

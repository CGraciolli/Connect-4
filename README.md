# Connect 4

A game of Connect 4.
There are 4 difficulties:
1. In easy, the computer plays randomly.
2. In medium, the computer recognizes moves that will win or lose immediatly.
3. In hard, the computer learns with each match.
4. In very hard, the computer starts with a base knowledge acquired by playing against itself and continues to learn during the matches against the human.

This project comes from a online course from KeepCoding (Curso Resolución de Problemas con OOP y TDD - Introducción IA y Machine Learning)

What I did by myself:
1. Implemented the possibility of the computer learning prior to starting the game.
2. The function get_help.
3.The ability to learn after winning (the computer only learnt when losing before).
4. The ability to learn by looking at symmetric moves on the board.
5. The class Knowledge (it was an attribute of oracle before).

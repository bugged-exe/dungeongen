# dungeongen
A program that generates a grid and prints a dungeon with one room in the terminal.

## Design Choices
Below are the design choices I have gone for.

### Tile Representation
Tiles will be represented as an Enum, for example (Tiles.DOOR, Tiles.WATER, etc)

### Grid Structure
There will be a Grid class with a width and a height, and a way of getting
and setting tiles.

### Coordinates
To get a specific tile will be a 2 vars passed into the get function, (x, y)

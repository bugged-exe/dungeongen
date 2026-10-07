from .tiles import Tiles


class Grid:
    def __init__(self, width: int, height: int, fill: Tiles = Tiles.WALL) -> None:
        if width < 1 or height < 1:
            raise ValueError(f"Width or height of the grid is set to less than 1, this will cause a crash. w={width} h={height}")

        self._width: int = width
        self._height: int = height

        self._tiles: list[list[Tiles]] = self.build_tiles(fill)

    def build_tiles(self, fill: Tiles) -> list[list[Tiles]]:
        tiles: list[list[Tiles]] = []

        for _ in range(self._height):
            row_map: list[Tiles] = []
            for _ in range(self._width):
                row_map.append(fill)

            tiles.append(row_map)
        return tiles
        
    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 <= y < self._height
            
    def get(self, x: int, y: int) -> Tiles:
        if not self.in_bounds(x, y):
            raise IndexError("The specified x and y coords are not within the bounds of the grid.")
        
        return self._tiles[y][x]

    def set(self, x: int, y: int, tile: Tiles) -> None:
        if not self.in_bounds(x, y):
            raise IndexError("The specified x and y coords are not within the bounds of the grid.")

        self._tiles[y][x] = tile

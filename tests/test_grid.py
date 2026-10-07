import pytest

from dungeongen.grid import Grid
from dungeongen.tiles import Tiles

# --- construction ---------------------------------------------------------


def test_new_grid_has_correct_size():
    g = Grid(5, 3)
    assert g.width == 5
    assert g.height == 3


def test_new_grid_is_filled_with_wall_by_default():
    g = Grid(5, 3)
    for y in range(3):
        for x in range(5):
            assert g.get(x, y) == Tiles.WALL


def test_new_grid_uses_custom_fill():
    g = Grid(4, 4, fill=Tiles.FLOOR)
    for y in range(4):
        for x in range(4):
            assert g.get(x, y) == Tiles.FLOOR


@pytest.mark.parametrize("w, h", [(0, 5), (5, 0), (0, 0), (-1, 5), (5, -1)])
def test_invalid_size_raises_value_error(w, h):
    with pytest.raises(ValueError):
        Grid(w, h)


def test_one_by_one_grid_is_valid():
    g = Grid(1, 1)
    assert g.get(0, 0) == Tiles.WALL


# --- properties -----------------------------------------------------------


def test_width_and_height_are_read_only():
    g = Grid(5, 3)
    with pytest.raises(AttributeError):
        g.width = 10  # type: ignore[misc]
    with pytest.raises(AttributeError):
        g.height = 10  # type: ignore[misc]


# --- in_bounds ------------------------------------------------------------


@pytest.mark.parametrize("x, y", [(0, 0), (4, 0), (0, 2), (4, 2), (2, 1)])
def test_in_bounds_true_for_valid_coords(x, y):
    g = Grid(5, 3)
    assert g.in_bounds(x, y) is True


@pytest.mark.parametrize(
    "x, y",
    [(-1, 0), (0, -1), (5, 0), (0, 3), (5, 3), (-1, -1), (100, 100)],
)
def test_in_bounds_false_for_invalid_coords(x, y):
    g = Grid(5, 3)
    assert g.in_bounds(x, y) is False


# --- get / set ------------------------------------------------------------


def test_set_then_get_returns_the_new_tile():
    g = Grid(5, 3)
    g.set(2, 1, Tiles.FLOOR)
    assert g.get(2, 1) == Tiles.FLOOR


def test_set_does_not_change_other_tiles():
    g = Grid(5, 3)
    g.set(4, 2, Tiles.FLOOR)
    assert g.get(0, 0) == Tiles.WALL
    assert g.get(3, 2) == Tiles.WALL
    assert g.get(4, 1) == Tiles.WALL


def test_set_works_on_all_four_corners():
    g = Grid(5, 3)
    corners = [(0, 0), (4, 0), (0, 2), (4, 2)]
    for x, y in corners:
        g.set(x, y, Tiles.FLOOR)
    for x, y in corners:
        assert g.get(x, y) == Tiles.FLOOR
    assert g.get(2, 1) == Tiles.WALL


def test_rows_are_not_shared():
    # Catches the [[fill] * width] * height bug: changing one tile
    # must not change the same column in every other row.
    g = Grid(3, 3)
    g.set(0, 0, Tiles.FLOOR)
    assert g.get(0, 1) == Tiles.WALL
    assert g.get(0, 2) == Tiles.WALL


def test_x_and_y_are_not_swapped():
    # Non-square grid so a swapped x/y either lands on the wrong tile
    # or raises an error.
    g = Grid(5, 2)
    g.set(4, 0, Tiles.FLOOR)
    assert g.get(4, 0) == Tiles.FLOOR
    assert g.get(0, 1) == Tiles.WALL


# --- out-of-bounds errors -------------------------------------------------


@pytest.mark.parametrize("x, y", [(-1, 0), (0, -1), (5, 0), (0, 3), (5, 3)])
def test_get_out_of_bounds_raises_index_error(x, y):
    g = Grid(5, 3)
    with pytest.raises(IndexError):
        g.get(x, y)


@pytest.mark.parametrize("x, y", [(-1, 0), (0, -1), (5, 0), (0, 3), (5, 3)])
def test_set_out_of_bounds_raises_index_error(x, y):
    g = Grid(5, 3)
    with pytest.raises(IndexError):
        g.set(x, y, Tiles.FLOOR)


def test_failed_set_does_not_modify_grid():
    g = Grid(5, 3)
    with pytest.raises(IndexError):
        g.set(5, 3, Tiles.FLOOR)
    for y in range(3):
        for x in range(5):
            assert g.get(x, y) == Tiles.WALL

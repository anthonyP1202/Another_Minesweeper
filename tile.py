class Tile:
    def __init__(self, location, is_mine=False, mine_value=1):
        self.is_mine = is_mine  # Instance variable for whether this tile is a mine
        self.location = location  # Location of the tile
        self.surrounding_mine = 0  # Instance variable for the count of surrounding mines


    def surrounding_mines(self, board, away=1):
        '''Checks the surrounding tiles and counts the mines to update the surrounding mine value'''
        # If this tile is a mine, set surrounding_mine to 10
        if self.is_mine:
            self.surrounding_mine = 9
            return

        # Reset surrounding mines for this tile
        self.surrounding_mine = 0

        # Check all tiles within the "away" distance (default is 1, so 8 surrounding tiles)
        for i in range(-away, away + 1):
            for j in range(-away, away + 1):
                # Skip the tile itself
                if i == 0 and j == 0:
                    continue

                # Calculate surrounding tile's coordinates
                x = self.location[0] + i
                y = self.location[1] + j

                # Check if the surrounding coordinates are within the board's bounds
                if 0 <= x < len(board) and 0 <= y < len(board[0]):
                    if board[x][y].is_mine:  # Check if the surrounding tile is a mine
                        self.surrounding_mine += 1

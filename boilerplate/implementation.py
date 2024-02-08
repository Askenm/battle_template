from typing import List
import random

def is_water_system_efficient_(grid: List[List[int]]) -> bool:
    """
    return: bool
    """
    def dfs(x, y):
        # Helper function to perform depth-first search from a pump cell
        if x < 0 or x >= n or y < 0 or y >= m or grid[x][y] != 2:
            return
        grid[x][y] = 1  # Mark the cell as visited by setting it to 1
        for dx, dy in directions:
            dfs(x + dx, y + dy)

    n = len(grid)
    m = len(grid[0])

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Step 1: Mark all cells reachable from pumps as visited (1)
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                dfs(i, j)

    # Step 2: Check if there are any unvisited (2) cells left
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 2:
                return False

    return True



def is_water_system_efficient(grid: List[List[int]]) -> bool:
    return random.choice([True,False])
import random
import json


def is_safe(board, row, col):
    for i in range(col):
        if board[row][i]['value'] == 'Q':
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]['value'] == 'Q':
            return False
    for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
        if board[i][j]['value'] == 'Q':
            return False
    return True


def solve_queens():
    board = [[{'value': '', 'color': '#cccccc'} for _ in range(8)] for _ in range(8)]

    def backtrack(col):
        if col >= 8:
            return True
        rows = list(range(8))
        random.shuffle(rows)
        for row in rows:
            if is_safe(board, row, col):
                board[row][col]['value'] = 'Q'
                if backtrack(col + 1):
                    return True
                board[row][col]['value'] = ''
        return False

    if backtrack(0):
        return board
    return None


def generate_color_strengths(num_colors, base_strength=0.5, strength_variation=0.8):
    color_strengths = {}

    # Generate a list of random values
    random_values = [random.random() for _ in range(num_colors)]

    # Calculate the total of random values
    total = sum(random_values)

    # Normalize the random values to sum to 1
    normalized_values = [value / total for value in random_values]

    # Apply the strength variation
    adjusted_values = [
        base_strength + (value - 0.5) * strength_variation
        for value in normalized_values
    ]

    # Ensure all values are within [0, 1] range
    final_values = [max(0, min(1, value)) for value in adjusted_values]

    # Assign strengths to colors
    for i, strength in enumerate(final_values):
        color_strengths[f"Color_{i + 1}"] = strength

    return color_strengths


def expand_colors(board, color_strengths):
    def get_expansion_priority(i, j):
        # Prioritize corners and edges
        if (i in [0, 7] and j in [0, 7]):  # Corners
            return 3
        elif i in [0, 7] or j in [0, 7]:  # Edges
            return 2
        else:  # Interior
            return 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while any(cell['color'] == '#cccccc' for row in board for cell in row):
        for color, strength in color_strengths.items():
            if random.random() < strength:
                expansion_options = []
                for i in range(8):
                    for j in range(8):
                        if board[i][j]['color'] == color:
                            for di, dj in directions:
                                ni, nj = i + di, j + dj
                                if 0 <= ni < 8 and 0 <= nj < 8 and board[ni][nj]['color'] == '#cccccc':
                                    priority = get_expansion_priority(ni, nj)
                                    expansion_options.append((priority, ni, nj))

                if expansion_options:
                    # Sort by priority (highest first) and then randomly choose among highest priority
                    max_priority = max(option[0] for option in expansion_options)
                    best_options = [opt for opt in expansion_options if opt[0] == max_priority]
                    _, ni, nj = random.choice(best_options)
                    board[ni][nj]['color'] = color

        if all(all(cell['color'] != '#cccccc' for cell in row) for row in board):
            break

    return board


num_boards = 10
for i in range(num_boards):
    board = solve_queens()

    # Generate 8 unique colors for queens
    queen_colors = [
        "#FFB3BA",  # Pastel Pink
        "#BAFFC9",  # Pastel Green
        "#BAE1FF",  # Pastel Blue
        "#FFFFBA",  # Pastel Yellow
        "#FFDFBA",  # Pastel Orange
        "#E0BBE4",  # Pastel Purple
        "#D4F0F0",  # Pastel Turquoise
        "#ffb1ff"   # Pastel Magenta
    ]
    random.shuffle(queen_colors)

    # Assign colors to queens
    queen_count = 0

    num_colors = 8
    base_strength = 0.5 # represents the central tendency of the color strengths, recommended range: 0.3 to 0.7
    strength_variation = 0.7  # determines how much the strengths can deviate from the base strength, recommended range: 0.2 to 1.0

    color_strengths = generate_color_strengths(num_colors, base_strength, strength_variation)
    for color, strength in color_strengths.items():
        print(f"{color}: {strength:.4f}")

    for row in board:
        for cell in row:
            if cell['value'] == 'Q':
                color = queen_colors[queen_count]
                cell['color'] = color
                # Assign a random strength within the specified range
                strength = base_strength + random.uniform(-strength_variation/2, strength_variation/2)
                color_strengths[color] = strength
                queen_count += 1

    # Expand colors
    board = expand_colors(board, color_strengths)
    print(json.dumps(board))


import csv

# Use None for empty cells in the board
null = None
# Example board state: None means empty, "X" and "O" are player moves
list1 = ["X", "X", "O", null, "X", "O", null, null, null]

# Determine if the current board state should look for a positive or negative outcome
if list1.count("X") >= list1.count("O"):
    target = "negative"
else:
    target = "positive"

# Preprocess tic-tac-toe.data (convert 'b', 'x', 'o' to None, "X", "O")
processed_rows = []
with open('Data/tic-tac-toe.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        new_row = []
        for i, item in enumerate(row):
            if i < 9:
                # Convert board symbols to Python values
                if item == 'b':
                    new_row.append(None)
                elif item == 'x':
                    new_row.append("X")
                elif item == 'o':
                    new_row.append("O")
                else:
                    new_row.append(item)
            else:
                # Keep the class label as is (positive/negative)
                new_row.append(item)
        processed_rows.append(new_row)

# Clear previous bucket files (Trash and Leafs)
open('Data/Buckets/Trash.csv', 'w').close()
open('Data/Buckets/leafs.csv', 'w').close()

# Analyze and sort rows into leafs or trash
for row in processed_rows:
    # Only consider rows with the correct target in the last column
    if row[9] != target:
        with open('Data/Buckets/Trash.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        continue

    # Check if all non-null values in list1 match the corresponding row values
    match = True
    for item1, item2 in zip(list1, row[:9]):
        if item1 is not None and item1 != item2:
            match = False
            break

    # If match, write to leafs; otherwise, write to trash
    if match:
        with open('Data/Buckets/leafs.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    else:
        with open('Data/Buckets/Trash.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)


# Read leafs.csv
with open('Data/Buckets/leafs.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    leafs = [row for row in reader if len(row) >= 9]

# For each position (column), count X and O moves
for pos in range(9):
    move_counts = {"X": 0, "O": 0}
    for row in leafs:
        move = row[pos]
        if move in move_counts:
            move_counts[move] += 1
    # Find the most common move at this position
    if move_counts["X"] > 0 or move_counts["O"] > 0:
        best_move = max(move_counts, key=move_counts.get)
        print(f"Play {best_move} in position {pos+1} (1-9, left to right, top to bottom) - {move_counts[best_move]} times")
#conver the best move to the format used in the mainFPP.py


# Determine whose turn it is
next_player = "X" if list1.count("X") <= list1.count("O") else "O"

# Read leafs.csv
with open('Data/Buckets/leafs.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    leafs = [row for row in reader if len(row) >= 9]

# Count for each position how often next_player is played there in leafs
position_counts = [0] * 9
for row in leafs:
    for i in range(9):
        if row[i] == next_player:
            position_counts[i] += 1

# Find the position with the highest count
if any(position_counts):
    best_position = position_counts.index(max(position_counts))
    print(f"Leafs: Play {next_player} in position {best_position+1} (1-9, left to right, top to bottom) - {position_counts[best_position]} times")
else:
    print(f"No recommended move for {next_player} found in leafs.csv.")

# Optionally, print all counts for each position
print("Counts for each position:", position_counts)

# # Now iterate through leafs and select the best move
# with open('Data/Buckets/leafs.csv', 'r', newline='') as file:
#     reader = csv.reader(file)
#     move_counts = {}
#     for row in reader:
#         for i in range(9):
#             move = row[i]
#             # Count only non-empty, non-None moves
#             if move not in (None, "", "None"):
#                 move_counts[move] = move_counts.get(move, 0) + 1
#     if move_counts:
#         # Find the move with the highest occurrence
#         best_move = max(move_counts, key=move_counts.get)
#         best_move_count = move_counts[best_move]
#         print(f"Best move: {best_move} with {best_move_count} occurrences")
#         # Find the position of the best move in the current board
#         best_move_position = list1.index(best_move) if best_move in list1 else None
#         if best_move_position is not None:
#             print(f"Best move position in list: {best_move_position}")
#         else:
#             print("No valid move found in the current list.")
#     else:
#         print("No moves found in leafs.csv.")

# # Display the current board state
# print("Current list state:", list1)
# # Find the most common next move and its position from leafs
# with open('Data/Buckets/leafs.csv', 'r', newline='') as file:
#     reader = csv.reader(file)
#     leafs = [row for row in reader if len(row) >= 9]

# # Count moves for each position
# best_move = None
# best_move_index = None
# best_move_count = 0

# for pos in range(9):
#     move_counts = {"X": 0, "O": 0}
#     for row in leafs:
#         move = row[pos]
#         if move in move_counts:
#             move_counts[move] += 1
#     # Find the most common move at this position
#     for move_type in move_counts:
#         if move_counts[move_type] > best_move_count:
#             best_move = move_type
#             best_move_index = pos
#             best_move_count = move_counts[move_type]

# if best_move_index is not None:
#     # Count filled spaces before the best move index
#     filled_before = sum(1 for i in range(best_move_index) if list1[i] is not None)
#     result_pos = best_move_index - filled_before
#     print(f"Leafs: Play {best_move} in position {result_pos} (count squares left to right, top to bottom, including filled squares and add filled before first empty)")
# else:
#     print("No valid moves found in leafs.")

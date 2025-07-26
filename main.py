# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with home() function.
def home() :
    
    return render_template('index.html')

null = None


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()  # retrieve the data sent from JavaScript
    board = data.get('board')  # board is a list from JS

    # Convert JS nulls to Python None
    board = [cell if cell in ["X", "O"] else None for cell in board]

    # Use your best move function (choose minimax or model)
    # AI plays as "O", human plays as "X"
    _, best_move = minimax(board, "O")  # AI is O

    # Return the best move index (0-8) as JSON
    return jsonify({'best_move': best_move})


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True)
    
#notes
# main purpose of flask is for forms



import joblib

# Load your trained random forest model
clf = joblib.load("tic_tac_toe_random_forest.joblib")

def board_to_features(board):
    # Convert board to model input: X=1, O=-1, None/empty=0
    mapping = {"X": 1, "O": -1, None: 0}
    return [mapping.get(cell, 0) for cell in board]

def best_move_model(board, player):
    # Finds the best move using the trained model
    best_score = None
    best_positions = []
    for i in range(9):  # Iterate over all board positions
        if board[i] is None:  # Only consider empty squares
            new_board = board.copy()
            new_board[i] = player  # Simulate playing at position i
            features = board_to_features(new_board)
            pred = clf.predict([features])[0]  # Predict outcome
            # For X, prefer positive; for O, prefer negative
            score = 1 if (player == "X" and pred == 1) or (player == "O" and pred == -1) else -1
            if best_score is None or score > best_score:
                best_score = score
                best_positions = [i]  # Start new best positions list
            elif score == best_score:
                best_positions.append(i)  # Add to best positions if tied
    return best_positions

# Example usage for model-based move
board = ["X", "O", None, None, None, "O", None, None, "X"]
positions = best_move_model(board, "X")
if positions:
    best_move_index = positions[0]
    # Count filled spaces before the best move index
    filled_before = sum(1 for i in range(best_move_index) if board[i] is not None)
    result_pos = best_move_index + 1 + filled_before  # 1-based index plus filled count
    print(f"Play X in position {result_pos} (count squares left to right, top to bottom, including filled squares and add filled before first empty)")
else:
    print("No valid moves found by model.")

def best_move_model(board, player):
    moves = []
    boards = []
    for i in range(9):
        if board[i] is None:
            new_board = board.copy()
            new_board[i] = player
            boards.append(board_to_features(new_board))
            moves.append(i)
    if not boards:
        return []
    preds = clf.predict(boards)
    scores = [1 if (player == "X" and p == 1) or (player == "O" and p == -1) else -1 for p in preds]
    max_score = max(scores)
    return [moves[i] for i, s in enumerate(scores) if s == max_score]



def minimax(board, player):
    # Finds the best move using the minimax algorithm
    opponent = "O" if player == "X" else "X"

    # Check for terminal state (win/loss/draw)
    winner = check_winner(board)
    if winner == player:
        return 1, None  # Win
    elif winner == opponent:
        return -1, None  # Loss
    elif all(cell is not None for cell in board):
        return 0, None  # Draw

    # Try all possible moves
    best_score = None
    best_move = None
    for i in range(9):
        if board[i] is None:  # Only consider empty squares
            board[i] = player  # Simulate playing at position i
            score, _ = minimax(board, opponent)  # Recursively evaluate opponent's response
            board[i] = None  # Undo move
            score = -score  # Minimax: maximize your score, minimize opponent's
            if best_score is None or score > best_score:
                best_score = score
                best_move = i
    return best_score, best_move

def check_winner(board):
    # Checks if there is a winner on the board
    lines = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # columns
        [0,4,8],[2,4,6]           # diagonals
    ]
    for line in lines:
        a, b, c = line
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return board[a]  # Return "X" or "O" if there's a winner
    return None  # No winner

# Example usage for minimax move
board = ["X", "O", None, None, None, "O", None, None, "X"]
score, move = minimax(board, "X")
print(f"Minimax best move for X is at position: {move+1 if move is not None else 'None'} (1-9)")


def minimax(board, player, alpha=float('-inf'), beta=float('inf')):
    """
    Minimax algorithm with alpha-beta pruning for tic-tac-toe.
    - board: current board state (list of 9 elements)
    - player: "X" or "O" (whose turn)
    - alpha: best score that the maximizer can guarantee so far
    - beta: best score that the minimizer can guarantee so far
    Returns: (score, move_index)
    """
    opponent = "O" if player == "X" else "X"

    # Check for terminal state (win/loss/draw)
    winner = check_winner(board)
    if winner == player:
        return 1, None  # Win for current player
    elif winner == opponent:
        return -1, None  # Loss for current player
    elif all(cell is not None for cell in board):
        return 0, None  # Draw

    best_score = None
    best_move = None

    # Iterate through all possible moves
    for i in range(9):
        if board[i] is None:  # Only consider empty squares
            board[i] = player  # Simulate move
            score, _ = minimax(board, opponent, alpha, beta)  # Recursively evaluate
            board[i] = None  # Undo move
            score = -score  # Flip score for minimax (opponent's best is your worst)

            # Update best score and move
            if best_score is None or score > best_score:
                best_score = score
                best_move = i

            # Alpha-beta pruning logic:
            alpha = max(alpha, best_score)  # Maximizer updates alpha
            if alpha >= beta:
                break  # Prune: no need to check further moves

    return best_score, best_move
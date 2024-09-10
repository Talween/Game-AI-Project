# Main Authors: Talween, Sagar, Gaganjot
# Main Reviewer:  Talween, Sagar, Gaganjot

def copy_board(board):
    # Create a deep copy of the current board state to avoid mutating the original board
    current_board = []   
    height = len(board)  # Get the number of rows in the board
    for i in range(height):
        # Append a copy of each row to the new board
        current_board.append(board[i].copy())
    return current_board

def evaluate_board(board, player):
    # Evaluate the board and return a score based on the number and position of pieces
    score = 0  # Initialize score to 0
    for row in board:
        for cell in row:
            if cell == 4 * player:
                # If there are 4 consecutive pieces of the player, it's a winning board
                score += 100 * player  # Assign a high score for a winning position
            elif cell == player:
                # Increment score for each piece the player has on the board
                score += 1
            elif cell == -player:
                # Decrease score for each piece the opponent has on the board
                score -= 1
    return score  # Return the final calculated score

class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height=4):
            # Initialize the node with a copy of the board, depth, and the current player
            self.board = copy_board(board)
            self.depth = depth  # Current depth of the node in the game tree
            self.player = player  # Player to move at this node
            self.children = []  # List to hold child nodes (possible moves from this position)
            
            # If the current depth is less than the maximum tree height, generate children nodes
            if depth < tree_height:
                self.generate_children(tree_height)

        def generate_children(self, tree_height):
            # Generate all possible board states (children) from the current node
            height = len(self.board)  # Get the number of rows in the board
            width = len(self.board[0])  # Get the number of columns in the board
            for row in range(height):
                for col in range(width):
                    # Check if the current cell is empty (i.e., a valid move)
                    if self.board[row][col] == 0:
                        new_board = copy_board(self.board)  # Copy the current board state
                        new_board[row][col] = self.player  # Place the player's piece in the empty cell
                        # Create a new child node with the updated board, increased depth, and the opponent's turn
                        self.children.append(GameTree.Node(new_board, self.depth + 1, -self.player, tree_height))

    def __init__(self, board, player, tree_height=4):
        # Initialize the game tree with the root node, representing the current state of the game
        self.player = player  # The player whose move is being simulated by the tree
        self.root = self.Node(board, 0, player, tree_height)  # The root node represents the current board state

    def minimax(self, node, maximizing_player):
        # Minimax algorithm to evaluate the best move from the current node
        # Base case: if there are no children (no further moves possible) or the maximum depth is reached
        if len(node.children) == 0 or node.depth == 3:
            return evaluate_board(node.board, self.player)  # Evaluate and return the score of the board

        if maximizing_player:
            # If the current player is maximizing (trying to get the highest score)
            max_eval = float('-inf')  # Start with the lowest possible value
            for child in node.children:
                # Recursively evaluate each child node with the minimizing player
                eval = self.minimax(child, False)
                max_eval = max(max_eval, eval)  # Choose the maximum value from the evaluations
            return max_eval
        else:
            # If the current player is minimizing (trying to get the lowest score)
            min_eval = float('inf')  # Start with the highest possible value
            for child in node.children:
                # Recursively evaluate each child node with the maximizing player
                eval = self.minimax(child, True)
                min_eval = min(min_eval, eval)  # Choose the minimum value from the evaluations
            return min_eval

    def get_move(self):
        # Determine the best move by evaluating all possible moves from the root node
        best_move = None  # Initialize the best move as None
        best_score = float('-inf')  # Start with the lowest possible value for the best score

        for child in self.root.children:
            # Evaluate each child node (possible move) using the minimax algorithm
            score = self.minimax(child, False)  # Evaluate the move assuming the opponent will minimize the score
            if score > best_score:
                # If the score for this move is better than the current best score, update the best move
                best_score = score
                max_row_index = 0
                max_col_index = 0
                max_val = float('-inf')
                for i in range(len(child.board)):
                    for j in range(len(child.board[0])):
                        # Identify the location of the move on the board by finding the highest value piece
                        if child.board[i][j] * self.player > max_val:
                            max_val = child.board[i][j] * self.player
                            max_row_index = i  # Row index of the move
                            max_col_index = j  # Column index of the move
                best_move = (max_row_index, max_col_index)  # Store the best move coordinates

        return best_move  # Return the coordinates of the best move

    def clear_tree(self):
        # Clear the game tree to free up memory after a move has been decided
        self.root = None  # Set the root node to None, effectively clearing the tree

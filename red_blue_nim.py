import sys

# Constants
RED = "red"
BLUE = "blue"

# Function to check if a pile is empty
def is_empty(piles):
    return piles[RED] == 0 or piles[BLUE] == 0

# Function to calculate score
def calculate_score(piles, version):
    if version == "standard":
        return 2 * piles[RED] + 3 * piles[BLUE]
    elif version == "misere":
        return 2 * piles[RED] + 3 * piles[BLUE] if is_empty(piles) else 0

# Function to print current state
def print_state(piles):
    print("Red Pile:", piles[RED])
    print("Blue Pile:", piles[BLUE])

# Function to prompt human player for move
def get_human_move(piles):
    print_state(piles)
    print("Your Turn:")
    while True:
        pile = input("Choose a pile (red/blue): ").lower()
        if pile not in [RED, BLUE]:
            print("Invalid pile. Please choose red or blue.")
            continue
        num_marbles = input("Choose 1 or 2 marbles to remove: ")
        if num_marbles not in ["1", "2"]:
            print("Invalid number of marbles. Please choose 1 or 2.")
            continue
        num_marbles = int(num_marbles)
        if num_marbles > piles[pile] or num_marbles < 1:
            print("Invalid number of marbles. Please choose a valid number.")
            continue
        return pile, num_marbles

# Function to perform computer move using Minimax with Alpha-Beta Pruning
def get_computer_move(piles, version, depth=None):
    # Helper function to evaluate the score of a node
    def evaluate_node(piles, depth, is_maximizing_player, alpha, beta):
        if is_empty(piles) or depth == 0:
            return calculate_score(piles, version)
        
        if is_maximizing_player:
            best_val = float('-inf')
            best_move = None
            for pile, num_marbles in [("red", 2), ("blue", 2), ("red", 1), ("blue", 1)]:
                if piles[pile] >= num_marbles:
                    new_piles = piles.copy()
                    new_piles[pile] -= num_marbles
                    val = evaluate_node(new_piles, depth - 1, False, alpha, beta)
                    if val > best_val:
                        best_val = val
                        best_move = (pile, num_marbles)
                    alpha = max(alpha, best_val)
                    if beta <= alpha:
                        break
            return best_val, best_move
        else:
            best_val = float('inf')
            best_move = None
            for pile, num_marbles in [("blue", 1), ("red", 1), ("blue", 2), ("red", 2)]:
                if piles[pile] >= num_marbles:
                    new_piles = piles.copy()
                    new_piles[pile] -= num_marbles
                    val = evaluate_node(new_piles, depth - 1, True, alpha, beta)
                    if val < best_val:
                        best_val = val
                        best_move = (pile, num_marbles)
                    beta = min(beta, best_val)
                    if beta <= alpha:
                        break
            return best_val, best_move
    
    # Main function body
    best_move = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    if depth is None:
        depth = float('inf')  # Set depth to infinity if not provided
    for pile, num_marbles in [("red", 2), ("blue", 2), ("red", 1), ("blue", 1)]:
        if piles[pile] >= num_marbles:
            new_piles = piles.copy()
            new_piles[pile] -= num_marbles
            score, move = evaluate_node(new_piles, depth, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move

# Function to play a full game
def play_game(num_red, num_blue, version="standard", first_player="computer", depth=None):
    piles = {RED: num_red, BLUE: num_blue}
    current_player = first_player
    
    # Display initial state
    print("Initial State:")
    print_state(piles)

    while not is_empty(piles):
        if version == "misere" and is_empty(piles):
            winner = "computer" if current_player == "human" else "human"
            score = calculate_score(piles, version)
            print("Game Over!")
            print("Winner:", winner)
            print("Score:", score)
            return

        if current_player == "human":
            pile, num_marbles = get_human_move(piles)
        else:
            pile, num_marbles = get_computer_move(piles, version, depth)
            print("Computer chose to remove", num_marbles, "marbles from", pile, "pile.")

        piles[pile] -= num_marbles
        if is_empty(piles):
            break
        
        # Check for empty piles in standard version
        if version == "standard" and is_empty(piles):
            winner = "computer" if current_player == "human" else "human"
            score = calculate_score(piles, version)
            print("Game Over!")
            print("Winner:", winner)
            print("Score:", score)
            return

        current_player = "human" if current_player == "computer" else "computer"

    if version == "standard":
        winner = "computer" if current_player == "human" else "human"
    elif version == "misere":
        winner = "human" if current_player == "human" else "computer"

    score = calculate_score(piles, version)
    print("Game Over!")
    print("Winner:", winner)
    print("Score:", score)

if __name__ == "__main__":
    # Parse command line arguments
    args = sys.argv[1:]
    num_red = int(args[0])
    num_blue = int(args[1])
    version = args[2] if len(args) > 2 else "standard"
    first_player = args[3] if len(args) > 3 else "computer"
    depth = int(args[4]) if len(args) > 4 else None

    # Play the game
    play_game(num_red, num_blue, version, first_player, depth)



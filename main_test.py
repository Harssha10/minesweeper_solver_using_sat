from get_clauses import get_clauses
from sat_solver import custom_sat
from show_board import show_board
from automation import debug_board


# Get initial state
main_map, exposed_cells = debug_board()
clauses = get_clauses(main_map)
results = custom_sat(clauses)

# Create GUI live board instance
board = show_board(results, exposed_cells)


def update_loop():
    # Fetch updated state from Selenium
    new_map, new_exposed = debug_board()

    # Only update if changed
    if new_exposed != exposed_cells:
        print("🔄 Board changed — updating inference...")
        clauses = get_clauses(new_map)
        new_results = custom_sat(clauses)
        board.update(new_results, new_exposed)
        
    # schedule next check
    board.root.after(1000, update_loop)   # every 1 second


# Start loop
board.root.after(1000, update_loop)
board.root.mainloop()

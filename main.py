from get_clauses import get_clauses
from sat_solver import custom_sat
from show_board import show_board
from automation import debug_board

Main_map,exposed_cells=debug_board()
clauses=get_clauses(Main_map)
results={}
for i in clauses:
    temp=custom_sat(clauses)
    results.update(temp)
show_board(results,exposed_cells)
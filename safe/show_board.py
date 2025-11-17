import tkinter as tk

CELL_SIZE = 40

number_colors = {
    0: "gray",
    1: "blue",
    2: "green",
    3: "red",
    4: "darkblue",
    5: "brown",
    6: "cyan",
    7: "black",
    8: "gray"
}


def get_cell_display(cell, solver_results, exposed):
    # CASE 1: Player flagged (-2 inside exposed)
    if cell in exposed and exposed[cell] == -2:
        return "🚩", "#ffe680", "red"   # yellow background flagged
    # CASE 2: Player revealed → show number
    if cell in exposed and exposed[cell] >= 0:
        val = exposed[cell]
        return str(val), "#ffffff", number_colors[val]
    # CASE 3: Solver deduction (only if not revealed)
    state = solver_results.get(cell, None)
    if state == 1:
        return "💣", "#ff5c5c", "black"     # forced mine
    elif state == 0:
        return "✔", "#b3ffb3", "green"     # forced safe
    else:
        return "?", "#dddddd", "black"     # unknown cell


def show_board(solver_results, exposed):

    root = tk.Tk()
    root.title("SAT + Gameplay Minesweeper Board")

    max_r = max(r for r,_ in solver_results)
    max_c = max(c for _,c in solver_results)

    for r in range(max_r + 1):
        for c in range(max_c + 1):

            text, bg, fg = get_cell_display((r,c), solver_results, exposed)

            label = tk.Label(
                root,
                text=text,
                width=2,
                height=1,
                font=("Arial", 16, "bold"),
                borderwidth=2,
                relief="ridge",
                bg=bg,
                fg=fg
            )
            label.grid(row=r, column=c, padx=1, pady=1)

    root.mainloop()

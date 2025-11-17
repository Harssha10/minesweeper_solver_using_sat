import tkinter as tk
import random
CELL_SIZE = 32

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
def show_board(solver_results, exposed):
    root = tk.Tk()
    root.title("SAT-Assisted Minesweeper")
    max_r = 8
    max_c = 8
    board_frame = tk.Frame(root)
    board_frame.grid(row=0, column=0, padx=10, pady=10)
    widgets = {}
    solver_revealed = {}   # {cell: "safe" / "mine"}
    def display_cell(cell):
        # 1) Game-exposed cells (numbers & flags)
        if cell in exposed:
            v = exposed[cell]
            if v == -2:
                return "🚩", "#ffdb70", "black"
            return str(v), "#ffffff", number_colors.get(v, "black")

        # 2) Cells revealed by SAT buttons
        if cell in solver_revealed:
            kind = solver_revealed[cell]
            if kind == "mine":
                return "💣", "#ff6b6b", "black"
            elif kind == "safe":
                return "✔", "#b7ffb7", "green"

        # 3) Everything else: still hidden
        return "", "#c0c0c0", "black"

    def refresh():
        for (r, c), label in widgets.items():
            text, bg, fg = display_cell((r, c))
            label.config(text=text, bg=bg, fg=fg)

    def reveal_random_safe():
        # cells SAT knows safe (0) and not yet shown anywhere
        candidates = [
            cell for cell, val in solver_results.items()
            if val == 0 and cell not in exposed and cell not in solver_revealed
        ]
        if candidates:
            cell = random.choice(candidates)
            solver_revealed[cell] = "safe"
            refresh()

    def reveal_random_mine():
        # cells SAT knows mine (1) and not yet shown anywhere
        candidates = [
            cell for cell, val in solver_results.items()
            if val == 1 and cell not in exposed and cell not in solver_revealed
        ]
        if candidates:
            cell = random.choice(candidates)
            solver_revealed[cell] = "mine"
            refresh()

    def reveal_all():
        # show every SAT-known cell, but don't override exposed numbers/flags
        for cell, val in solver_results.items():
            if cell in exposed:
                continue
            if val == 0:
                solver_revealed[cell] = "safe"
            elif val == 1:
                solver_revealed[cell] = "mine"
        refresh()

    # ---- build board UI ----
    for r in range(max_r + 1):
        for c in range(max_c + 1):
            text, bg, fg = display_cell((r, c))
            lbl = tk.Label(
                board_frame,
                text=text,
                width=2,
                height=1,
                font=("Arial", 14, "bold"),
                relief="ridge",
                borderwidth=1,
                bg=bg,
                fg=fg,
            )
            lbl.grid(row=r, column=c, padx=1, pady=1)
            widgets[(r, c)] = lbl
    # ---- buttons (smaller, tighter) ----
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=1, column=0, pady=5)
    tk.Button(btn_frame, text="Reveal Safe", width=12,
              command=reveal_random_safe).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Reveal Mine", width=12,
              command=reveal_random_mine).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Reveal All", width=12,
              command=reveal_all).grid(row=0, column=2, padx=5)
    root.mainloop()

import customtkinter as ctk
from backtracking import BacktrackingSolver
from genetics import GeneticSolver

ctk.set_appearance_mode("dark")

class SolverController:
    def __init__(self, app, canvas, n, algorithm):
        self.app = app
        self.canvas = canvas
        self.n = n
        self.algorithm = algorithm
        self.solve_and_draw()

    def draw_board(self, board, n, is_genetic=False):
        self.canvas.delete("all")
        size = 50
        for i in range(n):
            for j in range(n):
                x1, y1 = j * size, i * size
                x2, y2 = x1 + size, y1 + size
                fill = "#444" if (i + j) % 2 == 0 else "#222"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#666")
                if is_genetic:
                    if board[i] == j:
                        self.canvas.create_text(x1 + 25, y1 + 25, text="♛", font=("Arial", 24), fill="#ff69b4")
                else:
                    if board[i][j] == 1:
                        self.canvas.create_text(x1 + 25, y1 + 25, text="♛", font=("Arial", 24), fill="#ff69b4")

    def show_message(self, title, message):
        popup = ctk.CTkToplevel(self.app)
        popup.title(title)
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14), wraplength=250)
        label.pack(pady=20)
        button = ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color="#ff69b4", hover_color="#ff85c1")
        button.pack(pady=10)
        popup.transient(self.app)
        popup.grab_set()

    def solve_and_draw(self):
        if self.algorithm == "Backtracking":
            solver = BacktrackingSolver(self.n)
            if solver.solve():
                board = solver.get_board()
                self.canvas.configure(width=self.n * 50, height=self.n * 50)
                self.draw_board(board, self.n, is_genetic=False)
            else:
                self.show_message("Result", "No solution found!")
        else:
            solver = GeneticSolver(self.n)
            result = solver.solve()
            if result:
                self.canvas.configure(width=self.n * 50, height=self.n * 50)
                self.draw_board(result, self.n, is_genetic=True)
            else:
                self.show_message("Result", f"No solution found after {solver.RETRY_LIMIT} attempts.")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("N-Queens Solver")
        self.geometry("450x650")

        self.entry_label = ctk.CTkLabel(self, text="")
        self.entry_label.pack(pady=(20, 0))

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter n")
        self.entry.pack(pady=5)

        self.algo_var = ctk.StringVar(value="Backtracking")

        self.radio1 = ctk.CTkRadioButton(self, text="Backtracking Algorithm", variable=self.algo_var, value="Backtracking")
        self.radio1.pack(pady=5)
        self.radio2 = ctk.CTkRadioButton(self, text="Genetic Algorithm", variable=self.algo_var, value="Genetic")
        self.radio2.pack(pady=5)

        self.solve_btn = ctk.CTkButton(self, text="Solve!", command=self.start, fg_color="#ff69b4", hover_color="#ff85c1")
        self.solve_btn.pack(pady=20)

        self.canvas = ctk.CTkCanvas(self, width=400, height=400, bg="#111")
        self.canvas.pack(pady=10)

    def show_message(self, title, message):
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("300x150")
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 14), wraplength=250)
        label.pack(pady=20)
        button = ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color="#ff69b4", hover_color="#ff85c1")
        button.pack(pady=10)
        popup.transient(self)
        popup.grab_set()

    def start(self):
        val = self.entry.get()
        try:
            n = int(val)
            if n < 4:
                self.show_message("Error", "Number must be at least 4.")
                return
        except ValueError:
            self.show_message("Error", "Please enter a valid number.")
            return

        algorithm = self.algo_var.get()
        SolverController(self, self.canvas, n, algorithm)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

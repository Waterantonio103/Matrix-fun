from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static, Button
from textual.containers import Grid, Horizontal, Center
from inverse_laplace import determinant, cofactor, adjugate, inverse, estimate_calc_time
from gauss_jordan import reduc_identity
import inverse_gauss
from time import perf_counter
from random import randint

ROWS = COLUMNS = int(input("Matrix Size : "))
METHOD = input("Method (laplace/gauss/gauss-jordan): ").strip().lower()

while METHOD not in ("laplace", "gauss", "gauss-jordan"):
    METHOD = input("Choose 'laplace', 'gauss', or 'gauss-jordan': ").strip().lower()

METHOD_KEY = METHOD.replace("-", "_")
METHOD_LABEL = "Gauss-Jordan" if METHOD == "gauss-jordan" else METHOD.capitalize()
LAPLACE_BASE_SIZE = 10
LAPLACE_BASE_SECONDS = 17
GAUSS_BASE_SIZE = 10
GAUSS_BASE_SECONDS = 0.002
TERMINAL_ONLY_SIZE = 50
MATRIX_PREVIEW_SIZE = 6

CELL_WIDTH = 10
CELL_HEIGHT = 3
GRID_GUTTER = 1

GRID_WIDTH = COLUMNS * CELL_WIDTH + (COLUMNS - 1) * GRID_GUTTER
GRID_HEIGHT = ROWS * CELL_HEIGHT + (ROWS - 1) * GRID_GUTTER

if ROWS > TERMINAL_ONLY_SIZE and METHOD == "laplace":
    print("Laplace is too slow for matrices larger than 50x50. Switching to gauss.")
    METHOD = "gauss"
    METHOD_KEY = METHOD.replace("-", "_")
    METHOD_LABEL = METHOD.capitalize()

def format_seconds(seconds):
    if seconds < 60:
        return f"{seconds:.2f}s"
    if seconds < 3600:
        return f"{seconds / 60:.2f}m"
    if seconds < 86400:
        return f"{seconds / 3600:.2f}h"
    return f"{seconds / 86400:.2f}d"

def estimate_gauss_calc_time(base_size, base_seconds, target_size):
    return base_seconds * (target_size / base_size) ** 5

def input_int(prompt, default=None):
    while True:
        raw_value = input(prompt).strip()
        if not raw_value and default is not None:
            return default
        try:
            return int(raw_value)
        except ValueError:
            print("Enter an integer.")

def matrix_preview(matrix=None, size=None, limit=MATRIX_PREVIEW_SIZE):
    if matrix is None:
        row_count = size
        column_count = size
    else:
        row_count = len(matrix)
        column_count = len(matrix[0]) if matrix else 0

    shown_rows = min(row_count, limit)
    shown_columns = min(column_count, limit)
    lines = ["["]

    for row_index in range(shown_rows):
        if matrix is None:
            values = ["None"] * shown_columns
        else:
            values = [repr(matrix[row_index][column_index]) for column_index in range(shown_columns)]

        if column_count > shown_columns:
            values.append("...")
        lines.append(f"  [{', '.join(values)}],")

    if row_count > shown_rows:
        lines.append("  ...")

    lines.append("]")
    return "\n".join(lines)

def build_terminal_matrix():
    print(f"\nTerminal-only mode for {ROWS}x{COLUMNS}.")
    print("Matrix template:")
    print(matrix_preview(size=ROWS))

    mode = input("\nEnter 'r' to randomize or 'm' to enter values manually: ").strip().lower()
    while mode not in ("r", "random", "m", "manual"):
        mode = input("Choose 'r' for randomize or 'm' for manual: ").strip().lower()

    if mode in ("r", "random"):
        random_min = input_int("Random minimum [-1000]: ", -1000)
        random_max = input_int("Random maximum [1000]: ", 1000)
        if random_min > random_max:
            random_min, random_max = random_max, random_min
        return [
            [randint(random_min, random_max) for _ in range(COLUMNS)]
            for _ in range(ROWS)
        ]

    matrix = []
    for row_index in range(ROWS):
        row = []
        for column_index in range(COLUMNS):
            row.append(input_int(f"matrix[{row_index}][{column_index}]: "))
        matrix.append(row)
    return matrix

def build_terminal_estimate_text():
    if METHOD == "laplace":
        seconds = estimate_calc_time(
            LAPLACE_BASE_SIZE,
            LAPLACE_BASE_SECONDS,
            ROWS,
        )
    else:
        seconds = estimate_gauss_calc_time(
            GAUSS_BASE_SIZE,
            GAUSS_BASE_SECONDS,
            ROWS,
        )
    return f"Estimated {METHOD_LABEL} time for {ROWS}x{COLUMNS}: {format_seconds(seconds)}"

def gauss_jordan_inverse(matrix):
    matrix_copy = [row[:] for row in matrix]
    start = perf_counter()
    inv = reduc_identity(matrix_copy)
    total_time = perf_counter() - start
    return inv, total_time

def run_terminal_mode():
    matrix = build_terminal_matrix()
    print("\nMatrix:")
    print(matrix_preview(matrix))
    print(build_terminal_estimate_text())

    if METHOD == "gauss-jordan":
        gj_inv, gj_total_time = gauss_jordan_inverse(matrix)

        print("\nInverse (Gauss-Jordan):")
        if gj_inv is None:
            print("No inverse exists (determinant is 0)")
        else:
            print(matrix_preview(gj_inv))
        print(f"Total Time (Gauss-Jordan): {gj_total_time:.6f}s")
        return

    if METHOD == "gauss":
        start = perf_counter()
        det = inverse_gauss.determinant(matrix)
        det_time = perf_counter() - start

        start = perf_counter()
        cof = inverse_gauss.cofactor(matrix)
        cof_time = perf_counter() - start

        start = perf_counter()
        adj = inverse_gauss.adjugate(matrix, cof)
        adj_time = perf_counter() - start

        start = perf_counter()
        inv = inverse_gauss.inverse(matrix, det, adj)
        inv_time = perf_counter() - start

        total_time = det_time + cof_time + adj_time + inv_time

        print(f"\nDeterminant (Gauss): {det}")
        print("Cofactor (Gauss):")
        print(matrix_preview(cof))
        print("Adjugate (Gauss):")
        print(matrix_preview(adj))
        print("Inverse (Gauss):")
        if isinstance(inv, str):
            print(inv)
        else:
            print(matrix_preview(inv))
        print(f"Total Time (Gauss): {total_time:.6f}s")
        return

    start = perf_counter()
    det = determinant(matrix)
    det_time = perf_counter() - start

    start = perf_counter()
    cof = cofactor(matrix)
    cof_time = perf_counter() - start

    start = perf_counter()
    adj = adjugate(matrix, cof)
    adj_time = perf_counter() - start

    start = perf_counter()
    inv = inverse(matrix, det, adj)
    inv_time = perf_counter() - start

    total_time = det_time + cof_time + adj_time + inv_time

    print(f"\nDeterminant (Laplace): {det}")
    print("Cofactor (Laplace):")
    print(matrix_preview(cof))
    print("Adjugate (Laplace):")
    print(matrix_preview(adj))
    print("Inverse (Laplace):")
    if isinstance(inv, str):
        print(inv)
    else:
        print(matrix_preview(inv))
    print(f"Total Time (Laplace): {total_time:.6f}s")

class Mat(App):
    
    CSS = f"""

    Screen {{
        align: center middle;
    }}

    #matrix_rows {{
        width: auto;
        height: auto;
    }}

    #matrix_grid {{
        align: center middle;
        grid-size: {COLUMNS};
        grid-gutter: {GRID_GUTTER};
        width: {GRID_WIDTH};
        height: {GRID_HEIGHT};
    }}

    Input {{
        height: {CELL_HEIGHT};
        width: {CELL_WIDTH};
    }}

    #left_brace,
    #right_brace {{
        width: 1;
        height: {GRID_HEIGHT};
    }}

    #left_brace,
    #right_brace {{
        content-align: center middle;
    }}

    #btn_container{{
        padding: 2;
    }}

    #button_row {{
        width: auto;
        height: auto;
    }}

    #submit_btn,
    #randomize_btn {{
        width: auto;
        margin: 0 1;
    }}

    #results_container {{
        align: center middle;
    }}

    .result_box {{
        width: 70%;
        height: auto;
        min-height: 3;
        margin: 1 0 0 0;
        padding: 1 2;
        border: round $primary;
        content-align: center middle;
        display: none;
    }}

    .time_box {{
        width: 70%;
        height: auto;
        margin: 0 0 1 0;
        padding: 0 2;
        color: blue;
        text-style: bold;
        content-align: center middle;
        display: none;
    }}
    """

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]

            # ----APP RENDER----

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Horizontal(id="matrix_rows"):
                yield Static(self.make_brace(), id="left_brace")
                with Grid(id="matrix_grid"):
                    for i in range(ROWS * COLUMNS):
                        yield Input(
                            type="text",
                            placeholder="",
                            id=f"cell_{i}",
                        )
                yield Static(self.make_brace(), id="right_brace")
        with Center(id="btn_container"):
            with Horizontal(id="button_row"):
                yield Button(
                    id="submit_btn",
                    label="submit matrix",
                )
                yield Button(
                    id="randomize_btn",
                    label="randomize",
                )
        with Center(id="results_container"):
            yield Static("", id="current_matrix", classes="result_box")
            yield Static("", id="determinant_laplace", classes="result_box")
            yield Static("", id="determinant_laplace_time", classes="time_box")
            yield Static("", id="determinant_gauss", classes="result_box")
            yield Static("", id="determinant_gauss_time", classes="time_box")
            yield Static("", id="cofactor_laplace", classes="result_box")
            yield Static("", id="cofactor_laplace_time", classes="time_box")
            yield Static("", id="cofactor_gauss", classes="result_box")
            yield Static("", id="cofactor_gauss_time", classes="time_box")
            yield Static("", id="adjugate_laplace", classes="result_box")
            yield Static("", id="adjugate_laplace_time", classes="time_box")
            yield Static("", id="adjugate_gauss", classes="result_box")
            yield Static("", id="adjugate_gauss_time", classes="time_box")
            yield Static("", id="inverse_laplace", classes="result_box")
            yield Static("", id="inverse_laplace_time", classes="time_box")
            yield Static("", id="inverse_gauss", classes="result_box")
            yield Static("", id="inverse_gauss_time", classes="time_box")
            yield Static("", id="inverse_gauss_jordan", classes="result_box")
            yield Static("", id="total_gauss_jordan_time", classes="time_box")
            yield Static("", id="total_laplace_time", classes="time_box")
            yield Static("", id="total_gauss_time", classes="time_box")
            yield Static("", id="estimate_time", classes="time_box")
        yield Footer()

            #----Per-Cell SUBMIT----

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in ("row_count", "column_count"):
            return
        cell_index = int(event.input.id.split("_")[1])
        self.notify(f"cell_{cell_index:02} submitted with: {event.input.value}")
        self.submit_matrix()

            #----SUBMIT MATRIX----

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            self.submit_matrix()
        
        if event.button.id == "randomize_btn":
            for i in range (ROWS * COLUMNS):
                self.query_one(f"#cell_{i}", Input).value = str(randint(-1000,1000))
       
            #----BUILD MATRIX----

    def submit_matrix(self) -> None:
        unformatted_matrix = []
        k = 0
        while k < ROWS * COLUMNS:
            cell_number = self.query_one(f"#cell_{k}", Input).value
            if not cell_number.strip():
                unformatted_matrix.append(int(0))
            else:
                unformatted_matrix.append(int(cell_number))
            k += 1
        
        #----GET ANSWERS----

        matrix = self.matrix_format(unformatted_matrix)

        if METHOD == "gauss-jordan":
            gj_inv, gj_total_time = gauss_jordan_inverse(matrix)
            estimate_times = self.build_estimate_text()

            current_matrix = self.query_one("#current_matrix", Static)
            inverse_result = self.query_one("#inverse_gauss_jordan", Static)
            total_time_result = self.query_one("#total_gauss_jordan_time", Static)
            estimate_time_result = self.query_one("#estimate_time", Static)

            current_matrix.display = True
            inverse_result.display = True
            total_time_result.display = True
            estimate_time_result.display = True

            current_matrix.update(f"Current matrix: {matrix}")
            if gj_inv is None:
                inverse_text = "No inverse exists (determinant is 0)"
            else:
                inverse_text = gj_inv
            inverse_result.update(f"Inverse ({METHOD_LABEL}): {inverse_text}")
            total_time_result.update(f"Total Time ({METHOD_LABEL}): {gj_total_time:.6f}s")
            estimate_time_result.update(estimate_times)
            return

        if METHOD == "laplace":
            det_func = determinant
            cof_func = cofactor
            adj_func = adjugate
            inv_func = inverse
        else:
            det_func = inverse_gauss.determinant
            cof_func = inverse_gauss.cofactor
            adj_func = inverse_gauss.adjugate
            inv_func = inverse_gauss.inverse

        start = perf_counter()
        det = det_func(matrix)
        det_time = perf_counter() - start

        start = perf_counter()
        cof = cof_func(matrix)
        cof_time = perf_counter() - start

        start = perf_counter()
        adj = adj_func(matrix, cof)
        adj_time = perf_counter() - start

        start = perf_counter()
        inv = inv_func(matrix, det, adj)
        inv_time = perf_counter() - start

        total_time = det_time + cof_time + adj_time + inv_time
        estimate_times = self.build_estimate_text()

        #----BUILD ANSWERS POST-SUBMIT----

        current_matrix = self.query_one("#current_matrix", Static)

        determinant_result = self.query_one(f"#determinant_{METHOD_KEY}", Static)
        determinant_time_result = self.query_one(f"#determinant_{METHOD_KEY}_time", Static)

        cofactor_result = self.query_one(f"#cofactor_{METHOD_KEY}", Static)
        cofactor_time_result = self.query_one(f"#cofactor_{METHOD_KEY}_time", Static)

        adjugate_result = self.query_one(f"#adjugate_{METHOD_KEY}", Static)
        adjugate_time_result = self.query_one(f"#adjugate_{METHOD_KEY}_time", Static)

        inverse_result = self.query_one(f"#inverse_{METHOD_KEY}", Static)
        inverse_time_result = self.query_one(f"#inverse_{METHOD_KEY}_time", Static)

        total_time_result = self.query_one(f"#total_{METHOD_KEY}_time", Static)
        estimate_time_result = self.query_one("#estimate_time", Static)

        current_matrix.display = True
        determinant_result.display = True
        determinant_time_result.display = True
        cofactor_result.display = True
        cofactor_time_result.display = True
        adjugate_result.display = True
        adjugate_time_result.display = True
        inverse_result.display = True
        inverse_time_result.display = True
        total_time_result.display = True
        estimate_time_result.display = True

        current_matrix.update(f"Current matrix: {matrix}")

        determinant_result.update(f"Determinant ({METHOD_LABEL}): {det}")
        determinant_time_result.update(f"Time: {det_time:.6f}s")

        cofactor_result.update(f"Cofactor ({METHOD_LABEL}): {cof}")
        cofactor_time_result.update(f"Time: {cof_time:.6f}s")

        adjugate_result.update(f"Adjugate ({METHOD_LABEL}): {adj}")
        adjugate_time_result.update(f"Time: {adj_time:.6f}s")

        inverse_result.update(f"Inverse ({METHOD_LABEL}): {inv}")
        inverse_time_result.update(f"Time: {inv_time:.6f}s")

        total_time_result.update(f"Total Time ({METHOD_LABEL}): {total_time:.6f}s")
        
        estimate_time_result.update(estimate_times)

    def make_brace(self) -> str:
        return "\n".join("|" for _ in range(GRID_HEIGHT))
    
            #----MATRIX FORMATTER----

    def matrix_format(self, unformatted_matrix):

        matrix = []
        
        for row_index in range(ROWS):
            row = []
            for column_index in range(COLUMNS):
                index = row_index * COLUMNS + column_index
                row.append(unformatted_matrix[index])
            
            matrix.append(row)
        
        return matrix

    def build_estimate_text(self):
        if METHOD == "laplace":
            seconds = estimate_calc_time(
                LAPLACE_BASE_SIZE,
                LAPLACE_BASE_SECONDS,
                ROWS,
            )
        else:
            seconds = estimate_gauss_calc_time(
                GAUSS_BASE_SIZE,
                GAUSS_BASE_SECONDS,
                ROWS,
            )
        return f"Estimated {METHOD_LABEL} time for {ROWS}x{COLUMNS}: {self.format_seconds(seconds)}"

    def format_seconds(self, seconds):
        if seconds < 60:
            return f"{seconds:.2f}s"
        if seconds < 3600:
            return f"{seconds / 60:.2f}m"
        if seconds < 86400:
            return f"{seconds / 3600:.2f}h"
        return f"{seconds / 86400:.2f}d"

    def on_mount(self) -> None:
        self.title = "Matrix Inversion Calculator"
        self.sub_title = f"V-0.1 - {METHOD_LABEL}"

if __name__ == "__main__" and ROWS <= TERMINAL_ONLY_SIZE:
    Mat().run()
elif __name__ == "__main__":
    run_terminal_mode()

import curses
import tabulate
import qiskit

from curses.textpad import Textbox


def color_transformation(string):
    # dark purple color
    return f"\033[95m{string}\033[00m"


def color_analysis(string):
    # light purple, pink color
    return f"\033[94m{string}\033[00m"


TRANSPILER_STEPS_DIMS = {
    "PASSES_START_ROW": 6,
    "PASSES_START_COL": None,  # updated whenever the window is resized
}


transpiler_headers = [
    "Pass Name",
    "Pass Type",
    "Runtime",
    "Depth",
    "Size",
    "1q Gates",
    "2q Gates",
    "Width",
]

transpiler_data = [
    ["UnRoll3qOrMore", "Transformation1", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation2", "5 ms", 9, 24, 10, 4, 6],
    ["TrivialLayout", "Analysis1", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis2", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis3", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis4", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis5", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis6", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis7", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis8", "5 ms", 9, 44, 10, 7, 6],
    ["TrivialLayout", "Analysis9", "5 ms", 9, 44, 10, 7, 6],
    ["SetLayout", "Transformation3", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation4", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation5", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation6", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation7", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation8", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation9", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation10", "5 ms", 9, 24, 10, 4, 6],
    ["SetLayout", "Transformation11", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation12", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation13", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation14", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation15", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation16", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation17", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation18", "5 ms", 9, 24, 10, 4, 6],
    ["UnRoll3qOrMore", "Transformation19", "5 ms", 9, 24, 10, 4, 6],
]


PASSES_INFO = {"total_passes": len(transpiler_data), "pass_id": -1}

# add the whitespace option
tabulate.PRESERVE_WHITESPACE = True

# make table
pass_table = tabulate.tabulate(
    headers=transpiler_headers,
    tabular_data=transpiler_data,
    tablefmt="simple_grid",
    stralign="center",
    numalign="center",
    showindex="always",
).splitlines()

# make passes pad list
passes_pad_list = []


def get_center(width, string_len, divisor=2):
    return max(0, int(width // divisor - string_len // 2 - string_len % 2))


def get_title(cols):
    title_rows = 4
    title_cols = cols
    begin_row = 1
    title_window = curses.newwin(title_rows, title_cols, begin_row, 0)

    # add title
    title = "Qiskit Transpiler Debugger"[: cols - 1]
    start_x_title = get_center(title_cols, len(title))
    title_window.bkgd(curses.color_pair(2))
    title_window.hline(0, 0, "-", title_cols)
    title_window.addstr(1, start_x_title, title, curses.A_BOLD)
    title_window.hline(2, 0, "-", title_cols)

    # add subtitle
    qiskit_version = "qiskit-terra v" + str(qiskit.__qiskit_version__["qiskit-terra"])
    backend_name = "ibmq_manila"
    optimization_level = 3
    shots = 1024
    seed = 42

    subtitle = (
        f"{qiskit_version} | backend : {backend_name} | optimization_level : {optimization_level} | shots : {shots} | random_seed : {seed}"
    )[: cols - 1]
    start_x_subtitle = get_center(title_cols, len(subtitle))
    title_window.addstr(3, start_x_subtitle, subtitle)

    return title_window


def get_overview(cols):
    overview_rows = 26
    overview_cols = cols
    begin_row = 6
    overview_win = curses.newwin(overview_rows, overview_cols, begin_row, 0)

    # add pass overview
    transform = 14
    analysis = 24
    total_passes = f"Total Passes : {38}"[: overview_cols - 1]
    pass_categories = f"Transformation : {transform} | Analysis : {analysis}"[
        : overview_cols - 1
    ]
    start_x = 5
    overview_win.addstr(5, start_x, "Pass Overview"[: overview_cols - 1], curses.A_BOLD)
    overview_win.addstr(6, start_x, total_passes)
    overview_win.addstr(7, start_x, pass_categories)

    # add runtime
    runtime = 400
    runtime_str = f"Runtime : {runtime} ms"[: overview_cols - 1]
    overview_win.addstr(9, start_x, runtime_str, curses.A_BOLD)

    # add circuit stats
    stats_str = "Circuit Statistics"[: overview_cols - 1]
    overview_win.addstr(11, start_x, stats_str, curses.A_BOLD)

    headers = ["Property", "Initial", "Final"]
    rows = []
    rows.append(["Depth", 9, 29])
    rows.append(["Width", 4, 9])
    rows.append(["Op Count", 10, 45])
    rows.append(["Size", 24, 48])

    stats_table = tabulate.tabulate(
        rows, headers=headers, tablefmt="simple_grid", stralign=("center")
    ).splitlines()

    max_line_length = len(stats_table[0])

    # add title
    overview_str = "TRANSPILATION OVERVIEW"[: overview_cols - 1]
    start_x_overview = start_x + get_center(max_line_length, len(overview_str))

    overview_win.hline(0, start_x, "_", min(cols, max_line_length))
    overview_win.addstr(2, start_x_overview, overview_str, curses.A_BOLD)
    overview_win.hline(3, start_x, "_", min(cols, max_line_length))
    for row in range(12, 12 + len(stats_table)):
        overview_win.addstr(row, start_x, stats_table[row - 12][: overview_cols - 1])

    TRANSPILER_STEPS_DIMS["PASSES_START_COL"] = start_x + max_line_length + 5

    return overview_win


def get_statusbar(rows, cols, status_type="normal"):
    # normal        : normal status bar
    # index         : index status bar - user is entering the numbers (requires input to be shown to user)
    # invalid       : error status bar - user has entered an invalid character
    # out_of_bounds : out of bounds status bar - user has entered a number out of bounds
    # pass          : pass status bar - user has entered a valid number and is now viewing the pass details

    # NOTE : processing is done after the user presses enter.

    # This will only return a status bar window, TEXT processing is done within this function ONLY

    status_strings = {
        "normal": " STATUS BAR  | Press ↑↓ keys or mouse cursor to scroll | 'I' to index into a pass | 'Q' to exit",
        "index": " STATUS BAR  | Enter the index of the pass you want to view : ",
        "invalid": " STATUS BAR  | Invalid input entered. Press Enter to continue.",
        "out_of_bounds": " STATUS BAR  | Number entered is out of bounds. Please Enter to continue.",
        "pass": " STATUS BAR  | Press 'N/P' to move to next/previous pass | 'I' to index into a pass | 'B' to go back to all passes | 'Q' to exit",
    }

    statusbarstr = status_strings[status_type][: cols - 1]

    statusbar_window = curses.newwin(1, cols, rows - 1, 0)
    statusbar_window.bkgd(" ", curses.color_pair(3))

    offset = 0
    statusbar_window.addstr(0, offset, statusbarstr)
    offset += len(statusbarstr)

    # now if index, enter a blinking cursor
    if status_type == "index":
        textbox = Textbox(statusbar_window)
        textbox.edit()
        str_value = (
            textbox.gather().split(":")[1].strip()
        )  # get the value of the entered text

        try:
            num = int(str_value)
            if num >= PASSES_INFO["total_passes"] or num < 0:
                statusbarstr = status_strings["out_of_bounds"]
            else:
                statusbarstr = status_strings["pass"]
                PASSES_INFO["pass_id"] = num
        except:
            # Invalid number entered
            statusbarstr = status_strings["invalid"]
        statusbarstr = statusbarstr[: cols - 1]

        # display the new string
        statusbar_window.clear()
        offset = 0
        statusbar_window.addstr(0, 0, statusbarstr)
        offset += len(statusbarstr)

    statusbar_window.addstr(0, offset, " " * (cols - offset - 1))

    return statusbar_window


def get_pass_title(cols):
    height = 4
    width = max(5, cols - TRANSPILER_STEPS_DIMS["PASSES_START_COL"])
    pass_title = curses.newwin(
        height,
        width,
        TRANSPILER_STEPS_DIMS["PASSES_START_ROW"],
        TRANSPILER_STEPS_DIMS["PASSES_START_COL"],
    )
    # add the title of the table
    transpiler_passes = "Transpiler Passes"[: cols - 1]
    start_header = get_center(width, len(transpiler_passes))
    try:
        pass_title.hline(0, 0, "_", width - 4)
        pass_title.addstr(2, start_header, "Transpiler Passes", curses.A_BOLD)
        pass_title.hline(3, 0, "_", width - 4)
    except:
        pass_title = None

    return pass_title


def get_pass_pad():
    # first tabulate the passes then only create the pad

    # these tabulated passes will be a global variable
    # populated only once and same is for the pad

    start_x = 4
    table_width = len(pass_table[0]) + start_x
    table_height = len(pass_table) + 1
    pass_pad = curses.newpad(table_height, table_width)

    for row in range(3):
        pass_pad.addstr(
            row,
            start_x,
            pass_table[row][: table_width - 1],
            curses.A_BOLD | curses.color_pair(1),
        )

    # now start adding the passes
    for row in range(3, len(pass_table)):
        if "Transformation" in pass_table[row]:
            pass_pad.addstr(row, start_x, pass_table[row][: table_width - 1])
        else:
            pass_pad.addstr(row, start_x, pass_table[row][: table_width - 1])

    # populated pad with passes
    return pass_pad


def get_pass_deails_pad(curr_id):
    # 1. We'll be given an index
    # 2. Take that index, get the correct transpiler pass (transpilation step)
    # 3. Using the transpilation step, get the pass details (pass name, pass type, circuit diagram, etc.)
    # 4. Create a new pad with the pass details
    # 5. Return the pad

    # dummy for now , to check the rendering mechanisms
    # need to arrange in correct form
    start_x = 4
    table_width = len(pass_table[0]) + start_x
    table_height = 150  # for now
    pass_type = transpiler_data[curr_id][1]

    pass_pad = curses.newpad(table_height, table_width)
    pass_pad.addstr(0, start_x, pass_type, curses.A_BOLD | curses.color_pair(1))

    # populated pad with passes
    return pass_pad


def render_transpilation_pad(pass_pad, curr_row, rows, cols):
    """Function to render the pass pad.

    NOTE : this is agnostic of whether we are passing the base pad
           or the individual transpiler pass pad. Why?

           Because we are not shifting the pad, we are just refreshing it.
    """
    # 4 rows for the title + curr_row (curr_row is the row of the pass)
    title_height = 5
    start_row = TRANSPILER_STEPS_DIMS["PASSES_START_ROW"] + title_height

    if start_row >= rows - 2:
        return
    if TRANSPILER_STEPS_DIMS["PASSES_START_COL"] >= cols - 1:
        return

    pass_pad.refresh(
        curr_row,
        0,
        start_row,
        TRANSPILER_STEPS_DIMS["PASSES_START_COL"],
        rows - 2,
        cols - 1,
    )


def draw_menu(stdscr):
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.bkgd(curses.color_pair(4))

    # to hide the cursor
    curses.curs_set(0)

    curr_row = 0
    last_width, last_height = 0, 0
    status_type = "normal"
    status_window, title_window = None, None

    height, width = stdscr.getmaxyx()

    base_passes_pad = get_pass_pad()

    # Loop where k is the last character pressed
    while k not in [ord("q"), ord("Q")]:
        # Initialization
        height, width = stdscr.getmaxyx()
        # nice, clear out the terminal if changed the height and then re-render
        if last_height + last_width > 0 and (
            last_width != width or last_height != height
        ):
            stdscr.clear()
        if k == curses.KEY_UP:
            curr_row -= 1
            curr_row = max(curr_row, 0)
        elif k == curses.KEY_DOWN:
            curr_row += 1
            curr_row = min(curr_row, len(pass_table) - 1)
        elif k in [ord("i"), ord("I")]:
            # user wants to index into the pass
            status_type = "index"

        elif k in [ord("n"), ord("N")]:
            if status_type in ["index", "pass"]:
                PASSES_INFO["pass_id"] = min(
                    PASSES_INFO["pass_id"] + 1, PASSES_INFO["total_passes"] - 1
                )
                status_type = "pass"

        elif k in [ord("p"), ord("P")]:
            if status_type in ["index", "pass"]:
                PASSES_INFO["pass_id"] = max(0, PASSES_INFO["pass_id"] - 1)
                status_type = "pass"

        elif k in [ord("b"), ord("B")]:
            # reset the state variables
            status_type = "normal"
            PASSES_INFO["pass_id"] = -1

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Refresh the screen
        stdscr.refresh()

        if width != last_width or height != last_height:
            title_window = get_title(width)
            title_window.refresh()

            info_window = get_overview(width)
            info_window.refresh()

            pass_title_window = get_pass_title(width)
            if pass_title_window:
                pass_title_window.refresh()

        status_window = get_statusbar(height, width, status_type)
        status_window.refresh()

        if status_type == "normal":
            render_transpilation_pad(base_passes_pad, curr_row, height, width)
        elif status_type in ["index", "pass"]:
            # using zero based indexing
            if PASSES_INFO["pass_id"] >= 0:
                status_type = "pass"
                render_transpilation_pad(
                    get_pass_deails_pad(PASSES_INFO["pass_id"]), curr_row, height, width
                )
        last_width = width
        last_height = height

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
